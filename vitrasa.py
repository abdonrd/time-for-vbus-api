# coding=utf-8

from suds.client import Client


class Vitrasa(object):
    WSDL_URL = 'http://sira.intecoingenieria.com/SWEstimacionParada.asmx?WSDL'

    def __init__(self):
        self.client = Client(url=self.WSDL_URL)

    def get_stops(self, latitude=None, longitude=None):
        pass

    def get_stop(self, stop_number):
        pass

    def get_stop_estimates(self, stop_number):
        pass


class Stop(object):
    def __init__(self, number, name, lng, lat, distance=None):
        self.number = number
        self.name = name
        self.location = {
            'lng': lng,
            'lat': lat
        }
        self.distance = distance


class Bus(object):
    def __init__(self, line, route, minutes):
        self.line = line
        self.route = route
        self.minutes = minutes
