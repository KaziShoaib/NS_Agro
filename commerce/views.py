from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from commerce.models import *

from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.

#@login_required(login_url='login')
def index(request):
  items = Item.objects.all()
  return render(request, 'commerce/index.html', {
    'items':items
  })


def login_view(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request,user)
      return HttpResponseRedirect(reverse('index'))
    else:
      return render(request, 'commerce/login.html', {
        'message':'wrong credentials'
      })
  else:
    return render(request, 'commerce/login.html')


@login_required(login_url='login')
def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def addItem_view(request):
  if request.method == 'POST':
    name = request.POST['name']
    description = request.POST['description']
    price = float(request.POST['price'])
    
    files = request.FILES
    image = files.get("image")

    i = Image.open(image)
    if i.format == 'PNG':
      i = i.convert('RGB')
    thumb_io = BytesIO()
    i.save(thumb_io, format='JPEG', quality=80)
    inmemory_uploaded_file = InMemoryUploadedFile(thumb_io, None, 'foo.jpeg', 'image/jpeg', thumb_io.tell(), None)

    seller_id = int(request.POST['seller'])
    seller = Seller.objects.get(id=seller_id)

    item = Item(name=name, description=description, price=price, image=inmemory_uploaded_file, seller=seller)
    item.save()

    return HttpResponseRedirect(reverse('index'))


  else:
    sellers = Seller.objects.all()
    return render(request, 'commerce/addItem.html', {
      'sellers':sellers
    })


@login_required(login_url='login')
def seller_view(request):
  if request.method == 'POST':
    name = request.POST['name']
    phone = request.POST['phone']
    seller = Seller(name=name, phoneNumber=phone)
    seller.save()
    return HttpResponseRedirect(reverse('sellers'))
  else:
    sellers = Seller.objects.all()
    return render(request, 'commerce/seller.html', {
      'sellers':sellers
    })


@login_required(login_url='login')
def deleteSeller_view(request, id):
  seller = Seller.objects.get(id=id)
  seller.delete()
  return HttpResponseRedirect(reverse('sellers'))


@login_required(login_url='login')
def deleteItem_view(request, id):
  item = Item.objects.get(id=id)
  item.delete()
  return HttpResponseRedirect(reverse('index'))
