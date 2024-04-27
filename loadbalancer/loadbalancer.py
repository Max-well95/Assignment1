from flask import Flask, request, jsonify
import random
import string
import zlib

app = Flask(__name__)

class ConsistentHashMap:
    def __init__(self, N, M, K):
        self.N = N  # Number of server containers
        self.M = M  # Total number of slots in hash map
        self.K = K  # Number of virtual servers for each server container
        self.hash_map = {}  # Initialize hash map

    def add_server(self, server_address):
        # Add server to hash map with virtual server replicas
        for j in range(self.K):
            virtual_server = f"{server_address}_{j}"
            slot = self.hash_function(virtual_server)
            self.hash_map[slot] = server_address

    def remove_server(self, server_address):
        # Remove server and its virtual server replicas from hash map
        for j in range(self.K):
            virtual_server = f"{server_address}_{j}"
            slot = self.hash_function(virtual_server)
            del self.hash_map[slot]

    def get_assigned_server(self, request_path):
        # Get server assigned to handle request
        slot = self.hash_function(request_path)
        while slot not in self.hash_map:
            slot = (slot + 1) % self.M
        return self.hash_map[slot]

    def hash_function(self, key):
        # Implement CRC32 hash function
        hash_value = zlib.crc32(key.encode())
        return hash_value % self.M

# Initialize consistent hash map
N = 3  # Number of server containers
M = 512  # Total number of slots in hash map
K = 92  # Number of virtual servers for each server container
hash_map = ConsistentHashMap(N, M, K)

# Placeholder for managed replicas
replicas = ["Server 1", "Server 2", "Server 3"]

# Endpoint to get the status of replicas
@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

# Endpoint to add new server instances
@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    if len(hostnames) != n:
        return jsonify({"error": "Number of hostnames does not match the number of instances to add"}), 400

    # Add servers to consistent hash map
    for hostname in hostnames:
        hash_map.add_server(hostname)

    replicas.extend(hostnames)
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

# Endpoint to remove server instances
@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    hostnames = data.get('hostnames', [])
    for hostname in hostnames:
        if hostname in replicas:
            replicas.remove(hostname)
            hash_map.remove_server(hostname)
    return jsonify({"message": {"N": len(replicas), "replicas": replicas}, "status": "successful"}), 200

# Endpoint to route requests to server replicas
@app.route('/<path>', methods=['GET'])
def route_request(path):
    # Route request using consistent hash map
    assigned_server = hash_map.get_assigned_server(path)
    return jsonify({"message": f"Request routed to {assigned_server}"}), 200

if __name__ == '__main__':
    app.run(port=5000)


