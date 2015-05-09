# coding=utf-8

import os
import json
from xml.etree import ElementTree

from suds import WebFault
from suds.client import Client


WSDL_URL = 'http://sira.intecoingenieria.com/SWEstimacionParada.asmx?WSDL'


def get_stops():
    stops_data = json.load(open(
        os.path.join(os.path.dirname(__file__), 'vitrasa_stops.json')
    ))

    stops = []

    for stop_data in stops_data:
        stops.append(Stop(
            number=stop_data['number'],
            name=stop_data['name'],
            lng=stop_data['location']['lng'],
            lat=stop_data['location']['lat']
        ))

    return stops


def get_stops_around(latitude=None, longitude=None):
    client = Client(url=WSDL_URL)

    factory = client.factory.create('tns:BuscarParadas')
    factory.Latitud = latitude
    factory.Longitud = longitude

    try:
        response = client.service.BuscarParadas(factory)
    except WebFault:
        raise Error

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


def get_stop(stop_number):
    client = Client(url=WSDL_URL)

    factory = client.factory.create('tns:BuscarParadasIdParada')
    factory.IdParada = stop_number

    try:
        response = client.service.BuscarParadasIdParada(factory)
    except WebFault:
        raise Error

    response_encoded = response.encode('utf-8')

    tag_paradas = ElementTree.fromstring(response_encoded)
    tag_parada = tag_paradas.find('Parada')

    stop = Stop(
        number=int(tag_parada.get('idparada')),
        name=tag_parada.get('nombre'),
        lng=float(tag_parada.get('longitud')),
        lat=float(tag_parada.get('latitud'))
    )

    return stop


def get_stop_estimates(stop_number):
    client = Client(url=WSDL_URL)

    factory = client.factory.create('tns:EstimacionParadaIdParada')
    factory.IdParada = stop_number

    try:
        response = client.service.EstimacionParadaIdParada(factory)
    except WebFault:
        raise Error

    response_encoded = response.encode('utf-8')

    tag_newdataset = ElementTree.fromstring(response_encoded)

    buses = []

    for tag_estimaciones in tag_newdataset:
        buses.append(Bus(
            line=tag_estimaciones.find('Linea').text,
            route=tag_estimaciones.find('Ruta').text,
            minutes=int(tag_estimaciones.find('minutos').text)
        ))

    buses = sorted(buses, key=lambda bus: bus.minutes)

    return buses


class Error(Exception):
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

    def to_dict(self):
        data = {
            'number': self.number,
            'name': self.name,
            'location': self.location
        }

        if self.distance:
            data['distance'] = self.distance

        return data


class Bus(object):
    def __init__(self, line, route, minutes):
        self.line = line
        self.route = self.clean_route(route)
        self.minutes = minutes

    @staticmethod
    def clean_route(route):
        route = route.replace('*', '')

        if isinstance(route, unicode):
            if route in BUS_FIXED_ROUTES.iterkeys():
                route = BUS_FIXED_ROUTES[route]

        return route

    def to_dict(self):
        data = {
            'line': self.line,
            'route': self.route,
            'minutes': self.minutes
        }

        return data


BUS_FIXED_ROUTES = {
    u'A GUÃA': u'A GUÍA',
    u'ARAGÃ“N': u'ARAGÓN',
    u'ENCARNACIÃ“N por G. BARBÃ“N': u'ENCARNACIÓN por G. BARBÓN',
    u'ENCARNACIÃ“N por TRAV. DE VIGO': u'ENCARNACIÓN por TRAV. DE VIGO',
    u'ESTACION TREN por P. ESPAÃ‘A': u'ESTACION TREN por P. ESPAÑA',
    u'GARCIA BARBÃ“N': u'GARCIA BARBÓN',
    u'MATAMÃ': u'MATAMÁ',
    u'MUIÃ‘OS - SAIANS': u'MUIÑOS - SAIANS',
    u'MUIÃ‘OS': u'MUIÑOS',
    u'P. ESPAÃ‘A - P. AMERICA': u'P. ESPAÑA - P. AMERICA',
    u'PLAZA ESPAÃ‘A': u'PLAZA ESPAÑA',
    u'PRAZA AMÃ‰RICA': u'PRAZA AMÉRICA',
    u'PRAZA ESPAÃ‘A': u'PRAZA ESPAÑA',
    u'RÃOS': u'RÍOS'
}
