from django.shortcuts import render
from django.contrib.auth.decorators import login_required

products = [
    {
        'category': 'Meat',
        'name': 'Steak',
    },
    {
        'category': 'Vegetables',
        'name': 'Tomato',
    },
    {
        'category': 'Water',
        'name': 'Viva',
    },
    {
        'category': 'Milk',
        'name': 'Luxlait',
    },
    {
        'category': 'Meat',
        'name': 'Chicken Nuggets',
    },
    {
        'category': 'Vegetables',
        'name': 'Salad',
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
