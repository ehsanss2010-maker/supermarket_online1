from django.db import models

class Product(models.Model):
    serial = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=512)
    category = models.CharField(max_length=256, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial} - {self.name}"
