from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from store import models
from store.models import Product, Customer, Collection, Order, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'Ok'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>=10':
            return queryset.filter(inventory__gte=10)
        else:
            return queryset


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # --------------------------
    # Свойства полей формы для добавления нового продукта
    autocomplete_fields = ['collection']
    # Если я введу в поле title слова Brown Shoes, то
    # в поле slug автоматически появится текст brown-shoes
    prepopulated_fields = {
        'slug': ['title']
    }
    # --------------------------
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 100
    list_filter = ['collection', 'last_update', InventoryFilter]
    # Указываем джанге при обращении к БД сразу заполнить данными
    # collection-объекты, сокращая тем самым число обращений к базе
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        # Обнуляем поле inventory в таблице store_product
        # для выбранных записей (queryset)
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS  # Вид картинки с сообщением
        )

    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            # синтаксис ссылок для навигации внутри приложения такой
            # admin:app_model_page
            # Идентификатор секции, в которую помещается список на любой
            # админской странице странице обозначен как changelist
            # (<div class="module filtered" id="changelist">)
            reverse('admin:store_product_changelist')
            # Здесь мы добавляем к адресу запрос на поиск продуктов,
            # принадлежащих данной (напр 7) коллекции .../?collection__id=7
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        # Литерал 'products' задан в атрибуте related_name для поля collection
        # в классе Product
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10

    # Выполнять поиск совпадений с началом слова (startswith) вне
    # зависимости от регистра (insensitive)
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
            'customer__id': str(customer.id)
        }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


# TabularInline - поля формы расположены в строку
# StackedInline - поля формы расположены вертикально (друг под другом)
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10  # Максимальное число продуктов для добавления в заказ
    model = OrderItem
    # 0 - не желаем видеть дополнительные пустые записи
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer_name']

    def customer_name(self, order):
        return order.customer
