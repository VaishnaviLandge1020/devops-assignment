from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

metrics = PrometheusMetrics(app)

FlaskInstrumentor().instrument_app(app)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>System Status</title></head>
    <body style="background:#0d1117;color:#c9d1d9;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="background:#161b22;padding:40px;border-radius:12px;text-align:center;border:1px solid #30363d;">
            <h1 style="color:#2ea043;">OPERATIONAL</h1>
            <p>API Gateway v4 with Observability</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({"service": "api-gateway", "status": "healthy"})

@app.route('/orders')
def orders():
    return jsonify({"service": "orders-service", "data": "Order List Fetched"})

@app.route('/inventory')
def inventory():
    return jsonify({"service": "inventory-service", "data": "Inventory Count Fetched"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)