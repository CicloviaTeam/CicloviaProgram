# coding=utf-8
import xml.etree.ElementTree as ET
import decimal
import random
import math
from operator import attrgetter
import timeit
import traceback

from scipy.stats import norm
import simpy
import numpy
from django.utils import timezone
import matplotlib.pyplot as plt
import threading
import time as timeLib

from PrintXML import printOrganizedXML
from CicloviaProgram.models import Ciclovia, Track, SimulationResultsCompiled


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
        self.probabilityBegin = probabilityBegin
        self.probabilityEnd = probabilityEnd
        self.tracksId = tracksId
        self.tracksProb = tracksProb
        self.tracksDirection = tracksDirection
        self.arrivalProportion = 0
        self.arrivalsPerHour = []
        self.numberInTrack = 0
        self.numParticipantsInTrack = []
        self.flowInTrack = []
        self.totalArrivals = 0
        #todo Aqui se ponen los nuevos parametros del track
        self.number_of_semaphores = 0
        self.hasSlope = 0
        self.quality_of_track = 0


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

    #This method gives a neighboor of a track, in a specific direction
    def giveNeighboorInDirection(self, direction):
        probabilities = []
        ids = []
        if(direction == "begin"):
            probabilities.append(self.probabilityBegin)
        else:
            probabilities.append(self.probabilityEnd)

        ids.append(self.idNum)
        for index, direct in enumerate(self.tracksDirection):
            if(direct[1] == direction):
                probabilities.append(self.tracksProb[index])
                ids.append(self.tracksId[index])
        if(len(ids)==1):
            return [self.idNum, direction]

        probabilitiesArray = numpy.array(probabilities, dtype=numpy.dtype(numpy.float64))
        idsArray = numpy.array(ids, dtype=numpy.dtype(numpy.float64))

        bins = numpy.cumsum(probabilitiesArray)
        sample = numpy.random.random_sample(1)
        listProbabilities = idsArray[numpy.digitize(sample, bins)]



        if listProbabilities[0]==self.idNum:
            return [listProbabilities[0],direction]
        enterTo = "begin"
        for index, neighboor  in enumerate(self.tracksId):
            if listProbabilities[0] == neighboor:
                direction = self.tracksDirection[index]
                enterTo =direction[0]
        #OJO ACA
        neighboorIdDir = [listProbabilities[0],enterTo]

        return neighboorIdDir


    #This method updates the number of participants in a track
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

    #This method updates the flow of participants in a track
    def updateFlowInTrack(self, time):

        #Changed 60 to 30
        timeInterval = math.floor(time/30)
        self.flowInTrack[int(timeInterval)] += 1


#This class represents a type of participant
class ParticipantTypeObj:

    #This is the constructor of the class Ciclovia
    #It takes the parameters provided as arguments and stores them in the object
    def __init__(self, activity, velocity, percentage):
        self.activity = activity
        self.velocity = velocity
        self.percentage = percentage

    #This method prints the basic information of the Ciclovia
    def printInfo(self):
        print(self.activity, self.velocity, self.percentage)


#This class represents a the simulation information
class SimulationObj:

    #This is the constructor of the class Simulation
    #It takes the parameters provided as arguments and stores them in the object
    def __init__(self, replications, arrivalsProbabilityDistribution):
        self.replications = replications
        self.arrivalsProbabilityDistribution = arrivalsProbabilityDistribution

    #This method prints the basic information of the Simulation parameters
    def printInfo(self):
        print(self.replications, self.arrivalsProbabilityDistribution)



#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   DEFINICIONES PARA CREAR Y MODIFICAR LA CICLOVIA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

#This definition reads a data file and build the Ciclovia model
def buildCiclovia(filename, pUser):
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
            #Track probability se deberia quitar
            trackProbability =  0

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
                #Modified to give From and To
                neighboorsFromDirec= neighboor.find('from').text
                neighboorsFromToDirec = [neighboorsFromDirec, neighboorsDirec]

                neighboorsDirection.append(neighboorsFromToDirec)
                sumProb+= neighboorProb
            if sumProb != 1.0:
                print("Error la suma de probabilidades no es 1")

            newTrack = TrackObj(trackId, trackDistance, trackProbability,
                                trackProbabilityBegin, trackProbabilityEnd,
                                neighboorsIds, neighboorsProbs,
                                neighboorsDirection)
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
            #print("Como es un modelo, voy a guardar la info en la base de datos")
            cicloviaDB = Ciclovia(user=pUser, name=ciclovia.name, place=ciclovia.place, start_hour = ciclovia.startHour, end_hour = ciclovia.endHour, num_tracks = ciclovia.numTracks)
            cicloviaDB.save()
            #print("ID de la Ciclovia en la base de datos")
            #print(cicloviaDB.id)
            for track in ciclovia.tracks:
                #Modified probabilities
                trackDB = cicloviaDB.track_set.create(id_track=track.idNum, distance=track.distance, probability=track.probability, probabilityBegin=track.probabilityBegin, probabilityEnd=track.probabilityEnd)
                trackDB.save()
                #print("ID del trayecto en la base de datos")
                #print(trackDB.id)
                for index, neighboor in enumerate(track.tracksId):
                    #print("Entro a los trayectos")
                    directionsFromTo = track.tracksDirection[index]
                    neighboorDB = trackDB.neighboorinfo_set.create(neighboorId=neighboor, probability=track.tracksProb[index], direction=directionsFromTo[1], fromDirection=directionsFromTo[0])
                    neighboorDB.save()
                    #print("Vecino")
                    #print(neighboorDB)
        return ciclovia
    except:
        print ("Ocurrio un error")

#This definition reads a data file and build the Ciclovia model
def buildCicloviaFromJson(json_data, pUser):
    try:

        #In this part, the Ciclovia is created given a XML file
        # tree = ET.ElementTree(file=filename)
        #The root of the XML is taken
        # root = tree.getroot()
        #This is the list that contains all the tracks of a Ciclovia
        trackSet = []
        #This is the type of XML (model or experiment)
        typeCiclovia = json_data['type']

        #In this part, all the tracks are built and they are added to the trackSet
        for track in json_data['track']:
            trackId = int(track['id'])
            trackDistance = int(track['distance'])
            #Track probability se deberia quitar
            trackProbability =  0

            #Modified probabilities
            trackProbabilityBegin =  decimal.Decimal(track['probabilityBegin'])
            trackProbabilityEnd =  decimal.Decimal(track['probabilityEnd'])
            neighboorsIds = []
            neighboorsProbs = []
            neighboorsDirection = []
            #Direction = if begin = 0, if end 1
            sumProb = trackProbability

            for neighboor in track['neighboor']:
                if neighboor['id'] != '':
                    neighboorId = int(neighboor['id'])
                    neighboorsIds.append(neighboorId)
                    neighboorProb= decimal.Decimal(neighboor['probability'])
                    neighboorsProbs.append(neighboorProb)
                    neighboorsDirec= neighboor['direction']
                    #Modified to give From and To
                    neighboorsFromDirec= neighboor['from']
                    neighboorsFromToDirec = [neighboorsFromDirec, neighboorsDirec]

                    neighboorsDirection.append(neighboorsFromToDirec)
                    sumProb+= neighboorProb
            if sumProb != 1.0:
                print("Error la suma de probabilidades no es 1")

            newTrack = TrackObj(trackId, trackDistance, trackProbability,
                                trackProbabilityBegin, trackProbabilityEnd,
                                neighboorsIds, neighboorsProbs,
                                neighboorsDirection)
            trackSet.append(newTrack)

        #In this part all the attributes of a Ciclovia are assigned
        name = json_data['name']
        place = json_data['place']
        startHour = decimal.Decimal(json_data['startHour'])
        if startHour > 24 :
            print("Error: se ha excedido el maximo de horas en un dia (24)")
        endHour = decimal.Decimal(json_data['endHour'])
        if endHour > 24 :
                print("Error: se ha excedido el maximo de horas en un dia (24)")
        numTracks = int(json_data['numTracks'])
        if numTracks > 30 :
                print("Error: se ha excedido el maximo numero de trayectos (30)")
        ciclovia = CicloviaObj(name, place, startHour, endHour, numTracks, trackSet)


        #Only loads info in database if it is a model (no an experiment)
        #OJO: CAMBIAR A MODEL en lugar de MODELC
        if(typeCiclovia=="model"):
            #print("Como es un modelo, voy a guardar la info en la base de datos")
            cicloviaDB = Ciclovia(user=pUser, name=ciclovia.name, place=ciclovia.place, start_hour = ciclovia.startHour, end_hour = ciclovia.endHour, num_tracks = ciclovia.numTracks)
            cicloviaDB.save()
            #print("ID de la Ciclovia en la base de datos")
            #print(cicloviaDB.id)
            for track in ciclovia.tracks:
                #Modified probabilities
                trackDB = cicloviaDB.track_set.create(id_track=track.idNum, distance=track.distance, probability=track.probability, probabilityBegin=track.probabilityBegin, probabilityEnd=track.probabilityEnd)
                trackDB.save()
                #print("ID del trayecto en la base de datos")
                #print(trackDB.id)
                for index, neighboor in enumerate(track.tracksId):
                    #print("Entro a los trayectos")
                    directionsFromTo = track.tracksDirection[index]
                    neighboorDB = trackDB.neighboorinfo_set.create(neighboorId=neighboor, probability=track.tracksProb[index], direction=directionsFromTo[1], fromDirection=directionsFromTo[0])
                    neighboorDB.save()
                    #print("Vecino")
                    #print(neighboorDB)
        return ciclovia
    except:
        traceback.print_exc()
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
            neighboorsDirec= neighboor.find('direction').text
            #Modified to give From and To
            neighboorsFromDirec= neighboor.find('from').text
            neighboorsFromToDirec = [neighboorsFromDirec, neighboorsDirec]

            neighboorsDirection.append(neighboorsFromToDirec)
            for neighboorTrack in ciclovia.tracks:
                found= False
                if(neighboorTrack.idNum == neighboorId and found!=True):
                    neighboorTrack.tracksId.append(trackId);
                    neighboorTrack.tracksProb.append(neighboorToTrackProb);
                    found=True
                    #print("Se agrego la prob del nuevo trayecto al vecino")
            sumProb+= neighboorProb
        if sumProb != 1.0:
            print("Error la suma de probabilidades no es 1")

        newTrack = TrackObj(trackId, trackDistance, trackProbability, trackProbabilityBegin, trackProbabilityEnd, neighboorsIds, neighboorsProbs, neighboorsDirection)

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
                #print("Se elimino el trayecto")
            else:
                for index, elem in enumerate(track.tracksId):
                    if(elem==trackId):
                        track.tracksId.pop(index)
                        track.tracksProb.pop(index)
                        #print ("Se elimino la prob en el trayecto vecino")


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
            childTrackNeighboorDirect = ET.SubElement(childTrackNeighboor, 'direction')
            childTrackNeighboorProb.text = str(track.tracksDirection[1,index])
            childTrackNeighboorDirect = ET.SubElement(childTrackNeighboor, 'from')
            childTrackNeighboorProb.text = str(track.tracksDirection[0,index])
    print printOrganizedXML(rootCiclovia)
    tree = ET.ElementTree(rootCiclovia)
    tree.write("CicloviaExperiment.xml")

#This definitions builds a Ciclovia from the database, given its name and place
def loadCiclovia(cicloviaId):

    #query_cicloviaFromDB = Ciclovia.objects.filter(place=placeC)
    #for ciclovia in query_cicloviaFromDB:
    ciclovia = Ciclovia.objects.get(id=cicloviaId)
    name = str(ciclovia.name.encode('utf-8'))
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
                tracksDir.append([neighboor.fromDirection,neighboor.direction])
            loadedTrack = TrackObj(idTrack, distance, probability, probabilityBegin, probabilityEnd, tracksId, tracksProb, tracksDir)
            print("REVISOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO LOADTRACK")
            print(str(loadedTrack))
            loadedTrack.arrivalProportion = arrivalProportion
            tracksUpdated.append(loadedTrack)
        loadedCiclovia.tracks = tracksUpdated
        print("Voy a asignar los arribos")
        #Esto no esta haciendo nada
        loadedCiclovia.assignArrivalsToTrack

        for track in loadedCiclovia.tracks:
            arrivalSet = []
            for arrivalAtHour in loadedCiclovia.arrivalProportionPerHour:
                arrivalRate = decimal.Decimal(arrivalAtHour[1])*decimal.Decimal(track.arrivalProportion)*decimal.Decimal(loadedCiclovia.referenceArrivalRate)*decimal.Decimal(track.distance)/900
                # print("Para el trayecto " + str(track.idNum) + " en la hora " + str(arrivalAtHour) + " la tasa es " + str(arrivalRate))
                # print("Se esta multiplicando " + str(arrivalAtHour[1]) + "*" + str(track.arrivalProportion) + "*" + str(loadedCiclovia.referenceArrivalRate))
                arrivalSet.append(arrivalRate)
                loadedCiclovia.maxArrivals+=arrivalRate
                track.arrivalsPerHour = arrivalSet

        print(loadedCiclovia.printInfo())


        return loadedCiclovia

def copyCiclovia(ciclovia_id, pName, pUser):
    """Crea una copia de la ciclovía dada por parámetro y la llama con el nombre
    dado por parámetro. Retorna la copia creada."""
    oldCiclovia = Ciclovia.objects.get(pk=ciclovia_id)
    newCiclovia = Ciclovia(user=pUser,name=pName,place=oldCiclovia.place,
        start_hour=oldCiclovia.start_hour,end_hour=oldCiclovia.end_hour,
        num_tracks=oldCiclovia.num_tracks,reference_track=oldCiclovia.reference_track,
        reference_hour=oldCiclovia.reference_hour,
        reference_arrival_rate=oldCiclovia.reference_arrival_rate,
        arrivals_loaded=oldCiclovia.arrivals_loaded)
    newCiclovia.save()
    for oldTrack in oldCiclovia.track_set.all():
        newTrack= Track(ciclovia=newCiclovia, id_track=oldTrack.id_track,
            distance=oldTrack.distance, probability=oldTrack.probability,
            probabilityBegin=oldTrack.probabilityBegin,
            probabilityEnd=oldTrack.probabilityEnd,
            arrival_proportion=oldTrack.arrival_proportion,
            number_of_semaphores=oldTrack.number_of_semaphores,
            hasSlope=oldTrack.hasSlope,quality_of_track=oldTrack.quality_of_track)
        newTrack.save()
        for oldNeighboor in oldTrack.neighboorinfo_set.all():
            newTrack.neighboorinfo_set.create(
                neighboorId=oldNeighboor.neighboorId,
                probability=oldNeighboor.probability,
                direction=oldNeighboor.direction,
                fromDirection=oldNeighboor.fromDirection)
    for oldParticipantType in oldCiclovia.participanttype_set.all():
        newCiclovia.participanttype_set.create(activity=oldParticipantType.activity,
            velocity=oldParticipantType.velocity,percentage=oldParticipantType.percentage)
    for oldTimeInSystemDistribution in oldCiclovia.timeinsystemdistribution_set.all():
        newCiclovia.timeinsystemdistribution_set.create(time=oldTimeInSystemDistribution.time,
            percentage=oldTimeInSystemDistribution.percentage)
    for oldArrivalsProportionPerHour in oldCiclovia.arrivalsproportionperhour_set.all():
        newCiclovia.arrivalsproportionperhour_set.create(hour=oldArrivalsProportionPerHour.hour,
            proportion=oldArrivalsProportionPerHour.proportion)
    return newCiclovia

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   DEFINICIONES PARA COMPARAR LAS SIMULACIONES
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

class simulationComp:
    """Resultados de comparar las simulaciones"""
    def __init__(self, simulation1, simulation2):
        self.simulation1 = simulation1
        self.simulation2 = simulation2
        self.same_avg_total_arrivals = self.compareValues(simulation1.avg_total_arrivals,
            simulation1.hw_total_arrivals, simulation2.avg_total_arrivals,
            simulation2.hw_total_arrivals)
        self.same_average_number_system = self.compareValues(simulation1.average_number_system,
            simulation1.hw_number_system, simulation2.average_number_system,
            simulation2.hw_number_system)
        self.trackComparable = False
        self.trackComparisons = []
        self.compareTracks()

    @staticmethod
    def compareValues(val1, hw1, val2, hw2):
        """Compara los intervalos de confianza para determinar si son iguales estadísticamente"""
        if val1+hw1 <val2-hw2 or val2+hw2<val1-hw1:
            return False
        else:
            return True

    def compareTracks(self):
        """Determina si los trayectos son comparables y los compara."""
        track_set1 = self.simulation1.simulationresultscompiledpertrack_set.all()\
            .order_by('track')
        track_set2 = self.simulation2.simulationresultscompiledpertrack_set.all()\
            .order_by('track')
        self.trackComparable = True
        for track1 in track_set1:
            found = False
            for track2 in track_set2:
                if track1.track == track2.track:
                    found = True
                    self.trackComparisons.append(trackComparison(track1,track2))
            if not found:
                self.trackComparable = False
        if not len(track_set1)==len(track_set2):
            self.trackComparable = False

class trackComparison:
    """Guarda la información de la comparación de dos trayectos."""
    def __init__(self, track1, track2):
        self.track1 = track1
        self.track2 = track2
        self.comparisons = []
        self.makeComparisons()

    def makeComparisons(self):
        self.comparisons.append(simulationComp.compareValues(self.track1.average_number_track,
            self.track1.hw_number_track,self.track2.average_number_track,
            self.track2.hw_number_track))
        self.comparisons.append(simulationComp.compareValues(self.track1.average_total_arrivals,
            self.track1.hw_total_arrivals,self.track2.average_total_arrivals,
            self.track2.hw_total_arrivals))
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   SIMULACION USANDO SIMPY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# This class represents the Discrete Event Simulation
class SimulationDES:
    # This is the constructor of the class SimulationDES
    # It takes the parameters provided as arguments and stores them in the object
    def __init__(self, random_seed, cicloviaId, resultsCompiledId, isValidation):
        self.random_seed = random_seed
        self.ciclovia = loadCiclovia(cicloviaId)
        self.isValidation = isValidation
        #Change 60 to 30
        self.simTime = (self.ciclovia.endHour - self.ciclovia.startHour+1)*30
        self.env = simpy.Environment()
        self.numberInCiclovia = 0
        self.totalArrivals = 0
        self.listNumberInSystem = []
        self.listTimeInSystem = []
        self.results = []
        self.ciclovia.printInfo()

    # This class allows the execution of the simulation
    def execute(self, cicloviaId, resultsCompiledId):
        random.seed(self.random_seed)
        originalTime = timeit.default_timer()
        self.env.run(until=self.simTime)
        timeOfEnvRun = timeit.default_timer() - originalTime
        #todo se debe optimizar esta funcion!!!!!!
        self.printResults(cicloviaId, resultsCompiledId)
        timeOfPrinting = timeit.default_timer() - timeOfEnvRun
        print("Tiempo de correr Env.Run: " + str(timeOfEnvRun))
        print("Tiempo de imprimir: " + str(timeOfPrinting))

    # This method represents the participant as an object and handles the events of the participant
    # This method includes routing
    # ACAAAAAAAA SE PODRIAN QUITAR PARAMETROS
    def participant(self, partArriving, track, idNum, participantType, arrivalTime, timeInSystem):

        for event in partArriving.eventsList:
            eventType = partArriving
            yield self.env.timeout(decimal.Decimal(event[3]))
            if(event[0]==0):
                event[1].numberInTrack -= decimal.Decimal(1)
                event[1].updateNumberInTrack(self.env.now)
                event[2].numberInTrack += decimal.Decimal(1)
                event[2].updateNumberInTrack(self.env.now)

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




    #This methods represents the participant as an object and the associated events
    def participantValidation(self, partArriving, track, idNum, participantType, arrivalTime, timeInSystem):
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
        timeParticipantsSystem = self.weightedValuesSoft(durationValues, durationProbabilities, (self.ciclovia.maxArrivals*55))
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
        typeParticipantsSystem = self.weightedValues(typeValuesArray, typeProbabilitiesArray, (self.ciclovia.maxArrivals*55))

        i = 0
        j = 0
        noEnter = 0
        for track in self.ciclovia.tracks:
            #Changed 60 to 30
            track.flowInTrack = [0]*(int(self.simTime/30))

        for track in self.ciclovia.tracks:
            initialTime = 0
            indexHour = 0
            enterParticipants = 0

            for indexHour, hour in enumerate(track.arrivalsPerHour):
                j+=1
                #print("Deben llegar " + str(hour) + "a la hora %d"  % j)
                lastArrival = initialTime
                #print("Index es" + str(indexHour))
                #print("Last arrival es " + str(lastArrival))
                #Changed 60 to 30
                #print("En la hora " + str(indexHour) + " en el trayecto " + str(track.idNum) + " la tasa de arribos es " + str(30/hour))
                while(lastArrival<((indexHour+1)*30)):
                    #print("Entro al while!")
                    #trackNum = track.idNum
                    #Modified here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #Add +1 to hour: time =...(/hour+1 ) double check
                    #Changed 60 to 30
                    time = -math.log(1.0 - random.random())/float((hour))
                    #print("Tiempo expo: " + str(time))
                    arrivalTime = decimal.Decimal(time) + decimal.Decimal(lastArrival)
                    lastArrival = arrivalTime
                    #Changed 60 to 30
                    if(lastArrival>(indexHour+1)*30):
                        noEnter+=1
                    #Changed 60 to 30
                    if(lastArrival<(indexHour+1)*30):
                        i+=1
                        #print("last arrival es " + str(lastArrival))
                        #print("El valor de i es: " + str(i))
                        #print("Lenght " + str(len(timeParticipantsSystem)))
                        timeParticipantSystem =  timeParticipantsSystem[i]
                        #print("Itero en el while")
                        typeOfParticipant = self.ciclovia.typeParticipants[int(typeParticipantsSystem[i])]
                        #This assigns randomly if a participant enter by the end or by the begin of the track
                        assignEnterIn = random.random()
                        enterIn = "begin"
                        if(assignEnterIn>0.5):
                            enterIn = "end"
                        part = ParticipantObjSim(self.ciclovia, track, enterIn, i, typeOfParticipant, arrivalTime, timeParticipantSystem)
                        enterParticipants+=1

                        if(self.isValidation == True):
                            #print("Va a asignar ruta")
                            part.assignRoute()
                        #Imprimo la primera entidad que entra
                        participantList.append(part)
                        self.timeInSystemStatistic(timeParticipantSystem)


                #print("Salgo en el while")
                #Changed 60 to 30
                initialTime+=30
            track.totalArrivals = enterParticipants
            j=0

        self.calculateValuesTimeInSystemStatistic()
        self.totalArrivals = len(participantList)
        #First I must order the arrivals according to the arrivalTime
        participantListSorted = sorted(participantList, key=attrgetter('arrivalTime'))
        #print("Arribos totales" + str(len(participantListSorted)))
        #for index, partArriving in enumerate(participantListSorted ):
            #print("La hora es" + str(partArriving.arrivalTime))

        for index, partArriving in enumerate(participantListSorted):

            if(self.isValidation==True):
                part = self.participantValidation(partArriving, partArriving.track, partArriving.idNum, partArriving.participantType, partArriving.arrivalTime, partArriving.timeInSystem)
            else:
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

    # This definition generates a stream of values from a discrete probability distribution
    def weightedValuesSoft(self, valuesP, probabilitiesP, sizeP):
        minFrequency = 0.05
        values = valuesP
        probabilities = probabilitiesP
        total  = 0
        for freq in probabilities:
            total += freq
        relativeFrequencies = [0]*len(values)
        for index, freq in enumerate(probabilities):
            relativeFrequencies[index] = freq/total

        valuesLimits = []
        for index, value in enumerate(values):
            limits = 0
            if(index==0):
                #Limit = Ubicacion, Limite inferior, Limite superior, Ancho
                limits = [-1,0,values[index],1]
            elif(index==len(values)-1):
                limits = [1,values[index-1], values[index],1]
            else:
                limits = [0, values[index-1],values[index],1]
            valuesLimits.append(limits)

        valuesAdj = values
        probabilitiesAdj = probabilities
        relativeFrequenciesAdj = relativeFrequencies
        limitsAdj = valuesLimits

        change = False
        finish = False
        while(finish==False):
            counter = 0
            maxInterval = len(limitsAdj)
            change = False
            #print("Max int" + str(maxInterval))
            #print("Counter es " + str(counter))
            for index, interval in enumerate(limitsAdj):
                counter += 1
                #print("Relative freq for index " + str(index) + "is " + str(relativeFrequenciesAdj[index]))
                if(change==False and index>0 and relativeFrequenciesAdj[index]<minFrequency):
                    #Aca se deben unir intervalos
                    #print("Entrooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                    joinIntervalIndex = index-1
                    position = 1
                    #Aca debe ser un while
                    if(index<(len(limitsAdj)-1) and relativeFrequenciesAdj[index-1]>relativeFrequenciesAdj[index+1]):
                        joinIntervalIndex = index+1
                        position = -1
                    probabilitiesAdj[joinIntervalIndex] += probabilitiesAdj[joinIntervalIndex+position]
                    relativeFrequenciesAdj[joinIntervalIndex] = (probabilitiesAdj[joinIntervalIndex]+probabilitiesAdj[joinIntervalIndex+position])/total
                    limitsAdj[joinIntervalIndex][3] = limitsAdj[joinIntervalIndex][3]+ limitsAdj[index][3]
                    if(position==1):
                        limitsAdj[joinIntervalIndex][2] = limitsAdj[joinIntervalIndex+position][2]
                        valuesAdj[joinIntervalIndex] =  valuesAdj[joinIntervalIndex+position]
                    else:
                        limitsAdj[joinIntervalIndex][1] = limitsAdj[joinIntervalIndex+position][1]
                    #print("Values adj " + str(valuesAdj))
                    valuesAdj.pop(index)
                    #print("Values adj " + str(valuesAdj))
                    #print("Probs adj " + str(probabilitiesAdj))
                    probabilitiesAdj.pop(index)
                    #print("Probs adj " + str(probabilitiesAdj))
                    relativeFrequenciesAdj.pop(index)
                    limitsAdj.pop(index)
                    change = True
                    counter -= 1

            if(counter==maxInterval):
                finish = True



        weightedProbabilities = []
        totalWeight = 0
        for index, probability in enumerate(probabilitiesAdj):
            weightedProbabilities.append(probability*limitsAdj[index][3])
            totalWeight += probability*limitsAdj[index][3]
        for index, probability in enumerate(weightedProbabilities):
            probAdj = probability/totalWeight
            weightedProbabilities[index] = probAdj

        size = sizeP
        bins = numpy.cumsum(weightedProbabilities)
        x = numpy.random.random_sample(size)
        randomsObtained = numpy.digitize(x, bins)
        randomsList = []
        for randomValue in randomsObtained:
            indexNew = randomValue
            if(limitsAdj[indexNew][0] == 0):
                y = random.randint(limitsAdj[indexNew][1],limitsAdj[indexNew][2])
                randomsList.append(y)
            elif (limitsAdj[indexNew][0] == -1):
                y = random.randint(limitsAdj[indexNew][1],limitsAdj[indexNew][2])
                randomsList.append(y)
            elif(limitsAdj[indexNew][0] == 1):
                initialValue = limitsAdj[indexNew][1]
                rate = limitsAdj[indexNew][2] - limitsAdj[indexNew][1]
                y = -math.log(1.0 - random.random())*rate
                y += initialValue
                while(y>limitsAdj[indexNew][2]):
                    y = -math.log(1.0 - random.random())*rate
                    y += initialValue
                randomsList.append(y)

        return randomsList

    # This definition accumulates the current number in system
    def numberInSystemStatistic(self):
        size = len(self.listNumberInSystem)
        if(size == 0):
            info = [self.numberInCiclovia, self.env.now]
            self.listNumberInSystem.append(info)
        else:
            newInfo = [self.numberInCiclovia, (self.env.now-self.listNumberInSystem[size-1][1])]
            self.listNumberInSystem.append(newInfo)

    def timeInSystemStatistic(self, timeInSystem):
        self.listTimeInSystem.append(timeInSystem)

    def calculateValuesTimeInSystemStatistic(self):
        print('Average time in system:', numpy.mean(self.listTimeInSystem))
        print('Standard deviation:', numpy.std(self.listTimeInSystem))

    def showBarChart(self, n, xLabel, xInfo, yLabel, title):
        N = n
        means = xInfo
        ind = numpy.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars
        bars = plt.bar(ind, means, width, color='r')
        # add some text for labels, title and axes ticks
        plt.ylabel('Scores')
        plt.title(title)
        plt.xticks(ind+width/2., xLabel )
        plt.yticks(numpy.arange(0,81,10))
        plt.show()

    def printResults(self, cicloviaId, resultsCompiledId):
        # todo quitar este contador
        counterTest = 0
        cicloviaFromDB = Ciclovia.objects.get(id=cicloviaId)
        simTime = self.simTime
        totalArrivals = self.totalArrivals
        averageTime = numpy.mean(self.listTimeInSystem)
        standardDevTime = numpy.std(self.listTimeInSystem)
        listNumberInCiclovia = []
        listTimeNumberInCiclovia = []
        for value in self.listNumberInSystem:
            listNumberInCiclovia.append(float(value[0]))
            listTimeNumberInCiclovia.append(float(value[1]))

        avgNumberSystem = numpy.average(listNumberInCiclovia, weights=listTimeNumberInCiclovia)
        results = [simTime, totalArrivals, averageTime, standardDevTime, listNumberInCiclovia]
        self.results = results
        resultsCompiled = SimulationResultsCompiled.objects.get(id=resultsCompiledId)
        resultsDB = resultsCompiled.simulationresults_set.create(sim_time=self.simTime, date=timezone.now(), total_arrivals=self.totalArrivals, average_time=round(averageTime, 3), standard_deviation_time=round(standardDevTime, 3), average_number_system= round(avgNumberSystem,3))
        resultsDB.save()

        for track in self.ciclovia.tracks:
            counterTest += 1
            print("Track numero: " + str(counterTest))

            listNumberInTrack = []
            listTimeNumberInTrack = []
            for value in track.numParticipantsInTrack:
                listNumberInTrack.append(float(value[0]))
                listTimeNumberInTrack.append(float(value[1]))
            # Revisar
            # print("Sim time " + str(simTime))
            if len(listNumberInTrack) > 0:
                listNumberInTrack.append(listNumberInTrack[len(listNumberInTrack)-1])
                listTimeNumberInTrack.append(simTime - listTimeNumberInTrack[len(listTimeNumberInTrack)-1])

            avgNumberInTrack = 0
            if len(listNumberInTrack) == 0:
                resultsPerTrackDB = resultsDB.simulationresultspertrack_set.create(track = track.idNum, total_arrivals=0,  average_number_track=0)
            else:
                avgNumberInTrack = round(numpy.average(listNumberInTrack, weights=listTimeNumberInTrack),3)
                resultsPerTrackDB = resultsDB.simulationresultspertrack_set.create(track = track.idNum, total_arrivals=0,  total_flow=0, average_number_track=avgNumberInTrack)

            if self.isValidation:

                hourInterval = 1
                totalFlow = 0
                #Graficar
                yLabel = "Flujo"
                xLabel = ('8:00','8:30','9:00','9:30','10:00','10:30','11:00','11:30')
                values = track.flowInTrack
                title = "Flujo del trayecto " + str(track.idNum)
                # self.showBarChart(len(values), xLabel, values, yLabel, title)
                for timeInterval in track.flowInTrack:
                    # print("   El flujo en la hora " + str(hourInterval) + " es de " + str(timeInterval))
                    totalFlow += timeInterval
                    # Completar cargando los resultados a la base de datos
                    resultsFlowValidationDB = resultsPerTrackDB.simulationresultsflowpertrack_set.create(hour=hourInterval, flow_hour=timeInterval)
                    hourInterval += 1
                    resultsFlowValidationDB.save()
            resultsPerTrackDB.total_flow = totalFlow
            resultsPerTrackDB.save()


# This class represents an entity
class ParticipantObjSim:

    # This is the constructor of the class ParticipantObjSim
    # It takes the parameters provided as arguments and stores them in the object
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
        self.currentTimeForFlow = arrivalTime
        self.eventsList = []

    # This method assigns the route
    def assignRoute(self):
        # Arrival
        event = [1, self.track, self.track, self.arrivalTime]
        self.eventsList.append(event)
        sim_time = (self.ciclovia.endHour - self.ciclovia.startHour+1)*30

        while(self.timeLeftInSystem>0):
            distance = self.track.distance
            velocity = self.participantType.velocity
            # Todo change the velocity according to track parameters
            if self.track.number_of_semaphores > 0:
                binomialProb = 1
                velocity = velocity*binomialProb
            if self.track.hasSlope > 0:
                slopeCoef = 1
                velocity = velocity*slopeCoef
            if self.track.quality_of_track > 0:
                qualityCoef = 1
                velocity = velocity*qualityCoef
            time_for_track = 60*distance/(velocity)
            #Update flow if necessary
            #halfDistance = distance/2
            time_for_half_track = time_for_track/2
            #If the entity has enough time to go until the half of the track, the flow statistic has to be updated
            if time_for_half_track<self.timeLeftInSystem and (float(self.currentTimeForFlow)+float(time_for_half_track)<sim_time):
                time_sim_flow = float(self.currentTimeForFlow) + float(time_for_half_track)
                self.track.updateFlowInTrack(time_sim_flow)

            if time_for_track>self.timeLeftInSystem:
                #leavingTime = self.currentTime + self.timeLeftInSystem
                leaving_time = self.timeLeftInSystem
                self.timeLeftInSystem = 0
                #Leaving system = -1
                event = [-1, self.track, self.track, leaving_time]
                self.eventsList.append(event)

            else:
                #Info neighboor gives me an array with the nextTrack and with the direction
                #If a participant enters by the begin of the track, he has to go out from the end of the track
                out_in = "end"
                if self.direction == "end":
                    out_in = "begin"
                next_track = self.track.giveNeighboorInDirection(out_in)
                next_track_id = next_track[0]
                self.direction = next_track[1]
                next_track = self.ciclovia.getTrack(next_track_id)

                #Assign the opposite direction !
                if self.direction == "begin" and next_track_id == self.track.idNum:
                    self.direction = "end"
                if self.direction == "end" and next_track_id == self.track.idNum:
                    self.direction = "begin"

                #movingTime = self.currentTime + timeForTrack
                moving_time = time_for_track
                self.currentTimeForFlow = float(self.currentTimeForFlow) + time_for_track
                self.currentTime = moving_time
                self.timeLeftInSystem -= time_for_track
                #Moving from ciclovia = 0
                event = [0, self.track, next_track, moving_time]
                self.track = next_track
                self.eventsList.append(event)
                self.assignRoute()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#   EJECUCION DE LA APLICACION
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


# This method executes the simulation
def simulationExecution(cicloviaId, isValidation):

    start = timeit.default_timer()
    simulationRuns = 10
    if isValidation:
        simulationRuns = 10
    seed = 9243881

    cicloviaFromDB = Ciclovia.objects.get(id=cicloviaId)
    resultsCompiledDB = cicloviaFromDB.simulationresultscompiled_set.create(num_runs=0, date=timezone.now(), avg_total_arrivals=-1, stdev_total_arrivals = -1, hw_total_arrivals = -1, average_number_system = -1, stdev_number_system = -1, hw_number_system = -1, is_validation = isValidation )
    resultsCompiledDB.save()
    resultsCompiledId = resultsCompiledDB.id
    reps_exec_times = []
    totalTimeContruction = 0
    totalTimeEntityRouting = 0
    totalTimeExecution = 0
    threads = []
    for i in range(simulationRuns):
        timeRep = timeit.default_timer()

        simDES = SimulationDES(seed, cicloviaId, resultsCompiledId, isValidation)
        timeRepContructor = timeit.default_timer() - timeRep
        totalTimeContruction += timeRepContructor

        simDES.env.process(simDES.participantArrivals())
        timeRepEntityRouting = timeit.default_timer() - timeRep
        totalTimeEntityRouting += timeRepEntityRouting
        #t = threading.Thread(name="Rep-"+str(i), target=simDES.execute, args=(cicloviaId, resultsCompiledId,))
        simDES.execute(cicloviaId, resultsCompiledId)
        #threads.append(t)
        #t.start()
        timeRepExecution = timeit.default_timer() - timeRep
        totalTimeExecution += timeRepExecution

        seed *= 2
        seed += i
        timeRep = timeit.default_timer() - timeRep
        reps_exec_times.append(timeRep)
        # simDES.printResults(cicloviaId)
    # Espera 10 segundos y mira si ya todos los threads han terminado
    waitTime = 10
    #threadsToFinish = numpy.ones(simulationRuns)
    #while numpy.sum(threadsToFinish):
    #    print("Espera " + str(waitTime) + " segundos")
    #    print("Faltan " + str(numpy.sum(threadsToFinish)) + " por terminar")
    #    timeLib.sleep(waitTime)
    #    for i in range(len(threads)):
    #        if threads[i].isAlive() == 0:
    #            threadsToFinish[i] = 0

    print("Tiempos de replicas: ")
    print(reps_exec_times)
    print("Numero de replicas: " + str(simulationRuns))
    print("Tiempo del constructor: " + str(totalTimeContruction))
    print("Tiempo del ruteo: " + str(totalTimeEntityRouting))
    print("Tiempo de la ejecucion: " + str(totalTimeExecution))

    normalval = norm.ppf(0.975, loc=0, scale=1)
    sqrtvals = numpy.sqrt([simulationRuns])
    listTotalArrivals = []
    listNumberSystem = []
    listInfoTracks = []
    listFlowTracks = []
    listFlowPerHourTracks = []
    for track in range(cicloviaFromDB.num_tracks):
        listPerTrack = []
        listFlowPerTrack = []
        listDetailFlowPerTrack = []
        listInfoTracks.append(listPerTrack)
        listFlowTracks.append(listFlowPerTrack)
        listFlowPerHourTracks.append(listDetailFlowPerTrack)
        timeIntervals = len(cicloviaFromDB.arrivalsproportionperhour_set.all())
        listFlowPerHour = []
        for hour in range(timeIntervals):
            listPerHour = []
            listDetailFlowPerTrack.append(listPerHour)

    queryFromDB = resultsCompiledDB.simulationresults_set.all()
    for result in queryFromDB:
        listTotalArrivals.append(result.total_arrivals)
        listNumberSystem.append(result.average_number_system)

        infoTracks = result.simulationresultspertrack_set.all()

        for track in infoTracks:
            listInfoTracks[track.track-1].append(track.average_number_track)
            listFlowTracks[track.track-1].append(track.total_flow)

            queryFlowFromDB = track.simulationresultsflowpertrack_set.all()
            for flow in queryFlowFromDB:
                listFlowPerHourTracks[track.track-1][flow.hour-1].append(flow.flow_hour)

    for index, listPerTrack in enumerate(listInfoTracks):
        avg_number_track = round(numpy.mean(listPerTrack), 3)
        std_number_track = round(numpy.std(listPerTrack),  3)
        hw_number_track = round(normalval*std_number_track/sqrtvals[0], 3)
        if(len(listInfoTracks)>1):
            std_number_track = round(numpy.std(listPerTrack), 3)
        avg_total_flow = 0
        std_total_flow = 0
        if(isValidation == True):
            avg_total_flow = round(numpy.mean(listFlowTracks[index]),3)
            if(len(listInfoTracks)>1):
                std_total_flow = round(numpy.std(listFlowTracks[index]),3)
        resultsPerTrackCompiledDB = resultsCompiledDB.simulationresultscompiledpertrack_set.create(track = index+1, average_number_track = avg_number_track, stdev_number_track = std_number_track, hw_number_track=hw_number_track,average_total_flow=avg_total_flow, stdev_total_flow=std_total_flow)
        resultsPerTrackCompiledDB.save()

        # Aca se debe compilar el flujo por trayecto
        if(isValidation==True):
            for index2, hourInt in enumerate(listFlowPerHourTracks[index]):
                avg_flow_hourInt = round(numpy.mean(hourInt),3)
                std_flow_hourInt = 0
                if(len(listInfoTracks)>1):
                    std_flow_hourInt = round(numpy.std(hourInt),3)
                resultsPerHourPerTrackCompiledDB = resultsPerTrackCompiledDB.simulationresultscompiledflowtrack_set.create(track_simulation = index+1, hour = index2+1, avg_flow_hour=avg_flow_hourInt,stdev_flow_hour = std_flow_hourInt, hw_flow_hour=0)

                resultsPerHourPerTrackCompiledDB.save()

            resultsPerTrackCompiledDB.save()

    resultsCompiledDB.avg_total_arrivals = round(numpy.mean(listTotalArrivals),3)
    resultsCompiledDB.average_number_system = round(numpy.mean(listNumberSystem),3)
    resultsCompiledDB.num_runs = simulationRuns
    if(simulationRuns>1):
        resultsCompiledDB.stdev_total_arrivals = round(numpy.std(listTotalArrivals),3)
        resultsCompiledDB.hw_total_arrivals = round(normalval*\
            resultsCompiledDB.stdev_total_arrivals/sqrtvals[0],3)
        resultsCompiledDB.stdev_number_system = round(numpy.std(listNumberSystem),3)
        resultsCompiledDB.hw_number_system = round(normalval*\
            resultsCompiledDB.stdev_number_system/sqrtvals[0],3)
    resultsCompiledDB.save()
    stop = timeit.default_timer()
    time = stop - start
    print("El tiempo de ejecucion total es " + str(time))

    return resultsCompiledDB.id



