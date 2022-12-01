from store.models import Product

# Для повышения производительности подсказки

# Preload related objects
Product.objects.select_related('...')
Product.objects.prefetch_related('...')

# Load only what you need
Product.objects.only('title')
Product.objects.defer('description')

# Use values
Product.objects.values()  # dictionary
Product.objects.values_list()  # list

# Count properly
Product.objects.count()

# Bulk create/update
Product.objects.bulk_create([...])

