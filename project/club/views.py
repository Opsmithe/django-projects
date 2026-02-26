from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Names

# Create your views here.
def members(request):
    mymembers = Names.objects.all()
    paginator = Paginator(mymembers, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.page(page_number)

    return render(request, 'first.html', {'page': page})

def details(request, slug):
    mymember = get_object_or_404(Names, slug=slug)
    return render(request, 'details.html', {'mymember': mymember})

def main(request):
    return render(request, 'main.html')

def testing(request):
    context = {'fruits': ["banana", "apple", "oranges"]}
    return render(request, 'test.html', context)

