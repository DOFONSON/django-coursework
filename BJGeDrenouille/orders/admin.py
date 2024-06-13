from django.contrib import admin

from orders.models import Order, OrderItem

# admin.site.register(Order)
# admin.site.register(OrderItem)

class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = ("product", "name", "price", "quantity")
    search_fields = ("product", "name")
    extra = 0
    raw_id_fields = ["product"]

class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0
    date_hierarchy = "created_timestamp"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "name", "price", "quantity"]
    search_fields = ["order", "product", "name"]
    list_display_links = ["order", "product"]
    raw_id_fields = ["order", "product"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    search_fields = ["id", "user__username"]
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
    )
    inlines = (OrderItemTabulareAdmin,)
    list_display_links = ["id", "user"]
    raw_id_fields = ["user"]
    date_hierarchy = "created_timestamp"
    short_description = "Заказ"