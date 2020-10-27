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


# ------------------------------------------- Load cashier tickets csv file on database --------------------------------

from. models import Products
import pandas as pd
from glob import glob

def cashierTicketsToDB():
    # combine cashier ticket files
    stock_files = sorted(glob('/Users/tim/Desktop/UNI.lu/Semester 3/BSP3/Code/GoodnessGroceries_Project/simulated_csv_files/cashier_tickets/cashier_ticket_*.csv'))
    result = pd.concat((pd.read_csv(file) for file in stock_files), ignore_index=True)
    result.to_csv('/Users/tim/Desktop/UNI.lu/Semester 3/BSP3/Code/GoodnessGroceries_Project/simulated_csv_files/cashier_tickets/cashier_tickets_combined.csv', index=False)

    # delete unnecessary columns
    for i in range((len(result.columns)-2)//3):
        result = result.drop(columns=['products/'+str(i)+'/product_name', 'products/'+str(i)+'/price'])

    # rename column headers in order for the models.py to be able to use it
    for i in range(len(result.columns)):
        result = result.rename({'products/'+str(i)+'/product_ean': 'products_'+str(i)+'_product_ean'}, axis=1)

    # rearrange rows an columns such that it fits in the model
    result = result.melt(id_vars=['participant_id', 'timestamp'], var_name='product_ean', value_name='products')
    result = result.drop(columns=['product_ean'])
    result = result.dropna()
    result = result.astype({'products': int})

    # remove products that are not part of the study
    p = pd.read_csv('/Users/tim/Desktop/UNI.lu/Semester 3/BSP3/Code/GoodnessGroceries_Project/static_csv_files/products.csv')
    code_of_products_in_study = []
    for code in p.code:
        code_of_products_in_study.append(code)
    result = result[result.products.isin(code_of_products_in_study)]

    # save file with combined and relevant data
    result.to_csv('/Users/tim/Desktop/UNI.lu/Semester 3/BSP3/Code/GoodnessGroceries_Project/simulated_csv_files/cashier_tickets/cashier_tickets_combined.csv', index=False)

    Products.objects.from_csv("simulated_csv_files/cashier_tickets/cashier_tickets_combined.csv")


# ------------------------------------------- Create TEST API ----------------------------------------------------------
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UsersSerializer, ProductsSerializer
from.models import Users


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Products.objects.all()
        serializer = ProductsSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
