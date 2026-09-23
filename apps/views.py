from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from apps.models import Product



class ProductListView(ListView):
    model = Product
    template_name = 'apps/product-list.html'
    context_object_name = 'products'
    paginate_by = 3



class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product-details.html'
    context_object_name = 'product'
    
class LoginTemplateView(TemplateView):
    template_name = 'apps/auth/login.html'

class RegisterTemplateView(TemplateView):
    template_name = 'apps/auth/register.html'

class SettingsTemplateView(TemplateView):
    template_name = 'apps/auth/settings.html'
# Create your views here.
class ProfileTemplateView(TemplateView):
    template_name = 'apps/profile.html'