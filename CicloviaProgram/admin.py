# coding=utf-8
from django.contrib import admin
from CicloviaProgram.models import Ciclovia
from CicloviaProgram.models import Track
from CicloviaProgram.models import NeighboorInfo
from CicloviaProgram.models import Document
from CicloviaProgram.models import ParticipantType
from CicloviaProgram.models import SimulationParameters
from CicloviaProgram.models import TimeInSystemDistribution
from CicloviaProgram.models import ArrivalsProportionPerHour
from CicloviaProgram.models import SimulationResultsCompiled
from CicloviaProgram.models import SimulationResults
from CicloviaProgram.models import SimulationResultsCompiledPerTrack
from CicloviaProgram.models import SimulationResultsPerTrack
from CicloviaProgram.models import SimulationResultsCompiledFlowTrack
from CicloviaProgram.models import SimulationResultsFlowPerTrack
from CicloviaProgram.models import InverseSimulation


class CicloviaAdmin(admin.ModelAdmin):
##     list_display = ('user', 'name', 'place', 'start_hour', 'end_hour', 'num_tracks')
     list_display = ('name', 'place', 'start_hour', 'end_hour', 'num_tracks')

class TrackAdmin(admin.ModelAdmin):
     list_display = ('id_track', 'distance', 'probability', 'arrival_proportion')

class NeighboorAdmin(admin.ModelAdmin):
     list_display = ('neighboorId',  'probability')

class DocumentAdmin(admin.ModelAdmin):
     list_display = ('filename',  'docfile')

class ParticipantTypeAdmin(admin.ModelAdmin):
     list_display = ('activity',  'velocity', 'percentage')

class SimulationParametersAdmin(admin.ModelAdmin):
     list_display = ('replications',  'arrivals_probability_distribution')

class TimeInSystemDistributionAdmin(admin.ModelAdmin):
     list_display = ('time',  'percentage', 'ciclovia')

class ArrivalsProportionPerHourAdmin(admin.ModelAdmin):
     list_display = ('hour',  'proportion')
     
class SimulationResultsCompiledAdmin(admin.ModelAdmin):
     list_display = ('date',  'num_runs', 'avg_total_arrivals', 'stdev_total_arrivals', 'average_number_system', 'stdev_number_system', 'is_validation','ciclovia')

class SimulationResultsAdmin(admin.ModelAdmin):
     list_display = ('date',  'sim_time', 'total_arrivals', 'average_time', 'standard_deviation_time', 'average_number_system')

class SimulationResultsCompiledPerTrackAdmin(admin.ModelAdmin):
     list_display = ('track',  'average_number_track', 'stdev_number_track', 'average_total_flow', 'stdev_total_flow')
     
class SimulationResultsPerTrackAdmin(admin.ModelAdmin):
     list_display = ('track',  'total_arrivals', 'total_flow', 'average_number_track')

class SimulationResultsCompiledFlowPerTrackAdmin(admin.ModelAdmin):
     list_display = ('track_simulation','hour',  'avg_flow_hour', 'stdev_flow_hour')	
     
class SimulationResultsFlowPerTrackAdmin(admin.ModelAdmin):
     list_display = ('track_simulation','hour',  'flow_hour')

class InverseSimulationAdmin(admin.ModelAdmin):
    list_display = ('ciclovia', 'lastModified', 'finished', 'creationTime', 'progress')


admin.site.register(Ciclovia, CicloviaAdmin)

admin.site.register(Track, TrackAdmin)

admin.site.register(NeighboorInfo, NeighboorAdmin)

admin.site.register(Document, DocumentAdmin)

admin.site.register(TimeInSystemDistribution, TimeInSystemDistributionAdmin)

admin.site.register(ArrivalsProportionPerHour, ArrivalsProportionPerHourAdmin)

admin.site.register(ParticipantType, ParticipantTypeAdmin)

admin.site.register(SimulationParameters, SimulationParametersAdmin)

admin.site.register(SimulationResultsCompiled, SimulationResultsCompiledAdmin)

admin.site.register(SimulationResults, SimulationResultsAdmin)

admin.site.register(SimulationResultsCompiledPerTrack, SimulationResultsCompiledPerTrackAdmin)

admin.site.register(SimulationResultsPerTrack, SimulationResultsPerTrackAdmin)

admin.site.register(SimulationResultsCompiledFlowTrack, SimulationResultsCompiledFlowPerTrackAdmin)

admin.site.register(SimulationResultsFlowPerTrack, SimulationResultsFlowPerTrackAdmin)

admin.site.register(InverseSimulation, InverseSimulationAdmin)
