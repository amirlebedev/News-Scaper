# News-Scaper
Database:
https://amirlebedev.github.io/News-Scaper/

Packages: requests, bs4, , selenium (chrome driver), PySimpleGui.

Operation:
1. Gets all the main "hubs" for articles.
2. Searches each hub for articles by identifying keywords in the URL.
3. Gets the articles.
4. Finds metadata (author, tags, publish date, title).
5. Puts the article link with the metadata in a main text database.
6. Goes over the database and archives every article in theback Machine archiver.
7. Makes a backup and changes the text database to fit Markdown syntax.
