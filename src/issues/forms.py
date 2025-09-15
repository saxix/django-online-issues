from typing import TYPE_CHECKING, Any, TypedDict

from django import forms

if TYPE_CHECKING:
    from issues.backends._base import BaseBackend


class IssueFormCleanedData(TypedDict):
    type: str
    title: str
    description: str
    add_screenshot: bool
    screenshot: str


class IssueForm(forms.Form):
    type = forms.ChoiceField(
        choices=(
            ("bug", "bug"),
            ("enhancement", "enhancement"),
            ("feature", "feature"),
            ("suggestion", "suggestion"),
        )
    )
    title = forms.CharField(widget=forms.TextInput({"placeholder": "issue title", "autofocus": "autofocus"}))
    description = forms.CharField(widget=forms.Textarea({"placeholder": "description"}))
    add_screenshot = forms.BooleanField(required=False, widget=forms.CheckboxInput, initial=True)
    screenshot = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args: Any, backend: "BaseBackend", **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["type"].choices = backend.get_issue_choices()  # type: ignore[attr-defined]
