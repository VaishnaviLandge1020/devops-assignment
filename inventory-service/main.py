from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)
# Enable Metrics & Tracing
metrics = PrometheusMetrics(app)
FlaskInstrumentor().instrument_app(app)

@app.route('/health')
def health():
    return jsonify({"service": "inventory-service", "status": "healthy"})

@app.route('/')
def home():
    return jsonify({"data": "This is the Inventory Service", "stock": 999})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)