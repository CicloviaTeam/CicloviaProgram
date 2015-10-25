# coding=utf-8
from xml.etree import ElementTree
from xml.dom import minidom

def printOrganizedXML(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")