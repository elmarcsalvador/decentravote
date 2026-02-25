import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("contract_data.json") as f:
    contract_data = json.load(f)

contract = w3.eth.contract(
    address=w3.to_checksum_address(contract_data["address"]),
    abi=contract_data["abi"]
)

accounts = list(w3.eth.accounts)
admin_account = accounts[0]

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["evoting"]
voters = db["voters"]


# ------------------------
# Register Voter
# ------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    wallet = data.get("wallet")

    if not name or not wallet:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    if voters.find_one({"wallet": wallet}):
        return jsonify({"success": False, "message": "Already registered"}), 400

    voters.insert_one({
        "name": name,
        "wallet": wallet,
        "has_voted": False
    })

    return jsonify({"success": True, "message": "Voter registered successfully"})


# ------------------------
# Add Candidate
# ------------------------
@app.route("/add_candidate", methods=["POST"])
def add_candidate():
    name = request.json.get("name")

    tx = contract.functions.addCandidate(name).transact({
        "from": admin_account
    })
    w3.eth.wait_for_transaction_receipt(tx)

    return jsonify({"success": True, "message": "Candidate added"})


# ------------------------
# Get Candidates
# ------------------------
@app.route("/candidates")
def get_candidates():
    total = contract.functions.candidateCount().call()
    result = []

    for i in range(1, total + 1):
        candidate = contract.functions.candidates(i).call()
        result.append({
            "id": candidate[0],
            "name": candidate[1],
            "votes": candidate[2]
        })

    return jsonify(result)


# ------------------------
# Vote
# ------------------------
@app.route("/vote", methods=["POST"])
def vote():
    wallet = request.json.get("wallet")
    candidate_id = int(request.json.get("candidate_id"))

    voter = voters.find_one({"wallet": wallet})

    if not voter:
        return jsonify({"success": False, "message": "Not registered"}), 400

    if voter["has_voted"]:
        return jsonify({"success": False, "message": "Already voted"}), 400

    tx = contract.functions.vote(candidate_id).transact({
        "from": wallet
    })
    w3.eth.wait_for_transaction_receipt(tx)

    voters.update_one(
        {"wallet": wallet},
        {"$set": {"has_voted": True}}
    )

    return jsonify({"success": True, "message": "Vote cast successfully"})

# Add this underneath your existing routes in app.py

# ------------------------
# Admin Login
# ------------------------
@app.route("/admin_login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Hardcoded credentials for demonstration
    if username == "admin" and password == "admin123":
        return jsonify({"success": True, "message": "Login successful"})
    
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# ------------------------
# Candidate Login & Score
# ------------------------
@app.route("/candidate_login", methods=["POST"])
def candidate_login():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    # Hardcoded prototype password for candidates
    if password != "cand123":
        return jsonify({"success": False, "message": "Invalid password"}), 401
    
    # Search the blockchain for the candidate's name
    total = contract.functions.candidateCount().call()
    for i in range(1, total + 1):
        candidate = contract.functions.candidates(i).call()
        if candidate[1].lower() == name.lower():
            return jsonify({
                "success": True, 
                "name": candidate[1], 
                "votes": candidate[2]
            })
            
    return jsonify({"success": False, "message": "Candidate not found on blockchain"}), 404

# ------------------------
# Get All Ganache Accounts
# ------------------------
@app.route("/accounts", methods=["GET"])
def get_accounts():
    # Returns the list of available Ganache accounts
    return jsonify({
        "success": True, 
        "accounts": accounts
    })


if __name__ == "__main__":
    app.run(port=5000)