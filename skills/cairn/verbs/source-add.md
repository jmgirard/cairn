# source add

Puts one source on the shelf and writes its reference note.

## Steps

1. Get the source's file. Given a URL whose full text cannot be fetched, such as a paywall or a refused request, stop and ask the user for the file. Write no note from an abstract. (stop)
2. Put the file on the shelf in the home folder, named for the source's citekey.
3. Write the note from its template: the citation, what was read and when, and each value or claim taken from the source, with its page number.
4. Add the note's line to the index.
5. Commit the note and the index line to the default branch and push. During work on a branch, commit them there, so they ride in the PR. In a guest repo both live in the home folder.
6. If the profile has a `Zotero collection:` line: tell the user that Zotero will ask them to allow a write, then run the Zotero script's `add` with that collection, the shelf file, and the source's title, DOI, year, and authors. It looks the source up by DOI, then by title and year. It adds the item with the file attached if the source is absent, and puts the item in the collection either way. Say what was added or was already there. A failure here never blocks the note.

## Done

The file is on the shelf, the note is written, and the index has its line. In the user's own repos both are committed. Where the profile names a Zotero collection, the user has been told what Zotero now holds, or that the Zotero step failed.
