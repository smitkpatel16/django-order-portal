from django.contrib import admin
from django import forms
from django.urls import path
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Inventory, Order
from .utils import ExportCsvMixin
# Register your models here.


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    change_list_template = 'admin/order_admin/product/product_list.html'
    list_display = ('productname', 'price', 'description')
    list_filter = ('productname', 'price', 'description')
    search_fields = ('productname', 'price', 'description')
    actions = ["export_as_csv"]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            for i, x in enumerate(csv_data):
                if not i:
                    continue
                fields = x.split(",")
                print(fields)
                if len(fields) < 3:  # blank row
                    break
                try:
                    item = Product.objects.get(productname=fields[0])
                except Product.DoesNotExist:
                    Product.objects.create(productname=fields[0], price=float(
                        fields[1]), description=fields[2])
                else:
                    item = Product.objects.filter(
                        productname=fields[0]
                    ).update(
                        price=float(fields[1]),
                        description=fields[2]
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


@ admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    list_filter = ('product', 'quantity')
    search_fields = ('product', 'quantity')


@ admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order_date',
                    'shipped_date', 'status')
    list_filter = ('product', 'quantity', 'order_date',
                   'shipped_date', 'status')
    search_fields = ('product', 'quantity', 'order_date',
                     'shipped_date', 'status')
