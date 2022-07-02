from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path("login", views.login_view, name="login"),
  path('logout', views.logout_view, name="logout"),
  path('addItem', views.addItem_view, name="addItem"),
  path('sellers', views.seller_view, name='sellers'),
  path('deleteSeller/<int:id>', views.deleteSeller_view, name='deleteSeller'),
  path('deleteItem/<int:id>', views.deleteItem_view, name='deleteItem')
]
