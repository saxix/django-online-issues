# Creating a Custom Backend

You can create your own backend to integrate with other services.

1.  Create a new file, for example, `myapp/backends.py`.
2.  Define a `Backend` class that inherits from `issues.backends._base.BaseBackend`.
3.  Implement the `create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:` method.

```python
# myapp/backends.py
from issues.backends._base import BaseBackend
from issues.forms import IssueFormCleanedData

class MyCustomBackend(BaseBackend):
    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        """
        Sends the ticket to a custom service.

        'cleaned_data' is a dictionary containing the form data:
        - type: The type of the issue (e.g., 'bug', 'enhancement').
        - title: The ticket title.
        - description: The ticket description.
        - add_screenshot: A boolean indicating if a screenshot should be included.
        - screenshot: The base64-encoded image data (if 'add_screenshot' is True).
        """
        # You can get the full description, including context information,
        # by using the get_description method.
        full_description = self.get_description(cleaned_data)

        # Your logic to send the ticket to your service
        # For example, using an API client:
        #
        # my_api_client = Client(token=self.get_option("MY_API_KEY"))
        # my_api_client.create_issue(
        #     title=cleaned_data['title'],
        #     body=full_description,
        #     labels=[cleaned_data['type']],
        # )

        print(f"Ticket '{cleaned_data['title']}' created.")
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
