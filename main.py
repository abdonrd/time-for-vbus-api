# coding=utf-8

from flask import Flask, g

from vitrasa import Vitrasa


app = Flask(__name__)


@app.before_request
def init_vitrasa():
    g.vitrasa = Vitrasa()


if __name__ == '__main__':
    app.run()
