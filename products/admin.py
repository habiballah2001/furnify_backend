from django.contrib import admin
from .models import Product, Category, Review, Discount,Provider


admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Discount)
admin.site.register(Provider)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.calculate_price()
        super().save_model(request, obj, form, change)