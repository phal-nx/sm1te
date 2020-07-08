"""
Routing app for the client facing web server
"""

from flask import Flask, render_template, g, jsonify, request

app = Flask(__name__)


@app.route('/enrollment', methods=['POST'])
def enrollment():
    # Parse Request
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))