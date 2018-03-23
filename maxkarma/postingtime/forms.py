from django import forms

class SubredditForm(forms.Form):
    subreddit = forms.CharField(label='Subreddit (without /r/)', max_length=100)
