from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from .forms import *
from CicloviaProgram.models import Ciclovia, Track, Document, SimulationParameters, SimulationResultsCompiled, \
    SimulationResults, SimulationResultsPerTrack, SimulationResultsFlowPerTrack, SimulationResultsCompiledPerTrack
import CicloviaScript
import traceback
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .authentication import *
from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.decorators import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from myCicloviaProject import settings as settings

def index(request):
    return render(request, 'ciclovia/index.html')

@login_required(login_url='CicloviaProgram:login')
def userModels(request):
    '''
    if request.method == 'POST':
	form = UploadForm(request.POST, request.FILES)
	if form.is_valid():
	    #fileObj = request.FILES['file']
	    #name = fileObj['filename']
	    #CicloviaScript.buildCiclovia(fileObj)
	    #return render(request, 'ciclovia/main.html')
	    newdoc = Document(filename = request.POST['filename'],docfile = request.FILES['docfile'])
	    newdoc.save(form)	    
	    CicloviaScript.buildCiclovia(newdoc)	  
    '''

    ciclovia_list = Ciclovia.objects.order_by('-name')[:10]
    template = loader.get_template('ciclovia/userModels.html')
    context = RequestContext(request, {
        'ciclovia_list': ciclovia_list,
    })
    return HttpResponse(template.render(context))

@login_required(login_url='CicloviaProgram:login')
def detail(request, ciclovia_id):
    return HttpResponse("Esta es la Ciclovia %s." % ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def detail(request, ciclovia_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    return render(request, 'ciclovia/detail.html', {'ciclovia': ciclovia})

@login_required(login_url='CicloviaProgram:login')
def detailArrival(request, ciclovia_id):
    return HttpResponse("Esta es la Ciclovia %s." % ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def detailArrival(request, ciclovia_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    return render(request, 'ciclovia/detailArrival.html',
                  {'ciclovia': ciclovia})

@login_required(login_url='CicloviaProgram:login')
def detailNeighboor(request, ciclovia_id, track_id):
    return HttpResponse("Este es el Track %s." % track_id)

@login_required(login_url='CicloviaProgram:login')
def detailNeighboor(request, ciclovia_id, track_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    track = get_object_or_404(Track, pk=track_id)
    return render(request, 'ciclovia/detailNeighboor.html',
                  {'ciclovia': ciclovia, 'track': track})

@login_required(login_url='CicloviaProgram:login')
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(filename = request.POST['filename'],
                              docfile = request.FILES['docfile'])
            newdoc.save(form)
	    name = settings.MEDIA_ROOT + str(newdoc.docfile)
	    CicloviaScript.buildCiclovia(name, request.user)
	    ciclovia_list = Ciclovia.objects.order_by('-name')[:10]
	    template = loader.get_template('ciclovia/userModels.html')
	    context = RequestContext(request, {
		   'ciclovia_list': ciclovia_list,
	       })
	    return HttpResponse(template.render(context))

    else:
        form = UploadForm()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'ciclovia/upload.html', {'form': form})

@login_required(login_url='CicloviaProgram:login')
def borrarCiclovia(request, ciclovia_id):
    ciclovia = Ciclovia.objects.get(pk=ciclovia_id).delete()
    return HttpResponseRedirect(reverse('CicloviaProgram:userModels'))

@login_required(login_url='CicloviaProgram:login')
def uploadArrivalInfo(request, ciclovia_id):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(filename = request.POST['filename']
                              ,docfile = request.FILES['docfile'])
            newdoc.save(form)
	    name = settings.MEDIA_ROOT + str(newdoc.docfile)
	    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	    cicloviaToLoad = CicloviaScript.loadCiclovia(ciclovia_id)
	    CicloviaScript.assignArrivalInfo(cicloviaToLoad, ciclovia_id, name)
	    ciclovia_list = Ciclovia.objects
	    cicloviaLoad = get_object_or_404(Ciclovia, pk=ciclovia_id)
	    return render(request, 'ciclovia/detailArrival.html',
                          {'ciclovia': cicloviaLoad})

    else:
        form = UploadForm()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'ciclovia/upload.html', {'form': form})

@login_required(login_url='CicloviaProgram:login')
def simulationResults(request, ciclovia_id):
    return HttpResponse("Estos son los resultados de la Ciclovia %s." %
                        ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def simulationResults(request, ciclovia_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    results_id = CicloviaScript.simulationExecution(ciclovia_id, False)
    results = get_object_or_404(SimulationResultsCompiled, pk=results_id)
    return render(request, 'ciclovia/simulationResults.html',
                  {'ciclovia': ciclovia, 'results': results})

@login_required(login_url='CicloviaProgram:login')
def simulationResultsValidation(request, ciclovia_id):
    return HttpResponse("Estos son los resultados de la Ciclovia %s." %
                        ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def simulationResultsValidation(request, ciclovia_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    results_id = CicloviaScript.simulationExecution(ciclovia_id,True)
    results = get_object_or_404(SimulationResultsCompiled, pk=results_id)
    return render(request, 'ciclovia/simulationResultsValidation.html',
                  {'ciclovia': ciclovia, 'results': results})

@login_required(login_url='CicloviaProgram:login')
def detailTrackValidation(request, ciclovia_id, track_id):
    return HttpResponse("Esta es la Ciclovia %s." % ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def detailTrackValidation(request, ciclovia_id, track_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    print("La llave es " + track_id)
    track = get_object_or_404(SimulationResultsCompiledPerTrack, pk=track_id)

    #return render(request, 'ciclovia/detailTrackValidation.html', {'ciclovia': ciclovia, 'track': track})
    return render(request, 'ciclovia/detailTrackValidation.html',
                  {'ciclovia': ciclovia, 'track': track})

@login_required(login_url='CicloviaProgram:login')
def detailValidationSingleRun(request, ciclovia_id, run_id):
    return HttpResponse("Esta es la Ciclovia %s." % ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def detailValidationSingleRun(request, ciclovia_id, run_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    print("La llave es " + run_id)
    result = get_object_or_404(SimulationResults, pk=run_id)

    return render(request, 'ciclovia/detailValidationSingleRun.html',
                  {'ciclovia': ciclovia, 'run': result})

@login_required(login_url='CicloviaProgram:login')
def detailtrackValidationSingleRun(request, ciclovia_id, run_id, track_id):
    return HttpResponse("Esta es la Ciclovia %s." % ciclovia_id)

@login_required(login_url='CicloviaProgram:login')
def detailTrackValidationSingleRun(request, ciclovia_id, run_id, track_id):
    ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
    print("La llave es " + run_id)
    result = get_object_or_404(SimulationResults, pk=run_id)
    track = get_object_or_404(SimulationResultsPerTrack, pk=track_id)

    return render(request, 'ciclovia/detailTrackValidationSingleRun.html',
                  {'ciclovia': ciclovia, 'run': result, 'track': track})

@login_required(login_url='CicloviaProgram:login')
def simulationResultsImg(request, ciclovia_id, results_id):
    cicloviaN = get_object_or_404(Ciclovia, pk=ciclovia_id)
    results = get_object_or_404(SimulationResultsCompiled, pk=results_id)
    import charts
    print(request)
    #Crea el objeto que representa el grafico de barras
    d = charts.BarChart()
    #Esta lista representa los datos que van a ser graficados
    data = []
    #Busca cual es la informacion que desea el usuario y la pone en la
    #variable data
    queryFromDB = results.simulationresults_set.all()
    if request.GET.get('data', '') == 'total_arrivals':
        for i in queryFromDB:
            data.append(i.total_arrivals)
            print("Estoy en la iteracion " + str(i) + "de total arrivals")
            print(i.total_arrivals)
            d.changeTitle('Numero total de arribos')
    elif request.GET.get('data', '') == 'average_number_system':
        for i in queryFromDB:
            data.append(i.average_number_system)
            print("Estoy en la iteracion " + str(i) + "de num promedio")
            print(i.average_number_system)
            d.changeTitle('Numero promedio de personas')
    else:
        data = [0, 0, 0, 0]

    d.chart.data = [data]
    d.chart.valueAxis.valueMin = 2000
    print(d.chart.data)
    draw = d.asString('png')

    return HttpResponse(draw, 'png')

@login_required(login_url='CicloviaProgram:login')
def adminSimulation(request):

    simulation_list = SimulationParameters.objects.order_by('-replications')[:1]
    template = loader.get_template('ciclovia/adminSimulation.html')
    context = RequestContext(request, {
        'simulation_list': simulation_list,
    })
    return HttpResponse(template.render(context))

#Cretate user if none is loged in.
@user_passes_test(notAutheticated,login_url='CicloviaProgram:index')
def newUser(request):
    if request.method == 'POST':
        # form = NewUserForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=request.POST['username'])
            except (KeyError, User.DoesNotExist):
##                CreateU(form.cleaned_data['username']
##                        ,form.cleaned_data['email'],
##                        form.cleaned_data['password'])
                # CreateU(form.cleaned_data['username'],
                #         form.cleaned_data['password1'])
                form.save()
                userTemp = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'])
                login(request, userTemp)
                return HttpResponseRedirect(reverse('CicloviaProgram:user'))
            else:
                #User alredy exists, redisplay user creation form with error.
##                error_msg = 'El usuario ya existe.'
                return render(request, 'ciclovia/new_user.html',
                              {'error':'El usuario ya existe.', 'form':form})
    else:
        # form = NewUserForm()
        form = UserCreationForm()
    return render(request, 'ciclovia/new_user.html',{'form':form})

#User page.

def user(request):
    if request.method == 'POST':
        if request.POST['opcion']=='Cerrar sesion':
            return auth_views.logout(request,next_page='CicloviaProgram:index')
        elif request.POST['opcion']=='Borrar usuario':
            DeleteU(request.user.username)
            return auth_views.logout(request,next_page='CicloviaProgram:index')
        elif request.POST['opcion']=='Actualizar datos':
            request.user.first_name=request.POST['first_name']
            request.user.last_name=request.POST['last_name']
            request.user.email=request.POST['email']
            request.user.save()
            form = UserChangeForm()
            return render(request, 'ciclovia/user.html',
                          {'form': form,'mensaje': 'Se han actualizado los datos del usuario.'})
    else:
        form = UserChangeForm()
        return render(request, 'ciclovia/user.html', {'form': form})



