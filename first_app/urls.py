from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from . import views

# app_name = 'first_app'
urlpatterns = [
    url(r'^register_user/', views.register_user, name='register_user'),
    url(r'^login/', views.login, name='login'),
    url(r'^change_pass/', views.change_pass, name='change_pass'),
    url(r'^approval_pending/', views.get_approval_pending_users, name='approval_pending'),
    url(r'^details/', views.employee_detail, name='details'),
    url(r'^edit_details/(?P<id>[A-Za-z_0-9\-]+)', views.edit_details, name='edit_details'),
    url(r'^edit_details/', views.edit_details, name='edit_details'),
    url(r'^base/', views.base, name='base'),
    url(r'^admin/', views.admin, name='admin'),
    url(r'^$', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)