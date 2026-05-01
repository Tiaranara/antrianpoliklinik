from django.urls import path
from . import views

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('login/', views.login_pasien, name='login_pasien'),
    path('register/', views.register_pasien, name='register_pasien'),
    path('logout/', views.logout_pasien, name='logout_pasien'),
    path('ambil/', views.ambil_antrian, name='ambil_antrian'),
    path('konfirmasi/', views.konfirmasi_antrian, name='konfirmasi_antrian'),
    path('status/<int:antrian_id>/', views.status_antrian, name='status_antrian'),
    path('daftar/', views.daftar_antrian, name='daftar_antrian'),
]
