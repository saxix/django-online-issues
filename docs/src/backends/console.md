# Console Backend

**Path**: `issues.backends.console.Backend`

The console backend is the default backend. It prints the issue details directly to the Django console.

### Options:

No specific options are required.

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.console.Backend",
}
```
