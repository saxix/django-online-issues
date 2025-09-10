# Azure DevOps Backend

**Path**: `issues.backends.azure_devops.Backend`

The Azure DevOps backend creates a work item in a specified Azure DevOps project.

This backend supports screenshot uploads. The screenshot is uploaded as an attachment and linked in the description. The description is rendered as Markdown.

### Options:

-   **SERVER_URL**: Your Azure DevOps server URL. Defaults to `https://dev.azure.com`.
-   **PROJECT**: The name of your Azure DevOps organization and project, in the format `organization/project`.
-   **TOKEN**: Your Azure DevOps Personal Access Token with `Work Items - Read & Write` permissions.


### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.azure_devops.Backend",
    "OPTIONS": {
        "SERVER_URL": "https://dev.azure.com",
        "PROJECT": "your_organization/your_project",
        "TOKEN": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }
}
```
