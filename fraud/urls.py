#import path
from django.urls import path
from .views import *
app_name='fraud'


urlpatterns = [
    path('send/transaction', Send_transaction.as_view()),
    path('list/transaction',List_transaction.as_view()),
    path('list/review',List_review_transaction.as_view()),
    path('add/blacklist', Add_to_blacklist.as_view()),
    path('add/global/blacklist', Add_to_global_blacklist.as_view()),
    path('add/whitelist', Add_to_whitelist.as_view()),
    path('add/global/whitelist', Add_to_global_whitelist.as_view()),
    path('login',login_API),
    path('change/password',Change_password.as_view()),
    path('signup',sign_up_API),
    path('reset/password',reset_password),
    #path('add/review',add_review.as_view()),
    
]

