#!/usr/bin/python3
"""
Script that starts a Flask web application with six routes.
The application listens on 0.0.0.0, port 5000.
"""
from flask import Flask, render_template

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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Route handler for '/python/<text>'.
    Displays 'Python' followed by the value of text.
    Replace underscore symbols with spaces.
    Default text value is 'is cool'.
    Returns: String 'Python <text>'
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Route handler for '/number/<n>'.
    Displays 'n is a number' only if n is an integer.
    Returns: String '<n> is a number'
    """
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Route handler for '/number_template/<n>'.
    Displays an HTML page only if n is an integer.
    Returns: HTML page with the number inside H1 tag
    """
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
