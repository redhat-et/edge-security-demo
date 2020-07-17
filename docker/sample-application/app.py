import os

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    pod_ip = os.getenv('POD_IP')
    if pod_ip is None:
        pod_ip = '<unknown>'

    node_ip = os.getenv('NODE_IP')
    if node_ip is None:
        node_ip = '<unknown>'

    return 'Howdy folks! 👍\nPOD IP: %s\nNODE IP: %s\n' % (pod_ip, node_ip)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
