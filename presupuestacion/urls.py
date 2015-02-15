from django.conf.urls import patterns, url
from presupuestacion import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^proyecto/(?P<proyecto_slug>[\w\-]+)/$', views.proyecto, name='proyecto'),  # New!
                       url(r'^add_proyecto/$', views.add_proyecto, name='add_proyecto'), # NEW MAPPING!
                       url(r'^proyecto/(?P<proyecto_slug>[\w\-]+)/add_poste/$', views.add_poste, name='add_poste'),
                       #url(r'^proyecto/(?P<proyecto_slug>\w+)/add_poste/$',views.add_poste,name='add_poste'),
                       url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^restricted/', views.restricted, name='restricted'),
                       url(r'^like_category/$', views.like_category, name='like_category'),
                       url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
)