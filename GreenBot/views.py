from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

products = [
    {
        'category': 'Meat',
        'name': 'Steak',
        'price': 10,
    },
    {
        'category': 'Vegetables',
        'name': 'Tomato',
        'price': 5,
    },
    {
        'category': 'Water',
        'name': 'Viva',
        'price': 2,
    },
    {
        'category': 'Milk',
        'name': 'Luxlait',
        'price': 3,
    },
    {
        'category': 'Meat',
        'name': 'Chicken Nuggets',
        'price': 7,
    },
    {
        'category': 'Vegetables',
        'name': 'Salad',
        'price': 2,
    },
]


@login_required()
def home(request):
    context = {
        'products': products
    }
    return render(request, 'GreenBot/home.html', context)


@login_required()
def about(request):
    return render(request, 'GreenBot/about.html', {'title': 'About'})


class ChartView(TemplateView):
    template_name = 'GreenBot/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = products
        return context
