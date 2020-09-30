from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

# ----------- import csv file of products and convert it into a list of dictionaries -----------
import csv

list_of_products = []

data = csv.DictReader(open("list_of_products.csv", encoding='utf-8-sig'), delimiter=';')

for d in data:
    list_of_products.append(d)

print(list_of_products)
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
        'products': list_of_products
    }
    return render(request, 'GreenBot/product_overview.html', context)


class MostExpensiveProducts(TemplateView):
    template_name = 'GreenBot/most_expensive_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = list_of_products
        return context


class MostSoldProducts(TemplateView):
    template_name = 'GreenBot/most_sold_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = list_of_products
        return context
