from flask import Flask, jsonify

app = Flask(__name__)


# Endpoint 1: Hello World
@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World"})


# Endpoint 2: Health Check
@app.route('/health')
def health_check():
    # Check the health of the application
    is_healthy = True

    if is_healthy:
        response = {"status": "success", "message": "Application is online"}
    else:
        response = {"status": "failure", "message": "Application is offline"}

    return jsonify(response)

    
if __name__ == '__main__':
    # Run on port 8080
    app.run(port=8080)
