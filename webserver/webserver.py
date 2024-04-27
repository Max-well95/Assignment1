from flask import Flask, jsonify

app = Flask(__name__)

# Define /home endpoint
@app.route('/home', methods=['GET'])
def home():
    return jsonify({
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    })

# Define /heartbeat endpoint
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200


if __name__ == '__main__':
    app.run(port=5000)

