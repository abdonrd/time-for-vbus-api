# coding=utf-8

from xml.etree import ElementTree

from suds import WebFault
from suds.client import Client


class Vitrasa(object):
    class Error(Exception):
        pass

    WSDL_URL = 'http://sira.intecoingenieria.com/SWEstimacionParada.asmx?WSDL'

    def __init__(self):
        self.client = Client(url=self.WSDL_URL)

    def get_stops(self, latitude=None, longitude=None):
        if latitude and longitude:
            factory = self.client.factory.create('tns:BuscarParadas')
            factory.Latitud = latitude
            factory.Longitud = longitude

            try:
                response = self.client.service.BuscarParadas(factory)
            except WebFault:
                raise self.Error

            response_encoded = response.encode('utf-8')

            tag_paradas = ElementTree.fromstring(response_encoded)

            stops = []

            for tag_parada in tag_paradas:
                stops.append(Stop(
                    number=int(tag_parada.get('idparada')),
                    name=tag_parada.get('nombre'),
                    lng=float(tag_parada.get('longitud')),
                    lat=float(tag_parada.get('latitud')),
                    distance=float(tag_parada.get('distancia'))
                ))

            stops = sorted(stops, key=lambda stop: stop.distance)

            return stops

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
