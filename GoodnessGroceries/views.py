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
    return render(request, 'GoodnessGroceries/home.html')


@login_required()
def about(request):
    return render(request, 'GoodnessGroceries/about.html', {'title': 'About'})


@login_required()
def product_overview(request):
    context = {
        'products': load_csv_file()
    }
    return render(request, 'GoodnessGroceries/product_overview.html', context)


class MostExpensiveProducts(TemplateView):
    template_name = 'GoodnessGroceries/most_expensive_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file()
        return context


class MostSoldProducts(TemplateView):
    template_name = 'GoodnessGroceries/most_sold_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file()
        return context


number_of_indicators = {}
class MostPopularIndicators(TemplateView):
    # ---- Get number of occurrences of the indicators -------------------------
    list_of_indicators = []
    for product in load_csv_file():
        for indicator in product['product_indicators'].split(","):
            list_of_indicators.append(indicator)
            number_of_indicators[indicator] = list_of_indicators.count(indicator)
    # --------------------------------------------------------------------------
    template_name = 'GoodnessGroceries/most_popular_indicators.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = number_of_indicators
        return context


number_of_product_types = {}
class MostPopularProductTypes(TemplateView):
    # ---- Get number of occurrences of the product types -------------------------
    list_of_product_types = []
    for product in load_csv_file():
        list_of_product_types.append(product['product_type'])
        number_of_product_types[product['product_type']] = list_of_product_types.count(product['product_type'])
    # --------------------------------------------------------------------------
    template_name = 'GoodnessGroceries/most_popular_product_types.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = number_of_product_types
        return context
