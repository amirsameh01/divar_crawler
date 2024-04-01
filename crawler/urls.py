
from django.urls import path
from crawler.views import SearchView
urlpatterns = [
    # path('phonenumber/', otp_pull),
    # path('otp/', otp_authenticate),
    path('search/', SearchView.as_view(), name='search'),
]
