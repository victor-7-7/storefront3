from django.dispatch import receiver
from store.signals import order_created

# Эта функция-ресивер будет вызвана в ответ на сигнал, отправленный
# сигнальным объектом order_created.
@receiver(order_created)
def on_order_created(sender, **kwargs):
  print(kwargs['order'])



