import pandas as pd
import glob as glob
import numpy as np
# import matplotlib.pyplot as plt
import xml.etree.ElementTree
from xml.dom import minidom

data_dir  = '/home/nmoran/Dropbox/Apps/tapiriik'
first_date = '2017-05-01' # start back in may

files = glob.glob('%s/*.tcx' % data_dir)


#e = xml.etree.ElementTree.parse(files[0]).getroot()

class Activity(object):

    def __init__(self, path):
        self.path = path
        self.doc = minidom.parse(path)

    def activity_type(self):
        return self.doc.getElementsByTagName('Activity')[0].attributes['Sport'].value


    def total_distance(self):
        laps = self.doc.getElementsByTagName('Lap')
        return np.sum([float(x.getElementsByTagName('DistanceMeters')[0].firstChild.nodeValue) for x in laps])

# doc = minidom.parse(files[0])
# activities = doc.getElementsByTagName('Activity')

activities = [Activity(x) for x in files]
distances = [x.total_distance() for x in activities]