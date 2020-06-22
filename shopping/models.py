from django.db import models

class Product(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField()
	image = models.ImageField(default = 'default.jpg', upload_to = 'product_pics')
	cost = models.FloatField(default = 0.0)
	avg_rating = models.FloatField(null = True, blank = True)

	def __str__(self):
		return self.title