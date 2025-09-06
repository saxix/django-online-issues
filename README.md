# Django Online Issues


[![Test](https://github.com/saxix/django-online-issues/actions/workflows/test.yml/badge.svg)](https://github.com/saxix/django-online-issues/actions/workflows/test.yml)
[![Lint](https://github.com/saxix/django-online-issues/actions/workflows/lint.yml/badge.svg)](https://github.com/saxix/django-online-issues/actions/workflows/lint.yml)
[![codecov](https://codecov.io/github/saxix/django-online-issues/graph/badge.svg?token=FBUB7HML5S)](https://codecov.io/github/saxix/django-online-issues)
[![Documentation](https://github.com/saxix/django-online-issues/actions/workflows/docs.yml/badge.svg)](https://saxix.github.io/django-online-issues/)
[![Pypi](https://badge.fury.io/py/saxix-django-online-issues.svg)](https://badge.fury.io/py/saxix-django-online-issues)


**Django Online Issues** is a reusable Django app for collecting and reporting user-submitted issues (tickets).
It provides a view and a form to submit tickets and forwards them to configurable backends
like GitLab, GitHub, email, or simply the development console.

## Features

-   **Easy Integration**: Seamlessly add a ticketing system to your Django project.
-   **Multiple Backends**: Send tickets to various platforms. Built-in backends include:
    -   Console (default)
    -   Email
    -   GitLab
    -   GitHub
    -   (Others can be easily added)
-   **Configurable**: Customize the backend and its options through Django's settings.
-   **Extensible**: Create your own custom backends to integrate with any issue-tracking system.
-   **Screenshot Capture**: Users can attach a screenshot of the current page to the ticket.


### Planned (contributions are welcome)

- Jira
- Azure Devops
- Redmine
- Odoo Helpdesk
- ...

## Screenshot

#### In App popup (with ap screenshot)
<img src="docs/_images/popup.png" alt="Popup Screenshot" width="600"/>

#### GitLab Ticket
<img src="docs/_images/gitlab.png" alt="Popup Screenshot" width="600"/>

#### Github Ticket
<img src="docs/_images/github.png" alt="Popup Screenshot" width="600"/>
