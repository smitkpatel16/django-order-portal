from django.db import models

# Create your models here.


class Product(models.Model):
    productname = models.CharField(max_length=255, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    description = models.TextField()

    # this is done here to display a proper product name in inventory and order
    def __str__(self):
        return self.productname


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, default='Pending')
