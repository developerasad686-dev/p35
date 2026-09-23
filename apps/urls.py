from django.urls import path

from apps.views import ProductDetailView, ProductListView, LoginTemplateView, ProfileTemplateView, RegisterTemplateView, SettingsTemplateView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail_page'),
    path('auth/login/', LoginTemplateView.as_view(), name='login_page'),
    path('auth/register/', RegisterTemplateView.as_view(), name='register_page'),
    path('auth/settings/', SettingsTemplateView.as_view(), name='settings_page'),
    path('pages/profile/', ProfileTemplateView.as_view(), name='profile_page'),
]