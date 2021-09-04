from django.http import HttpResponse
from django.shortcuts import render
import csv
import pandas as pd
import math

# Create your views here.
from django.views.generic import TemplateView, FormView
from .forms import TickerForm

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))


class PortfolioHomeView(FormView):
    form_class = TickerForm
    template_name = 'portfolio/portfolio.html'
    success_url = '/portfolio/'

    def form_valid(self, form):
        tickers = self.request.POST.getlist('state[]')
        print(tickers)
        with open('./apps/data/tickers.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(tickers)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        old_df = pd.read_csv('./apps/data/tickers.csv', sep=',', header=None)
        df = old_df.transpose()
        weights = [1 / df.shape[0] for i in list(range(df.shape[0]))]
        with open('./apps/data/weights.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(weights)
        df.columns = ['tickers']
        weights_df = pd.read_csv('./apps/data/weights.csv', header=None)
        df['weights'] = weights_df.transpose()
        context['newport'] = df.transpose()
        return context

