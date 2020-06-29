from django.shortcuts import render
from django.http import HttpResponse
from django.http import *
from .models import SortedFile
from .forms import UserForm
from .parser import main_prod
import csv


def m304(request):
    return HttpResponseNotModified()


def m400(request):
    return HttpResponseBadRequest("<h2>Bad Request</h2>")


def m403(request):
    return HttpResponseForbidden("<h2>Forbidden</h2>")


def m404(request):
    return HttpResponseNotFound("<h2>Not Found</h2>")


def m405(request):
    return HttpResponseNotAllowed("<h2>Method is not allowed</h2>")


def m410(request):
    return HttpResponseGone("<h2>Content is no longer here</h2>")


def m500(request):
    return HttpResponseServerError("<h2>Something is wrong</h2>")


# получение данных из бд
def index(request):
    return render(request, "index.html")


def show(request):
    t = 'База данных'
    headers = {'id': 'Номер',
                'city':'Город',
                'address': 'Улица',
                'group': 'Сообщество',
                'number': 'Номер телефона сообщества',
                'group_ref': 'Ссылка на сообщество',
                'info': 'Информация о товарах'}
    sorts = SortedFile.objects.all()
    return render(request, "index.html", {"sorts": sorts, "h1": t, "headers": headers})


# сохранение данных в бд
def create(request):
    message=''
    if request.method == "POST":
        SortedFile.objects.all().delete()
        product_name = request.POST.get("product_name")
        city_name = request.POST.get("city_name")
        message = main_prod(product_name, city_name)
        counter = 0
        with open('vk_parser_sorted.csv', encoding='utf8', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Город':
                    counter = counter + 1
                    created = SortedFile.objects.get_or_create(
                       id=counter,
                       city=row[0],
                       address=row[1],
                       group=row[2],
                       number=row[3],
                       group_ref=row[4],
                       info=row[5],
                    )
        if message == 0:
            message = ''
    return render(request, "index.html", {"message": message})


