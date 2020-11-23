from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import *

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
    users = Users.objects.all()
    prod_reviews = ProductReviews.objects.all()

    # get total number of users and product reviews
    total_users = users.count()
    total_prod_reviews = prod_reviews.count()

    # order product reviews per participant_id and timestamp
    same_ids = []
    for prod_review in prod_reviews:
        same_ids.append(prod_review.participant_id)

    prod_reviews_with_same_id = dict()
    for id in sorted(set(same_ids)):
        prod_reviews_with_same_id[id] = prod_reviews.filter(participant_id=id).order_by('-timestamp')

    # get number of product reviews per day for past 10 days
    timestamps = []
    recent_prod_review_of_last_10_days = ProductReviews.objects.order_by('-timestamp')
    for prod_review in recent_prod_review_of_last_10_days:
        if prod_review.timestamp.date() not in timestamps:
            timestamps.append(prod_review.timestamp.date())

    number_of_prod_reviews_per_day = dict()

    for date in timestamps[:10]:
        number_of_prod_reviews_per_day[date] = 0
        for prod_review in prod_reviews:
            if prod_review.timestamp.date() == date:
                number_of_prod_reviews_per_day[date] += 1

    context = {'total_users': total_users, 'total_prod_reviews': total_prod_reviews,
               'prod_reviews_with_same_id': prod_reviews_with_same_id,
               'number_of_prod_reviews_per_day': number_of_prod_reviews_per_day}

    return render(request, 'GoodnessGroceries/home.html', context)


@login_required()
def about(request):
    return render(request, 'GoodnessGroceries/about.html', {'title': 'About'})


# ---------- Get products data from database, put them in a csv file and return this file ------------------------------
def get_products_from_db():
    with open('products.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['code', 'name', 'description', 'type', 'category', 'provider', 'image_url',
                         'indicators_0_indicator_id', 'indicators_0_indicator_description',
                         'indicators_1_indicator_id', 'indicators_1_indicator_description',
                         'indicators_2_indicator_id', 'indicators_2_indicator_description'])

        for product in StaticProducts.objects.all().values_list('code', 'name', 'description', 'type', 'category',
                                                                'provider', 'image_url',
                                                                'indicators_0_indicator_id',
                                                                'indicators_0_indicator_description',
                                                                'indicators_1_indicator_id',
                                                                'indicators_1_indicator_description',
                                                                'indicators_2_indicator_id',
                                                                'indicators_2_indicator_description'):
            writer.writerow(product)


@login_required()
def product_overview(request):
    products = StaticProducts.objects.all()

    context = {'products': products}

    return render(request, 'GoodnessGroceries/product_overview.html', context)


# ----------------------------------- Filter Users ---------------------------------------------------------------------
from .filters import UserFilter

@login_required()
def user_overview(request):
    users = Users.objects.all()

    myFilter = UserFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {'users': users, 'myFilter': myFilter}

    return render(request, 'GoodnessGroceries/user_overview.html', context)


@login_required()
def user_overview_filtered(request, participant_id):
    users = Users.objects.filter(participant_id=participant_id).order_by('-participant_id')

    myFilter = UserFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {'users': users, 'myFilter': myFilter}

    return render(request, 'GoodnessGroceries/user_overview.html', context)


# ------------------------------------------ Product Reviews -----------------------------------------------------------
def product_reviews_overview(request):
    prod_reviews = ProductReviews.objects.all()

    same_ids = []
    for prod_review in prod_reviews:
        same_ids.append(prod_review.participant_id)

    prod_reviews_with_same_id = dict()
    for id in sorted(set(same_ids)):
        prod_reviews_with_same_id[id] = prod_reviews.filter(participant_id=id).order_by('-timestamp')

    context = {'prod_reviews_with_same_id': prod_reviews_with_same_id}

    return render(request, 'GoodnessGroceries/product_reviews_overview.html', context)


# ------------------------------------------ Statistics ----------------------------------------------------------------
class MostExpensiveProducts(TemplateView):
    template_name = 'GoodnessGroceries/most_expensive_products.html'

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file("static_csv_files/products.csv")
        return context
    """


class MostSoldProducts(TemplateView):
    template_name = 'GoodnessGroceries/most_sold_products.html'

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = load_csv_file("static_csv_files/products.csv")
        return context
    """


number_of_indicators = {}
class MostPopularIndicators(TemplateView):
    template_name = 'GoodnessGroceries/most_popular_indicators.html'

    """
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = number_of_indicators
        return context
    """


number_of_product_types = {}
class MostPopularProductTypes(TemplateView):
    template_name = 'GoodnessGroceries/most_popular_product_types.html'

    """
    # ---- Get number of occurrences of the product types -------------------------
    list_of_product_types = []
    for product in load_csv_file("static_csv_files/products.csv"):
        list_of_product_types.append(product['type'])
        number_of_product_types[product['type']] = list_of_product_types.count(product['type'])
    # --------------------------------------------------------------------------

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = number_of_product_types
        return context
    """


# ------------------------------ Automated Check for unprocessed files and process them --------------------------------
import pandas as pd
from glob import glob
import os


o_directory = '/Users/tim/Desktop/UNI.lu/Semester_3/BSP3/Code/GoodnessGroceries_Project/simulated_csv_files/files_to_be_processed/'

o_path = '/Users/tim/Desktop/UNI.lu/Semester_3/BSP3/Code/GoodnessGroceries_Project/simulated_csv_files/files_to_be_processed/cashier_ticket_*.csv'
d_path = '/Users/tim/Desktop/UNI.lu/Semester_3/BSP3/Code/GoodnessGroceries_Project/simulated_csv_files/processed_files/last_processed_cashier_ticket.csv'


def check_for_files(origin_path, destination_path):
    if len(glob(origin_path)) != 0:
        if os.path.isfile(glob(origin_path)[0]):
            cashierTicketsToDB(origin_path, destination_path)
            for file_id in range(len(glob(origin_path))):
                os.replace(glob(origin_path)[0], destination_path)


def cashierTicketsToDB(origin_path, destination_path):
    # combine cashier ticket files
    stock_files = sorted(glob(origin_path))
    result = pd.concat((pd.read_csv(file) for file in stock_files), ignore_index=True)
    result.to_csv(destination_path, index=False)

    # delete unnecessary columns
    for i in range((len(result.columns)-2)//3):
        result = result.drop(columns=['products/'+str(i)+'/product_name', 'products/'+str(i)+'/price'])

    # rename column headers in order for the models.py to be able to use it
    for i in range(len(result.columns)):
        result = result.rename({'products/'+str(i)+'/product_ean': 'product_'+str(i)+'_product_ean'}, axis=1)

    # rearrange rows an columns such that it fits in the model
    result = result.melt(id_vars=['participant_id', 'timestamp'], var_name='product_ean', value_name='product')
    result = result.drop(columns=['product_ean'])
    result = result.dropna()
    result = result.astype({'product': int})

    # remove products that are not part of the study
    get_products_from_db()
    p = pd.read_csv('products.csv')
    code_of_products_in_study = []
    for code in p.code:
        code_of_products_in_study.append(code)
    result = result[result['product'].isin(code_of_products_in_study)]

    # save file with combined and relevant data
    result.to_csv(destination_path, index=False)

    CashierTicketProducts.objects.from_csv(destination_path)


# ------------------------------------------- Import - Export ----------------------------------------------------------
def ImportExportView(request):
    template = 'GoodnessGroceries/import_export.html'

    return render(request, template)


# ------------------------------------------- Upload of Static Files ---------------------------------------------------
import io
from.models import StaticProducts, StaticIndicators, StaticIndicatorCategories


@login_required()
def static_products_upload(request):
    template = 'GoodnessGroceries/upload_static_products.html'

    if request.method == 'POST':
        uploaded_file = request.FILES['static_products_file']

        data_set = uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            _, created = StaticProducts.objects.update_or_create(
                code=column[0],
                name=column[1],
                description=column[2],
                type=column[3],
                category=column[4],
                provider=column[5],
                image_url=column[6],
                indicators_0_indicator_id=column[7],
                indicators_0_indicator_description=column[8],
                indicators_1_indicator_id=column[9],
                indicators_1_indicator_description=column[10],
                indicators_2_indicator_id=column[11],
                indicators_2_indicator_description=column[12]
            )

    return render(request, template)


@login_required()
def static_indicators_upload(request):
    template = 'GoodnessGroceries/upload_static_indicators.html'

    if request.method == 'POST':
        uploaded_file = request.FILES['static_indicators_file']

        data_set = uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            _, created = StaticIndicators.objects.update_or_create(
                id=column[0],
                name=column[1],
                category_id=column[2],
                icon_name=column[3],
                general_description=column[4]
            )

    return render(request, template)


@login_required()
def static_indicator_categories_upload(request):
    template = 'GoodnessGroceries/upload_static_indicator_categories.html'

    if request.method == 'POST':
        uploaded_file = request.FILES['static_indicator_categories_file']

        data_set = uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            _, created = StaticIndicatorCategories.objects.update_or_create(
                id=column[0],
                name=column[1],
                icon_name=column[2],
                description=column[3]
            )

    return render(request, template)


# ------------------------------------------- Download Dynamic CSV Files -----------------------------------------------
from django.views.generic import View
from django.http import HttpResponse


# cashier tickets products download
class CashierTicketsProductsDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('cashier_tickets_products.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('participant_id', 'timestamp', 'product')
        data = CashierTicketProducts.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# product reviews download
class ProductReviewsDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('product_reviews.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('participant_id', 'product_ean', 'selected_indicator_main_id', 'selected_indicator_secondary_id',
                      'free_text_indicator', 'price_checkbox_selected')
        data = ProductReviews.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# monitoring data download
class MonitoringDataDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('monitoring_data.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('participant_id', 'timestamp', 'activity_name', 'metadata')
        data = MonitoringData.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# users download
class UsersDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('users.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('participant_id', 'status', 'product_category_1', 'product_category_2', 'product_category_3', 'product_category_4',
                      'indicator_category_1', 'indicator_category_2', 'indicator_category_3', 'indicator_category_4')
        data = Users.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# ------------------------------------------- Download Static CSV Files ------------------------------------------------
# static products download
class StaticProductsDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('static_products.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('code', 'name', 'description', 'type', 'category', 'provider', 'image_url', 'indicators_0_indicator_id',
                      'indicators_0_indicator_description', 'indicators_1_indicator_id', 'indicators_1_indicator_description',
                      'indicators_2_indicator_id', 'indicators_2_indicator_description')
        data = StaticProducts.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# static indicators download
class StaticIndicatorsDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('static_indicators.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('id', 'name', 'category_id', 'icon_name', 'general_description')
        data = StaticIndicators.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# static indicator categories download
class StaticIndicatorCategoriesDownload(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format('static_indicator_categories.csv')
        response['Content-Disposition'] = cd

        fieldnames = ('id', 'name', 'icon_name', 'description')
        data = StaticIndicatorCategories.objects.values(*fieldnames)

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response


# ------------------------------------------- Create APIs --------------------------------------------------------------
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CashierTicketProductsSerializer, MonitoringDataSerializer, ProductReviewsSerializer, UsersSerializer, UsersStatusSerializer


class GetBoughtProducts(APIView):
    def get(self, request, participant_id, *args, **kwargs):
        # return 404 error if request id is not in the database
        try:
            product = CashierTicketProducts.objects.filter(participant_id=participant_id, reviewed=False)
        except CashierTicketProducts.DoesNotExist:
            return HttpResponse(status=404)
        serializer = CashierTicketProductsSerializer(product, many=True)
        return Response(serializer.data)


class PostMonitoringData(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MonitoringDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PostProductsReview(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class FetchUserStatus(APIView):
    def get(self, request, participant_id, *args, **kwargs):
        # return 404 error if request id is not in the database
        try:
            user = Users.objects.get(participant_id=participant_id)
        except Users.DoesNotExist:
            return HttpResponse(status=404)
        serializer = UsersStatusSerializer(user, many=False)
        return Response(serializer.data)


class RequestUserAccess(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            if Users.objects.filter(participant_id=request.data['participant_id']).exists():
                return Response(serializer.errors)
            else:
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(serializer.errors)
