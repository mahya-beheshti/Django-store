from typing import Any
from django.contrib import admin , messages
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.http import HttpRequest
from . import models
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10' , 'LOW')
        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_select_related = ["collection"]
    list_per_page = 10
    list_filter = ['collection' , 'last_update' , InventoryFilter]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "LOW"
        return "OK"

    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request , queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products where updated',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "order"]
    ordering = ["first_name", "last_name"]
    list_editable = ["membership"]
    list_per_page = 10
    search_fields = ["first_name__startswith", "last_name__startswith"]

    def order(self, customer):
        url = (
            reverse("admin:store_order_changelist")  
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        queryset = models.Order.objects.filter(customer=customer).aggregate(count=Count('id'))
        return format_html('<a href="{}">{}</a>', url, queryset['count'])

# admin.site.register(models.Collection)
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count("product"))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer"]
