# coding: utf-8
# # Analyze the relationship between a post getting karma and the the time the post was made

import scipy as sc
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import praw
from .secrets import cid, cs
import datetime

import pomegranate
from pomegranate import *

import pymc3

def get_recommendation(subreddit):
    df = pd.DataFrame
    p = praw.Reddit(
        client_id=cid, client_secret=cs, user_agent='sub-scraper script')

    posts = [(datetime.datetime.utcfromtimestamp(subm.created_utc).hour,
              subm.score) for subm in p.subreddit(subreddit).top(limit=1000)]
    data = pd.DataFrame(posts, columns=['hour', 'score'])

    def make_plots(X, x='hour', y='score'):
        X1 = X.copy()
        X1.hour = X1.hour.apply(lambda x: int(x))
        X1.groupby('hour').mean().plot.bar()
        X1.groupby('hour').sum().plot.bar()
        plt.figure()
        sns.regplot(data=X, x=x, y=y)

    # data.plot.hist(x='hour', y='score')
    X = data[data.score > sc.percentile(data.score, 80)]
    # make_plots(X)

    def make_gmm(n_components=3, shift=0):
        while True:
            m = GeneralMixtureModel.from_samples(
                NormalDistribution,
                n_components=n_components,
                X=X.hour.values.reshape(-1, 1),
                weights=X.score.values)
            #m=GaussianKernelDensity.from_samples(X.hour.values.reshape(-1,1), weights=X.score.values)
            xx = sc.linspace(0 - shift, 24 + shift, 1000)
            yy = m.probability(xx)
            if not sc.isnan(yy).any():
                break
        return m, xx, yy

    m, xx, yy = make_gmm(3)
    samples = sc.array(m.sample(10000))
    p = 10
    lo, hi = pymc3.stats.hpd(samples, alpha=1 - p / 100)
    # print(f'We recommend posting between {lo} and {hi} for a benefit of {round(100*(data[[lo<x<hi for x in data.hour]].score.mean()/data.score.mean()-1))}%')
    return (lo, hi)
