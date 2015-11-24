# coding=utf-8

from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.colors import *

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