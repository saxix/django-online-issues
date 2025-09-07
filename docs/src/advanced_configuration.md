# Advanced Configuration

## Issue Template

You can customize the issue description by overriding the `ISSUE_TEMPLATE` setting. The default template is:

```
- User: {user}
- UserAgent: {user_agent}
- Remote IP: {remote_ip}
- Url: {url}
- Version: {version}
---
{description}

{screenshot}
```

## Annotations

The `ANNOTATIONS` setting allows you to override the functions used to get extra information for the issue. The default functions are:

- `get_client_ip`: `issues.utils.get_client_ip`
- `get_extra_info`: `issues.utils.get_extra_info`
- `get_labels`: `issues.utils.get_labels`
- `get_version`: `issues.utils.get_version`
- `get_user`: `issues.utils.get_user`
- `get_user_agent`: `issues.utils.get_user_agent`

You can provide your own functions to customize the information that is sent with the issue.
