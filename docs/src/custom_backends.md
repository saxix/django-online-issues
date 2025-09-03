# Creating a Custom Backend

You can create your own backend to integrate with other services.

1.  Create a new file, for example, `myapp/backends.py`.
2.  Define a `Backend` class that inherits from `issues.backends._base.BaseBackend`.
3.  Implement the `create_ticket(self, data: dict)` method.

```python
# myapp/backends.py

from issues.backends._base import BaseBackend

class MyCustomBackend(BaseBackend):
    def create_ticket(self, data: dict[str, any]) -> bool:
        """
        Sends the ticket to a custom service.

        'data' contains:
        - title: The ticket title.
        - description: The ticket description.
        - screenshot: The base64-encoded image (if present).
        - ... and other info added via 'get_ticket_data'.
        """
        ticket_data = self.get_ticket_data(data)
        # Your logic to send the ticket
        print(f"Ticket created: {ticket_data['title']}")
        return True
```

4.  Update your `settings.py` to use the new backend:

```python
# settings.py

ISSUES = {
    "BACKEND": "myapp.backends.MyCustomBackend",
    "OPTIONS": {
        "MY_API_KEY": "secret-key",
    },
}
```
You can access the options in your backend with `self.get_option("MY_API_KEY")`.
