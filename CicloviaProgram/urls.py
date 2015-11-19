# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from CicloviaProgram import views

urlpatterns = patterns('',
                    # Páginas principales.
    url(r'^$', views.index, name='index'),
    # ex: /ciclovias/
    url(r'^models/$', views.userModels, name='userModels'),
    # ex: /ciclovias/5/
    url(r'^(?P<ciclovia_id>\d+)/$', views.detail, name='detail'),
    url(r'^editCiclovia/(?P<ciclovia_id>\d+)/$', views.editCiclovia, name='editCiclovia'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^uploadFormCiclovia$', views.uploadFormCiclovia, name='uploadFormCiclovia'),
    url(r'^copyCiclovia/(?P<ciclovia_id>\d+)$', views.copiarCiclovia, name='copyCiclovia'),
    url(r'^borrarCiclovia/(?P<ciclovia_id>\d+)/$', views.deleteCiclovia, name='borrarCiclovia'),
    url(r'^(?P<ciclovia_id>\d+)/(?P<track_id>\d+)/$',
        views.detailNeighboor, name='detailNeighboor'),
    url(r'^editNeighboor/(?P<ciclovia_id>\d+)/(?P<track_id>\d+)/$',
        views.editNeighboor, name='editNeighboor'),
    url(r'^(?P<ciclovia_id>\d+)/uploadArrivalInfo/$',
        views.uploadArrivalInfo, name='uploadArrivalInfo'),
    url(r'^(?P<ciclovia_id>\d+)/uploadArrivalInfoForm/$',
        views.uploadArrivalInfoForm, name='uploadArrivalInfoForm'),
    url(r'^(?P<ciclovia_id>\d+)/detailArrival$',
        views.detailArrival, name='detailArrival'),
    url(r'^(?P<ciclovia_id>\d+)/editArrivalInfo$',views.editArrivalInfo, name="editArrivalInfo"),
    url(r'^adminSimulation/$', views.adminSimulation, name='adminSimulation'),
                       # Páginas de simulación
    url(r'^(?P<ciclovia_id>\d+)/simulationResults/$',
        views.simulationResults, name='simulationResults'),
    url(r'^simulationResultsOld/(?P<ciclovia_id>\d+)/$',
        views.simulationResultsOld, name='simulationResultsOld'),
    url(r'^simulationList$', views.simulationList,name='simulationList'),
    url(r'^compareSimulations$',views.compareSimulations, name='compareSimulations'),
                       # Páginas de validación
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsValidation/$',
        views.simulationResultsValidation, name='simulationResultsValidation'),
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsValidationOld/$',
        views.simulationResultsValidationOld, name='simulationResultsValidationOld'),
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
                       # Gráficas
    url(r'^charts/pie/$',views.piechart, name='pieChart'),
    url(r'^charts/verticalBarChart/$',views.verticalBarChart, name='vBarChart'),
    url(r'^charts/graph/$',views.graphImg, name='graph'),
    url(r'^(?P<ciclovia_id>\d+)/simulationResultsImg/(?P<results_id>\d+)/$',
        views.simulationResultsImg, name='simulationResultsImg'),
                    # Páginas de usuario.
    url(r'^login$', auth_views.login,
        {'template_name':'ciclovia/login.html'}, name='login'),
    url(r'^newUser$', views.newUser, name='newUser'),
    url(r'^user$', views.user, name='user'),
    url(r'^changePassword$',auth_views.password_change,
        {'template_name':'ciclovia/cambiarContrasena.html',
         'post_change_redirect':'CicloviaProgram:cambiarContrasenaExito'}, name="cambiarContrasena"),
    url(r'^changePasswordSuccess$', auth_views.password_change_done,
        {'template_name':'ciclovia/cambiarContrasenaExito.html'}, name='cambiarContrasenaExito'),
    url(r'^passwordReset$', auth_views.password_reset, {'template_name':'ciclovia/passwordReset.html'
        ,'email_template_name':'ciclovia/passwordResetEmail.html','subject_template_name':'ciclovia/passwordResetSubject.txt'
        ,'post_reset_redirect':'CicloviaProgram:passwordResetDone',}, name='passwordReset'),
    url(r'^passwordResetDone$',auth_views.password_reset_done, {'template_name':'ciclovia/passwordResetDone.html'},
        name='passwordResetDone'),
    url(r'^passwordResetConfirm/(?P<uidb64>.+)/(?P<token>.+)$',auth_views.password_reset_confirm,
        {'template_name':'ciclovia/passwordResetConfirm.html', 'post_reset_redirect':'CicloviaProgram:passwordResetComplete'}
        , name='passwordResetConfirm'),
    url(r'^passwordResetComplete$',auth_views.password_reset_complete,
        {'template_name':'ciclovia/passwordResetComplete.html'}, name='passwordResetComplete'),
)

