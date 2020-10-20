from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# ----------- import csv a file and convert it into a list of dictionaries --------------------
import csv


def load_csv_file(file_name):
    output_list = []

    data = csv.DictReader(open(file_name, encoding='utf-8-sig'), delimiter=',')

    for d in data:
        output_list.append(d)
    return output_list
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
        'products': load_csv_file("static_csv_files/products.csv")
    }
    return render(request, 'GoodnessGroceries/product_overview.html', context)


class MostExpensiveProducts(TemplateView):
    template_name = 'GoodnessGroceries/most_expensive_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file("static_csv_files/products.csv")
        return context


class MostSoldProducts(TemplateView):
    template_name = 'GoodnessGroceries/most_sold_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file("static_csv_files/products.csv")
        return context


number_of_indicators = {}
class MostPopularIndicators(TemplateView):
    # ---- Get number of occurrences of the indicators -------------------------
    list_of_indicators = []
    for product in load_csv_file("static_csv_files/products.csv"):
        for i in range(3):
            indicator = product['indicators/'+str(i)+'/indicator_id']
            for ind in load_csv_file("static_csv_files/indicators.csv"):
                if indicator == ind['id']:
                    list_of_indicators.append(ind['name'])
                    number_of_indicators[ind['name']] = list_of_indicators.count(ind['name'])
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
    for product in load_csv_file("static_csv_files/products.csv"):
        list_of_product_types.append(product['type'])
        number_of_product_types[product['type']] = list_of_product_types.count(product['type'])
    # --------------------------------------------------------------------------
    template_name = 'GoodnessGroceries/most_popular_product_types.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = number_of_product_types
        return context

