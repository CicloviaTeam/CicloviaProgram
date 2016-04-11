# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This section contains the objects associated with the information of the structure of the Ciclovia
# - 1 - Ciclovia: contains the general information of the Ciclovia
# - 2 - Track: contains the main information of a track that belongs to a Ciclovia
# - 3 - NeighboorInfo: contains the relations between the tracks 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This object represents a Ciclovia
class Ciclovia(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=20)
    start_hour = models.FloatField(default=0)
    end_hour = models.FloatField(default=0)
    num_tracks = models.IntegerField(default=1)
    reference_track = models.IntegerField(default=0)
    reference_hour = models.IntegerField(default=0)
    reference_arrival_rate = models.FloatField(default=0)    
    arrivals_loaded = models.BooleanField(default=False)
        
    def __unicode__(self):  
        return self.name + " " + self.user.username


# This object represents a Track
class Track(models.Model):
    ciclovia = models.ForeignKey(Ciclovia)
    id_track = models.IntegerField(default=100)
    distance = models.FloatField(default=1)
    probability = models.FloatField(default=1)
    # Modified probabilities
    probabilityBegin = models.FloatField(default=1)
    probabilityEnd = models.FloatField(default=1)
    arrival_proportion = models.FloatField(default=1)

    # New Velocity parameters
    number_of_semaphores = models.IntegerField(default=1)
    # 0: no slope, 1: has middle slope, 2: high slope
    hasSlope = models.IntegerField(default=1)
    quality_of_track = models.IntegerField(default=1)

    def __unicode__(self):  
        return str(self.id_track)   


# This object represents the relation between two tracks
class NeighboorInfo(models.Model):
    track = models.ForeignKey(Track)
    neighboorId = models.IntegerField(default=1)
    probability = models.FloatField(default=1)
    direction = models.CharField(max_length=10)   
    fromDirection = models.CharField(max_length=10)   
    
    def __unicode__(self):  
        return str(self.neighboorId) + "," + str(self.probability)   

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This section contains the objects associated with the information of the arrivals' behavior
# - 1 - ParticipantType: contains the information related to the types of activities that people do in a Ciclovia
# - 2 - TimeInSystemDistribution: contains the information of the distribution of the time in system
# - 3 - ArrivalsProportionPerHour: contains the relative proportion of arrivals that occur in an hour
# - 4 - Document: contains the location of the XML files with the documents of the structure and the arrivals of the Ciclovia
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# This object represents a Type of participant
class ParticipantType(models.Model):
    ciclovia = models.ForeignKey(Ciclovia)
    activity = models.CharField(max_length=30)
    velocity = models.FloatField(default=1)
    percentage = models.FloatField(default=1)
       
    def __unicode__(self):  
        return self.activity
    

# This object represents one of the values of the time in system distribution
class TimeInSystemDistribution(models.Model):
    ciclovia = models.ForeignKey(Ciclovia)
    time = models.FloatField(default=1)
    percentage = models.FloatField(default=1)
       
    def __unicode__(self):  
        return str(self.time)
    

# This object represents one of the values of the time in system distribution
class ArrivalsProportionPerHour(models.Model):
    ciclovia = models.ForeignKey(Ciclovia)
    hour = models.FloatField(default=1)
    proportion = models.FloatField(default=1)
       
    def __unicode__(self):  
        return str(self.hour)


# This object represents the XML document which contains the information of a Ciclovia
class Document(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')    
    
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This section contains the objects associated with the information of the simulation
# - 1 - SimulationParameters: contains the information related to the specific details for simulation's execution
# - 2 - SimulationResultsCompiled: contains the statistics of a serie of runs
# - 3 - SimulationResults: contains the statistics of a single run
# - 4 - SimulationResultsCompiledPerTrack: contains the statistics of a serie of runs for a single track 
# - 5 - SimulationResultsPerTrack: contains the statistics of a single run in a specific track
# - 6 - SimulationResultsCompiledFlowPerTrack: contains the statistics associated to the flow of a serie of runs for a single track 
# - 7 - SimulationResultsFlowPerTrack: contains the statistics associated to the flow of a single run in a specific track
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# This object represents default information of the simulation
class SimulationParameters(models.Model):
    replications = models.FloatField(default=1)
    arrivals_probability_distribution = models.CharField(max_length=30)
               
    def __unicode__(self):  
        return str(self.replications)+ "," + str(self.arrivals_probability_distribution)


# This object represents the statistics for a serie of runs
class SimulationResultsCompiled(models.Model):
    ciclovia = models.ForeignKey(Ciclovia)
    date = models.DateTimeField('date executed')
    num_runs = models.FloatField(default=0)
    avg_total_arrivals = models.IntegerField(default=0)
    stdev_total_arrivals = models.IntegerField(default=0)
    hw_total_arrivals = models.IntegerField(default=0)   
    average_number_system = models.FloatField(default=0)
    stdev_number_system = models.FloatField(default=0)
    hw_number_system = models.FloatField(default=0)
    is_validation = models.BooleanField(default=False)
    
    def __unicode__(self):  
        return 'Fecha: ' + self.date.strftime('%Y-%m-%d %H:%M %Z') + ', Replicas: ' + str(self.num_runs)


# This obhect represents the results of a single run
class SimulationResults(models.Model):
    ciclovia = models.ForeignKey(SimulationResultsCompiled)
    date = models.DateTimeField('date executed')
    sim_time = models.FloatField(default=0)
    total_arrivals = models.IntegerField(default=0)
    average_time = models.FloatField(default=0)
    standard_deviation_time = models.FloatField(default=0)
    average_number_system = models.FloatField(default=0)
    is_validation = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.sim_time)+ "," + str(self.total_arrivals)

# This object represents the statistics per track for a serie of runs
class SimulationResultsCompiledPerTrack(models.Model):
    simulation_compiled = models.ForeignKey(SimulationResultsCompiled)
    track = models.IntegerField(default=0)
    average_number_track = models.IntegerField(default=0)
    stdev_number_track = models.IntegerField(default=0)
    hw_number_track = models.IntegerField(default=0)
    average_total_arrivals = models.IntegerField(default=0)
    stdev_total_arrivals = models.IntegerField(default=0)
    hw_total_arrivals = models.IntegerField(default=0)
    average_total_flow = models.IntegerField(default=0)
    stdev_total_flow = models.IntegerField(default=0)
    hw_total_flow = models.IntegerField(default=0)
    
    def __unicode__(self):  
        return str(self.simulation_compiled) + "," + str(self.track)+ "," + str(self.average_number_track) + "," \
        + str(self.stdev_number_track) + "," + str(self.average_total_flow)+ "," + str(self.stdev_total_flow)
       
# This object represents the information associated with the flow that occurs in a single track
class SimulationResultsPerTrack(models.Model):
    simulation = models.ForeignKey(SimulationResults)
    track = models.IntegerField(default=0)
    total_arrivals = models.IntegerField(default=0)
    total_flow = models.FloatField(default=0)
    average_number_track = models.IntegerField(default=0)
    
    def __unicode__(self):  
        return str(self.simulation)+ "," + str(self.track)+ "," + str(self.total_arrivals)
    
# This object represents the information associated with the flow of the track in a signle run
class SimulationResultsCompiledFlowTrack(models.Model):
    track_simulation = models.ForeignKey(SimulationResultsCompiledPerTrack)
    hour = models.IntegerField(default=0)
    avg_flow_hour = models.FloatField(default=0)
    stdev_flow_hour = models.FloatField(default=0)
    hw_flow_hour = models.FloatField(default=0)
            
    def __unicode__(self):  
        return str(self.track_simulation)+ "," + str(self.hour)+ "," + str(self.avg_flow_hour)        
        
# This object represents the information associated with the flow of the track in a signle run
class SimulationResultsFlowPerTrack(models.Model):
    track_simulation = models.ForeignKey(SimulationResultsPerTrack)
    hour = models.IntegerField(default=0)
    flow_hour = models.IntegerField(default=0)
            
    def __unicode__(self):  
        return str(self.track_simulation)+ "," + str(self.hour)+ "," + str(self.flow_hour)        

# This object represents the information involved in a inverse simulation
class InverseSimulation(models.Model):
    ciclovia = models.ForeignKey(Ciclovia)
    lastModified = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(default=False)
    creationTime = models.DateTimeField(auto_now_add=True)
    # This number is between 0 and 100 (completion percentage)
    progress = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.ciclovia)+","+str(self.creationTime)