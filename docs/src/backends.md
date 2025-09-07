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

## Configuration in Django Settings

To use a backend, you need to configure it in your Django project's `settings.py` file. The `ISSUES_BACKEND` setting should be a dictionary specifying the backend path and its options. For example:

```python
ISSUES_BACKEND = {
    "PATH": "issues.backends.github.Backend",
    "OPTIONS": {
        "API_TOKEN": "your_github_token",
        "REPOSITORY_OWNER": "your_github_username",
        "REPOSITORY_NAME": "your_repo_name",
    }
}
```

**Important**: Avoid hardcoding sensitive information like API tokens directly in your `settings.py` file. Consider using environment variables or a dedicated secrets management solution for production environments.
