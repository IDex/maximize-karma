from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SubredditForm
from django.contrib import messages
from .maxkarmarec import get_recommendation
from .utils import hour_to_time
import datetime
from django.views.decorators.cache import cache_page


def index(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            return redirect(
                f"/postingtime/subreddit/{form.cleaned_data.get('subreddit')}")
        else:
            messages.add_message(request, messages.ERROR,
                                 'Invalid form input.')
    form = SubredditForm()
    context = dict(form=form)
    return render(request, 'postingtime/index.html', context)


@cache_page(None)
def get_subreddit(request, subreddit):
    lo, hi, img = get_recommendation(subreddit)
    context = {
        'recommendation':
        f'We recommend posting between {hour_to_time(lo)} and {hour_to_time(hi)} UTC.',
        'subreddit':
        f'{subreddit}',
        'img':
        img
    }
    return render(request, 'postingtime/subreddit.html', context)
