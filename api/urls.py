from django.urls import path
from .views import TransferBalanceAPIView,MytokenManager,MytokenVendor,RegisterManagerAPI,RegisterVendorAPI,ProductCreateView,ProductListView,ProductRetrieveView,FavorisCreateView,FavorisListView,TransactionListView

urlpatterns = [
    ####login#####
    path('LoginManager/', MytokenManager.as_view(), name='token_obtain_pairManager'),
    path('LoginVendor/', MytokenVendor.as_view(), name='token_obtain_pairVendor'),
    ####register#####
    path('RegisterManager/', RegisterManagerAPI.as_view(), name='user-registerManager'),
    path('RegisterVendor/', RegisterVendorAPI.as_view(), name='user-registerVendor'),
    ### transfer
    path('Transfer/', TransferBalanceAPIView.as_view(), name='transfer-balance'),
    ##post product 
    path('createPoduct/', ProductCreateView.as_view(), name='product-create'),
    ##get all product
    path('getAllProducts/', ProductListView.as_view(), name='product-list'),
    ##getproductby id 
    path('getProductsById/<int:id>/', ProductRetrieveView.as_view(), name='product-detail'),
    ##post favoris
    path('createFavoris/', FavorisCreateView.as_view(), name='favoris-create'),
    ##get allfavoris
    path('getAllFavoris/', FavorisListView.as_view(), name='favoris-list'),
    ##get transaction 
    path('getAllTransaction/', TransactionListView.as_view(), name='transactio-list'),

]
