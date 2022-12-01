from django.urls import path
from store import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')


# 1 - parent_router, 2 - parent_prefix
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls



# urlpatterns2 = [
#     path('products/', views.product_list),
#     path('products/<int:prod_id>/', views.product_detail),
#     path('collections/', views.collection_list),
#     # --------------------
#     # path('collections/<int:coll_id>/', views.collection_detail, name='collection-detail'),
#     # Обязателен литерал pk (!), если в ProductSerializer поле collection сериализуется
#     # как HyperlinkedRelatedField
#     path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
# ]
