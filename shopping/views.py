from django.shortcuts import render, redirect
from .models import Product
from users.models import Reviews
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.forms import ProductReviewForm
from django.urls import reverse
from django.contrib import messages
from users.models import Cart, Reviews
from users.views import placeOrder
from django import template


class SearchListView(ListView):
    model = Product
    template_name = 'shopping/search_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(title__icontains=query)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'shopping/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        for prod in qs:
            total_reviews, count = 0, 0
            reviews = Reviews.objects.filter(product__pk=prod.pk)
            #print(f'{prod} review is {reviews.count()}')
            for review in reviews:
                total_reviews += review.rating
                count += 1
            if (count != 0):
                avg_review = total_reviews / count
                avg_review = float(round(avg_review, 2))
                Product.objects.filter(pk=prod.pk).update(avg_rating=avg_review)
            else:
                Product.objects.filter(pk=prod.pk).update(avg_rating=0)
        if (self.kwargs.get('par', None) == None):
            qs = qs.order_by("-id")
        elif (self.kwargs['par'] == 'flash'):
            qs = qs.order_by("-id")
            placeOrder(self.request)
            messages.success(self.request, f'Your order has been placed successfully')
            Cart.objects.filter(user=self.request.user).delete()
        elif (self.kwargs['par'] == 'cost'):
            qs = qs.order_by("-cost")
        elif (self.kwargs['par'] == 'ratings'):
            qs = qs.order_by("-avg_rating")
        elif (self.kwargs['par'] == 'cost_filter'):
            start = self.request.GET.get('from')
            end = self.request.GET.get('to')
            if start != "" and end != "":
                qs = Product.objects.filter(cost__gte=start, cost__lte=end)
        elif (self.kwargs['par'] == 'rating_filter'):
            start = self.request.GET.get('from')
            end = self.request.GET.get('to')
            if start != "" and end != "":
                qs = Product.objects.filter(avg_rating__gte=start, avg_rating__lte=end)
        return qs


class editReview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reviews
    fields = ['comment', 'rating']

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.get_object().product.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.get_object().product
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        if (review.user == self.request.user):
            return True
        else:
            return False


class deleteReview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reviews

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.get_object().product.pk})

    def test_func(self):
        # print("id " + str(self.kwargs['id']))
        # print(Reviews.objects.filter(pk = self.kwargs['id']).first())
        # review = Reviews.objects.filter(pk = self.kwargs['id']).first()
        review = self.get_object()
        if (review.user == self.request.user):
            return True
        else:
            return False


class ProductDetailView(DetailView):
    model = Product


    # def form_valid(self, form):
    # 	form.instance.author = self.request.user
    # 	return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'request': self.request})
    #     return kwargs

    # def __init__(self, *args, **kwargs):
    # 	super(ProductDetailView, self).__init__(*args, **kwargs)
    # 	form = ProductReviewForm()
    # 	form.instance.user = self.request.user
    # 	form.instance.product = kwargs.get(pk)

    def avgReview(self):
        prod = Product.objects.get(pk=self.kwargs['pk'])

        total_reviews, count = 0, 0
        reviews = Reviews.objects.filter(product__pk=prod.pk)
        for review in reviews:
            total_reviews += review.rating
            count += 1
        if (count != 0):
            avg_review = total_reviews / count
            avg_review = float(round(avg_review, 2))
            Product.objects.filter(pk=prod.pk).update(avg_rating=avg_review)
        else:
            Product.objects.filter(pk=prod.pk).update(avg_rating=0)

    def addReview(self, request, **kwargs):
        form = ProductReviewForm(request.POST)
        form.instance.user = self.request.user
        form.instance.product = Product.objects.filter(id=kwargs.get('pk')).first()
        if (form.is_valid()):
            form.save()

    def post(self, request, **kwargs):
        self.addReview(request, **kwargs)
        return redirect('product-detail', pk=kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add = 'add'
        remove = 'remove'
        context['add'] = add
        context['remove'] = remove
        context['form'] = ProductReviewForm()
        reviews = Reviews.objects.filter(product__pk = self.kwargs['pk'])
        context['reviews'] = reviews
        has_reviewed = False
        if self.request.user.is_authenticated:
	        if Reviews.objects.filter(user=self.request.user, product=self.get_object()).count():
	            has_reviewed = True
        self.avgReview()
        # total_reviews, count = 0, 0
        # for review in reviews:
        # 	total_reviews += review.rating
        # 	count += 1
        # if(count != 0):
        # 	avg_review = total_reviews/count
        # 	avg_review = float(round(avg_review,2))
        # 	# This is an alternative method to update.
        # 	# p = Product.objects.filter(id = self.kwargs.get('pk')).first()
        # 	# p.avg_rating = avg_review
        # 	# p.save()
        # 	Product.objects.filter(id = self.kwargs.get('pk')).update(avg_rating = avg_review)
        # else:
        # 	Product.objects.filter(id = self.kwargs.get('pk')).update(avg_rating = 0)
        # 	avg_review = 0
        context['avg_review'] = Product.objects.get(pk = self.kwargs['pk']).avg_rating
        context['has_reviewed'] = has_reviewed
        return context