# app.py
from flask import Flask
from prometheus_client import start_http_server, Counter
import logging
from logstash import LogstashHandler

app = Flask(__name__)

# Create a counter metric to track requests
REQUESTS = Counter('http_requests_total', 'Total number of HTTP requests')

# Set up logging to Logstash
logger = logging.getLogger('python-app')
logger.setLevel(logging.INFO)
logstash_handler = LogstashHandler('logstash', 5044)  # Default Logstash port
logger.addHandler(logstash_handler)

@app.route('/')
def hello():
    REQUESTS.inc()  # Increment the request counter
    logger.info('Request received to / endpoint')
    return "Hello, World!"

if __name__ == '__main__':
    start_http_server(8000)  # Prometheus will scrape this port for metrics
    app.run(host='0.0.0.0', port=5000)
