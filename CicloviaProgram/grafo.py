# coding=utf-8
from reportlab.graphics.shapes import *
from reportlab.lib.colors import Color, getAllNamedColors

d = Drawing(1000,700)
Nodos=[1,2,3,4,5,6,7,8,9,10] #Index from 0.
Arcos=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[1,10],[3,7]]
ArrNodos=[]   #Inicializar vacio arreglo de nodos.
ArrLineas=[]
yCero=50
xCero=50
deltaX=70*1.5
deltaY=150
maxNivel = 0

class Point(object):
    """Clase que representa un punto"""

    def __init__(self, pX, pY):
        self.x = pX
        self.y = pY

class Nodo(object):
    """Información del nodo a dibujar"""

    def __init__(self, pNumero):
        """Constructor basico"""
        #Variables
        self.numero = pNumero
        self.posX = 0
        self.posY = 0
        self.radio = 25
        self.puntoIzq = Point(0, 0)
        self.puntoDer = Point(0, 0)
        self.puntoSup = Point(0, 0)
        self.puntoInf = Point(0, 0)
        self.centro = Point(self.posX,self.posY)
        self.circulo = Circle(self.centro.x,self.centro.y, self.radio)
        self.dibujado = False
        self.nivelDibujado = 0
        self.numNodoDibujado = 0

def buscarNodo(num):
    """Busca el nodo con el número num"""
    for nodo in ArrNodos:
        if nodo.numero==num:
            return nodo
    return 0

def parametrosDibujo(nodo):
    """Asigna los parametros de dibujo."""
    nodo.puntoIzq = Point(nodo.posX - nodo.radio*1.5, nodo.posY)
    nodo.puntoDer = Point(nodo.posX + nodo.radio*1.5, nodo.posY)
    nodo.puntoSup = Point(nodo.posX, nodo.posY + nodo.radio)
    nodo.puntoInf = Point(nodo.posX, nodo.posY - nodo.radio)
    nodo.centro = Point(nodo.posX,nodo.posY)
    nodo.circulo = Ellipse(nodo.centro.x,nodo.centro.y, nodo.radio*1.5,nodo.radio )

def nivelDeDibujo(nodo1,nodo2):
    """Determina el nivel en el que se va a dibujar el nodo2 respecto al nodo1."""
    global maxNivel
    if abs(nodo1.numNodoDibujado-nodo2.numNodoDibujado)>1:
        i=0
        while i==nodo1.nivelDibujado:
            i+=1
        if i>maxNivel:
            maxNivel = i
        return i
    else:
        return nodo2.nivelDibujado

def asignarPosicionOrd():
    """Asigna la posición de cada nodo siguiendo el orden de los arcos. El
    algorítmo falla si se debe relocalizar un nodo que había relocalizado a otro, pero
    dada la estrcutura de conexión bidireccional de los nodos en la ciclovía,
    esa situación no se presenta."""
    global ArrNodos
    ArrNodos = []
    for i in range(len(Nodos)):  #Inicializar objetos.
        ArrNodos.append(Nodo(Nodos[i]))

    numnodo = 0     #Contador de columnas.
    nivel = 0   #Contador de filas.

    for arc in Arcos:
        nodo1=buscarNodo(arc[0])
        nodo2=buscarNodo(arc[1])

        if not nodo1.dibujado and not nodo2.dibujado:  #No existe ninguno.
            nodo1.dibujado = True
            nodo1.posX=xCero+deltaX*numnodo
            nodo1.posY=yCero+deltaY*nivel
            nodo1.nivelDibujado=nivel
            nodo1.numNodoDibujado=numnodo
            parametrosDibujo(nodo1)
            numnodo+=1
        elif not nodo2.dibujado:    #Exite nodo1 pero no existe nodo2.
            nodo2.dibujado = True
            nodo2.numNodoDibujado=numnodo
            nivel=nivelDeDibujo(nodo1,nodo2)
            nodo2.nivelDibujado=nivel
            nodo2.posX=xCero+deltaX*numnodo
            nodo2.posY=yCero+deltaY*nivel
            parametrosDibujo(nodo2)
            numnodo+=1
        elif not nodo1.dibujado:    #Exite nodo2 pero no existe nodo1.
            nodo1.dibujado = True
            nodo1.numNodoDibujado=numnodo
            nivel=nivelDeDibujo(nodo2,nodo1)
            nodo1.nivelDibujado=nivel
            nodo1.posX=xCero+deltaX*numnodo
            nodo1.posY=yCero+deltaY*nivel
            parametrosDibujo(nodo1)
            numnodo+=1
        else:   #El último en ser dibujado debe ser relocalizado.
            if comparar(nodo1.numNodoDibujado, nodo2.numNodoDibujado)==1:#Relocalizar el 1.
                nivel=nivelDeDibujo(nodo2,nodo1)
                nodo1.nivelDibujado=nivel
                nodo1.posY=yCero+deltaY*nivel
                parametrosDibujo(nodo1)
            else:#Relocalizar el 2.
                nivel=nivelDeDibujo(nodo1,nodo2)
                nodo2.nivelDibujado=nivel
                nodo2.posY=yCero+deltaY*nivel
                parametrosDibujo(nodo2)

        if not nodo2.dibujado:#Ninguno estaba dibujado.
            nodo2.dibujado=True
            nodo2.posX=xCero+deltaX*numnodo
            nodo2.posY=yCero+deltaY*nivel
            nodo2.nivelDibujado=nivel
            nodo2.numNodoDibujado=numnodo
            parametrosDibujo(nodo2)
            numnodo+=1

        nivel=0

    for nodo in ArrNodos:#Nodos despegados.
        if not nodo.dibujado:
            nodo.dibujado = True
            nodo.posX=xCero+deltaX*numnodo
            nodo.posY=yCero+deltaY*nivel
            nodo.nivelDibujado=nivel
            nodo.numNodoDibujado=numnodo
            parametrosDibujo(nodo)
            numnodo+=1

def comparar(int1, int2):
    """Compara dos numeros, 1 si int1 es mayor que int2, 0 si son iguales, -1 si int1 es menor que int2."""
    if int1-int2>0:
        return 1
    elif int1-int2<0:
        return -1
    else:
        return 0

def conectarPorDerecha(nodo1, nodo2):
    """Conecta el nodo1 desde la derecha a la izquierda del nodo2."""
    global ArrLineas
    linea = Line(nodo1.puntoDer.x,nodo1.puntoDer.y, nodo2.puntoIzq.x,nodo2.puntoIzq.y)
    ArrLineas.append(linea)

def conectarPorIzquierda(nodo1,nodo2):
    """Conecta el nodo1 desde la izquierda a la derecha del nodo2."""
    global ArrLineas
    linea = Line(nodo1.puntoIzq.x,nodo1.puntoIzq.y,nodo2.puntoDer.x,nodo2.puntoDer.y)
    ArrLineas.append(linea)

def conectarPorDebajo(nodo1,nodo2):
    """Conecta el nodo1 desde la parte inferior a la parte superior del nodo2."""
    global ArrLineas
    linea = Line(nodo1.puntoInf.x,nodo1.puntoInf.y,nodo2.puntoSup.x,nodo2.puntoSup.y)
    ArrLineas.append(linea)

def conectarPorArriba(nodo1,nodo2):
    """Conecta el nodo1 desde la parte superior a la parte inferior del nodo2."""
    global ArrLineas
    linea = Line(nodo1.puntoSup.x,nodo1.puntoSup.y,nodo2.puntoInf.x,nodo2.puntoInf.y)
    ArrLineas.append(linea)

def arcosRectosOrdenados():
    """Dibuja los arcos."""
    global ArrLineas
    ArrLineas = []
    for arc in Arcos:
        nodo1=buscarNodo(arc[0])
        nodo2=buscarNodo(arc[1])
        if comparar(nodo1.nivelDibujado,nodo2.nivelDibujado)==0:
            if comparar(nodo1.posX, nodo2.posX)==1:
                conectarPorIzquierda(nodo1,nodo2)
            else:
                conectarPorDerecha(nodo1,nodo2)
        else:
            if comparar(nodo1.nivelDibujado,nodo2.nivelDibujado)==1:
                conectarPorDebajo(nodo1,nodo2)
            else:
                conectarPorArriba(nodo1,nodo2)

def dibujarPartes():
    """Dibujar nodos y arcos."""

    for linea in ArrLineas:
        linea.strokeColor = Color(0,0.51,0.84)
        linea.strokeWidth = 2
        d.add(linea)

    for nodo in ArrNodos:
        # nodo.circulo.setFill('blue')
        # nodo.circulo.setOutline('cyan')
        nodo.circulo.fillColor = Color(0,0.51,0.84)
        nodo.circulo.strokeColor = Color(0,0.51,0.84)
        # nodo.circulo.strokeWidth = 5
        d.add(nodo.circulo)
        tex = String(nodo.centro.x,nodo.centro.y,str(nodo.numero))
        tex.textAnchor = 'middle'
        tex.fontSize = 18
        tex.fillColor = getAllNamedColors()['white']
        d.add(tex)



def dibujar():
    global d
    global maxNivel
    d = Drawing(1000,700)
    maxNivel = 0
    asignarPosicionOrd()
    arcosRectosOrdenados()
    dibujarPartes()
    d.width = 2*xCero + deltaX*(len(Nodos)-1)
    d.height = 2*yCero + deltaY*maxNivel
    return d

def dibujarGrafo(pNodos,pArcos):
    global Nodos
    global Arcos
    Nodos = pNodos
    Arcos = pArcos
    return dibujar()