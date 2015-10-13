import xml.etree.ElementTree as ET
import decimal
import simpy
import collections
import random
import math
import scipy
import numpy
from operator import attrgetter, itemgetter
from PrintXML import printOrganizedXML
from django.utils import timezone
import timeit


from CicloviaProgram.models import Ciclovia, Track, NeighboorInfo, ArrivalsProportionPerHour, TimeInSystemDistribution, SimulationResults


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   OBJETOS - CLASES
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

#This class represents a Ciclovia model
class CicloviaObj:
    
    #This is the constructor of the class Ciclovia
    #It takes the parameters provided as arguments and stores them in the object
    def __init__(self, name, place, startHour, endHour, numTracks, tracks):
        self.name = name
        self.place = place
        self.startHour = startHour
        self.endHour = endHour
        self.numTracks = numTracks
        self.tracks = tracks
        self.referenceTrack = 0
        self.referenceHour = 0
        self.referenceArrivalRate = 0
        self.timeUnits = ""
        self.timeInSystemDistribution = []
        self.arrivalProportionPerHour = []
        self.typeParticipants = []
        self.maxArrivals = 0
        
    #This class prints the basic information of the Ciclovia
    def printInfo(self):
        print"Nombre: " + self.name
        print"Lugar: " + self.place
        print"Hora inicio: " + str(self.startHour)
        print"Hora fin: " + str(self.endHour)
        print"Num trayectos:" + str(self.numTracks)
        print"Trayecto referencia: " + str(self.referenceTrack)
        print"Hora referencia: " + str(self.referenceHour)
        print"Tasa de arribos referencia " + str(self.referenceArrivalRate)
        print"Unidades de tiempo: " + self.timeUnits
        print"Distribucion tiempo servicio " + str(self.timeInSystemDistribution)
        print"Arribos por hora: " + str(self.arrivalProportionPerHour)
        print"Trayectos: "
        for track in self.tracks:
            print (track.idNum, track.distance, track.probability, track.tracksId, track.tracksProb, track.arrivalProportion)
            print("Proporcion de arribos" + str(track.arrivalsPerHour))
        print"Participantes: "        
        for typeParticipant in self.typeParticipants:
            print (typeParticipant.activity, typeParticipant.velocity, typeParticipant.percentage)        
            
    #This gives a track, given its ID 
    def getTrack(self, trackId):
        for track in self.tracks:
            if(track.idNum==trackId):            
                return track
            
    #This assigns the arrival, according to the hour and the track density
    def assignArrivalsToTrack(self):
        for track in self.tracks:
            arrivalSet = []
            for arrivalAtHour in self.arrivalProportionPerHour:                 
                arrivalRate = arrivalAtHour[1]*decimal.Decimal(track.arrivalProportion)*decimal.Decimal(self.referenceArrivalRate)*decimal.Decimal(track.distance)
                arrivalSet.append(arrivalRate)
                self.maxArrivals+=arrivalRate
            track.arrivalsPerHour = arrivalSet
                 
        
#This class represents a Track from a Ciclovia
class TrackObj:
    
    #This is the constructor of the class Track
    def __init__(self, idNum, distance, probability, probabilityBegin, probabilityEnd, tracksId, tracksProb, tracksDirection):
            self.idNum = idNum
            self.distance = distance
            self.probability = probability
            #Modified probabilities
            self.probabilityBegin = probabilityBegin
            self.probabilityEnd = probabilityEnd
            
            self.tracksId = tracksId 
            self.tracksProb = tracksProb 
            self.tracksDirection = tracksDirection
            self.arrivalProportion = 0
            self.arrivalsPerHour = []
            #self.numParticipants = []
            #self.timeNumParticpants = []
            self.numberInTrack = 0
            self.numParticipantsInTrack = []
    
    #This gives the probability of a neighboor track, given its ID 
    def getProb(self, trackId):
        for index, neighboor in enumerate(self.tracksId):
            if(neighboor==trackId):
                return self.tracksProb.pop(index)
        return -1
    
    #This recalculates the probability of the tracks, given the new neighboor ID
    def recalculateProb(self, newTrackId):
        newTrackProb = self.getProb(newTrackId)
        newProb = 1-newTrackProb
        self.probability = self.probability*newProb
        for index, neighboor in enumerate(self.tracksId):
            if(neighboor!=trackId):
                self.tracksProb[index] = self.tracksProb.pop(index)*newProb
                
    def giveNeighboorInDirection(self, direction):
        probabilities = []
        ids = []
        for index, direct in enumerate(self.tracksDirection):
            #print("La direccion solicitada es " + direction + " la iterada es " + direct)
            #if(direct == direction):
            probabilities.append(self.tracksProb[index])
            ids.append(self.tracksId[index])       
        probabilities.append(self.probability)   
        probabilitiesArray = numpy.array(probabilities, dtype=numpy.dtype(numpy.float64))
        ids.append(self.idNum)   
        idsArray = numpy.array(ids, dtype=numpy.dtype(numpy.float64))
        #print("Las probabilidades son " + str(probabilities))
        #print("Los ids son " + str(ids))
        bins = numpy.cumsum(probabilitiesArray)        
        listProbabilities = idsArray[numpy.digitize(numpy.random.random_sample(2), bins)]        
        #return numpy.digitize(numpy.random.random_sample(1), bins)[0]   
        #print("Retorno ")
        #print(listProbabilities[0])
        return listProbabilities[0]    
    
                
        #return ids[numpy.digitize(numpy.random.random_sample(1), bins)] 
        #print("Retorno")
        #print(numpy.digitize(numpy.random.random_sample(1), bins)[0])
        #return numpy.digitize(numpy.random.random_sample(1), bins)[0]       
     
    
    def updateNumberInTrack(self, time):
        size = len(self.numParticipantsInTrack)
        if(size == 0):
            initialNumber = [0, 0]
            self.numParticipantsInTrack.append(initialNumber) 
            info = [self.numberInTrack,time]
            self.numParticipantsInTrack.append(info)   
        else:
            newInfo = [self.numberInTrack, (time-self.numParticipantsInTrack[size-1][1])]
            self.numParticipantsInTrack.append(newInfo)      
             
     
                
#This class represents a type of participant
class ParticipantTypeObj:
    
    #This is the constructor of the class Ciclovia
    #It takes the parameters provided as arguments and stores them in the object
    def __init__(self, activity, velocity, percentage):
        self.activity = activity
        self.velocity = velocity
        self.percentage = percentage
               
    #This class prints the basic information of the Ciclovia
    def printInfo(self):
        print(self.activity, self.velocity, self.percentage)
            

#This class represents a the simulation information
class SimulationObj:
    
    #This is the constructor of the class Simulation
    #It takes the parameters provided as arguments and stores them in the object
    def __init__(self, replications, arrivalsProbabilityDistribution):
        self.replications = replications
        self.arrivalsProbabilityDistribution = arrivalsProbabilityDistribution
               
    #This class prints the basic information of the Simulation parameters
    def printInfo(self):
        print(self.replications, self.arrivalsProbabilityDistribution)
             
    

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   DEFINICIONES PARA CREAR Y MODIFICAR LA CICLOVIA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
                
#This definition reads a data file and build the Ciclovia model 
def buildCiclovia(filename):
    try:       
   
        #In this part, the Ciclovia is created given a XML file
        tree = ET.ElementTree(file=filename)
     
        #The root of the XML is taken
        root = tree.getroot()
        #This is the list that contains all the tracks of a Ciclovia
        trackSet = []
        #This is the type of XML (model or experiment)
        typeCiclovia = root.find('type').text        
        
        
        #In this part, all the tracks are built and they are added to the trackSet
        for track in root.findall('track'):
            trackId = int(track.find('id').text)
            trackDistance = int(track.find('distance').text)
            trackProbability =  decimal.Decimal(track.find('probability').text)
            #Modified probabilities
            trackProbabilityBegin =  decimal.Decimal(track.find('probabilityBegin').text)
            trackProbabilityEnd =  decimal.Decimal(track.find('probabilityEnd').text)
            neighboorsIds = []
            neighboorsProbs = []
            neighboorsDirection = []
            #Direction = if begin = 0, if end 1
            sumProb = trackProbability
            for neighboor in track.findall('neighboor'):
                neighboorId = int(neighboor.find('id').text)
                neighboorsIds.append(neighboorId)
                neighboorProb= decimal.Decimal(neighboor.find('probability').text)
                neighboorsProbs.append(neighboorProb)
                neighboorsDirec= neighboor.find('direction').text
                #neighboorDir = 0
                #if(neighboorsDirec == "end"):
                    #neeighboorDir = 1
                neighboorsDirection.append(neighboorsDirec)   
                sumProb+= neighboorProb                 
            if sumProb != 1.0:
                print("Error la suma de probabilidades no es 1")
            
            newTrack = TrackObj(trackId, trackDistance, trackProbability, trackProbabilityBegin, trackProbabilityEnd, neighboorsIds, neighboorsProbs, neighboorsDirection)
            trackSet.append(newTrack)
        
        #In this part all the attributes of a Ciclovia are assigned
        name = root.find('name').text
        place = root.find('place').text
        startHour = decimal.Decimal(root.find('startHour').text)
        if startHour > 24 :
            print("Error: se ha excedido el maximo de horas en un dia (24)")    
        endHour = decimal.Decimal(root.find('endHour').text)
        if endHour > 24 :
                print("Error: se ha excedido el maximo de horas en un dia (24)")     
        numTracks = int(root.find('numTracks').text)
        if numTracks > 30 :
                print("Error: se ha excedido el maximo numero de trayectos (30)")     
        ciclovia = CicloviaObj(name, place, startHour, endHour, numTracks, trackSet)
       
        #Only loads info in database if it is a model (no an experiment)
        #OJO: CAMBIAR A MODEL en lugar de MODELC    
        if(typeCiclovia=="model"):
            print("Como es un modelo, voy a guardar la info en la base de datos")
            cicloviaDB = Ciclovia(name=ciclovia.name, place=ciclovia.place, start_hour = ciclovia.startHour, end_hour = ciclovia.endHour, num_tracks = ciclovia.numTracks)
            cicloviaDB.save()        
            print("ID de la Ciclovia en la base de datos")
            print(cicloviaDB.id)   
            for track in ciclovia.tracks:
                #Modified probabilities
                trackDB = cicloviaDB.track_set.create(id_track=track.idNum, distance=track.distance, probability=track.probability, probabilityBegin=track.probabilityBegin, probabilityEnd=track.probabilityEnd)
                trackDB.save()
                print("ID del trayecto en la base de datos")
                print(trackDB.id)
                for index, neighboor in enumerate(track.tracksId):
                    neighboorDB = trackDB.neighboorinfo_set.create(neighboorId=neighboor, probability=track.tracksProb[index], direction=track.tracksDirection[index])
                    neighboorDB.save()
                    print("Vecino")
                    print(neighboorDB)      
        return ciclovia
    except:
        print ("Ocurrio un error")
    
    

#This definition adds new tracks to the model
def addTracks(dataFile, ciclovia):
    
    tree = ET.parse(dataFile)
    root = tree.getroot()
    
    #In this part, all the new tracks are built and they are added to the Ciclovia set. 
    #Neighboors' probabilities are modified too.
    for newTrack in root.findall('newTrack'):
        trackId = int(newTrack.find('id').text)
        trackDistance = int(newTrack.find('distance').text)
        trackProbability =  decimal.Decimal(newTrack.find('probability').text)
        #Modified probabilities
        trackProbabilityBegin =  decimal.Decimal(newTrack.find('probabilityBegin').text)
        trackProbabilityEnd =  decimal.Decimal(newTrack.find('probabilityEnd').text)        
        neighboorsIds = []
        neighboorsProbs = []
        sumProb = trackProbability
        for neighboor in newTrack.findall('neighboor'):
            neighboorId = int(neighboor.find('id').text)
            neighboorsIds.append(neighboorId)
            neighboorProb= decimal.Decimal(neighboor.find('trackToNeighboorProbability').text)
            neighboorToTrackProb= decimal.Decimal(neighboor.find('neighboorToTrackProbability').text)
            neighboorsProbs.append(neighboorProb)
            for neighboorTrack in ciclovia.tracks:
                found= False
                if(neighboorTrack.idNum == neighboorId and found!=True):
                    neighboorTrack.tracksId.append(trackId);
                    neighboorTrack.tracksProb.append(neighboorToTrackProb);
                    found=True
                    print("Se agrego la prob del nuevo trayecto al vecino")
            sumProb+= neighboorProb
        if sumProb != 1.0:
            print("Error la suma de probabilidades no es 1")
        newTrack = TrackObj(trackId, trackDistance, trackProbability, neighboorsIds, neighboorsProbs)
        ciclovia.tracks.append(newTrack)

#This definition removes tracks from the Ciclovia
def removeTracks(dataFile, ciclovia):
   
    tree = ET.parse(dataFile)
    root = tree.getroot()
    #In this part, all the tracks are deleted from the Ciclovia
    #Neighboors' probabilities are modified too.
    for removeTrack in root.findall('trackToRemove'):
        trackId = int(removeTrack.find('id').text)
        for track in ciclovia.tracks:
            found= False
            if(track.idNum == trackId):
                ciclovia.tracks.remove(track)
                print("Se elimino el trayecto")
            else:
                for index, elem in enumerate(track.tracksId):
                    if(elem==trackId):
                        track.tracksId.pop(index)
                        track.tracksProb.pop(index)
                        print ("Se elimino la prob en el trayecto vecino")
                               
                   
#This definition reads a data file and assigns the information of the arrivals to the tracks
def assignArrivalInfo(ciclovia, ciclovia_id, filename):
   
    tree = ET.ElementTree(file=filename)
    root = tree.getroot()

    cicloviaFromDB = Ciclovia.objects.get(id=ciclovia_id)
    
    #This is the type of XML (model or experiment)
    nameCiclovia = root.find('name').text
    if(nameCiclovia!=cicloviaFromDB.name):
        print("Error, los nombres no coinciden")
    
    #In this part all the attributes of a Ciclovia are assigned
    cicloviaFromDB.reference_arrival_rate = decimal.Decimal(root.find('arrivalRate').text)   
    #cicloviaFromDB.timeUnits = root.find('unitsTime').text
    cicloviaFromDB.reference_track  = root.find('referenceTrack').text
    cicloviaFromDB.reference_hour = root.find('referenceHour').text
    cicloviaFromDB.arrivals_loaded = True
    cicloviaFromDB.save()
   
    
    #This is the list that contains the proportion of arrivals per hour of a Ciclovia
    hourProportionSet = []
            
    #In this part, all the tracks are built and they are added to the trackSet
    for hour in root.findall('hour'):
        hourValue = int(hour.find('time').text)
        proportionValue = decimal.Decimal(hour.find('proportion').text)
        timeProportion = [hourValue, proportionValue]      
        hourProportionSet.append(timeProportion)
        timeInSystemValueDB = cicloviaFromDB.arrivalsproportionperhour_set.create(hour = hourValue,  proportion = proportionValue)
        timeInSystemValueDB.save()          
    
    #ciclovia.arrivalProportionPerHour = hourProportionSet   
        
    #In this part, all the proportions are assigned to the tracks
    for track in root.findall('track'):
        trackId = int(track.find('id').text)
        proportion = decimal.Decimal(track.find('proportion').text)
        query_tracksFromDB = cicloviaFromDB.track_set.all()
        found = False
        for trackDB in query_tracksFromDB:  
            if(found == False and trackDB.id_track == trackId):
                trackDB.arrival_proportion = proportion
                trackDB.save()
                found=True
                       
        #foundTrack = ciclovia.getTrack(trackId)   
        #foundTrack.arrival_proportion = proportion       
        
     
        
    participantsSet = []  
        
    #In this part, all the types of participants are built and they are added to the participantSet
    for participant in root.findall('participantType'):
        activityPart = participant.find('activity').text
        velocityPart = decimal.Decimal(participant.find('velocity').text)
        percentagePart = decimal.Decimal(participant.find('percentage').text)    
        typeParticipant = ParticipantTypeObj(activityPart, velocityPart, percentagePart)
        participantsSet.append(typeParticipant)
        participantDB = cicloviaFromDB.participanttype_set.create(activity=activityPart, velocity=velocityPart, percentage=percentagePart)
        participantDB.save()
    #ciclovia.typeParticipants = participantsSet  
        
    #This is the list that contains the proportion of arrivals per hour of a Ciclovia
    timeInSystemSet = []
    
    #In this part, all the tracks are built and they are added to the trackSet
    for timeSystem in root.findall('timeInSystem'):
        for group in timeSystem.findall('group'):
            timeSystem = int(group.find('time').text)
            percentageTime = decimal.Decimal(group.find('percentage').text)
            timeDistribution = [timeSystem, percentageTime]      
            timeInSystemSet.append(timeDistribution)
            timeInSystemValueDB = cicloviaFromDB.timeinsystemdistribution_set.create(time = timeSystem,  percentage = percentageTime)
            timeInSystemValueDB.save()              
        #ciclovia.timeInSystemDistribution = timeInSystemSet     
        
       
    
#This definition reads a data file and assigns the information of the arrivals to the tracks
def assignArrivalInfoNoDB(ciclovia, filename):

    tree = ET.ElementTree(file=filename)
    root = tree.getroot()

    #In this part all the attributes of a Ciclovia are assigned
    ciclovia.referenceArrivalRate = root.find('arrivalRate').text    
    #cicloviaFromDB.timeUnits = root.find('unitsTime').text
    ciclovia.referenceTrack  = root.find('referenceTrack').text
    ciclovia.referenceHour = root.find('referenceHour').text
     
    #This is the list that contains the proportion of arrivals per hour of a Ciclovia
    hourProportionSet = []
            
    #In this part, all the hour proportions are built and they are added to the hourProportionSet
    for hour in root.findall('hour'):
        time = int(hour.find('time').text)
        proportion = decimal.Decimal(hour.find('proportion').text)
        timeProportion = [time, proportion]      
        hourProportionSet.append(timeProportion)
    
    ciclovia.arrivalProportionPerHour = hourProportionSet   
    
        
    #In this part, all the proportions are assigned to the tracks
    for track in root.findall('track'):
        trackId = int(track.find('id').text)
        proportion = decimal.Decimal(track.find('proportion').text)
        foundTrack = ciclovia.getTrack(trackId)   
        foundTrack.arrivalProportion = proportion      
        
    participantsSet = []
    
      
    #In this part, all the tracks are built and they are added to the trackSet
    for participant in root.findall('participantType'):
        activityPart = participant.find('activity').text
        velocityPart = decimal.Decimal(participant.find('velocity').text)
        percentagePart = decimal.Decimal(participant.find('percentage').text)    
        typeParticipant = ParticipantTypeObj(activityPart, velocityPart, percentagePart)
        participantsSet.append(typeParticipant)
    ciclovia.typeParticipants = participantsSet  
    
    #This is the list that contains the proportion of arrivals pero hour of a Ciclovia
    timeInSystemSet = []
    
    #In this part, all the tracks are built and they are added to the trackSet
    for timeSystem in root.findall('timeInSystem'):
        for group in timeSystem.findall('group'):
            time = int(group.find('time').text)
            percentage = decimal.Decimal(group.find('percentage').text)
            timeDistribution = [time, percentage]      
            timeInSystemSet.append(timeDistribution)
        ciclovia.timeInSystemDistribution = timeInSystemSet        
    
    
                       
#This definition prints a XML file with the structure of a Ciclovia defined in an experiment                   
def printExperiment(ciclovia):
    rootCiclovia = ET.Element('ciclovia')
       
    childName = ET.SubElement(rootCiclovia, 'name')
    childName.text = ciclovia.name
    
    childPlace = ET.SubElement(rootCiclovia, 'place')
    childPlace.text = ciclovia.place    

    childStartHour = ET.SubElement(rootCiclovia, 'startHour')
    childStartHour.text = str(ciclovia.startHour)  
    
    childEndHour = ET.SubElement(rootCiclovia, 'endHour')
    childEndHour.text = str(ciclovia.endHour)    
    
    childNumTracks = ET.SubElement(rootCiclovia, 'numTracks')
    childNumTracks.text = str(ciclovia.numTracks)
    
    for track in ciclovia.tracks:
        childTrack = ET.SubElement(rootCiclovia, 'track')
        childTrackId = ET.SubElement(childTrack, 'id')
        childTrackId.text = str(track.idNum)
        childTrackDistance = ET.SubElement(childTrack, 'distance')
        childTrackDistance.text = str(track.distance)     
        childTrackProbability = ET.SubElement(childTrack, 'probability')
        childTrackProbability.text = str(track.probability) 
        #Modified probabilities
        childTrackProbabilityBegin = ET.SubElement(childTrack, 'probabilityBegin')
        childTrackProbabilityBegin.text = str(track.probabilityBegin)    
        childTrackProbabilityEnd = ET.SubElement(childTrack, 'probabilityEnd')
        childTrackProbabilityEnd.text = str(track.probabilityEnd)         
        for index, neighboor in enumerate(track.tracksId):
            childTrackNeighboor = ET.SubElement(childTrack, 'neighboor')
            childTrackNeighboorId = ET.SubElement(childTrackNeighboor, 'id')
            childTrackNeighboorId.text = str(neighboor)
            childTrackNeighboorProb = ET.SubElement(childTrackNeighboor, 'probability')
            childTrackNeighboorProb.text = str(track.tracksProb[index])
    print printOrganizedXML(rootCiclovia)    
    tree = ET.ElementTree(rootCiclovia)
    tree.write("CicloviaExperiment.xml")

#This definitions builds a Ciclovia from the database, given its name and place
def loadCiclovia(cicloviaId):
   
    #query_cicloviaFromDB = Ciclovia.objects.filter(place=placeC)
    #for ciclovia in query_cicloviaFromDB:
    ciclovia = Ciclovia.objects.get(id=cicloviaId)
    name = str(ciclovia.name)
    place = str(ciclovia.place)
    startHour = ciclovia.start_hour
    endHour = ciclovia.end_hour
    numTracks = ciclovia.num_tracks
    tracks = []
    loadedCiclovia = CicloviaObj(name, place, startHour, endHour, numTracks, tracks)
    print(loadedCiclovia.printInfo())
    query_tracksFromDB = ciclovia.track_set.all()
    for track in query_tracksFromDB:
        idTrack = track.id_track
        distance = track.distance
        probability = track.probability
        #Modified probabilities
        probabilityBegin = track.probabilityBegin
        probabilityEnd = track.probabilityEnd
        tracksId = []
        tracksProb = []
        tracksDir = []
        loadedTrack = TrackObj(idTrack, distance, probability, probabilityBegin, probabilityEnd, tracksId, tracksProb, tracksDir)
        loadedCiclovia.tracks.append(loadedTrack)
    print(loadedCiclovia.printInfo())
        
    #If arrivals are already loaded, I have to load all the information to the Ciclovia
    if(ciclovia.arrivals_loaded==True):
        print("Tengo que cargar toda la info del a Ciclovia")
        loadedCiclovia.referenceTrack = ciclovia.reference_track
        loadedCiclovia.referenceHour = ciclovia.reference_hour
        loadedCiclovia.referenceArrivalRate = ciclovia.reference_arrival_rate
            
        query_timeInSystemFromDB = ciclovia.timeinsystemdistribution_set.all()
        timeDistributionList = []
        for timeDistribution in query_timeInSystemFromDB:
            time = timeDistribution.time
            percentage = timeDistribution.percentage  
            timeDist = [time, percentage]  
            timeDistributionList.append(timeDist)
        loadedCiclovia.timeInSystemDistribution = timeDistributionList
                
        query_arrivalsProportionHourFromDB = ciclovia.arrivalsproportionperhour_set.all()
        arrivalsHourList = []
        for arrivalProportion in query_arrivalsProportionHourFromDB:
            hour = arrivalProportion.hour
            proportion = arrivalProportion.proportion 
            arrivalProp = [hour, proportion]
            arrivalsHourList.append(arrivalProp)             
        loadedCiclovia.arrivalProportionPerHour =  arrivalsHourList
                
        query_participantTypeFromDB = ciclovia.participanttype_set.all()
        participantsList = []
        for typeParticipant in query_participantTypeFromDB:
            activity = str(typeParticipant.activity)
            velocity = typeParticipant.velocity
            percentage = typeParticipant.percentage
            loadedPartType = ParticipantTypeObj(activity, velocity, percentage)                                                  
            participantsList.append(loadedPartType)   
        loadedCiclovia.typeParticipants = participantsList   
        
        query_tracksFromDB = ciclovia.track_set.all()
        tracksUpdated = []
        for track in query_tracksFromDB:
            idTrack = track.id_track
            distance = track.distance
            probability = track.probability
            #Modified probability
            probabilityBegin = track.probabilityBegin
            probabilityEnd = track.probabilityEnd
            arrivalProportion = track.arrival_proportion
            tracksId = []
            tracksProb = []
            tracksDir = []
            query_tracksIdProb = track.neighboorinfo_set.all()
            for neighboor in  query_tracksIdProb:
                tracksId.append(neighboor.neighboorId)
                tracksProb.append(neighboor.probability)   
                tracksDir.append(neighboor.direction)
            loadedTrack = TrackObj(idTrack, distance, probability, probabilityBegin, probabilityEnd, tracksId, tracksProb, tracksDir)
            loadedTrack.arrivalProportion = arrivalProportion
            tracksUpdated.append(loadedTrack)
        loadedCiclovia.tracks = tracksUpdated                
        loadedCiclovia.assignArrivalsToTrack
        
        for track in loadedCiclovia.tracks:
            arrivalSet = []
            for arrivalAtHour in loadedCiclovia.arrivalProportionPerHour:                 
                arrivalRate = decimal.Decimal(arrivalAtHour[1])*decimal.Decimal(track.arrivalProportion)*decimal.Decimal(loadedCiclovia.referenceArrivalRate)
                arrivalSet.append(arrivalRate)
                loadedCiclovia.maxArrivals+=arrivalRate
                track.arrivalsPerHour = arrivalSet        
        
        print(loadedCiclovia.printInfo())        
            
                        
        return loadedCiclovia
      

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   SIMULACION USANDO SIMPY
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
   
#This class represents the Discrete Event Simulation
class SimulationDES:
    
    #This is the constructor of the class SimulationDES
    #It takes the parameters provided as arguments and stores them in the object
    def __init__(self, random_seed, cicloviaId):       
        self.random_seed = random_seed
        self.ciclovia = loadCiclovia(cicloviaId) 
        self.simTime = (self.ciclovia.endHour - self.ciclovia.startHour)*60
        self.env = simpy.Environment()
        self.numberInCiclovia = 0
        self.totalArrivals = 0
        self.listNumberInSystem = []
        self.listTimeInSystem = []        
        self.results = []
        self.ciclovia.printInfo()
  
    #This class allows the execution of the simulation
    def execute(self, cicloviaId):
        #print("Voy a correr la simulacion") 
        random.seed(self.random_seed)     
        self.env.run(until=self.simTime)
        print("Ejecuto")
        self.printResults(cicloviaId)
    
    #This methods represents the participant as an object
    #ACAAAAAAAA SE PODRIAN QUITAR PARAMETROS
    '''
    def participant(self, partArriving, track, idNum, participantType, arrivalTime, timeInSystem):
        #print('%s entering in Ciclovia at %s by the track %s' % (idNum, self.env.now, track.idNum))        
        #print('%s entering in Ciclovia with time %s' % (idNum, timeInSystem))   
        
        for event in partArriving.eventsList:
            eventType = partArriving 
            yield self.env.timeout(decimal.Decimal(event[3]))
            if(event[0]==0):  
                print("Entro a actualizar con: " + str(idNum))
                print("Actual " +  str(event[1].idNum) + ":"  + str(event[1].numberInTrack))    
                print("Siguiente " +  str(event[2].idNum) + ":"  + str(event[2].numberInTrack))    
                event[1].numberInTrack -= decimal.Decimal(1)
                event[1].updateNumberInTrack(self.env.now)
                event[2].numberInTrack += decimal.Decimal(1)
                event[2].updateNumberInTrack(self.env.now)
                print("Actual " +  str(event[1].idNum) + ":"  + str(event[1].numberInTrack))    
                print("Siguiente " +  str(event[2].idNum) + ":"  + str(event[2].numberInTrack)) 
                print("Salgo de actualizar con: " + str(idNum))
                #print('%s moving in Ciclovia at %s' % (idNum, self.env.now))
            if(event[0]==-1):                
                self.numberInCiclovia -= decimal.Decimal(1)
                event[1].numberInTrack -= decimal.Decimal(1)
                event[1].updateNumberInTrack(self.env.now)
                self.numberInSystemStatistic()                   
                #print('%s leaving Ciclovia at %s' % (idNum, self.env.now))
                
            #revisar
        
        # Simulate spending time in the Ciclovia
        #yield self.env.timeout(decimal.Decimal(timeInSystem))
        #self.numberInCiclovia -= decimal.Decimal(1)
        #self.numberInSystemStatistic()        
        #print('%s leaving the Ciclovia at %s' % (idNum, self.env.now))    
    '''       
                    
    #This methods represents the participant as an object and the associated events
    def participant(self, partArriving, track, idNum, participantType, arrivalTime, timeInSystem):
        #print('%s entering in Ciclovia at %s by the track %s' % (idNum, self.env.now, track))
        #print('%s entering in Ciclovia with time %s' % (idNum, timeInSystem))   
        
        # Simulate spending time in the Ciclovia
        yield self.env.timeout(decimal.Decimal(timeInSystem))
        self.numberInCiclovia -= decimal.Decimal(1)
        self.numberInSystemStatistic()        
        #print('%s leaving the Ciclovia at %s' % (idNum, self.env.now))    
    
        
    #This method defines the arrival behavior and creates the participants until the sim time reaches simTime
    def participantArrivals(self):     
        #print("Va a crear participantes")
       
        participantList = []
        
        #This section creates the values to the time in system
        durationValues = []
        durationProbabilities = []
        
        print("Tam : ")  
        print(len(self.ciclovia.timeInSystemDistribution))
             
        for timeSystem in self.ciclovia.timeInSystemDistribution:
            durationValues.append(float(timeSystem[0]))
            durationProbabilities.append(float(timeSystem[1]))        
        durationValuesArray = numpy.array(durationValues, dtype=numpy.dtype(numpy.float64))        
        durationProbabilitiesArray = numpy.array(durationProbabilities, dtype=numpy.dtype(numpy.float64))       
        timeParticipantsSystem = self.weightedValues(durationValuesArray, durationProbabilitiesArray, (self.ciclovia.maxArrivals*2))
        print("llegoooo")
        
      
       
        #This section creates the values associated with the participant type
   
        typeValues = []
        typeProbabilities = []
        index = 0
        for typePart in self.ciclovia.typeParticipants:
            typeValues.append(index)
            typeProbabilities.append(float(typePart.percentage))
            index+=1
        typeValuesArray = numpy.array(typeValues, dtype=numpy.dtype(numpy.float64))
        typeProbabilitiesArray = numpy.array(typeProbabilities, dtype=numpy.dtype(numpy.float64))
        typeParticipantsSystem = self.weightedValues(typeValuesArray, typeProbabilitiesArray, (self.ciclovia.maxArrivals*2))
        
        i = 0
        j = 0   
        noEnter = 0
        for track in self.ciclovia.tracks:
            initialTime = 0 
            indexHour = 0
            
            for indexHour, hour in enumerate(track.arrivalsPerHour):
                j+=1                
                #print("Deben llegar " + str(hour) + "a la hora %d"  % j)
                lastArrival = initialTime
                #print("Index es" + str(indexHour))
                #print("Last arrival es " + str(lastArrival))
                while(lastArrival<((indexHour+1)*60)):   
                    #print("Entro al while!")                                                      
                    #trackNum = track.idNum
                    #Modified here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #Add +1 to hour: time =...(/hour+1 ) double check
                    time = -math.log(1.0 - random.random())*float(60/(hour))    
                    #print("Tiempo expo: " + str(time))
                    arrivalTime = decimal.Decimal(time) + decimal.Decimal(lastArrival)               
                    lastArrival = arrivalTime 
                    if(lastArrival>(indexHour+1)*60):
                        noEnter+=1
                    if(lastArrival<(indexHour+1)*60):
                        i+=1
                        #print("last arrival es " + str(lastArrival))
                        #print("El valor de i es: " + str(i))
                        #print("Lenght " + str(len(timeParticipantsSystem)))
                        timeParticipantSystem =  timeParticipantsSystem[i]   
                        #print("Itero en el while")
                        typeOfParticipant = self.ciclovia.typeParticipants[int(typeParticipantsSystem[i])]
                        part = ParticipantObjSim(self.ciclovia, track, "begin", i, typeOfParticipant, arrivalTime, timeParticipantSystem) 
                        
                        #part.assignRoute()
                        #Imprimo la primera entidad que entra
                        if(i == 100):
                            print("El trayecto por el que entra es: " + str(track.idNum))
                            #print("Entro a imprimir lista de eventos")
                            #print("Evento 1" +" tracks " + str(part.arrivalTrack.idNum))
                            #for event in part.eventsList:
                                #print("Evento " + str(event[0]) +" tracks " + str(event[1].idNum) + ":" + str(event[2].idNum))
                            #print("Entro a imprimir lista de eventos")
                            
                        participantList.append(part)          
                        self.timeInSystemStatistic(timeParticipantSystem)   
                        
                    
                #print("Salgo en el while")
                initialTime+=60
            j=0

        self.calculateValuesTimeInSystemStatistic()
        self.totalArrivals = len(participantList)
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO entraron " + str(noEnter))
        #First I must order the arrivals according to the arrivalTime
        participantListSorted = sorted(participantList, key=attrgetter('arrivalTime'))        
        #print("Arribos totales" + str(len(participantListSorted)))
        #for index, partArriving in enumerate(participantListSorted ):   
            #print("La hora es" + str(partArriving.arrivalTime))
                          
        for index, partArriving in enumerate(participantListSorted):
            part = self.participant(partArriving, partArriving.track, partArriving.idNum, partArriving.participantType, partArriving.arrivalTime, partArriving.timeInSystem)         
            if(index == 0):
                yield self.env.timeout(partArriving.arrivalTime)
            else:             
                yield self.env.timeout(partArriving.arrivalTime - participantListSorted[index-1].arrivalTime)  
            self.numberInCiclovia +=decimal.Decimal(1)
            #print("Con " + str(partArriving.idNum) +"Voy a agregar uno al numero en trayecto " + str(partArriving.arrivalTrack.idNum) + " y ahora es "  + str(partArriving.arrivalTrack.numberInTrack))
            partArriving.arrivalTrack.numberInTrack += decimal.Decimal(1)  
            #print("Con " + str(partArriving.idNum) + "Agrego uno al numero en trayecto " + str(partArriving.arrivalTrack.idNum) + " y ahora es "  + str(partArriving.arrivalTrack.numberInTrack))
            partArriving.arrivalTrack.updateNumberInTrack(self.env.now)            
            self.numberInSystemStatistic()           
            self.env.process(part)
                  
    #This definition generates a stream of values from a discrete probability distribution
    def weightedValues(self, values, probabilities, size):   
        print("size es" + str(size))
        bins = numpy.cumsum(probabilities)
        bins[len(bins)-1] = 1.0 
        print("Parametros")
        x = numpy.random.random_sample(size)
        for value in x:
            if(value > bins[len(bins)-1]):
                print("Es mayor: " + str(value))
        
        print(bins)
        return values[numpy.digitize(x, bins)]     
    
    #This definition accumulates the current number in system
    def numberInSystemStatistic(self):
        size = len(self.listNumberInSystem)
        if(size == 0):
            info = [self.numberInCiclovia, self.env.now]
            self.listNumberInSystem.append(info)
        else:
            newInfo = [self.numberInCiclovia, (self.env.now-self.listNumberInSystem[size-1][1])]
            self.listNumberInSystem.append(newInfo)     
            
          
        #if(self.env.now % 20 < 3):
            #print("En el tiempo" + str(self.env.now) + "hay un total de " + str(self.numberInCiclovia))
        #print(str(self.env.now) + "," + str(self.numberInCiclovia))
         
    def timeInSystemStatistic(self, timeInSystem):             
        self.listTimeInSystem.append(timeInSystem)
    
    def calculateValuesTimeInSystemStatistic(self):    
        print('Average time in system:', numpy.mean(self.listTimeInSystem))
        print('Standard deviation:', numpy.std(self.listTimeInSystem)) 
    
    def printResults(self, cicloviaId):
        cicloviaFromDB = Ciclovia.objects.get(id=cicloviaId)               
        simTime = self.simTime
        totalArrivals = self.totalArrivals
        averageTime = numpy.mean(self.listTimeInSystem)
        standardDevTime = numpy.std(self.listTimeInSystem)
        #numberInSystem = []
        #for value in self.listNumberInSystem:
            #if(value[1] % 20 < 3):
                #numberInSystem.append(value)
        listNumberInCiclovia = []
        listTimeNumberInCiclovia = []
        for value in self.listNumberInSystem:
            listNumberInCiclovia.append(float(value[0]))
            listTimeNumberInCiclovia.append(float(value[1]))            
            
        avgNumberSystem = numpy.average(listNumberInCiclovia, weights=listTimeNumberInCiclovia) 
        #avgNumberSystem = numpy.mean(self.listNumberInSystem) 
        results = [simTime, totalArrivals, averageTime, standardDevTime, listNumberInCiclovia]
        self.results = results
        resultsDB = cicloviaFromDB.simulationresults_set.create(sim_time = self.simTime, date=timezone.now(), total_arrivals=self.totalArrivals, average_time=round(averageTime, 3), standard_deviation_time=round(standardDevTime, 3), average_number_system= round(avgNumberSystem,3))
        resultsDB.save()                                        
        #print str(self.results)
        for track in self.ciclovia.tracks:
            #print("Entro a iterar en el track " + str(track.idNum) +" y el tamano de su lista es " + str(len(track.numParticipantsInTrack)))
            listNumberInTrack = []
            listTimeNumberInTrack = []            
            for value in track.numParticipantsInTrack:
                listNumberInTrack.append(float(value[0]))
                listTimeNumberInTrack.append(float(value[1]))
            #print(str(listNumberInTrack))
            #print(str(listTimeNumberInTrack))
            avgNumberInTrack = round(numpy.average(listNumberInTrack, weights=listTimeNumberInTrack),3)        
            print("El numero promedio en el trayecto " + str(track.idNum) + " es " + str(avgNumberInTrack))
            
                       

#This class represents an entity 
class ParticipantObjSim:        

    #This is the constructor of the class ParticipantObjSim
    #It takes the parameters provided as arguments and stores them in the object        
    def __init__(self, ciclovia, track, direction, idNum, participantType, arrivalTime, timeInSystem):
        self.ciclovia = ciclovia
        self.arrivalTrack = track
        self.track = track
        self.direction = direction
        self.idNum = idNum
        self.participantType = participantType
        self.arrivalTime = arrivalTime
        self.timeInSystem = timeInSystem 
        self.timeLeftInSystem = timeInSystem
        self.currentTime = arrivalTime
        self.eventsList = []
        
            
    #This methos assigns the route
    def assignRoute(self):
        #Arrival
        event = [1, self.track, self.track, self.arrivalTime]
        #self.eventsList.append(event)
        print("Ejecutando para la entidad " + str(self.idNum))
        #print("Entro por " + str(self.track.idNum))
        while(self.timeLeftInSystem>0):
            distance = self.track.distance
            #print("Distancia " + str(distance) + " velocidad" + str(self.participantType.velocity))
            timeForTrack = distance/(self.participantType.velocity)
            if(timeForTrack>self.timeLeftInSystem):
                #print("La entidad " + str(self.idNum) + " sale de la Ciclovia" )
                #leavingTime = self.currentTime + self.timeLeftInSystem
                leavingTime = self.timeLeftInSystem
                self.timeLeftInSystem = 0
                #Leaving system = -1
                event = [-1, self.track, self.track, leavingTime]
                #print("Info trayectos saliendo  " + str(self.track.idNum))
                #print("El trayecto es "+ str(self.track.idNum))
                self.eventsList.append(event)
                #sortedList = sorted(self.eventsList, key=itemgetter(3))
                #self.eventsList = sortedList
                #print("Lista de eventos " + str(self.eventsList))
            else:
                #Info neighboor gives me an array with the nextTrack and with the direction
                #print("La entidad " + str(self.idNum) + " se esta moviendo en la Ciclovia" )            
                nextTrackId = self.track.giveNeighboorInDirection(self.direction)  
                #print("Voy a buscar al trayecto " + str(nextTrackId) + " con el id " + str(self.idNum) + " y el tiempo " + str(self.timeLeftInSystem))
                nextTrack = self.ciclovia.getTrack(nextTrackId)
                #print("El trayecto siguiente es "+ str(nextTrack))
            
                if(self.direction == "begin" and nextTrackId == self.track.idNum):
                    self.direction = "end"
                    #print("Entre al if con begin")
                if(self.direction == "end" and nextTrackId == self.track.idNum):
                    self.direction = "begin"    
                    #print("Entre al if con end")
            
                #movingTime = self.currentTime + timeForTrack
                movingTime = timeForTrack
                self.currentTime = movingTime
                self.timeLeftInSystem -= timeForTrack
                #print("Mi nuevo tiempo es  " + str(self.timeLeftInSystem) + " y el tiempo en el trayecto es" + str(timeForTrack))
                #Moving from ciclovia = 0
                #REVISAR ESTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
                event = [0, self.track, nextTrack, movingTime]
                #print("Info trayectos moviendome  " + str(self.track.idNum) + " " + str(nextTrack.idNum))
                self.track = nextTrack
                self.eventsList.append(event)
                #self.assignRoute()
    
     
      
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   EJECUCION DE LA APLICACION
#----------------------------------------------------------------------------------------------------------------------------------------------------------------      

#This method executes the simulation
def simulationExecution(cicloviaId):
    
    start = timeit.default_timer()    
         
    seed = 9243881
    for i in range(1):
        simDES = SimulationDES(seed, cicloviaId)
        simDES.env.process(simDES.participantArrivals())
        simDES.execute(cicloviaId)
        seed*=2
        seed+=i
        #simDES.printResults(cicloviaId)
        
    stop = timeit.default_timer()
    time = stop - start
    print("El tiempo de ejecucion es " + str(time))
    

#print(random.expovariate(float(1/7)))
print(-math.log(1.0 - random.random())*7)
      
#EJECUCION

#exampleCiclovia = buildCiclovia('Formato Ciclovia.xml')
#assignArrivalInfoNoDB(exampleCiclovia, 'Formato Arribos Ciclovia.xml')
#exampleCiclovia.assignArrivalsToTrack()
#exampleCiclovia.printInfo()
#simDES = SimulationDES(42, exampleCiclovia)
#simDES.env.process(simDES.participantArrivals())
#simDES.execute()
#simDES.printResults()
#simDES.numberInUntilTime(60)

#exampleCiclovia.printInfo()
#loadCiclovia("Bogota")
#addTracks('Formato Ciclovia Agregar.xml', exampleCiclovia)
#exampleCiclovia.printInfo()
#removeTracks('Formato Ciclovia Eliminar.xml', exampleCiclovia)
#exampleCiclovia.printInfo()
#printExperiment(exampleCiclovia)


