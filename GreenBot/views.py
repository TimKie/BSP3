from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from product_list import products


@login_required()
def home(request):
    return render(request, 'GreenBot/home.html')


@login_required()
def about(request):
    return render(request, 'GreenBot/about.html', {'title': 'About'})


@login_required()
def product_overview(request):
    context = {
        'products': products
    }
    return render(request, 'GreenBot/product_overview.html', context)


class MostExpensiveProducts(TemplateView):
    template_name = 'GreenBot/most_expensive_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = products
        return context


class MostSoldProducts(TemplateView):
    template_name = 'GreenBot/most_sold_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = products
        return context
