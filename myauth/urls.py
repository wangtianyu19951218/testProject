from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myauth import views
#app_name = 'myauth'#只有在URL中声名app的名称，在网页中跳转URL
urlpatterns = [
    path('',views.home,name='homename'),
    path('login/',views.loginfun, name='login'),
    path('owner_login/', views.owner_login, name='owner_login'),
    #path('',views.home, name='backhome'),
    path('logout/', views.logoutfun),
    path('register/', views.register),
    path('search/', views.search,name='search'),
    path('test/', views.test, name='test'),
    path('showall/', views.showall, name='ajaxsend'),
    path('tes/', views.tes, name='tes'),
    path('input_shipinfo/', views.input_shipinfo, name='input_shipinfo'),
  ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)