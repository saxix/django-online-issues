# Usage

To display the issue reporting button in your templates, load the `issues` template tags and use the `issues_tags` tag. This is typically done in your base template.

```html
{% load issues %}

<!DOCTYPE html>
<html>
<head>
    ...
    {% issues_tags %}
</head>
<body>
    ...
    <a href="#" id="issue-opener">open issue</a>
</body>
</html>
```

This will render the necessary script tags and the issue reporting button.
