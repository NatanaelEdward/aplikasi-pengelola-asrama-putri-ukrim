from django.urls import path
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from . import views

from .views import mahasiswa_report_view,PendaftaranJson
from django.contrib.auth.views import LoginView
urlpatterns =[

    path('', views.login_view, name='login'),
    # path('', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('profil/',views.profil,name='profil'),
    path('logout/', views.logout_view, name='logout'),

    path('log',views.log,name='log'),

    path('mahasiswa-report/', mahasiswa_report_view, name='mahasiswa_report'),
     path('pendaftaran/json', PendaftaranJson.as_view(), name='pendaftaran_json'),

    path('mahasiswa',views.indexMahasiswa,name='mahasiswa'),
    path('tambahMahasiswa',views.tambahMahasiswa,name='tambahMahasiswa'),
    path('postMahasiswa',views.postMahasiswa,name='postMahasiswa'),
    path('updateMahasiswa/<str:nim>',views.updateMahasiswa,name='updateMahasiswa'),
    path('postUpdateMahasiswa',views.postUpdateMahasiswa,name='postUpdateMahasiswa'),
    path('hapusMahasiswa/<str:nim>',views.hapusMahasiswa,name='hapusMahasiswa'),
    path('postHapusMahasiswa/<str:nim>',views.postHapusMahasiswa,name='postHapusMahasiswa'),

    path('kamar',views.indexKamar,name='kamar'),
    path('tambahKamar',views.tambahKamar,name='tambahKamar'),
    path('postKamar',views.postKamar,name='postKamar'),
    path('updateKamar/<str:nomor_kamar>',views.updateKamar,name='updateKamar'),
    path('postUpdateKamar',views.postUpdateKamar,name='postUpdateKamar'),
    path('hapusKamar/<str:nomor_kamar>',views.hapusKamar,name='hapusKamar'),
    path('postHapusKamar/<str:nomor_kamar>',views.postHapusKamar,name='postHapusKamar'),

    path('pengelola',views.indexPengelola,name='pengelola'),
    path('tambahPengelola',views.tambahPengelola,name='tambahPengelola'),
    path('postPengelola',views.postPengelola,name='postPengelola'),

    path('updatePengelola',views.updatePengelola,name='updatePengelola'),

    path('postUpdatePengelola',views.postUpdatePengelola,name='postUpdatePengelola'),
    path('hapusPengelola/<int:id_pengelola>',views.hapusPengelola,name='hapusPengelola'),
    path('postHapusPengelola/<int:id_pengelola>',views.postHapusPengelola,name='postHapusPengelola'),

    path('pendaftaran',views.indexPendaftaran,name='pendaftaran'),
    path('updatePendaftaran/<str:id_pendaftaran>',views.updatePendaftaran,name='updatePendaftaran'),
    path('postUpdatePendaftaran',views.postUpdatePendaftaran,name='postUpdatePendaftaran'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
     path('upload-image', views.upload_image, name='upload_image'),
    ]
