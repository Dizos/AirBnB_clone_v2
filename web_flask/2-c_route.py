#!/usr/bin/python3
"""
Script that starts a Flask web application with three routes.
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


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Route handler for '/c/<text>'.
    Displays 'C' followed by the value of text.
    Replace underscore symbols with spaces.
    Returns: String 'C <text>'
    """
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
