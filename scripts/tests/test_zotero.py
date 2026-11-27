"""Tests for scripts/cairn_zotero.py against a stand-in for Zotero's local API.

The stand-in follows Zotero's documentation for the local API (Zotero 10):
reads need no key; a write needs the server ID and a key from
/local/authorize; a key from "Allow" is spent by one write; a file goes up in
three requests. No test talks to a real Zotero or touches ~/.cairn.

    python3 -m unittest discover -s scripts/tests
"""

import hashlib
import io
import json
import os
import stat
import sys
import tempfile
import threading
import unittest
import urllib.parse
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import cairn_zotero as cz  # noqa: E402

SERVER_ID = "SRV1"


class FakeZotero:
    def __init__(self):
        self.items = {}
        self.children = {}
        self.collections = []
        self.remember = False
        self.deny = False
        self.api_off = False
        self.fail_upload = False
        self.keys = set()
        self.remembered_keys = set()
        self.authorizations = 0
        self.writes = []
        self.uploads = {}
        self.registered = []
        self.serial = 0

    def add_item(self, key, title, doi="", date="", item_type="journalArticle", collections=()):
        self.items[key] = {
            "key": key, "version": 7,
            "data": {"key": key, "version": 7, "itemType": item_type, "title": title,
                     "DOI": doi, "date": date, "collections": list(collections)},
            "meta": {"parsedDate": date},
        }

    def add_pdf(self, parent, key, path):
        self.children.setdefault(parent, []).append({
            "key": key,
            "data": {"itemType": "attachment", "contentType": "application/pdf",
                     "filename": os.path.basename(path)},
            "links": {"enclosure": {"href": "file://" + path}},
        })

    def add_collection(self, key, name):
        self.collections.append({"key": key, "data": {"key": key, "name": name}})


def lower(headers):
    """Header names are not case sensitive; the tests look them up in lower case."""
    return {name.lower(): value for name, value in headers.items()}


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def handler_for(fake, base):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, body=None, headers=None):
            raw = b"" if body is None else (body if isinstance(body, bytes) else json.dumps(body).encode())
            self.send_response(status)
            for name, value in (headers or {}).items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):
            url = urllib.parse.urlparse(self.path)
            query = dict(urllib.parse.parse_qsl(url.query))
            path = url.path
            if path == "/api/":
                return self.reply(200, b"ok", {"Zotero-Server-ID": SERVER_ID})
            if fake.api_off:
                return self.reply(403)
            if path == "/api/users/0/collections":
                start, limit = int(query.get("start", 0)), int(query.get("limit", 25))
                return self.reply(200, fake.collections[start:start + limit],
                                  {"Total-Results": str(len(fake.collections))})
            if path == "/api/users/0/items":
                q = query.get("q", "").lower()
                hits = []
                for item in fake.items.values():
                    data = item["data"]
                    if query.get("qmode") == "everything":
                        ok = q in data["DOI"].lower() or q in data["title"].lower()
                    else:
                        ok = all(word in data["title"].lower() for word in q.split())
                    if ok:
                        hits.append(item)
                return self.reply(200, hits, {"Total-Results": str(len(hits))})
            parts = path.split("/")
            if len(parts) == 6 and parts[4] == "items" and parts[5] in fake.items:
                return self.reply(200, fake.items[parts[5]])
            if len(parts) == 7 and parts[6] == "children":
                return self.reply(200, fake.children.get(parts[5], []))
            self.reply(404)

        def body(self):
            return self.rfile.read(int(self.headers.get("Content-Length") or 0))

        def keyed(self):
            """Apply the write rules. True if the write may go ahead."""
            if self.headers.get("Zotero-Server-ID") != SERVER_ID:
                self.reply(428)
                return False
            key = self.headers.get("Zotero-API-Key")
            if key in fake.remembered_keys:
                return True
            if key in fake.keys:
                fake.keys.discard(key)
                return True
            self.reply(401)
            return False

        def do_POST(self):
            path = urllib.parse.urlparse(self.path).path
            body = self.body()
            if path == "/api/local/authorize":
                if self.headers.get("Zotero-Server-ID") != SERVER_ID:
                    return self.reply(428)
                fake.authorizations += 1
                if fake.deny:
                    return self.reply(403, {"denied": True})
                fake.serial += 1
                key = "KEY%d" % fake.serial
                (fake.remembered_keys if fake.remember else fake.keys).add(key)
                return self.reply(200, {"key": key, "remember": fake.remember})
            if path.startswith("/api/upload/"):
                if fake.fail_upload:
                    return self.reply(500)
                fake.uploads[path.rsplit("/", 1)[1]] = body
                return self.reply(201)
            if not self.keyed():
                return
            fake.writes.append(("POST", path, lower(self.headers), body))
            if path == "/api/users/0/collections":
                made = {}
                for index, spec in enumerate(json.loads(body)):
                    fake.serial += 1
                    key = "COLL%04d" % fake.serial
                    fake.add_collection(key, spec["name"])
                    made[str(index)] = {"key": key}
                return self.reply(200, {"successful": made, "failed": {}})
            if path == "/api/users/0/items":
                made = {}
                for index, spec in enumerate(json.loads(body)):
                    fake.items[spec["key"]] = {"key": spec["key"], "version": 1, "data": spec}
                    made[str(index)] = {"key": spec["key"]}
                return self.reply(200, {"successful": made, "failed": {}})
            if path.endswith("/file"):
                form = dict(urllib.parse.parse_qsl(body.decode()))
                if self.headers.get("If-None-Match") != "*":
                    return self.reply(428)
                if "upload" in form:
                    fake.registered.append(form["upload"])
                    return self.reply(204)
                fake.serial += 1
                upload = "UP%d" % fake.serial
                return self.reply(200, {"url": "%s/upload/%s" % (base(), upload),
                                        "uploadKey": upload, "form": form})
            self.reply(404)

        def do_PATCH(self):
            path = urllib.parse.urlparse(self.path).path
            body = self.body()
            if not self.keyed():
                return
            fake.writes.append(("PATCH", path, lower(self.headers), body))
            item = fake.items[path.rsplit("/", 1)[1]]
            if self.headers.get("If-Unmodified-Since-Version") != str(item["version"]):
                return self.reply(412)
            item["data"].update(json.loads(body))
            self.reply(204)

    return Handler


class Base(unittest.TestCase):
    def setUp(self):
        self.fake = FakeZotero()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.fake, lambda: self.base))
        self.base = "http://127.0.0.1:%d/api" % self.server.server_address[1]
        thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = os.path.join(self.tmp.name, "home")
        self.pdf = os.path.join(self.tmp.name, "girard2016.pdf")
        with open(self.pdf, "wb") as handle:
            handle.write(b"%PDF-1.7 not really a pdf")
        old = {name: os.environ.get(name) for name in ("CAIRN_ZOTERO_URL", "CAIRN_HOME")}
        os.environ["CAIRN_ZOTERO_URL"] = self.base
        os.environ["CAIRN_HOME"] = self.home
        self.addCleanup(self._restore, old)

    @staticmethod
    def _restore(old):
        for name, value in old.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def zotero(self):
        return cz.Zotero()

    def cli(self, *argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cz.main(["cairn_zotero.py", *argv])
        return code, out.getvalue().strip()

    def add_args(self, *extra):
        return ("add", "--collection", "chromodoris", "--file", self.pdf,
                "--title", "A Primer on Observational Measurement", "--doi", "10.1177/1073191116635807",
                "--year", "2016", "--author", "Girard, Jeffrey M.", "--author", "Cohn, Jeffrey F.",
                *extra)


class Find(Base):
    def test_doi_must_match_exactly(self):
        self.fake.add_item("AAAA1111", "Right one", doi="10.1000/abc")
        self.fake.add_item("BBBB2222", "Wrong one", doi="10.1000/abcdef")
        hits = self.zotero().find(doi="https://doi.org/10.1000/ABC")
        self.assertEqual([h["key"] for h in hits], ["AAAA1111"])

    def test_title_and_year_when_there_is_no_doi_match(self):
        self.fake.add_item("AAAA1111", "A Primer on Observational Measurement", date="2016-08")
        self.fake.add_item("BBBB2222", "A primer on observational measurement, revisited", date="2016")
        zotero = self.zotero()
        hits = zotero.find(doi="10.1/none", title="A primer on  observational measurement", year="2016")
        self.assertEqual([h["key"] for h in hits], ["AAAA1111"])
        self.assertEqual(zotero.find(title="A Primer on Observational Measurement", year="2015"), [])

    def test_attachments_and_notes_are_not_sources(self):
        self.fake.add_item("AAAA1111", "Same title", item_type="attachment")
        self.assertEqual(self.zotero().find(title="Same title"), [])

    def test_cli_prints_each_match_with_its_pdf_path(self):
        self.fake.add_item("AAAA1111", "Right one", doi="10.1000/abc", date="2011-04")
        self.fake.add_pdf("AAAA1111", "PDF11111", "/Users/x/Zotero/storage/PDF11111/right one.pdf".replace(" ", "%20"))
        code, out = self.cli("find", "--doi", "10.1000/abc")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), [
            "item AAAA1111",
            "  title: Right one",
            "  year: 2011",
            "  doi: 10.1000/abc",
            "  file: /Users/x/Zotero/storage/PDF11111/right one.pdf",
        ])

    def test_cli_exits_1_when_nothing_matches(self):
        self.assertEqual(self.cli("find", "--doi", "10.1000/none"), (1, "Not in Zotero."))

    def test_find_needs_something_to_look_for(self):
        self.assertEqual(self.cli("find")[0], 3)

    def test_find_makes_no_write(self):
        self.fake.add_item("AAAA1111", "Right one", doi="10.1000/abc")
        self.cli("find", "--doi", "10.1000/abc")
        self.assertEqual((self.fake.authorizations, self.fake.writes), (0, []))


class Collections(Base):
    def test_a_collection_past_the_first_page_is_found(self):
        for index in range(230):
            self.fake.add_collection("C%07d" % index, "name %d" % index)
        self.assertEqual(self.zotero().collection_key("name 215"), "C0000215")
        self.assertIsNone(self.zotero().collection_key("name 999"))

    def test_collect_adds_to_the_full_list_at_the_items_version(self):
        self.fake.add_collection("COLLAAAA", "chromodoris")
        self.fake.add_item("AAAA1111", "Right one", collections=["COLLOTHR"])
        code, out = self.cli("collect", "--collection", "chromodoris", "--key", "AAAA1111")
        self.assertEqual(code, 0)
        self.assertIn("Item AAAA1111 added to it", out)
        method, path, headers, body = self.fake.writes[0]
        self.assertEqual((method, path), ("PATCH", "/api/users/0/items/AAAA1111"))
        self.assertEqual(headers["if-unmodified-since-version"], "7")
        self.assertEqual(json.loads(body), {"collections": ["COLLOTHR", "COLLAAAA"]})

    def test_collect_writes_nothing_when_the_item_is_already_there(self):
        self.fake.add_collection("COLLAAAA", "chromodoris")
        self.fake.add_item("AAAA1111", "Right one", collections=["COLLAAAA"])
        code, out = self.cli("collect", "--collection", "chromodoris", "--key", "AAAA1111")
        self.assertEqual(code, 0)
        self.assertIn("was already in it", out)
        self.assertEqual(self.fake.writes, [])

    def test_a_missing_collection_is_created(self):
        self.fake.add_item("AAAA1111", "Right one")
        code, out = self.cli("collect", "--collection", "chromodoris", "--key", "AAAA1111")
        self.assertEqual(code, 0)
        self.assertIn('Created collection "chromodoris"', out)
        self.assertEqual([c["data"]["name"] for c in self.fake.collections], ["chromodoris"])
        self.assertEqual(len(self.fake.items["AAAA1111"]["data"]["collections"]), 1)


class Add(Base):
    def test_a_source_already_in_zotero_only_joins_the_collection(self):
        self.fake.add_collection("COLLAAAA", "chromodoris")
        self.fake.add_item("AAAA1111", "Something else entirely", doi="10.1177/1073191116635807")
        code, out = self.cli(*self.add_args())
        self.assertEqual(code, 0)
        self.assertIn("Already in Zotero as item AAAA1111; added to the collection. No file was added.", out)
        self.assertEqual([w[0] for w in self.fake.writes], ["PATCH"])
        self.assertEqual(self.fake.uploads, {})

    def test_an_absent_source_is_created_with_its_file(self):
        self.fake.add_collection("COLLAAAA", "chromodoris")
        code, out = self.cli(*self.add_args("--publication", "Assessment"))
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r'^Used collection "chromodoris"\. Added item \w{8} with girard2016\.pdf attached')

        paths = [w[1] for w in self.fake.writes]
        self.assertEqual(paths[0], "/api/users/0/items")
        parent, child = json.loads(self.fake.writes[0][3])
        self.assertEqual(parent["itemType"], "journalArticle")
        self.assertEqual(parent["title"], "A Primer on Observational Measurement")
        self.assertEqual(parent["DOI"], "10.1177/1073191116635807")
        self.assertEqual(parent["date"], "2016")
        self.assertEqual(parent["publicationTitle"], "Assessment")
        self.assertEqual(parent["collections"], ["COLLAAAA"])
        self.assertEqual(parent["creators"], [
            {"creatorType": "author", "lastName": "Girard", "firstName": "Jeffrey M."},
            {"creatorType": "author", "lastName": "Cohn", "firstName": "Jeffrey F."},
        ])
        self.assertEqual(child["itemType"], "attachment")
        self.assertEqual(child["linkMode"], "imported_file")
        self.assertEqual(child["parentItem"], parent["key"])
        self.assertEqual(child["filename"], "girard2016.pdf")
        self.assertEqual(child["contentType"], "application/pdf")
        self.assertNotEqual(child["key"], parent["key"])

        file_path = "/api/users/0/items/%s/file" % child["key"]
        self.assertEqual(paths[1:], [file_path, file_path])
        with open(self.pdf, "rb") as handle:
            content = handle.read()
        form = dict(urllib.parse.parse_qsl(self.fake.writes[1][3].decode()))
        self.assertEqual(form["md5"], hashlib.md5(content).hexdigest())
        self.assertEqual(form["filesize"], str(len(content)))
        self.assertEqual(form["filename"], "girard2016.pdf")
        self.assertTrue(form["mtime"].isdigit())
        self.assertEqual(list(self.fake.uploads.values()), [content])
        self.assertEqual(self.fake.registered, list(self.fake.uploads))

    def test_a_missing_file_stops_before_any_write(self):
        code, out = self.cli("add", "--collection", "c", "--file", self.pdf + ".none", "--title", "T")
        self.assertEqual(code, 3)
        self.assertIn("No file at", out)
        self.assertEqual((self.fake.authorizations, self.fake.writes), (0, []))

    def test_a_failed_upload_names_the_item_left_without_its_file(self):
        self.fake.add_collection("COLLAAAA", "chromodoris")
        self.fake.fail_upload = True
        code, out = self.cli(*self.add_args())
        self.assertEqual(code, 3)
        self.assertRegex(out, r"^Item \w{8} was created, but its file was not attached")


class Permission(Base):
    def test_every_write_carries_the_server_id_and_a_key(self):
        self.cli(*self.add_args())
        self.assertEqual(len(self.fake.writes), 4)  # collection, items, file slot, registration
        for _, _, headers, _ in self.fake.writes:
            self.assertEqual(headers["zotero-server-id"], SERVER_ID)
            self.assertTrue(headers["zotero-api-key"].startswith("KEY"))

    def test_allow_gives_one_key_for_each_write(self):
        code, _ = self.cli(*self.add_args())
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.authorizations, 4)
        self.assertFalse(os.path.exists(os.path.join(self.home, ".zotero-key")))

    def test_always_allow_asks_once_and_the_key_is_kept(self):
        self.fake.remember = True
        code, _ = self.cli(*self.add_args())
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.authorizations, 1)
        key_file = os.path.join(self.home, ".zotero-key")
        self.assertEqual(read(key_file).strip(), "KEY1")
        self.assertEqual(stat.S_IMODE(os.stat(key_file).st_mode), 0o600)
        self.assertEqual(read(os.path.join(self.home, ".gitignore")).splitlines(), [".zotero-key"])

        self.fake.add_item("AAAA1111", "Another", doi="10.1/x")
        code, _ = self.cli("collect", "--collection", "chromodoris", "--key", "AAAA1111")
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.authorizations, 1)  # the stored key was used

    def test_gitignore_keeps_its_other_lines(self):
        os.makedirs(self.home)
        with open(os.path.join(self.home, ".gitignore"), "w") as handle:
            handle.write("scratch/\n")
        self.fake.remember = True
        self.cli(*self.add_args())
        self.assertEqual(
            read(os.path.join(self.home, ".gitignore")).splitlines(),
            ["scratch/", ".zotero-key"],
        )

    def test_a_stored_key_zotero_no_longer_takes_is_replaced(self):
        os.makedirs(self.home)
        with open(os.path.join(self.home, ".zotero-key"), "w") as handle:
            handle.write("REVOKED\n")
        self.fake.remember = True
        self.fake.add_item("AAAA1111", "Another")
        code, _ = self.cli("collect", "--collection", "chromodoris", "--key", "AAAA1111")
        self.assertEqual(code, 0)
        self.assertNotEqual(read(os.path.join(self.home, ".zotero-key")).strip(), "REVOKED")

    def test_a_denied_dialog_ends_the_run_cleanly(self):
        self.fake.deny = True
        code, out = self.cli(*self.add_args())
        self.assertEqual(code, 3)
        self.assertEqual(out, "The write was denied in Zotero's dialog.")
        self.assertEqual(self.fake.writes, [])

    def test_local_api_switched_off_names_the_setting(self):
        self.fake.api_off = True
        code, out = self.cli("find", "--doi", "10.1/x")
        self.assertEqual(code, 3)
        self.assertIn("Allow other applications on this computer to communicate with Zotero", out)


class Reach(Base):
    def closed_port(self):
        self.server.shutdown()
        self.server.server_close()

    def test_unreachable_and_not_startable_exits_2(self):
        self.closed_port()
        out = io.StringIO()
        with redirect_stdout(out):
            try:
                cz.connect(starter=lambda: False)
                code = 0
            except cz.Unreachable:
                code = 2
        self.assertEqual(code, 2)

    def test_connect_waits_for_a_started_zotero_then_gives_up(self):
        self.closed_port()
        naps = []
        with self.assertRaises(cz.Unreachable):
            cz.connect(wait=9, starter=lambda: True, sleep=naps.append)
        self.assertEqual(naps, [3, 3, 3])

    def test_connect_returns_once_zotero_answers(self):
        calls = []
        zotero = cz.connect(starter=lambda: calls.append(1) or True, sleep=lambda s: None)
        self.assertEqual(calls, [])  # it answered at once, so nothing was started
        self.assertEqual(zotero.base, self.base)


class Meta(unittest.TestCase):
    def test_dois_and_titles_are_compared_in_one_form(self):
        self.assertEqual(cz.norm_doi(" DOI: 10.1000/ABC "), "10.1000/abc")
        self.assertEqual(cz.norm_doi("http://dx.doi.org/10.1000/abc"), "10.1000/abc")
        self.assertEqual(cz.norm_title("A  Primer: on Things!"), "a primer on things")

    def test_an_author_with_no_comma_is_one_name(self):
        args = cz.parser().parse_args(
            ["add", "--collection", "c", "--file", "f", "--title", "T", "--author", "R Core Team"])
        self.assertEqual(cz.item_meta(args)["creators"], [{"creatorType": "author", "name": "R Core Team"}])

    def test_new_keys_use_zoteros_alphabet(self):
        key = cz.new_key()
        self.assertEqual(len(key), 8)
        self.assertTrue(set(key) <= set(cz.KEY_CHARS))


if __name__ == "__main__":
    unittest.main()
