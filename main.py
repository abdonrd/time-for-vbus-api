# coding=utf-8

from flask import Flask, abort, g, jsonify, request
from flask.ext.cors import CORS

import vitrasa


app = Flask(__name__)
JSONIFY_PRETTYPRINT_REGULAR = False

cors = CORS(app)


def create_error_response(error):
    response = {
        'error': {
            'code': error.code,
            'message': error.name
        }
    }

    return jsonify(response), error.code


@app.errorhandler(400)
def bad_request(error):
    return create_error_response(error)


@app.errorhandler(404)
def page_not_found(error):
    return create_error_response(error)


@app.errorhandler(500)
def internal_server_error(error):
    return create_error_response(error)


@app.route('/stops', methods=['GET'])
def get_stops():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            stops = vitrasa.get_stops_around(latitude, longitude)
        except (ValueError, vitrasa.Error):
            abort(400)

        stops = sorted(stops, key=lambda stop: stop.distance)
    else:
        try:
            stops = vitrasa.get_stops()
        except vitrasa.Error:
            abort(400)

    return jsonify({
        'stops': [stop.to_dict() for stop in stops]
    })


@app.route('/stops/<stop_number>', methods=['GET'])
def get_stop(stop_number):
    try:
        stop = vitrasa.get_stop(stop_number)
    except vitrasa.Error:
        abort(400)

    return jsonify(stop.to_dict())


@app.route('/stops/<stop_number>/estimates', methods=['GET'])
def get_stop_estimates(stop_number):
    try:
        buses = vitrasa.get_stop_estimates(stop_number)
    except vitrasa.Error:
        abort(400)

    return jsonify({
        'buses': [bus.to_dict() for bus in buses]
    })


if __name__ == '__main__':
    app.run()
