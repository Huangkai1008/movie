from django import forms


class CommentForm(forms.Form):
    """
    评论表单
    """
    content = forms.CharField(required=True, widget=forms.Textarea)
    user_id = forms.CharField(widget=forms.HiddenInput)
    movie_id = forms.CharField(widget=forms.HiddenInput)