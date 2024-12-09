from flask import Flask, request, jsonify
import json
import hashlib
import time

app = Flask(__name__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=1, previous_hash="0")  # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return self.last_block["index"] + 1

    def proof_of_work(self, previous_proof):
        proof = 0
        while not self.valid_proof(previous_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(previous_proof, proof):
        guess = f"{previous_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        return self.chain[-1]

blockchain = Blockchain()

@app.route("/mine", methods=["GET"])
def mine():
    previous_block = blockchain.last_block
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = hashlib.sha256(json.dumps(previous_block).encode()).hexdigest()
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "New block mined",
        "block": block
    }
    return jsonify(response), 200

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values", 400
    index = blockchain.add_transaction(values["sender"], values["recipient"], values["amount"])
    return jsonify({"message": f"Transaction will be added to Block {index}"}), 201

@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
