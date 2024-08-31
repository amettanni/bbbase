import random
import time
from typing import Union
from aiohttp import ClientSession
import eth_account
from loguru import logger
from web3 import AsyncWeb3
from web3.middleware import async_geth_poa_middleware
from web3.types import TxParams
from web3.exceptions import TransactionNotFound

from settings import MainSettings as SETTINGS
from utils.config import ERC20_ABI, MAX_APPROVE, BASE_TOKENS, RPC
from utils.utils import async_sleep


class Account:
    def __init__(self, account_id: int, private_key: str, proxy: str | None, chain: str = 'base') -> None:
        self.account_id = account_id
        self.private_key = private_key
        
        self.chain_name = chain
        self.chain_id = RPC[chain]['chain_id']
        self.explorer = RPC[chain]['explorer']
        self.rpc = RPC[chain]['rpc']
        self.eip_1559_support = True

        self.proxy = f"http://{proxy}" if proxy else ""
        self.request_kwargs = {'proxy': f'http://{proxy}'} if proxy else {}
            
        self.w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(self.rpc),
            middlewares=[async_geth_poa_middleware],
            request_kwargs=self.request_kwargs
        )

        self.address = eth_account.Account.from_key(private_key).address

        self.LOG_LEVELS = {
            'info'      : logger.info,
            'success'   : logger.success,
            'error'     : logger.error,
            'warning'   : logger.warning,
            'debug'     : logger.debug
        }
    
    async def make_request(
        self, method: str = 'GET', url: str = None, headers: dict = None,
        params: dict = None, data: str = None, json: dict = None
    ):
        async with ClientSession() as session:
            async with session.request(
                method=method, url=url, headers=headers, data=data, params=params, json=json
            ) as response:
                data = await response.json()
                if response.status == 200:
                    return data
                else:
                    await async_sleep(1, 3, logs=False)
                    await self.make_request(method=method, url=url, headers=headers, data=data, params=params, json=json)
    
    def log_send(self, msg: str, status: str = 'info'):
        self.LOG_LEVELS[status](f'Account №{self.account_id} | {self.address} | {msg}')
    
    async def get_token_info(self, contract_address: str) -> Union[int, str, int]:
        contract_address = self.w3.to_checksum_address(contract_address)
        contract = self.get_contract(contract_address)
        
        symbol = await contract.functions.symbol().call()
        decimal = await contract.functions.decimals().call()
        balance_wei = await contract.functions.balanceOf(self.address).call()
        
        return balance_wei, symbol, decimal
    
    async def get_balance(self, contract_address: str = None) -> Union[float, int]:
        if contract_address:
            balance_wei, _, decimal = await self.get_token_info(contract_address)
            print(balance_wei, _, decimal)
            balance = balance_wei / 10 ** decimal
        else:
            balance_wei = await self.w3.eth.get_balance(self.address)
            balance = balance_wei / 10 ** 18

        return balance, balance_wei
    
    async def get_random_amount(self, token: str, min_amount: float, max_amount: float, decimal: int):
        amount = round(random.uniform(min_amount, max_amount), decimal)
        
        if token == 'ETH':
            amount_wei = self.w3.to_wei(amount, 'ether')
        
        else:
            _, _, decimal = await self.get_token_info(BASE_TOKENS[token])
            amount_wei = int(amount * 10 ** decimal)
        
        return amount_wei, amount
    
    async def get_percent_amount(self, token: str, min_percent: int, max_percent: int) -> Union[float, int]:
        if token == 'ETH':
            balance_wei = await self.w3.eth.get_balance(self.address)
            balance = balance_wei / 10 ** 18
        else:
            balance, balance_wei = await self.get_balance(BASE_TOKENS[token])
        
        random_percent = random.randint(min_percent, max_percent) / 100
        
        amount_wei = int(balance_wei * random_percent)
        amount = balance * random_percent
        
        return amount_wei, amount
    
    def get_contract(self, contract_address: str, abi=None):
        contract_address = self.w3.to_checksum_address(contract_address)

        abi = ERC20_ABI if abi is None else abi

        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        return contract
    
    async def get_allowance(self, token_address: str, contract_address: str):
        token_address = self.w3.to_checksum_address(token_address)
        contract_address = self.w3.to_checksum_address(contract_address)
        
        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = await contract.functions.allowance(self.address, contract_address).call()
        
        return amount_approved
    
    async def approve(self, amount_wei: int, token_address: str, contract_address: str):
        token_address = self.w3.to_checksum_address(token_address)
        contract_address = self.w3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)

        allowance_amount = await self.get_allowance(token_address, contract_address)

        if amount_wei > allowance_amount:
            self.log_send('Make approve.')

            tx_data = await self.get_tx_data()

            tx = await contract.functions.approve(contract_address, MAX_APPROVE).build_transaction(tx_data)

            await self.execute_transaction(tx)

            await async_sleep(5, 15, logs=False)
    
    async def get_priority_fee(self):
        fee_history = await self.w3.eth.fee_history(25, 'latest', [20.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]
        
        divisor_priority = max(len(non_empty_block_priority_fees), 1)
        
        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

        return priority_fee
    
    async def get_tx_data(self, value: int = 0):
        tx = {
            'chainId': await self.w3.eth.chain_id,
            'from': self.address,
            'value': value,
            'nonce': await self.w3.eth.get_transaction_count(self.address)
        }

        if self.eip_1559_support:
            base_fee = await self.w3.eth.gas_price
            max_priority_fee_per_gas = int(await self.get_priority_fee() * SETTINGS.GAS_MULTIPLAYER)
            max_fee_per_gas = int(base_fee + max_priority_fee_per_gas * SETTINGS.GAS_MULTIPLAYER)

            if max_priority_fee_per_gas > max_fee_per_gas:
                max_priority_fee_per_gas = int(max_fee_per_gas * 0.95)

            tx['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx['maxFeePerGas'] = max_fee_per_gas
            tx['type'] = '0x2'
        else:
            tx['gasPrice'] = int(await self.w3.eth.gas_price * SETTINGS.GAS_MULTIPLAYER)

        return tx

    async def sign(self, transaction):
        gas = await self.w3.eth.estimate_gas(transaction)
        gas = int(gas * SETTINGS.GAS_MULTIPLAYER)

        transaction.update({'gas': gas})

        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        return signed_tx

    async def send_raw_transaction(self, signed_txn):
        txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash

    async def wait_until_tx_finished(self, hash: str):
        attempts_count = 0

        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get('status')

                if status == 1:
                    self.log_send(f'{self.explorer}{hash.hex()} successfully!', status='success')
                    return True
                elif status is None:
                    await async_sleep(10, 10, logs=False)
                else:
                    self.log_send(f'{self.explorer}{hash.hex()} transaction failed!', status='error')
                    return False
            
            except TransactionNotFound:
                if attempts_count >= 30:
                    self.log_send(f'{self.explorer}{hash.hex()} transaction not found!', status='warning')
                    return False
                
                attempts_count += 1
                await async_sleep(10, 10, logs=False)
    
    async def execute_transaction(self, tx: TxParams):
        signed_tx = await self.sign(tx)
        tx_hash = await self.send_raw_transaction(signed_tx)

        return await self.wait_until_tx_finished(tx_hash)