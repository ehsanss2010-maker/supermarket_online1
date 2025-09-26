from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from .models import Product
from .utils import import_products_from_file  # تابعی که می‌نویسیم

class UploadFileForm(forms.Form):
    excel_file = forms.FileField(label="فایل اکسل (xls یا xlsx)")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('serial', 'name', 'price', 'stock')
    search_fields = ('serial', 'name')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.admin_site.admin_view(self.upload_excel_view), name='catalog_product_upload_excel'),
        ]
        return custom_urls + urls

    def upload_excel_view(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['excel_file']
                # فراخوانی تابع پردازش که نتیجهٔ دیکشنری با آمار برمی‌گرداند
                result = import_products_from_file(file)
                # نمایش پیام به ادمین
                messages.success(request, f"Imported: {result['created']} | Updated: {result['updated']} | Skipped: {result['skipped']}")
                # میتونیم صفحهٔ لیست محصولات رو نمایش بدیم یا فرم مجدد
                return redirect('..')
        else:
            form = UploadFileForm()
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title="آپلود فایل اکسل برای موجودی کالا",
        )
        return render(request, "admin/catalog/product_upload.html", context)
