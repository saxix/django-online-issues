# Available Backends and Options

Django Issues allows you to integrate with various issue tracking systems through its flexible backend architecture. Each backend handles the submission of issues differently, from simply printing to the console to creating tickets in external services like GitHub or GitLab.

Below is a list of the available backends and their specific configuration options:

## Console Backend (Default)

-   **Path**: `issues.backends.console.Backend`
-   **Description**: This is the default backend. It prints the issue details directly to the Django console.
-   **Options**: No specific options are required.

## Debug Backend

-   **Path**: `issues.backends.debug.DebugBackend`
-   **Description**: Stores the submitted issue in a Python list in memory. Useful for testing and debugging purposes without external dependencies.
-   **Options**: No specific options are required.

## Email Backend

-   **Path**: `issues.backends.email.Backend`
-   **Description**: Sends issue details via email to specified recipients.
-   **Options**:
    -   `RECIPIENTS`: A list of email addresses to which the issue ticket will be sent. Example: `["dev@example.com", "support@example.com"]`
    -   `SENDER`: The email address from which the issue ticket will be sent. Example: `"no-reply@your-app.com"`
-   **Note**: Ensure that Django's [email settings](https://docs.djangoproject.com/en/stable/topics/email/) are configured correctly in your project.

## GitHub Backend

-   **Path**: `issues.backends.github.Backend`
-   **Description**: Creates an issue in a specified GitHub repository.
-   **Options**:
    -   `API_TOKEN`: Your GitHub personal access token with appropriate repository permissions. Example: `"ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
    -   `PROJECT`: The username or organization and project name repository. Example: `"user/project"`
-   **Note**: This backend does not support screenshot uploads.


## GitLab Backend

-   **Path**: `issues.backends.gitlab.Backend`
-   **Description**: Creates an issue in a specified GitLab project.
-   **Options**:
    -   `API_TOKEN`: Your GitLab private access token with `api` scope. Example: `"glpat-xxxxxxxxxxxxxxxxxxxx"`
    -   `PROJECT`: The numeric ID or full path of your GitLab project (e.g., `group/project`). Example: `"your-group/your-project"` or `12345`

## GitHub Repo Backend

    A backend for creating issues on GitHub and uploading screenshots to the repository.
    It is intended to be used with a dedicated repository for the issues

    This backend requires a GitHub personal access token with the `public_repo` scope for
    public repositories, or the `repo` scope for private repositories.


-   **Path**: `issues.backends.github_repo.Backend`
-   **Description**: Creates an issue in a specified GitHub repository and uploads screenshots to the repository.
-   **Options**:
    -   `API_TOKEN`: Your GitHub personal access token with `public_repo` scope for public repositories, or `repo` scope for private repositories. Example: `"ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
    -   `PROJECT`: The username or organization and project name repository. Example: `"user/project"`
    -   `SCREENSHOT_REPO_PATH`: The path in the repository where screenshots will be stored. Defaults to `"screenshots/"`.
    -   `SCREENSHOT_BRANCH`: The branch where screenshots will be stored. Defaults to `"main"`.

### Configuration in Django Settings

To use a backend, you need to configure it in your Django project's `settings.py` file. The `ISSUES_BACKEND` setting should be a dictionary specifying the backend path and its options. For example:

```python
ISSUES_BACKEND = {
    "PATH": "issues.backends.github.Backend",
    "OPTIONS": {
        "API_TOKEN": "your_github_token",
        "PROJECT": "your_github_username/your_repo_name",
        "SCREENSHOT_REPO_PATH": "screenshots_folder/",
        "SCREENSHOT_BRANCH": "develop/",
    }
}
```

### Github Personal Access Token Configuration

If you want to use a Classic Personal Access Token (PAT)

note: In this case, the public_repo scope will appear explicitly in the list.


1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic).
1. Click Generate new token → Generate new token (classic).
1. Give it a descriptive note and set an expiration date. 4
1. Under Select scopes, check:

- repo → this covers both public and private repositories.
- If you only want public repositories, you can instead check public_repo.

6. Click Generate token.


If you want to use a Fine-grained Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens.
1. Click Generate new token.
1. Choose:

    - Resource owner (your account or organization).

    - Repository access → pick All repositories or specific ones.

1. Under Repository permissions, set the level you need (e.g., Read/Write for Contents, Metadata, Pull requests, etc.).

    - There is no single public_repo scope here, but you can replicate its effect by giving read/write access only to public repos.

![PAT configuration](./images/gh_token_perms.png)

1. Click Generate token.

**Important**: Avoid hardcoding sensitive information like API tokens directly in your `settings.py` file. Consider using environment variables or a dedicated secrets management solution for production environments.
