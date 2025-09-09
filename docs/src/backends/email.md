# Email Backend

**Path**: `issues.backends.email.Backend`

The email backend sends issue details via email to specified recipients.

!!! note

    Ensure that Django's [email settings](https://docs.djangoproject.com/en/stable/topics/email/) are configured correctly in your project.


### Options:

-   **RECIPIENTS**: A list of email addresses to which the issue ticket will be sent.

-   **SENDER**: The email address from which the issue ticket will be sent.


### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.email.Backend",
    "OPTIONS": {
        "RECIPIENTS": ["dev@example.com", "support@example.com"],
        "SENDER": "do-not-replya@exampel.com"
    }
}
```
