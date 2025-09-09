# Debug Backend

**Path**: `issues.backends.debug.Backend`

The debug backend stores the submitted issue in a Python list in memory. Useful for testing and debugging purposes without external dependencies.

### Options:

No specific options are required.

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.debug.Backend",
}
```
