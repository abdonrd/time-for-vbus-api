# coding=utf-8

from flask import Flask, abort, g, jsonify, request

from vitrasa import Vitrasa


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
