import json
from web3 import Web3
from solcx import compile_source

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    raise Exception("Ganache not connected")

account = w3.eth.accounts[0]

with open("../contracts/Voting.sol", "r") as file:
    contract_source_code = file.read()

compiled_sol = compile_source(
    contract_source_code,
    solc_version="0.8.17"
)

contract_id, contract_interface = compiled_sol.popitem()
bytecode = contract_interface["bin"]
abi = contract_interface["abi"]

Voting = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = Voting.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt["contractAddress"]

with open("contract_data.json", "w") as f:
    json.dump({
        "address": contract_address,
        "abi": abi
    }, f)

print("Deployed at:", contract_address)