from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shopping.urls')),
    path('register/', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'),name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'),name = 'logout'),
    path('profile/', user_views.updateProfile, name = 'profile'),
    path('cart/<str:par1>/<str:par2>/', user_views.updateCart, name = 'cart'),
    path('mycart/', user_views.viewCart, name = 'mycart'),
    path('checkout/', user_views.checkout, name = 'checkout'),
    path('orders/', user_views.viewOrder.as_view(), name='orders')
]

if(settings.DEBUG):
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 