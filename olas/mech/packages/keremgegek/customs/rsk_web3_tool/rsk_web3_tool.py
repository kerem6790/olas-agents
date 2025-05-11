# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2025 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""The implementation of the rsk_web3_tool tool."""

from web3 import Web3
from eth_account import Account
from eth_typing import Address
from eth_utils import to_checksum_address


def run(*args, **kwargs):
    """The callable for the rsk_web3_tool tool."""
    action = kwargs.get("action")
    rpc_url = kwargs.get("rpc_url")
    private_key = kwargs.get("private_key")

    if not rpc_url:
        return "Error: RPC URL is required"

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        return "Error: Could not connect to RSK network"

    if action == "get_address":
        if not private_key:
            return "Error: Private key is required"
        account = Account.from_key(private_key)
        return account.address

    elif action == "call_contract":
        contract_address = kwargs.get("contract_address")
        abi = kwargs.get("abi")
        function_name = kwargs.get("function_name")
        function_args = kwargs.get("function_args", [])

        if not all([contract_address, abi, function_name]):
            return "Error: contract_address, abi, and function_name are required"

        contract = w3.eth.contract(
            address=to_checksum_address(contract_address),
            abi=abi
        )

        if not private_key:
            # Read-only call
            result = contract.functions[function_name](*function_args).call()
            return str(result)

        # Write call
        account = Account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(account.address)
        gas_price = w3.eth.gas_price
        chain_id = w3.eth.chain_id

        tx = contract.functions[function_name](*function_args).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': gas_price,
            'chainId': chain_id
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return w3.to_hex(tx_hash)

    elif action == "erc20_balance":
        contract_address = kwargs.get("contract_address")
        if not contract_address:
            return "Error: contract_address is required"

        contract = w3.eth.contract(
            address=to_checksum_address(contract_address),
            abi=[{
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }]
        )

        if not private_key:
            return "Error: Private key is required"
        account = Account.from_key(private_key)
        balance = contract.functions.balanceOf(account.address).call()
        return str(balance)

    elif action == "erc20_transfer":
        contract_address = kwargs.get("contract_address")
        to_address = kwargs.get("to_address")
        amount = kwargs.get("amount")

        if not all([contract_address, to_address, amount, private_key]):
            return "Error: contract_address, to_address, amount, and private_key are required"

        contract = w3.eth.contract(
            address=to_checksum_address(contract_address),
            abi=[{
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            }]
        )

        account = Account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(account.address)
        gas_price = w3.eth.gas_price
        chain_id = w3.eth.chain_id

        tx = contract.functions.transfer(
            to_checksum_address(to_address),
            int(amount)
        ).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': gas_price,
            'chainId': chain_id
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return w3.to_hex(tx_hash)

    else:
        return f"Error: Unknown action {action}"

