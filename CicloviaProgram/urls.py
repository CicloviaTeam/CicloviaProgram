from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from CicloviaProgram import views

urlpatterns = patterns('',
                    # Paginas principales.
    url(r'^$', views.index, name='index'),
    # ex: /ciclovias/
    url(r'^models/$', views.userModels, name='userModels'),
    # ex: /ciclovias/5/
    url(r'^(?P<ciclovia_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<ciclovia_id>\d+)/(?P<track_id>\d+)/$',
        views.detailNeighboor, name='detailNeighboor'),   
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^uploadFormCiclovia$', views.uploadFormCiclovia, name='uploadFormCiclovia'),
    url(r'^borrarCiclovia/(?P<ciclovia_id>\d+)/$', views.borrarCiclovia, name='borrarCiclovia'),
    url(r'^(?P<ciclovia_id>\d+)/uploadArrivalInfo/$',
        views.uploadArrivalInfo, name='uploadArrivalInfo'),
    url(r'^(?P<ciclovia_id>\d+)/detailArrival$',
        views.detailArrival, name='detailArrival'), 
    url(r'^adminSimulation/$', views.adminSimulation, name='adminSimulation'),
    url(r'^(?P<ciclovia_id>\d+)/simulationResults/$',
        views.simulationResults, name='simulationResults'),
                    # Paginas de validacion
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsValidation/$',
        views.simulationResultsValidation, name='simulationResultsValidation'),
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsValidationPerTrack'+
        '/(?P<track_id>\d+)/$', views.detailTrackValidation,
        name='detailTrackValidation'),  
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsValidationOneRun'+
        '/(?P<run_id>\d+)/$', views.detailValidationSingleRun,
        name='detailValidationSingleRun'),  
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsValidationOneRun'+
        '/(?P<run_id>\d+)/(?P<track_id>\d+)/$',
        views.detailTrackValidationSingleRun,
        name='detailTrackValidationSingleRun'),  
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsImg/(?P<results_id>\d+)/$',
        views.simulationResultsImg, name='simulationResultsImg'),
                    # Paginas de usuario.
    url(r'^login$', auth_views.login,
        {'template_name':'ciclovia/login.html'}, name='login'),
    url(r'^newUser$', views.newUser, name='newUser'),
    url(r'^user$', views.user, name='user'),
    url(r'^cambiarContrasena$',auth_views.password_change,
        {'template_name':'ciclovia/cambiarContrasena.html',
         'post_change_redirect':'CicloviaProgram:cambiarContrasenaExito'}, name="cambiarContrasena"),
    url(r'^cambiarContrasenaExito$', auth_views.password_change_done,
        {'template_name':'ciclovia/cambiarContrasenaExito.html'}, name='cambiarContrasenaExito'),
)

