# GitHub Repo Backend

**Path**: `issues.backends.github_repo.Backend`

The GitHub Repo backend creates an issue in a specified GitHub repository and uploads screenshots to the repository.

!!!note

    This backend require the `public_repo` permission granted to the token


### Options:

-   **API_TOKEN**: Your GitHub personal access token with `public_repo` scope for public repositories, or `repo` scope for private repositories.

-   **PROJECT**: The username or organization and project name repository.

-   **SCREENSHOT_REPO_PATH**: The path in the repository where screenshots will be stored.

-   **SCREENSHOT_BRANCH**: The branch where screenshots will be stored.

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.github_repo.Backend",
    "OPTIONS": {
        "API_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "PROJECT": "user/repo",
        "SCREENSHOT_REPO_PATH": "screenshots/",
        "SCREENSHOT_BRANCH": "main",
    }
}
```

#### How to configure your token

#####  1) Classic Personal Access Token (PAT)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic).
1. Click Generate new token → Generate new token (classic).
1. Give it a descriptive note and set an expiration date.
1. Under Select scopes, check:

      - repo → this covers both public and private repositories.
      - If you only want public repositories, you can instead check public_repo.

1. Click Generate token.

1.  Copy the token (you won’t be able to see it again).

In this case, the public_repo scope will appear explicitly in the list.

---

##### 2) Fine-grained Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens.
1. Click Generate new token.
1. Choose:
      - Resource owner (your account or organization).
      - Repository access → pick All repositories or specific ones.
1. Under Repository permissions, set the level you need.

       ![sc](../images/gh_token_perms.png)

1. Click Generate token.
