# coding=utf-8

from flask import Flask, g, jsonify

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


if __name__ == '__main__':
    app.run()
