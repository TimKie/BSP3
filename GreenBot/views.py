from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# ----------- import csv file of products and convert it into a list of dictionaries -----------
import csv


def load_csv_file():
    list_of_products = []

    data = csv.DictReader(open("list_of_products.csv", encoding='utf-8-sig'), delimiter=';')

    for d in data:
        list_of_products.append(d)
    return list_of_products
# ----------------------------------------------------------------------------------------------


@login_required()
def home(request):
    return render(request, 'GreenBot/home.html')


@login_required()
def about(request):
    return render(request, 'GreenBot/about.html', {'title': 'About'})


@login_required()
def product_overview(request):
    context = {
        'products': load_csv_file()
    }
    return render(request, 'GreenBot/product_overview.html', context)


class MostExpensiveProducts(TemplateView):
    template_name = 'GreenBot/most_expensive_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file()
        return context


class MostSoldProducts(TemplateView):
    template_name = 'GreenBot/most_sold_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file()
        return context


number_of_indicators = {}
class MostPopularIndicators(TemplateView):
    # ---- Get number of occurrences of the indicators -------------------------
    list_of_indicators = []
    for product in load_csv_file():
        list_of_indicators.append(product['indicator'])
        number_of_indicators[product['indicator']] = list_of_indicators.count(product['indicator'])
    # --------------------------------------------------------------------------
    template_name = 'GreenBot/most_popular_indicators.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = number_of_indicators
        return context
