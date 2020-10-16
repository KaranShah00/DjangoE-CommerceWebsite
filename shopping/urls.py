from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.ProductListView.as_view()),
    path('home/', views.ProductListView.as_view(), name="shopping-home"),
    path('home/<str:par>/', views.ProductListView.as_view(), name="shopping-home-parameters"),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name="product-detail"),
    path('review/<int:pk>/update/', views.editReview.as_view(), name = 'review-update'),
    path('review/<int:pk>/delete/', views.deleteReview.as_view(), name = 'review-delete'),
    path('search/', views.SearchListView.as_view(), name = 'search-result')
]
