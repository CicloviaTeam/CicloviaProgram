# coding=utf-8
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.decorators import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelform_factory
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

from .forms import *
from CicloviaProgram.models import Ciclovia, Track, Document, SimulationResultsCompiled, \
	SimulationResults, SimulationResultsPerTrack, SimulationResultsCompiledPerTrack
import CicloviaScript
from .authentication import *
from myCicloviaProject import settings as settings
import charts
import grafo


#El índice de la página.
def index(request):
	return render(request, 'ciclovia/index.html')

@login_required(login_url='CicloviaProgram:login')
def userModels(request):
	if not request.user.is_superuser:
		ciclovia_list = Ciclovia.objects.filter(user=request.user).order_by('-name')
	else:
		ciclovia_list = Ciclovia.objects.order_by('-name')
	template = loader.get_template('ciclovia/userModels.html')
	context = RequestContext(request, {
		'ciclovia_list': ciclovia_list,
	})
	return HttpResponse(template.render(context))

@login_required(login_url='CicloviaProgram:login')
def detail(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	resultset = ciclovia.simulationresultscompiled_set.filter(is_validation=False).order_by('-date')
	resultset2 = ciclovia.simulationresultscompiled_set.filter(is_validation=True).order_by('-date')
	if len(resultset)==0:
		resultset=None
	if len(resultset2)==0:
		resultset2=None
	return render(request, 'ciclovia/detail.html', {'ciclovia': ciclovia, 'resultset':resultset
	, 'resultset2':resultset2})

def graphImg(request):
	"""Retorna la representación gráfica de la ciclovía"""
	ciclovia = get_object_or_404(Ciclovia, pk=request.GET['ciclovia_id'])
	tracks = ciclovia.track_set.all()
	nodos = []
	arcos = []
	for track in tracks:
		neighboors = track.neighboorinfo_set.all()
		for neighboor in neighboors:
			arcos.append([track.id_track,neighboor.neighboorId])
		nodos.append(track.id_track)
	d = grafo.dibujarGrafo(nodos,arcos)
	outputimg = d.asString('gif')
	return HttpResponse(outputimg, 'image/gif')

@login_required(login_url='CicloviaProgram:login')
def editCiclovia(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	if ciclovia.arrivals_loaded:
		CicloviaForm = modelform_factory(Ciclovia, fields=('name', 'place', 'start_hour', 'end_hour'
			,'reference_track','reference_hour','reference_arrival_rate',))
		# TrackFormSet= inlineformset_factory(Ciclovia,Track,fields=('id_track','distance'
		# 	,'probabilityBegin', 'probabilityEnd','arrival_proportion', 'number_of_semaphores'
		# 	, 'hasSlope', 'quality_of_track'), extra=0)
		TrackFormSet= inlineformset_factory(Ciclovia,Track,fields=('id_track','distance'
			,'arrival_proportion', 'number_of_semaphores'
			, 'hasSlope', 'quality_of_track'), extra=0)
	else:
		CicloviaForm = modelform_factory(Ciclovia, fields=('name', 'place', 'start_hour',
			'end_hour',))
		# TrackFormSet= inlineformset_factory(Ciclovia,Track,fields=('id_track','distance'
		# 	,'probabilityBegin', 'probabilityEnd','number_of_semaphores'
		# 	, 'hasSlope', 'quality_of_track'), extra=0)
		TrackFormSet= inlineformset_factory(Ciclovia,Track,fields=('id_track','distance'
				,'number_of_semaphores'
				, 'hasSlope', 'quality_of_track'), extra=0)
	if request.method=='POST':
		form = CicloviaForm(request.POST, instance = ciclovia)
		formset = TrackFormSet(request.POST, request.FILES, instance = ciclovia)
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			ciclovia.num_tracks = ciclovia.track_set.count()
			ciclovia.save()
			return HttpResponseRedirect(reverse('CicloviaProgram:detail',args=[ciclovia_id]))
		else:
			return render(request,'ciclovia/editCiclovia.html',{'form':form,'formset':formset, 'ciclovia':ciclovia})
	else:
		form = CicloviaForm(instance=ciclovia)
		formset = TrackFormSet(instance=ciclovia)
		return render(request,'ciclovia/editCiclovia.html',{'form':form,'formset':formset, 'ciclovia':ciclovia})

@login_required(login_url='CicloviaProgram:login')
def copiarCiclovia(request, ciclovia_id):
	CicloviaScript.copyCiclovia(ciclovia_id, request.POST['nombre'], request.user)
	return HttpResponseRedirect(reverse('CicloviaProgram:userModels'))

@login_required(login_url='CicloviaProgram:login')
def detailArrival(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	return render(request, 'ciclovia/detailArrival.html',
				  {'ciclovia': ciclovia})

@login_required(login_url='CicloviaProgram:login')
def editArrivalInfo(request,ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	TimeSystemFormsetClass = inlineformset_factory(Ciclovia,TimeInSystemDistribution,
		fields=('time', 'percentage',), extra=0)
	ArrivalProportionPerHourFormsetClass = inlineformset_factory(Ciclovia,ArrivalsProportionPerHour,
		fields=('hour', 'proportion',), extra=0)
	ParticipantFormsetClass = inlineformset_factory(Ciclovia,ParticipantType,
		fields=('activity', 'velocity', 'percentage',), extra=0)
	if request.method == 'POST':
		timesystemformset = TimeSystemFormsetClass(request.POST, request.FILES, instance=ciclovia, prefix='timesystem')
		arrivalproportionperhourformset = ArrivalProportionPerHourFormsetClass(request.POST, request.FILES,
			instance=ciclovia, prefix='arrivalproportion')
		participantformset = ParticipantFormsetClass(request.POST, request.FILES,
			instance=ciclovia, prefix='participant')
		if timesystemformset.is_valid() and arrivalproportionperhourformset.is_valid()\
				and participantformset.is_valid():
			timesystemformset.save()
			arrivalproportionperhourformset.save()
			participantformset.save()
			return HttpResponseRedirect(reverse('CicloviaProgram:detail',args=[ciclovia_id]))
		else:
			return render(request,'ciclovia/editArrivalInfo.html',
				{'timesystemformset':timesystemformset, 'ciclovia':ciclovia,
				 'arrivalsproportionformset':arrivalproportionperhourformset,
				 'participantformset':participantformset})
	else:
		timesystemformset = TimeSystemFormsetClass(instance=ciclovia, prefix='timesystem')
		arrivalproportionperhourformset = ArrivalProportionPerHourFormsetClass(
			instance=ciclovia, prefix='arrivalproportion')
		participantformset = ParticipantFormsetClass(
			instance=ciclovia, prefix='participant')
		return render(request,'ciclovia/editArrivalInfo.html',
				{'timesystemformset':timesystemformset, 'ciclovia':ciclovia,
				 'arrivalsproportionformset':arrivalproportionperhourformset,
				 'participantformset':participantformset})

@login_required(login_url='CicloviaProgram:login')
def detailNeighboor(request, ciclovia_id, track_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	track = get_object_or_404(Track, pk=track_id)
	return render(request, 'ciclovia/detailNeighboor.html',
				  {'ciclovia': ciclovia, 'track': track})

@login_required(login_url='CicloviaProgram:login')
def editNeighboor(request, ciclovia_id, track_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	track = get_object_or_404(Track, pk=track_id)
	TrackForm = inlineformset_factory(Track,NeighboorInfo,
		fields=('neighboorId', 'probability', 'direction', 'fromDirection',), extra=0)
	if request.method == 'POST':
		formset= TrackForm(request.POST, request.FILES, instance=track)
		if formset.is_valid():
			formset.save()
			return HttpResponseRedirect(reverse('CicloviaProgram:detail',args=[ciclovia_id]))
		else:
			return render(request,'ciclovia/editNeighboor.html',
				{'formset':formset, 'track':track, 'ciclovia':ciclovia})
	else:
		formset=TrackForm(instance=track)
		return render(request,'ciclovia/editNeighboor.html',
				{'formset':formset, 'track':track, 'ciclovia':ciclovia})


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
		return HttpResponseRedirect(reverse('CicloviaProgram:userModels'))

	else:
		form = UploadForm()
	return render(request, 'ciclovia/upload.html', {'form': form})

@ensure_csrf_cookie
@login_required(login_url='CicloviaProgram:login')
def uploadFormCiclovia(request):
	if request.method=='POST':
		json_data = json.loads(request.body)
		CicloviaScript.buildCicloviaFromJson(json_data, request.user)
		return HttpResponseRedirect(reverse('CicloviaProgram:userModels'))
	else:
		return render(request,'ciclovia/uploadFormCiclovia.html')

@login_required(login_url='CicloviaProgram:login')
def deleteCiclovia(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	ciclovia.delete()
	return HttpResponseRedirect(reverse('CicloviaProgram:userModels'))

@login_required(login_url='CicloviaProgram:login')
def uploadArrivalInfo(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(filename = request.POST['filename']
							  ,docfile = request.FILES['docfile'])
			newdoc.save(form)
			name = settings.MEDIA_ROOT + str(newdoc.docfile)
			cicloviaToLoad = CicloviaScript.loadCiclovia(ciclovia_id)
			CicloviaScript.assignArrivalInfo(cicloviaToLoad, ciclovia_id, name)
			cicloviaLoad = get_object_or_404(Ciclovia, pk=ciclovia_id)
			return render(request, 'ciclovia/detailArrival.html',
							  {'ciclovia': cicloviaLoad})
		else:
			return render(request, 'ciclovia/upload.html', {'form': form})
	else:
		form = UploadForm()
	return render(request, 'ciclovia/upload.html', {'form': form})

@login_required(login_url='CicloviaProgram:login')
def uploadArrivalInfoForm(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	if request.method == 'POST':
		#todo cambiar esto para que funcione con el archivo en tipo JSON
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(filename = request.POST['filename']
							  ,docfile = request.FILES['docfile'])
			newdoc.save(form)
			name = settings.MEDIA_ROOT + str(newdoc.docfile)
			cicloviaToLoad = CicloviaScript.loadCiclovia(ciclovia_id)
			CicloviaScript.assignArrivalInfo(cicloviaToLoad, ciclovia_id, name)
			cicloviaLoad = get_object_or_404(Ciclovia, pk=ciclovia_id)
			return render(request, 'ciclovia/detailArrival.html',
							  {'ciclovia': cicloviaLoad})
		else:
			return render(request, 'ciclovia/uploadArrivalInfoForm.html', {'form': form})
	else:
		form = UploadForm()
	return render(request, 'ciclovia/uploadArrivalInfoForm.html', {'form': form})

@login_required(login_url='CicloviaProgram:login')
def simulationResults(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	results_id = CicloviaScript.simulationExecution(ciclovia_id,False)
	return HttpResponseRedirect(reverse('CicloviaProgram:simulationResultsOld',
		args=[ciclovia_id])+unicode("?results_id=" + str(results_id),'utf-8'))

@login_required(login_url='CicloviaProgram:login')
def simulationResultsOld(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
	return render(request, 'ciclovia/simulationResults.html',
				  {'ciclovia': ciclovia, 'results': results})

def piechart(request):
	d = charts.myPieChart()
	data = []
	categories = []
	if request.GET['data']=='avgnumbertrack':
		results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
		trackresults = results.simulationresultscompiledpertrack_set.all()
		for trackresult in trackresults:
			data.append(trackresult.average_number_track)
			categories.append("Trayecto " + str(trackresult.track))
		d.defineData(data,categories,'Número promedio por trayecto')
	elif request.GET['data']=='arrivalstrack':
		results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
		trackresults = results.simulationresultscompiledpertrack_set.all()
		for trackresult in trackresults:
			# data.append(trackresult.average_total_arrivals)
			data.append(10)
			categories.append("Trayecto " + str(trackresult.track))
		d.defineData(data,categories,"Número promedio de arribos")
		d.secondTitle("por trayecto")
	elif request.GET['data']=='flux':
		results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
		trackresults = results.simulationresultscompiledpertrack_set.all()
		for trackresult in trackresults:
			data.append(trackresult.average_total_flow)
			categories.append("Trayecto " + str(trackresult.track))
		d.defineData(data,categories,'Flujo promedio por trayecto')
	elif request.GET['data']=='avgflowtrackcompiled':
		srcpt = get_object_or_404(SimulationResultsCompiledPerTrack, pk=request.GET['srcpt_id'])
		for flowresult in srcpt.simulationresultscompiledflowtrack_set.all():
			data.append(flowresult.avg_flow_hour)
			categories.append("Intervalo " + str(flowresult.hour))
		d.defineData(data,categories, "Flujo promedio por intervalo")
	elif request.GET['data']=='totalfluxtrackonerun':
		results = get_object_or_404(SimulationResults, pk=request.GET['results_id'])
		for track in results.simulationresultspertrack_set.all():
			data.append(track.total_flow)
			categories.append("Trayecto " + str(track.track))
		d.defineData(data,categories,"Flujo total")
	elif request.GET['data']=='avgnumbertrackonerun':
		results = get_object_or_404(SimulationResults, pk=request.GET['results_id'])
		for track in results.simulationresultspertrack_set.all():
			data.append(track.average_number_track)
			categories.append("Trayecto " + str(track.track))
		d.defineData(data,categories,'Número promedio por trayecto')
	elif request.GET['data']=='fluxtrackonerun':
		results = get_object_or_404(SimulationResultsPerTrack, pk=request.GET['results_id'])
		for result in results.simulationresultsflowpertrack_set.all():
			data.append(result.flow_hour)
			categories.append("Intervalo " + str(result.hour))
		d.defineData(data,categories,'Flujo')
	# elif request.GET['data']=='gender':
	# 	data.append(50)
	# 	categories.append("Femenino")
	# 	data.append(50)
	# 	categories.append("Masculino")
	# 	d.defineData(data,categories,"Proporción por género")

	outputimg = d.asString('gif')
	return HttpResponse(outputimg, 'image/gif')

def verticalBarChart(request):
	barChart = charts.myVerticalBarChart()
	data = []
	categories = []
	if request.GET['data']=='avgnumbertrack':
		results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
		trackresults = results.simulationresultscompiledpertrack_set.all()
		for trackresult in trackresults:
			data.append([trackresult.average_number_track])
			categories.append("Trayecto " + str(trackresult.track))
		barChart.defineData(data,categories,'Número promedio por trayecto')
	elif request.GET['data']=='arrivalstrack':
		results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
		trackresults = results.simulationresultscompiledpertrack_set.all()
		for trackresult in trackresults:
			# Los datos del promedio del total de arribos no se han calculado.
			# data.append([trackresult.average_total_arrivals])
			data.append([10])
			categories.append("Trayecto " + str(trackresult.track))
		barChart.defineData(data,categories,"Número promedio de arribos")
		barChart.secondTitle("por trayecto")
	elif request.GET['data']=='flux':
		results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
		trackresults = results.simulationresultscompiledpertrack_set.all()
		for trackresult in trackresults:
			data.append([trackresult.average_total_flow])
			categories.append("Trayecto " + str(trackresult.track))
		barChart.defineData(data,categories,'Flujo promedio por trayecto')
	elif request.GET['data']=='avgflowtrackcompiled':
		srcpt = get_object_or_404(SimulationResultsCompiledPerTrack, pk=request.GET['srcpt_id'])
		for flowresult in srcpt.simulationresultscompiledflowtrack_set.all():
			data.append([flowresult.avg_flow_hour])
			categories.append("Intervalo " + str(flowresult.hour))
			barChart.defineData(data,categories, "Flujo promedio por intervalo")
	elif request.GET['data']=='totalfluxtrackonerun':
		results = get_object_or_404(SimulationResults, pk=request.GET['results_id'])
		for track in results.simulationresultspertrack_set.all():
			data.append([track.total_flow])
			categories.append("Trayecto " + str(track.track))
		barChart.defineData(data,categories,"Flujo total")
	elif request.GET['data']=='avgnumbertrackonerun':
		results = get_object_or_404(SimulationResults, pk=request.GET['results_id'])
		for track in results.simulationresultspertrack_set.all():
			data.append([track.average_number_track])
			categories.append("Trayecto " + str(track.track))
		barChart.defineData(data,categories,'Número promedio por trayecto')
	elif request.GET['data']=='fluxtrackonerun':
		results = get_object_or_404(SimulationResultsPerTrack, pk=request.GET['results_id'])
		for result in results.simulationresultsflowpertrack_set.all():
			data.append([result.flow_hour])
			categories.append("Intervalo " + str(result.hour))
		barChart.defineData(data,categories,'Flujo')
	elif request.GET['data']=='gender':
		data.append([50])
		categories.append("Femenino")
		data.append([50])
		categories.append("Masculino")
		barChart.defineData(data,categories,"Proporción por género")
	outputimg = barChart.asString('gif')
	return HttpResponse(outputimg, 'image/gif')

@login_required(login_url='CicloviaProgram:login')
def simulationResultsValidation(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	results_id = CicloviaScript.simulationExecution(ciclovia_id,True)
	return HttpResponseRedirect(reverse('CicloviaProgram:simulationResultsValidationOld',
		args=[ciclovia_id])+unicode("?results_id=" + str(results_id),'utf-8'))

@login_required(login_url='CicloviaProgram:login')
def simulationResultsValidationOld(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	results = get_object_or_404(SimulationResultsCompiled, pk=request.GET['results_id'])
	return render(request, 'ciclovia/simulationResultsValidation.html',
				  {'ciclovia': ciclovia, 'results': results})

@login_required(login_url='CicloviaProgram:login')
def inverseSimulationWarning(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	#results_id = CicloviaScript.simulationExecution(ciclovia_id,True)
	return render(request, 'ciclovia/inverseSimulationWarning.html', {'ciclovia':ciclovia})

@login_required(login_url='CicloviaProgram:login')
def inverseSimulationExecution(request, ciclovia_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	#results_id = CicloviaScript.inverseSimulation(ciclovia_id)
	return render(request, 'ciclovia/inverseSimulationWarning.html', {'ciclovia':ciclovia_id})

@login_required(login_url='CicloviaProgram:login')
def detailTrackValidation(request, ciclovia_id, track_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	track = get_object_or_404(SimulationResultsCompiledPerTrack, pk=track_id)
	return render(request, 'ciclovia/detailTrackValidation.html',
				  {'ciclovia': ciclovia, 'track': track})

@login_required(login_url='CicloviaProgram:login')
def detailValidationSingleRun(request, ciclovia_id, run_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	result = get_object_or_404(SimulationResults, pk=run_id)
	return render(request, 'ciclovia/detailValidationSingleRun.html',
				  {'ciclovia': ciclovia, 'run': result})

@login_required(login_url='CicloviaProgram:login')
def detailTrackValidationSingleRun(request, ciclovia_id, run_id, track_id):
	ciclovia = get_object_or_404(Ciclovia, pk=ciclovia_id)
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	result = get_object_or_404(SimulationResults, pk=run_id)
	track = get_object_or_404(SimulationResultsPerTrack, pk=track_id)
	return render(request, 'ciclovia/detailTrackValidationSingleRun.html',
				  {'ciclovia': ciclovia, 'run': result, 'track': track})

# @login_required(login_url='CicloviaProgram:login')
# def adminSimulation(request):
# 	if not request.user.is_superuser:
# 		raise PermissionDenied
# 	simulation_list = SimulationParameters.objects.order_by('-replications')[:1]
# 	template = loader.get_template('ciclovia/adminSimulation.html')
# 	context = RequestContext(request, {
# 		'simulation_list': simulation_list,
# 	})
# 	return HttpResponse(template.render(context))

def simulationList(request):
	"""Retorna un select con las simulaciones de la ciclovía o un mensaje si no hay ninguna."""
	ciclovia = get_object_or_404(Ciclovia, pk=request.GET['ciclovia_id'])
	if not (ciclovia.user == request.user or request.user.is_superuser):
		raise PermissionDenied
	simulation_list = ciclovia.simulationresultscompiled_set.filter(is_validation=False).order_by('-date')
	if request.GET['simsel']=="ciclovia1sel":
		return render(request,'ciclovia/simulationList.html',{'simulation_list':simulation_list,
			'simulationnum':'1'})
	else:
		return render(request,'ciclovia/simulationList.html',{'simulation_list':simulation_list,
			'simulationnum':'2'})

@login_required(login_url='CicloviaProgram:login')
def compareSimulations(request):
	"""Compara las simulaciones de dos ciclovías."""
	if not request.user.is_superuser:
		ciclovias = Ciclovia.objects.filter(user=request.user).order_by('-name')
	else:
		ciclovias = Ciclovia.objects.order_by('-name')
	if request.method == 'GET':
		return render(request,"ciclovia/compararCiclovias.html",{'ciclovias':ciclovias})
	elif request.method == 'POST':
		simulation1 = get_object_or_404(SimulationResultsCompiled, pk=request.POST['simulation1'])
		simulation2 = get_object_or_404(SimulationResultsCompiled, pk=request.POST['simulation2'])
		simulationComp = CicloviaScript.simulationComp(simulation1,simulation2)
		return render(request,"ciclovia/compareSimulationsResults.html",
			{'simulation1':simulation1,'simulation2':simulation2, 'simulationComp':simulationComp})

@user_passes_test(notAutheticated,login_url='CicloviaProgram:index')
def newUser(request):
	"""Cretate user if none is loged in."""
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
				form.save()
				userTemp = authenticate(username=form.cleaned_data['username'],
										password=form.cleaned_data['password1'])
				login(request, userTemp)
				return HttpResponseRedirect(reverse('CicloviaProgram:user'))
		else:
			#Redisplay user creation form with error(s).
			return render(request, 'ciclovia/new_user.html',
						  {'form':form})
	else:
		form = NewUserForm()
		return render(request, 'ciclovia/new_user.html',{'form':form})

def user(request):
	"""User page."""
	if request.method == 'POST':
		if request.POST['opcion']=='Cerrar sesión'.decode('utf-8'):
			return auth_views.logout(request,next_page='CicloviaProgram:index')
		elif request.POST['opcion']=='Borrar usuario':
			DeleteU(request.user.username)
			return auth_views.logout(request,next_page='CicloviaProgram:index')
		elif request.POST['opcion']=='Actualizar datos':
			form = UserChangeFormUniqueEmail(request.POST, instance=User.objects.get(pk=request.user.pk))
			if form.is_valid():
				userTemp = User.objects.get(pk=request.user.pk)
				if form.cleaned_data['email']==userTemp.email or \
								len(User.objects.filter(email=form.cleaned_data['email']))is 0:
					form.save()
					return render(request, 'ciclovia/user.html',
								  {'form': form,'mensaje': _('User info updated.')})
				else:
					form.add_error('email',forms.ValidationError(_('email already exists.'),code='used email'))
					return render(request, 'ciclovia/user.html', {'form': form})

			else:
				return render(request, 'ciclovia/user.html', {'form': form})
	else:
		form = UserChangeFormUniqueEmail(instance=User.objects.get(pk=request.user.pk))
		return render(request, 'ciclovia/user.html', {'form': form})




