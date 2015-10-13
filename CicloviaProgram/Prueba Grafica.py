from __future__ import division
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import scipy.stats as ss

def ejemploGrafica():
    x = linspace(0,5,50)
    y = x**2
    plot(x,y,'r')
    xlabel('x')
    ylabel('y')
    title(u'Título')
    show()
    
def ejemploGrafica2():
    N = 5
    menMeans = (20, 35, 30, 35, 27)
    menStd =   (2, 3, 4, 1, 2)
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
    
    womenMeans = (25, 32, 34, 20, 25)
    womenStd =   (3, 5, 2, 3, 3)
    rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
    
    ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
    autolabel(rects1)
    autolabel(rects2)
    plt.show()
    
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
    
        
#Para Ciclovia Script

def showBarChart(n, xLabels, xInfo, yLabel, title):
    N = n
    means = xInfo
        
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, means, width, color='r')

     
    # add some text for labels, title and axes ticks
    ax.set_ylabel(xLabel)
    ax.set_title(title)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( (xLabels) )

    autoLabel(rects1)
    plt.show()
    
    def showBarChart(self, n, xLabel, xInfo, yLabel, title):
           
        rects1 = plt.bar(ind, means, width, color='r')         
        # add some text for labels, title and axes ticks
        ax.set_ylabel(xLabel)
        ax.set_title(title)
        ax.set_xticks(ind+width)
        ax.set_xticklabels( (xLabel) )
           
        self.autoLabel(rects1)
        plt.show()      
        
def ejemploGrafica3():
    N = 8
    menMeans = (814, 1043, 702, 621, 620, 418, 261, 278)
   
        
    ind = np.arange(N)  # the x locations for the groups
    width = 0.90      # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width, color='r')
    
               
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Flujo')
    ax.set_title('Flujo del trayecto 3 por intervalo de tiempo')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('8:30','9:00','9:30','10:00','10:30','11:00','11:30','12:00') )
            
    autolabel(rects1)
    autolabel(rects2)
    plt.show()
    
def ejemploGrafica4():
    N = 6
    menMeans = (331, 424, 698, 516, 292, 173)
   
        
    ind = np.arange(N)  # the x locations for the groups
    width = 0.70      # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, menMeans, width+0.3, color='b')
    
               
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Flujo')
    ax.set_title('Numero promedio de participantes por trayecto')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('1','2','3','4','5','6') )
            
    autolabel(rects1)
    autolabel(rects2)
    plt.show()
    
def weightedValues():   
    minFrequency = 0.05
    values = [30,60,90,120,150,180,210,240,270,300]
    probabilities = [2, 53, 56, 89, 22, 37, 3, 17, 3, 0]
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
    print("se va a imprimir" + str(valuesLimits))
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
        print("Max int" + str(maxInterval))
        print("Counter es " + str(counter))    
        for index, interval in enumerate(limitsAdj):
            counter += 1
            print("Relative freq for index " + str(index) + "is " + str(relativeFrequenciesAdj[index]))
            if(change==False and index>0 and relativeFrequenciesAdj[index]<minFrequency):                
                #Aca se deben unir intervalos
                print("Entrooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
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
                print("Values adj " + str(valuesAdj))
                valuesAdj.pop(index)
                print("Values adj " + str(valuesAdj))
                print("Probs adj " + str(probabilitiesAdj))
                probabilitiesAdj.pop(index)
                print("Probs adj " + str(probabilitiesAdj))
                relativeFrequenciesAdj.pop(index)
                limitsAdj.pop(index)                
                change = True
                counter -= 1
            
        print("Counter es " + str(counter))       
        if(counter==maxInterval):
            print("Ya todos estan ok")
            print("Counter " + str(counter) + " LimitsAdj size " + str(len(limitsAdj)))
            finish = True 
        
        
    print("Intervalos ")
    print(str(valuesAdj))
    print(str(probabilitiesAdj))
    print(str(relativeFrequenciesAdj))
    print(str(limitsAdj))
    
    weightedProbabilities = []
    totalWeight = 0
    for index, probability in enumerate(probabilitiesAdj):
        #weightedProbabilities.append(probability)
        #totalWeight += probability
        weightedProbabilities.append(probability*limitsAdj[index][3])
        totalWeight += probability*limitsAdj[index][3]        
    for index, probability in enumerate(weightedProbabilities):
        #print("entre con "+ str(probability))
        probAdj = probability/totalWeight        
        weightedProbabilities[index] = probAdj
        #print("salgo con con "+ str(probability))
        
    #print("Weighted prob ahora es ")
    #print(str(weightedProbabilities))
    
   
    size = 1000
    #print("size es" + str(size))
    bins = np.cumsum(weightedProbabilities)
    #print("Los bins son " + str(bins))
    #bins[len(bins)-1] = 1.0 
    #print("Parametros")
    x = np.random.random_sample(size)
    #print("Se va a obtener" + str(x))
    #print(str(np.digitize(x, bins)))     
    randomsObtained = np.digitize(x, bins)
    #print("Se obtuvieron ")
    #print(str(randomsObtained))
    randomsList = []    
    for randomValue in randomsObtained:
        #indexNew = values.index(randomValue)
        indexNew = randomValue
        #print("Index New")
        #print(indexNew)
        #print( valuesLimits[indexNew])
        if(limitsAdj[indexNew][0] == 0):
            #print("Se va a usar uniforme")
            y = random.randint(limitsAdj[indexNew][1],limitsAdj[indexNew][2])
            randomsList.append(y)
            #print("Se genero " + str(y))
        elif (limitsAdj[indexNew][0] == -1):
            #print("Se va a usar uniforme iniciando en 0")
            y = random.randint(limitsAdj[indexNew][1],limitsAdj[indexNew][2])
            #print("Se genero " + str(y))  
            randomsList.append(y)
        elif(limitsAdj[indexNew][0] == 1):
            #print("Se va a usar exponencial 0")
            initialValue = limitsAdj[indexNew][1]
            rate = limitsAdj[indexNew][2] - limitsAdj[indexNew][1]
            #print("los parametros son ")
            #print("rate " + str(rate))
            #print("init value" + str(initialValue))
            y = -math.log(1.0 - random.random())*rate 
            #print("Se genero " + str(y))
            y += initialValue
            #if(y>limitsAdj[indexNew][2]+50):
                #y = limitsAdj[indexNew][2]+50  
            while(y>limitsAdj[indexNew][2]):
                y = -math.log(1.0 - random.random())*rate 
                y += initialValue
            randomsList.append(y)
        #print(str(y))   
        plt.clf()
        plt.hist(randomsList)
        plt.xlim(0, 300)           
            
            
            
def weightedValuesSoft():   
    values = [30,45,60,75,90,120,150,180,250]
    valuesLimits = []
    for index, value in enumerate(values):
        limits = 0 
        if(index==0):
            limits = (-1,0,value)
        elif(index==len(values)-1):
            limits = (1,values[index-1], values[index])
        else:
            limits = (0, (values[index-1]+values[index])/2,((values[index]+values[index+1])/2))
        valuesLimits.append(limits)
    print("se va a imprimir" + str(valuesLimits))
        
    probabilities = [0.02,0.01,0.19,0.01,0.17,0.32,0.07,0.14,0.07]
    size = 5000
    #print("size es" + str(size))
    bins = np.cumsum(probabilities)
    #print("Los bins son " + str(bins))
    #bins[len(bins)-1] = 1.0 
    #print("Parametros")
    x = np.random.random_sample(size)
    #print("Se va a obtener" + str(x))
    #print(str(np.digitize(x, bins)))     
    randomsObtained = np.digitize(x, bins)
    #print("Se obtuvieron ")
    #print(str(randomsObtained))
    randomsList = []    
    for randomValue in randomsObtained:
        #indexNew = values.index(randomValue)
        indexNew = randomValue
        #print("Index New")
        #print(indexNew)
        #print( valuesLimits[indexNew])
        if(valuesLimits[indexNew][0] == 0):
            #print("Se va a usar uniforme")
            y = random.randint(valuesLimits[indexNew][1],valuesLimits[indexNew][2])
            randomsList.append(y)
            #print("Se genero " + str(y))
        elif (valuesLimits[indexNew][0] == -1):
            #print("Se va a usar uniforme iniciando en 0")
            y = random.randint(valuesLimits[indexNew][1],valuesLimits[indexNew][2])
            #print("Se genero " + str(y))  
            randomsList.append(y)
        elif(valuesLimits[indexNew][0] == 1):
            #print("Se va a usar exponencial 0")
            initialValue = valuesLimits[indexNew][1]
            rate = (valuesLimits[indexNew][2] - valuesLimits[indexNew][1])
            y = -math.log(1.0 - random.random())*rate + initialValue
            if(y>500):
                y = 500
            #print("Se genero " + str(y))        
            randomsList.append(y)            
        
            
    
    print(randomsList)
                    
        #values[numpy.digitize(x, bins)]     

    #This definition generates a stream of values from a discrete probability distribution
def weightedValuesSoftPrevious(self, values, probabilities, size):  
    valuesLimits = []
    #print("Values ")
    #print(str(values))
    #print(len(values))
    for index, value in enumerate(values):
        #print("Entro la vez " + str(index))
        limits = 0 
        if(index==0):
            limits = (-1,0,((values[index]+values[index+1])/2))
        elif(index==len(values)-1):
            limits = (1,(values[index-1]+values[index])/2, values[index])
        else:
            limits = (0, (values[index-1]+values[index])/2,((values[index]+values[index+1])/2))
        valuesLimits.append(limits)        
        #print("Values limits")
        #print(str(valuesLimits))
        #print("size es" + str(size))
        bins = numpy.cumsum(probabilities)
        bins[len(bins)-1] = 1.0 
        #print("Parametros")
        x = numpy.random.random_sample(round(size))
        randomsObtained = numpy.digitize(x, bins)
        #print("Randoms values")
        print(str(randomsObtained))        
        randomsList = []    
        for randomValue in randomsObtained:
            #indexNew = values.index(randomValue)
            indexNew = randomValue
            #print("Index New")
            #print(indexNew)
            #print( valuesLimits[indexNew])
            #print("Entro")
            #print(indexNew)
            #print(len(valuesLimits))
            #print(valuesLimits[indexNew][0])
            if(valuesLimits[indexNew][0] == 0):
                #print("Se va a usar uniforme")
                y = random.randint(round(valuesLimits[indexNew][1]),round(valuesLimits[indexNew][2]))
                randomsList.append(y)
                #print("Se genero " + str(y))
            elif (valuesLimits[indexNew][0] == -1):
                #print("Se va a usar uniforme iniciando en 0")
                y = random.randint(round(valuesLimits[indexNew][1]),round((valuesLimits[indexNew][2])))
                #print("Se genero " + str(y))  
                randomsList.append(y)
            elif(valuesLimits[indexNew][0] == 1):
                #print("Se va a usar exponencial 0")
                initialValue = valuesLimits[indexNew][1]
                rate = valuesLimits[indexNew][2] - valuesLimits[indexNew][1]
                y = -math.log(1.0 - random.random())*rate + initialValue
                if(y>500):
                    y = 500
                    #print("Se genero " + str(y))        
                    randomsList.append(y)        
        return randomsList         
        
def trunc_exp_rv(low, high, scale, size):
    rnd_cdf = np.random.uniform(ss.expon.cdf(x=low, scale=scale),
                                        ss.expon.cdf(x=high, scale=scale),
                                        size=size)
    plt.his(tss.expon.ppf(q=rnd_cdf, scale=scale))
    plt.xlim(0, 125)
    #plt.hist(trunc_exp_rv(0, 120, 120, 1000))
        


        

  