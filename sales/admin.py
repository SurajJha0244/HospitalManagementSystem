from django.contrib import admin
from .models import (Customer,Sale,SaleItem)


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "organization",
    )

    search_fields = (
        "name",
        "phone",
    )


class SaleItemInline(admin.TabularInline):

    model = SaleItem

    extra = 0

    readonly_fields = (
        "subtotal",
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "customer",
        "total",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "invoice_number",
    )
    inlines = [
        SaleItemInline
    ]