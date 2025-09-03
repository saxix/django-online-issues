from django import forms


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
    url = forms.CharField(widget=forms.HiddenInput, required=False)
    add_screenshot = forms.BooleanField(required=False, widget=forms.CheckboxInput, initial=True)
    screenshot = forms.CharField(widget=forms.HiddenInput, required=False)
