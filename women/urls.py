from django.urls import path, re_path, register_converter
from women import views
from women import converters
from django.views.decorators.cache import cache_page


register_converter(converters.FourDigitYearConverter, 'year4')


urlpatterns = [path('', views.WomenHome.as_view(), name='home'),
               path('about/', views.about, name='about'),
               path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
               path('add_page/', views.AddPage.as_view(), name='addpost'),
               path('edit/<int:pk>', views.UpdatePage.as_view(), name='editpost'),
               path('delete/<int:pk>', views.DeletePage.as_view(), name='deletepost'),
               path('contact/', views.Contact.as_view(), name='contact'),
               path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
               path('tag/<slug:tag_slug>', views.WomenTag.as_view(), name='tag'),
               ]