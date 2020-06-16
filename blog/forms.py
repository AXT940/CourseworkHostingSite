from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class DeletePostForm(forms.Form):
    delete_confirm = forms.BooleanField(initial=False, label="Please confirm that you wish to delete this post.")
