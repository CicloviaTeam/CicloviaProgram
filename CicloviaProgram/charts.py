from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.lib.colors import darkcyan, blue, cyan, red
import traceback

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