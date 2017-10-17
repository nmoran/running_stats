import pandas as pd
import glob as glob
import numpy as np
# import matplotlib.pyplot as plt
import xml.etree.ElementTree
from xml.dom import minidom

#e = xml.etree.ElementTree.parse(files[0]).getroot()
def get_first_child_value(doc, tag, sub_tag=None):
    try:
        if sub_tag is None:
            return doc.getElementsByTagName(tag)[0].firstChild.nodeValue
        else:
            return doc.getElementsByTagName(tag)[0].getElementsByTagName(sub_tag)[0].firstChild.nodeValue
    except:
        return 0.0


class TrackPoint(object):

    def __init__(self, doc):
        self.doc = doc
        self.time = pd.to_datetime(get_first_child_value(doc, 'Time'))
        self.altitude = float(get_first_child_value(doc, 'AltitudeMeters'))
        self.distance = float(get_first_child_value(doc, 'DistanceMeters'))
        self.heart_rate = float(get_first_child_value(doc, 'HeartRateBpm', 'Value'))
        self.speed = float(get_first_child_value(doc, 'Speed'))
        self.cadence = float(get_first_child_value(doc, 'RunCadence'))

    def get_attributes(self):
        return {'time': self.time, 'altitude': self.altitude, 'distance': self.distance,
                'heart_rate': self.heart_rate, 'speed': self.speed, 'cadence': self.cadence}


class Lap(object):

    def __init__(self, doc):
        self.doc = doc

    def distance_meters(self):
        return float(self.doc.getElementsByTagName('DistanceMeters')[0].firstChild.nodeValue)

    def track_points(self):
        return pd.DataFrame([TrackPoint(x).get_attributes() for x in self.doc.getElementsByTagName('Trackpoint')])


class Activity(object):

    def __init__(self, path):
        self.path = path
        self.doc = minidom.parse(path)
        self.track_points = None
        self.laps = None

    def activity_type(self):
        return self.doc.getElementsByTagName('Activity')[0].attributes['Sport'].value

    def total_distance_meters(self):
        return np.sum([x.distance_meters() for x in self.get_laps()])

    def get_laps(self):
        if self.laps is None:
            self.laps = [Lap(x) for x in self.doc.getElementsByTagName('Lap')]
        return self.laps

    def get_all_track_points(self):
        if self.track_points is None:
            self.track_points = pd.concat(x.track_points() for x in self.get_laps()).reset_index()
        return self.track_points

    def start_time(self):
        df = self.get_all_track_points()
        return df['time'][0]

    def average_pace(self):
        return pd.Timedelta(1000/np.mean(self.get_all_track_points()['speed']), unit='s')

    def average_heart_rate(self):
        return np.mean(self.get_all_track_points()['heart_rate'])


if __name__ == '__main__':
    data_dir  = '/home/nmoran/Dropbox/Apps/tapiriik'
    first_date = '2017-05-01' # start back in may

    files = glob.glob('%s/*.tcx' % data_dir)

    activities = [Activity(x) for x in files]
    distances = [x.total_distance() for x in activities]
