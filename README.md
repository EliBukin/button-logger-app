Button Logger App

The Button Logger App is a Flask web application with a straightforward purpose:

    Button Push Logging:
        Every button push on the webpage is logged into an 'app-log' file with a timestamp.
        The last 6 entries are displayed on the webpage for quick reference.

    Error Management:
        If a false positive or double push is logged, you can easily delete it.
        Deletions are recorded in a separate 'deleted-entries-log' file, ensuring a clear record of all changes.

With the Button Logger App, you can efficiently monitor and manage button presses, maintaining accurate logs with ease.

this is the folder structure:

├── Dockerfile
└── app
    ├── app.py
    ├── log
    │   ├── app-log.txt
    │   └── deleted-entries-log.txt
    ├── static
    │   └── bla-bg.jpg
    └── templates
        └── index.html




