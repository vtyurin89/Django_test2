from django.urls import path

from .views import *

urlpatterns = [
    path('', AdHomepage.as_view(), name='index'),
    path('new/', AdNew.as_view(), name='new'),
    path('help/', help, name='help'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('show_ad/<slug:ad_slug>', AdShow.as_view(), name='show_ad'),
    path('category/<slug:cat_slug>', AdCategory.as_view(), name='category'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('search/', search, name='search'),
    path('account/ask_password_reset/', AskPasswordReset.as_view(), name='password_reset'),
    path('account/ask_password_reset_done/', AskPasswordResetDone.as_view(), name='password_reset_email_sent'),
    path('account/password_reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('account/password_reset/success/', PasswordResetComplete.as_view(), name='password_reset_complete'),
]