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
