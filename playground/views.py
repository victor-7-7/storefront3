import logging

import requests
from django.core.cache import cache
from django.core.mail import send_mail, BadHeaderError, mail_admins, EmailMessage
from django.db import connection
from django.db.models.functions import Concat
from django.shortcuts import render
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models import Count, ExpressionWrapper, DecimalField
from django.db.models import Value, Func, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView

from playground.tasks import notify_customers
from store.models import Product, Order, Customer
from django.contrib.contenttypes.models import ContentType

from tags.models import TaggedItem
from templated_mail.mail import BaseEmailMessage


def calculate():
    x = 1
    y = 2
    return x


logger = logging.getLogger(__name__)  # playground.views


@cache_page(5 * 60)
def say_hello(request):
    # queryset = Product.objects.select_related('collection').all()[:20]
    # queryset2 = Product.objects.prefetch_related(
    #     'promotions').select_related('collection').all()[:20]
    # return render(request, 'hello.html', {'content': 'Mosh', 'products': list(queryset2)})

    # <-placed_at> минус означает сортировку по полю placed_at в убывающем порядке
    # queryset3 = Order.objects.select_related('customer').order_by("-placed_at")[:10]
    # return render(request, 'hello.html', {'content': 'Mosh', 'orders': list(queryset3)})

    # queryset4 = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # queryset5 = Product.objects.filter(collection_id=1).aggregate(
    #     count=Count('id'), min_price=Min('unit_price'))
    # return render(request, 'hello.html', {'content': 'Mosh', 'result': queryset5})

    # Джанга добавит к набору дополнительный столбец is_new, заполнив его числом 1 (true)
    # queryset6 = Customer.objects.annotate(is_new=Value(True))

    # queryset7 = Customer.objects.annotate(
    #     # Concat
    #     # full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    #     # full_name=Concat('first_name', Value(' '), 'last_name')
    #     # Доп. поле - сколько заказов сделал каждый покупатель
    #     orders_per_customer=Count('order')
    # )[:7]

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset8 = Product.objects.annotate(discounted_price=discounted_price)[:7]

    # content_type = ContentType.objects.get_for_model(Product)
    # queryset9 = TaggedItem.objects.select_related('tag').filter(
    #     content_type=content_type, object_id=1
    # )[:7]
    # queryset10 = TaggedItem.objects.get_tags_for(Product, 1)[:7]

    # queryset11 = Product.objects.raw("SELECT * FROM store_product")[:7]
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * FROM store_product LIMIT 7')
    #     queryset12 = cursor.fetchall()
    #
    # return render(request, 'hello.html', {'content': 'Mosh', 'result': list(queryset12)})

    # -----------------------------------------------
    # try:
    #     send_mail('subject', 'message', 'info@moshbuy.com', ['bob@moshbuy.com'])
    # except BadHeaderError:
    #     pass

    # try:
    #     mail_admins('subject', 'message', html_message="html_message")
    # except BadHeaderError:
    #     pass

    # try:
    #     message = EmailMessage('subject', 'message', 'from@moshbuy.com', ['john@moshbuy.com'])
    #     message.attach_file('playground/static/images/dog.jpg')
    #     message.send()
    # except BadHeaderError:
    #     pass

    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Mosh'}
    #     )
    #     message.send(to=['john@moshbuy.com'])
    # except BadHeaderError:
    #     pass

    # -----------------------------------------------
    # notify_customers.delay('Delay message')

    # -----------------------------------------------
    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     # Симулируем медленный сервер (отвечает через 2 сек)
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     # Можно задать время валидности кэшированных данных
    #     # ttl (time-to-live) при закидывании в кэш
    #     # cache.set(key, data, timeout=10 * 60)
    #     # Но лучше задать таймаут глобально в опциях кэша (common.py)
    #     cache.set(key, data)
    #
    # return render(request, 'hello.html', {'content': cache.get(key)})

    # Чтобы не писать код кэширования, можно пометить метод say_hello()
    # аннотацией @cache_page(5 * 60) и тогда все просто...
    response = requests.get('https://httpbin.org/delay/2')
    data = response.json()

    return render(request, 'hello.html', {'content': data})


# С классами аннотация @cache_page не работает. Делаем по-другому -
# метод get() класса аннотируем так: @method_decorator(cache_page(5 * 60))
class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
            return render(request, 'hello.html', {'content': data})
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
            return render(request, 'hello.html', {'content': 'httpbin is offline'})


# Дальше, в видео 60 (часть 3) Мош показывает как манипулировать кэшем
# через командную строку, подключившись к redis-базе №2 в докер-контейнере

