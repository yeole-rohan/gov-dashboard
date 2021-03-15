from django.contrib import admin
from django.urls import path, include
from . import views
from .views import  GPRegister, S2Regsiter, ObservarRegsiter, CEORegister
urlpatterns = [
    # Home View
    path('', views.home, name="home"),
    path('dashboard/',views.index, name="index"),
    path('observar/',views.observar, name="observar"),
    # Ajax Views
    path('load-taluka/', views.load_taluka, name="ajax_taluka"),
    path('load-panchayat', views.load_panchayat,name="ajax_panchayat"),

    # Signup Views
    path('accounts/signup/gp/', GPRegister.as_view(), name="gp"),
    path('accounts/signup/s2/', S2Regsiter.as_view(), name="accountant"),
    path('accounts/signup/ceo/', CEORegister.as_view(), name="CEO"),
    path('accounts/signup/ob/', ObservarRegsiter.as_view(), name="ob"),

    # Confirmation, Pending, Approved, Payment Views
    path('confim-one/', views.confirm1, name="confirm1"),
    path('pay-one/', views.payment1, name="pay1"),
    path('pay-pending-for-pay-one/', views.pending1, name="pending1"),
    path('confirm-two/', views.confirm2, name="confirm2"),
    path('confirm-three/', views.confirm3, name="confirm3"),
    path('pay-two/', views.payment2, name="pay2"),
    path('pay-three/', views.payment3, name="pay3"),
    path('pay-four/', views.payment4, name="pay4"),
    path('pay-pending-for-pay-two/', views.pending2, name="pending2"),
    path('pay-pending-for-pay-three/', views.pending3, name="pending3"),
    path('confim-four/', views.confirm4, name="confirm4"), 
    path('pay-pending-for-pay-four/', views.pending4, name="pending4"),
    path('audit-msg/', views.audit_msg, name="audit_msg"),

    #s2 views
    path('my-dashboard/', views.s2dashboard, name="s2dashboard"),
    path('confirm-payment/<int:pay_id>/<int:user_id>/', views.confirm_payment, name="confirm_payment"),
    path("utr-missed/", views.utr_missed, name="utr_missed"),
    path("utr-matched/", views.utr_matched, name="utr_matched"),
    path('utr-change/<int:id>/', views.utr_change, name="utr_change"),
    path("utr-missed-two/", views.utr_missedtwo, name="utr_missedtwo"),
    path('utr-change-two/<int:id>/', views.utr_changetwo, name="utr_changetwo"),
    path('audit-approve/<int:id>/', views.audit_approve, name="audit-approve"),
    path('audit-miss-three/', views.audit_miss, name="audit_miss"),
    path('audit-miss-four/', views.audit_miss_four, name="audit_miss_four"),
    path('utr-change-three/<int:id>/', views.utr_changethree, name="utr_changethree"),
    path('audit-edit/<int:id>/', views.audit_edit, name="audit-edit"),
    path('utr-missed-three/', views.utr_missedthree, name="utr_missedthree"),
    path('utr-change-four/<int:id>/', views.utr_changefour, name="utr_changefour"),
    path('utr-missed-four/', views.utr_missedfour, name="utr_missedfour"),
    path('audit-edit-four/<int:id>/', views.audit_edit_four, name="audit-edit-four"),
    path('local', views.local, name="local"),

]