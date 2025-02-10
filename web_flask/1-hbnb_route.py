#!/usr/bin/python3
"""
Script that starts a Flask web application with two routes.
The application listens on 0.0.0.0, port 5000.
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Route handler for the root URL '/'.
    Returns: String 'Hello HBNB!'
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Route handler for '/hbnb'.
    Returns: String 'HBNB'
    """
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
