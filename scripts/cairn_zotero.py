#!/usr/bin/env python3
"""cairn zotero: look a source up in Zotero, or add it, over Zotero's local API.

    python3 cairn_zotero.py find --doi DOI
    python3 cairn_zotero.py find --title TITLE [--year YEAR]
    python3 cairn_zotero.py add --collection NAME --file PATH --title TITLE
                                [--doi DOI] [--year YEAR] [--author "Family, Given"]...
                                [--type TYPE] [--publication NAME] [--url URL]
    python3 cairn_zotero.py collect --collection NAME --key ITEMKEY

`find` prints each matching item with its key and the path of each PDF it
holds, and exits 0. It exits 1 when nothing matches.

`add` looks the source up first, by DOI and then by title and year. An item
that is already there is put in the collection and nothing else changes. An
item that is absent is created in the collection with the file attached.

`collect` puts an existing item in the collection.

`add` and `collect` create the collection if it is missing. Each prints what
it did.

Zotero must have "Allow other applications on this computer to communicate
with Zotero" switched on (Settings, Advanced), and writes need Zotero 10 or
later. The first write opens a dialog in Zotero. With "Allow", Zotero gives
a key for one request, so an `add` asks up to four times. With "Always
Allow", Zotero gives a key that keeps working, and this script stores it in
`~/.cairn/.zotero-key` and lists that file in `~/.cairn/.gitignore`.

If Zotero is not running, the script starts it in the background and waits
for it. It talks to this computer only. Exit codes: 0 done, 1 not found,
2 Zotero could not be reached, 3 Zotero refused or the request failed.
Python 3 standard library only.

The `CAIRN_ZOTERO_URL` variable replaces the API address, and `CAIRN_HOME`
replaces `~/.cairn`, both for tests.
"""

import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

APP_NAME = "cairn"
KEY_FILE = ".zotero-key"
KEY_CHARS = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
DIALOG_WAIT = 300  # seconds the user has to answer Zotero's dialog


class Unreachable(Exception):
    """Zotero's local API did not answer."""


class Refused(Exception):
    """Zotero answered, and the answer was no."""


def api_url():
    return (os.environ.get("CAIRN_ZOTERO_URL") or "http://localhost:23119/api").rstrip("/")


def home_root():
    return os.environ.get("CAIRN_HOME") or os.path.join(os.path.expanduser("~"), ".cairn")


def norm_doi(doi):
    doi = (doi or "").strip().lower()
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", doi)


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


class Zotero:
    def __init__(self, base=None, key_dir=None, opener=None):
        self.base = base or api_url()
        self.key_dir = key_dir or home_root()
        self.server_id = None
        self.key = None
        self.remembered = False
        self._open = opener or urllib.request.urlopen

    # ---- transport -------------------------------------------------------

    def _request(self, method, url, body=None, headers=None, timeout=30):
        headers = dict(headers or {})
        headers.setdefault("Zotero-API-Version", "3")
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with self._open(request, timeout=timeout) as response:
                return response.status, dict(response.headers), response.read()
        except urllib.error.HTTPError as err:
            with err:
                return err.code, dict(err.headers), err.read()
        except (urllib.error.URLError, OSError) as err:
            raise Unreachable(str(getattr(err, "reason", err)))

    def get(self, path, **params):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        status, headers, body = self._request("GET", url)
        if status == 403:
            raise Refused(
                "Zotero's local API is switched off. Turn on \"Allow other "
                "applications on this computer to communicate with Zotero\" "
                "in Zotero's Settings, under Advanced."
            )
        if status != 200:
            raise Refused("GET %s gave %d" % (path, status))
        return headers, json.loads(body or b"null")

    def get_all(self, path, **params):
        """Every object from a paged listing."""
        found, start = [], 0
        while True:
            headers, page = self.get(path, start=start, limit=100, **params)
            found.extend(page)
            total = int(headers.get("Total-Results") or len(found))
            start += len(page)
            if not page or start >= total:
                return found

    # ---- write permission ------------------------------------------------

    def _key_path(self):
        return os.path.join(self.key_dir, KEY_FILE)

    def _load_key(self):
        try:
            with open(self._key_path(), encoding="utf-8") as handle:
                key = handle.read().strip()
        except OSError:
            return
        if key:
            self.key, self.remembered = key, True

    def _store_key(self, key):
        os.makedirs(self.key_dir, exist_ok=True)
        path = self._key_path()
        with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as handle:
            handle.write(key + "\n")
        ignore = os.path.join(self.key_dir, ".gitignore")
        try:
            with open(ignore, encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except OSError:
            lines = []
        if KEY_FILE not in lines:
            with open(ignore, "a", encoding="utf-8") as handle:
                handle.write(KEY_FILE + "\n")

    def _forget_key(self):
        self.key, self.remembered = None, False
        try:
            os.remove(self._key_path())
        except OSError:
            pass

    def _server_id(self):
        if self.server_id is None:
            _, headers, _ = self._request("GET", self.base + "/")
            self.server_id = headers.get("Zotero-Server-ID")
            if not self.server_id:
                raise Refused(
                    "This Zotero gives no server ID, so it takes no writes. "
                    "Writes need Zotero 10 or later."
                )
        return self.server_id

    def _authorize(self):
        status, _, body = self._request(
            "POST",
            self.base + "/local/authorize",
            body=json.dumps({"appName": APP_NAME}).encode(),
            headers={"Content-Type": "application/json", "Zotero-Server-ID": self._server_id()},
            timeout=DIALOG_WAIT,
        )
        if status == 403:
            raise Refused("The write was denied in Zotero's dialog.")
        if status == 429:
            raise Refused("Zotero is showing too many dialogs. Wait a minute and try again.")
        if status != 200:
            raise Refused("Zotero's authorization gave %d" % status)
        answer = json.loads(body)
        self.key = answer["key"]
        self.remembered = bool(answer.get("remember"))
        if self.remembered:
            self._store_key(self.key)

    def write(self, method, path, body, headers=None, ok=(200, 201, 204)):
        """One write request. A key from "Allow" is spent by the request
        that uses it, so each write asks again unless Zotero remembers."""
        if self.key is None:
            self._load_key()
        for attempt in (1, 2):
            if self.key is None:
                self._authorize()
            send = dict(headers or {})
            send["Zotero-Server-ID"] = self._server_id()
            send["Zotero-API-Key"] = self.key
            status, got, answer = self._request(method, self.base + path, body=body, headers=send)
            if not self.remembered:
                self.key = None
            if status == 401 and attempt == 1:
                self._forget_key()  # a key Zotero no longer accepts
                continue
            if status not in ok:
                raise Refused("%s %s gave %d: %s" % (
                    method, path, status, answer[:200].decode("utf-8", "replace")))
            return status, got, answer
        raise Refused("%s %s was not authorized" % (method, path))

    # ---- reads -----------------------------------------------------------

    def find(self, doi=None, title=None, year=None):
        """Items that match the DOI exactly, else the title and the year."""
        hits = []
        if doi:
            want = norm_doi(doi)
            _, items = self.get("/users/0/items", q=want, qmode="everything", limit=50)
            hits = [i for i in items if norm_doi(i["data"].get("DOI")) == want]
        if not hits and title:
            want = norm_title(title)
            _, items = self.get("/users/0/items", q=title, qmode="titleCreatorYear", limit=50)
            for item in items:
                data = item["data"]
                if data.get("itemType") in ("attachment", "note", "annotation"):
                    continue
                if norm_title(data.get("title")) != want:
                    continue
                dated = (item.get("meta") or {}).get("parsedDate") or data.get("date") or ""
                if year and str(year) not in dated:
                    continue
                hits.append(item)
        return hits

    def pdf_paths(self, item_key):
        _, kids = self.get("/users/0/items/%s/children" % item_key)
        paths = []
        for kid in kids:
            data = kid["data"]
            if data.get("itemType") != "attachment" or data.get("contentType") != "application/pdf":
                continue
            href = ((kid.get("links") or {}).get("enclosure") or {}).get("href") or ""
            if href.startswith("file://"):
                paths.append(urllib.request.url2pathname(urllib.parse.urlparse(href).path))
        return paths

    def collection_key(self, name):
        for collection in self.get_all("/users/0/collections"):
            if collection["data"].get("name") == name:
                return collection["key"]
        return None

    # ---- writes ----------------------------------------------------------

    def ensure_collection(self, name):
        """(key, created) for the collection of that name."""
        key = self.collection_key(name)
        if key:
            return key, False
        _, _, answer = self.write(
            "POST", "/users/0/collections",
            json.dumps([{"name": name}]).encode(),
            headers={"Content-Type": "application/json"},
        )
        return _created(answer, 0), True

    def put_in_collection(self, item_key, collection_key):
        """True if the item was added, False if it was already there."""
        _, item = self.get("/users/0/items/%s" % item_key)
        held = list(item["data"].get("collections") or [])
        if collection_key in held:
            return False
        self.write(
            "PATCH", "/users/0/items/%s" % item_key,
            json.dumps({"collections": held + [collection_key]}).encode(),
            headers={
                "Content-Type": "application/json",
                "If-Unmodified-Since-Version": str(item["version"]),
            },
        )
        return True

    def create_with_file(self, meta, path, collection_key):
        """Create the item and its PDF attachment, then upload the file.
        Returns (item key, attachment key)."""
        with open(path, "rb") as handle:
            content = handle.read()
        name = os.path.basename(path)
        parent_key, child_key = new_key(), new_key()
        parent = dict(meta, key=parent_key, version=0, collections=[collection_key])
        child = {
            "key": child_key, "version": 0,
            "itemType": "attachment", "parentItem": parent_key,
            "linkMode": "imported_file", "title": name, "filename": name,
            "contentType": "application/pdf" if name.lower().endswith(".pdf")
            else "application/octet-stream",
            "tags": [], "relations": {},
        }
        _, _, answer = self.write(
            "POST", "/users/0/items", json.dumps([parent, child]).encode(),
            headers={"Content-Type": "application/json"},
        )
        parent_key, child_key = _created(answer, 0), _created(answer, 1)
        try:
            self._upload(child_key, name, content, path)
        except (Refused, Unreachable) as err:
            raise Refused(
                "Item %s was created, but its file was not attached: %s" % (parent_key, err))
        return parent_key, child_key

    def _upload(self, child_key, name, content, path):
        form = urllib.parse.urlencode({
            "md5": hashlib.md5(content).hexdigest(),
            "filename": name,
            "filesize": len(content),
            "mtime": int(os.path.getmtime(path) * 1000),
        }).encode()
        file_path = "/users/0/items/%s/file" % child_key
        form_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "If-None-Match": "*",
        }
        _, _, answer = self.write("POST", file_path, form, headers=form_headers)
        slot = json.loads(answer or b"{}")
        if slot.get("exists"):
            return
        payload = (slot.get("prefix") or "").encode() + content + (slot.get("suffix") or "").encode()
        status, _, body = self._request(
            "POST", slot["url"], body=payload,
            headers={"Content-Type": slot.get("contentType") or "application/octet-stream"},
            timeout=300,
        )
        if status not in (200, 201, 204):
            raise Refused("The file upload gave %d" % status)
        self.write(
            "POST", file_path,
            urllib.parse.urlencode({"upload": slot["uploadKey"]}).encode(),
            headers=form_headers,
        )


def new_key():
    return "".join(random.choice(KEY_CHARS) for _ in range(8))


def _created(answer, index):
    result = json.loads(answer or b"{}")
    made = (result.get("successful") or {}).get(str(index))
    if not made:
        failed = (result.get("failed") or {}).get(str(index)) or result
        raise Refused("Zotero did not create the object: %s" % json.dumps(failed)[:200])
    return made["key"]


def item_meta(args):
    meta = {"itemType": args.type, "title": args.title}
    if args.doi:
        meta["DOI"] = norm_doi(args.doi)
    if args.year:
        meta["date"] = str(args.year)
    if args.publication:
        meta["publicationTitle"] = args.publication
    if args.url:
        meta["url"] = args.url
    creators = []
    for author in args.author or []:
        family, _, given = (part.strip() for part in author.partition(","))
        if given:
            creators.append({"creatorType": "author", "lastName": family, "firstName": given})
        else:
            creators.append({"creatorType": "author", "name": family})
    if creators:
        meta["creators"] = creators
    return meta


def start_zotero():
    """Start Zotero in the background. True if a start was attempted."""
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", "-g", "-j", "-a", "Zotero"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os.name == "nt":
            return False
        else:
            subprocess.Popen(["zotero"], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        return True
    except OSError:
        return False


def connect(wait=45, starter=start_zotero, sleep=time.sleep):
    """A Zotero that answers, started first if it has to be."""
    zotero = Zotero()
    try:
        zotero.get("/users/0/collections", limit=1)
        return zotero
    except Unreachable:
        if not starter():
            raise
    waited = 0
    while True:
        sleep(3)
        waited += 3
        try:
            zotero.get("/users/0/collections", limit=1)
            return zotero
        except Unreachable:
            if waited >= wait:
                raise


def describe(zotero, item):
    data = item["data"]
    dated = (item.get("meta") or {}).get("parsedDate") or data.get("date") or ""
    lines = [
        "item %s" % item["key"],
        "  title: %s" % (data.get("title") or ""),
        "  year: %s" % dated[:4],
        "  doi: %s" % (data.get("DOI") or ""),
    ]
    lines.extend("  file: %s" % path for path in zotero.pdf_paths(item["key"]))
    return "\n".join(lines)


def run(args, zotero):
    if args.command == "find":
        hits = zotero.find(args.doi, args.title, args.year)
        if not hits:
            print("Not in Zotero.")
            return 1
        print("\n".join(describe(zotero, item) for item in hits))
        return 0

    if args.command == "collect":
        collection, created = zotero.ensure_collection(args.collection)
        added = zotero.put_in_collection(args.key, collection)
        print("%s collection \"%s\". Item %s %s." % (
            "Created" if created else "Used", args.collection, args.key,
            "added to it" if added else "was already in it"))
        return 0

    if not os.path.isfile(args.file):
        print("No file at %s" % args.file)
        return 3
    hits = zotero.find(args.doi, args.title, args.year)
    collection, created = zotero.ensure_collection(args.collection)
    made = "Created" if created else "Used"
    if hits:
        key = hits[0]["key"]
        added = zotero.put_in_collection(key, collection)
        print("%s collection \"%s\". Already in Zotero as item %s; %s. No file was added." % (
            made, args.collection, key,
            "added to the collection" if added else "already in the collection"))
        return 0
    key, attachment = zotero.create_with_file(item_meta(args), args.file, collection)
    print("%s collection \"%s\". Added item %s with %s attached (attachment %s)." % (
        made, args.collection, key, os.path.basename(args.file), attachment))
    return 0


def parser():
    top = argparse.ArgumentParser(prog="cairn_zotero.py", description=__doc__.split("\n\n")[0])
    commands = top.add_subparsers(dest="command", required=True)

    find = commands.add_parser("find")
    find.add_argument("--doi")
    find.add_argument("--title")
    find.add_argument("--year")

    add = commands.add_parser("add")
    add.add_argument("--collection", required=True)
    add.add_argument("--file", required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--doi")
    add.add_argument("--year")
    add.add_argument("--author", action="append")
    add.add_argument("--type", default="journalArticle")
    add.add_argument("--publication")
    add.add_argument("--url")

    collect = commands.add_parser("collect")
    collect.add_argument("--collection", required=True)
    collect.add_argument("--key", required=True)
    return top


def main(argv):
    args = parser().parse_args(argv[1:])
    if args.command == "find" and not (args.doi or args.title):
        print("find needs --doi or --title")
        return 3
    try:
        return run(args, connect())
    except Unreachable as err:
        print("Zotero could not be reached (%s)." % err)
        return 2
    except Refused as err:
        print(str(err))
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
