from django.db import models

class Product(models.Model):
    serial = models.CharField(max_length=255, unique=True)  # شماره سریال یا SKU
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    extra_data = models.JSONField(blank=True, null=True)  # برای هر دادهٔ اضافی
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial})"
