# coding=utf-8
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart, VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie, Pie3d
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.lineplots import ScatterPlot
from reportlab.graphics.charts.legends import Legend, TotalAnnotator
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.colors import *
import traceback
from reportlab.lib.validators import Auto



from reportlab.graphics.widgets.markers import makeMarker

class BarChart(Drawing):
	def __init__(self, width=400, height=200, *args, **kw):
		try:
			Drawing.__init__(self,width,height,*args,**kw)
			self.add(HorizontalBarChart(), name='chart')
			#set any shapes, fonts, colors you want here.  We'll just
			#set a title font and place the chart within the drawing
			self.chart.x = 20
			self.chart.y = 20
			self.chart.width = self.width - 20
			self.chart.height = self.height - 40
			self.chart.bars[0].fillColor = blue


			#La siguiente variable almacena los datos a graficar
			#self.chart.data = [[100,150,200,235]]
		except:
			traceback.print_exc()
	def changeTitle(self,title):
		self.add(String(100,185,title), name='title')
		self.title.fontName = 'Helvetica'
		self.title.fontSize = 14


class MyLineChartDrawing(Drawing):
	def __init__(self, width=600, height=400, *args, **kw):
		Drawing.__init__(self,width,height,*args,**kw)
		#
		#set any shapes, fonts, colors you want here.  We'll just
		#set a title font and place the chart within the drawing.
		#pick colors for all the lines, do as many as you need
		self.add(LinePlot(), name='chart')
		self.chart.x = 30
		self.chart.y = 30
		self.chart.width = self.width - 100
		self.chart.height = self.height - 75
		self.chart.lines[0].strokeColor = blue
		self.chart.lines[1].strokeColor = green
		self.chart.lines[2].strokeColor = yellow
		self.chart.lines[3].strokeColor = red
		self.chart.lines[4].strokeColor = black
		self.chart.lines[5].strokeColor = orange
		self.chart.lines[6].strokeColor = cyan
		self.chart.lines[7].strokeColor = magenta
		self.chart.lines[8].strokeColor = brown
		self.chart.fillColor = white
		self.chart.data = [((0, 50), (100,100), (200,200), (250,210), (300,300), (400,500))]
		self.chart.xValueAxis.labels.fontSize = 12
		self.chart.xValueAxis.forceZero = 0
		self.chart.xValueAxis.forceZero = 1
		self.chart.xValueAxis.gridEnd = 115
		self.chart.xValueAxis.tickDown = 3
		self.chart.xValueAxis.visibleGrid = 1
		self.chart.yValueAxis.tickLeft = 3
		self.chart.yValueAxis.labels.fontName = 'Times-Roman'
		self.chart.yValueAxis.labels.fontSize = 12
		self.chart.yValueAxis.forceZero = 1


		self.add(String(100,180,'Hello World'), name='title')
		self.title.fontName = 'Times-Roman'
		self.title.fontSize = 18
		self.title.x = self.width/2
		self.title.y = self.height - 18*1.2
		self.title.textAnchor ='middle'

		self.add(Legend(),name='Legend')
		self.Legend.fontName = 'Times-Roman'
		self.Legend.fontSize = 12
		self.Legend.x = self.width - 80
		self.Legend.y = 200
		self.Legend.dxTextSpace = 5
		self.Legend.dy = 5
		self.Legend.dx = 5
		self.Legend.deltay = 5
		self.Legend.alignment ='right'

		self.add(Label(),name='XLabel')
		self.XLabel.fontName = 'Times-Roman'
		self.XLabel.fontSize = 12
		self.XLabel.x = self.width/2
		self.XLabel.y = 5
		self.XLabel.textAnchor ='middle'
		self.XLabel.height = 20
		self.XLabel._text = "X Axis"

		self.add(Label(),name='YLabel')
		self.YLabel.fontName = 'Times-Roman'
		self.YLabel.fontSize = 12
		self.YLabel.x = 10
		self.YLabel.y = self.height/2
		self.YLabel.angle = 90
		self.YLabel.textAnchor ='middle'
		self.YLabel._text = "Y Axis"


class myPieChart(Drawing):
	def __init__(self, width=500, height=300, *args, **kw):
		Drawing.__init__(self,width,height,*args,**kw)

		self.add(Pie(), name='chart')
		self.chart.height				= 200
		self.chart.x                    = 30
		self.chart.y                    = (self.height-self.chart.height)/2
		self.chart.slices.strokeWidth   = 1
		self.chart.slices.popout        = 5
		self.chart.direction            = 'clockwise'
		self.chart.width                = self.chart.height
		self.chart.startAngle           = 90

		self.add(String(width/2,height-40,"Titulo"), name='title')
		self.title.fontSize = 18

		self.add(Legend(),name='legend')
		self.legend.x                   = width - 20
		self.legend.y                   = self.height/2
		self.legend.boxAnchor           = 'e'
		self.legend.subCols[1].align    = 'left'
		self.legend.subCols.rpad    	= 10
		self.legend.fontSize 			= 16
		self.legend.columnMaximum		= 10

		data                			= (9, 7, 6, 4, 2.5, 1.0)
		categories          			= ('A','B','C','D','E','F',)
		colors              			= [PCMYKColor(x,x-5,0,0) for x in (100,80,60,40,20,5)]
		self.chart.data     			= data
		# self.chart.simpleLabels 		= 0
		# self.chart.slices[0].label_width			= 20
		# self.chart.slices[0].label_height			= 20
		# self.chart.slices.fontSize = 14
		# self.chart.labels   = map(str, self.chart.data)
		self.legend.colorNamePairs = zip(colors, categories)
		for i, color in enumerate(colors): self.chart.slices[i].fillColor  = color

	def defineData(self, pData, pCategories, titulo):
		self.chart.data = pData
		self.title.text = titulo
		# colorSteps = [i for i in range(5,100,95/len(pData))]
		colors = [v for k,v in getAllNamedColors().iteritems()]
		self.legend.colorNamePairs = zip(colors, pCategories)

		for i, color in enumerate(colors):
			self.chart.slices[i].fillColor  = color
		self.legend.colorNamePairs = [(self.chart.slices[i].fillColor, (pCategories[i], '%0.2f' % self.chart.data[i])) for i in range(len(self.chart.data))]

	def secondTitle(self, title):
		self.add(String(self.width/2,self.height-40-self.title.fontSize*1.2,title), name='titletwo')
		self.titletwo.fontSize = self.title.fontSize

class myVerticalBarChart(Drawing):
	def __init__(self, width=550, height=300, *args, **kw):

		Drawing.__init__(self,width,height,*args,**kw)

		self.add(VerticalBarChart(), name='bar')
		self.bar.data             			= [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]
		self.bar.width                      = 300
		self.bar.height                     = 250
		self.bar.x                          = 60
		self.bar.y                          = 15
		self.bar.barSpacing                 = 5
		self.bar.groupSpacing               = 5
		self.bar.valueAxis.labels.fontName  = 'Helvetica'
		self.bar.valueAxis.labels.fontSize  = 14
		self.bar.valueAxis.forceZero        = 1
		self.bar.valueAxis.rangeRound       = 'both'
		self.bar.valueAxis.valueMax         = None#10#
		self.bar.valueAxis.visible			= 1
		self.bar.categoryAxis.categoryNames = ['Trayecto A','Trayecto B','Trayecto C','Trayecto D','Trayecto E','Trayecto F','Trayecto G','Trayecto H','Trayecto I','Trayecto J']
		self.bar.categoryAxis.labels.fillColor = None
		self.bar.categoryAxis.visible       = 1
		self.bar.categoryAxis.visibleTicks  = 0
		self.bar.strokeWidth                = 0.1
		self.bar.bars.strokeWidth           = 0.5
		n                                   = len(self.bar.data)
		colors = [v for k,v in getAllNamedColors().iteritems()]
		for i in range(n):
			self.bar.bars[i].fillColor		= colors[i]

		self.add(String(width/2,height-20,"Titulo"), name='title')
		self.title.fontSize = 18
		self.title.textAnchor='middle'

		self.add(Legend(),name="legend")
		self.legend.columnMaximum   = 10
		self.legend.fontName        = 'Helvetica'
		self.legend.fontSize        = self.bar.valueAxis.labels.fontSize
		self.legend.boxAnchor       = 'e'
		self.legend.x               = self.width - 20
		self.legend.y               = self.height/2
		self.legend.dx              = 8
		self.legend.dy              = 8
		self.legend.alignment       = 'right'
		self.legend.yGap            = 0
		self.legend.deltay          = 11
		# self.legend.dividerLines    = 1|2|4
		self.legend.subCols.rpad    = 10
		self.legend.dxTextSpace     = 5
		# self.legend.strokeWidth     = 0
		self.legend.dividerOffsY    = 6
		# self.legend.colEndCallout   = TotalAnnotator(rText='%.2f'%sum([x[0] for x in self.bar.data]), fontName='Helvetica-Bold', fontSize=self.legend.fontSize*1.1)
		self.legend.colorNamePairs  = [(self.bar.bars[i].fillColor, (self.bar.categoryAxis.categoryNames[i], '%0.2f' % self.bar.data[i][0])) for i in range(len(self.bar.data))]

	def defineData(self, pData, pCategories, titulo):
		self.bar.data = pData
		self.title.text = titulo
		self.bar.categoryAxis.categoryNames = pCategories
		colors = [v for k,v in getAllNamedColors().iteritems()]
		for i in range(len(pData)):
			self.bar.bars[i].fillColor		= colors[i]
		self.legend.colorNamePairs  = [(self.bar.bars[i].fillColor, (self.bar.categoryAxis.categoryNames[i], '%0.2f' % self.bar.data[i][0])) for i in range(len(self.bar.data))]

	def secondTitle(self, title):
		self.add(String(self.width/2,self.height-20-self.title.fontSize*1.2,title), name='titletwo')
		self.titletwo.fontSize = self.title.fontSize
		self.titletwo.textAnchor='middle'

class myPie3d(Drawing):
	def __init__(self, width=500, height=300, *args, **kw):
		Drawing.__init__(self,width,height,*args,**kw)
		self.add(Pie3d(), "chart")