from web3 import Web3
import time

class TokenEventProcessor:
	def __init__(self, rpc_url, token_address, private_key, whitelist_eoa, whitelist_contracts, contract_abi):
		self.web3 = Web3(Web3.HTTPProvider(rpc_url))

		if not self.web3.is_connected():
			raise ConnectionError("failed")

		self.token_address = token_address
		self.private_key = private_key
		self.account = self.web3.eth.account.from_key(private_key)

		self.whitelist_eoa = whitelist_eoa
		self.whitelist_contracts = whitelist_contracts

		assert self.account.address in self.whitelist_eoa, "account not in whitelist"

		self.contract = self.web3.eth.contract(address=self.token_address, abi=contract_abi)

		# event Transfer
		self.event_signature_hash = "0x" + self.web3.keccak(text="Transfer(address,address,uint256)").hex()
		self.last_block = self.web3.eth.block_number

	def process_event(self, log):
		event = self.contract.events.Transfer().process_log(log)
		from_address = event["args"]["from"]
		to_address = event["args"]["to"]

		print(f"Transfer: from {from_address}, to {to_address}")

		if (from_address in self.whitelist_contracts) and (to_address not in self.whitelist_contracts) and (
				to_address not in self.whitelist_eoa):
			txn = self.contract.functions.setBlacklist(to_address).build_transaction({
				'from': self.account.address,
				'gas': 50000,
				'gasPrice': self.web3.to_wei('5', 'gwei'),
				'nonce': self.web3.eth.get_transaction_count(self.account.address),
				'chainId': 56
			})

			signed_txn = self.web3.eth.account.sign_transaction(txn, self.private_key)
			txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
			print(f"Transaction sent, hash: {txn_hash.hex()}")

	def main_loop(self):
		while True:
			current_block = self.web3.eth.block_number
			if current_block > self.last_block:
				for block in range(self.last_block + 1, current_block + 1):
					print(f"{block}")
					self.last_block = block
					logs = self.web3.eth.get_logs({
						"fromBlock": block,
						"toBlock": block,
						"address": self.token_address,
						"topics": [self.event_signature_hash]
					})
					for log in logs:
						self.process_event(log)
			time.sleep(1)


if __name__ == "__main__":
	rpc_url = 'https://rpc.ankr.com/bsc'
	token_address = "0xf4F7d171430EA223424234288490f0FC3118"
	private_key = "9d0d7eb08d3ce320818fae9524422def28848b3648e2fc39"
	whitelist_eoa = ["0xF998b40EE52cB062342344fe6be096C211"]
	whitelist_contracts = ["0x10ED43C718714e242448B54704E256024E",
	                       "0x1A0A18AC4BECDDbd63234321A73d8927E416",
	                       "0xc2F52B4B1Ec6523426bDe7E8131910"]
	true = True
	false = False
	contract_abi = [{"type":"constructor","inputs":[{"name":"_name","type":"string","internalType":"string"},{"name":"_symbol","type":"string","internalType":"string"},{"name":"_totalSupply","type":"uint256","internalType":"uint256"}],"stateMutability":"nonpayable"},{"type":"function","name":"allowance","inputs":[{"name":"owner","type":"address","internalType":"address"},{"name":"spender","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"approve","inputs":[{"name":"spender","type":"address","internalType":"address"},{"name":"amount","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"balanceOf","inputs":[{"name":"account","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"blacklisted","inputs":[{"name":"","type":"address","internalType":"address"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"view"},{"type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint8","internalType":"uint8"}],"stateMutability":"view"},{"type":"function","name":"decreaseAllowance","inputs":[{"name":"spender","type":"address","internalType":"address"},{"name":"subtractedValue","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"increaseAllowance","inputs":[{"name":"spender","type":"address","internalType":"address"},{"name":"addedValue","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"name","inputs":[],"outputs":[{"name":"","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"setBlacklist","inputs":[{"name":"to","type":"address","internalType":"address"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"symbol","inputs":[],"outputs":[{"name":"","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"totalSupply","inputs":[],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"transfer","inputs":[{"name":"to","type":"address","internalType":"address"},{"name":"amount","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"transferFrom","inputs":[{"name":"from","type":"address","internalType":"address"},{"name":"to","type":"address","internalType":"address"},{"name":"amount","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"event","name":"Approval","inputs":[{"name":"owner","type":"address","indexed":true,"internalType":"address"},{"name":"spender","type":"address","indexed":true,"internalType":"address"},{"name":"value","type":"uint256","indexed":false,"internalType":"uint256"}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"name":"from","type":"address","indexed":true,"internalType":"address"},{"name":"to","type":"address","indexed":true,"internalType":"address"},{"name":"value","type":"uint256","indexed":false,"internalType":"uint256"}],"anonymous":false}]

	processor = TokenEventProcessor(rpc_url, token_address, private_key, whitelist_eoa, whitelist_contracts, contract_abi)
	processor.main_loop()
