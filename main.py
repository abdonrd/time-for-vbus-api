# coding=utf-8

from flask import Flask, abort, g, jsonify, request
from flask.ext.cors import CORS

from vitrasa import Vitrasa


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


@app.before_request
def init_vitrasa():
    g.vitrasa = Vitrasa()


@app.route('/stops', methods=['GET'])
def get_stops():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            abort(400)

    try:
        stops = g.vitrasa.get_stops(latitude, longitude)
    except Vitrasa.Error:
        abort(400)

    return jsonify({
        'stops': [stop.to_dict() for stop in stops]
    })


@app.route('/stops/<stop_number>', methods=['GET'])
def get_stop(stop_number):
    try:
        stop = g.vitrasa.get_stop(stop_number)
    except Vitrasa.Error:
        abort(400)

    return jsonify(stop.to_dict())


@app.route('/stops/<stop_number>/estimates', methods=['GET'])
def get_stop_estimates(stop_number):
    try:
        buses = g.vitrasa.get_stop_estimates(stop_number)
    except Vitrasa.Error:
        abort(400)

    return jsonify({
        'buses': [bus.to_dict() for bus in buses]
    })


if __name__ == '__main__':
    app.run()
