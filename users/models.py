from django.db import models
from django.contrib.auth.models import User
from shopping.models import Product
from django.urls import reverse
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
	address = models.TextField(max_length = 1000, null = True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)
		img = Image.open(self.image.path)

		if(img.height > 300 or img.width > 300):
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return str(self.user) + "'s Cart"

class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	amount = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.customer}'s order"

class OrderDetails(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	subtotal = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Order Details'

	def __str__(self):
		return f'{self.order}: {self.product}'

class Reviews(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	comment = models.TextField(max_length = 1000)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
        )

	rating = models.IntegerField(choices = RATINGS)
	
	class Meta:
		ordering = ['-rating']
		verbose_name_plural = 'Reviews'

	def __str__(self):
		return f'{self.user}: {self.rating} stars'

	def get_absolute_url(self):
		return reverse('product-detail', kwargs = {'pk': self.pk})