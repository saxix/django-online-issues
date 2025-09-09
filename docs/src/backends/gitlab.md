# GitLab Backend

**Path**: `issues.backends.gitlab.Backend`

The GitLab backend creates an issue in a specified GitLab project.

### Options:

-   **API_TOKEN**: Your GitLab private access token with `api` scope.

-   **PROJECT**: The numeric ID or full path of your GitLab project (e.g., `group/project`).

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.gitlab.Backend",
    "OPTIONS": {
        "API_TOKEN": "glpat-xxxxxxxxxxxxxxxxxxxx",
        "PROJECT": "group/project",
    }
}
```
