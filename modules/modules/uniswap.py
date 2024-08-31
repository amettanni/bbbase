import time

from hexbytes import HexBytes

from modules.account import Account
from utils.config import (
    UNISWAP_CONTRACTS, BASE_TOKENS, UNISWAP_QUOTER_ABI, UNISWAP_ROUTER_ABI
)
from settings import MainSettings as SETTINGS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class UniSwap(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.router_contract = self.get_contract(UNISWAP_CONTRACTS["router"], UNISWAP_ROUTER_ABI)
        self.quoter_contract = self.get_contract(UNISWAP_CONTRACTS["quoter"], UNISWAP_QUOTER_ABI)

    def get_path(self, from_token: str, to_token: str):
        from_token_bytes = HexBytes(BASE_TOKENS[from_token]).rjust(20, b'\0')
        to_token_bytes = HexBytes(BASE_TOKENS[to_token]).rjust(20, b'\0')
        fee_bytes = (500).to_bytes(3, 'big')

        return from_token_bytes + fee_bytes + to_token_bytes
        
    async def get_min_amount_out(self, path: bytes, amount_in_wei: int):
        min_amount_out, _, _, _ = await self.quoter_contract.functions.quoteExactInput(
            path,
            amount_in_wei
        ).call()

        return int(min_amount_out - (min_amount_out / 100 * SETTINGS.SLIPPAGE))

    @check_gas
    async def swap(
        self,
        from_token: str,
        to_token: str,
        min_amount: float,
        max_amount: float,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
        swap_reverse: bool,
        first_swap: bool = True
    ):
        try:

            if first_swap:
                try:
                    first_tx_status = await self.swap(to_token, from_token, 0.01, 0.01, decimal, True, 100, 100, False, False)
                    await async_sleep(5, 15, logs=False)
                except Exception as e:
                    self.log_send(f'Error in module «{__class__.__name__}» while making first reverse swap: {e}', status='error')

                if first_tx_status:
                    return first_tx_status


            self.log_send(f'{from_token} -> {to_token} | Swap on UniSwap.')

            if all_amount:
                amount_wei, _ = await self.get_percent_amount(from_token, min_percent, max_percent)
                self.log_send(f'Amount to swap (%) «{__class__.__name__}»: {amount_wei}', status='info')   
            else:
                amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimal)
                self.log_send(f'Amount to swap «{__class__.__name__}»: {amount_wei}', status='info')
            
            path = self.get_path(from_token, to_token)
            min_amount_out = await self.get_min_amount_out(path, amount_wei)
            
            if from_token != 'ETH':
                await self.approve(amount_wei, BASE_TOKENS[from_token], UNISWAP_CONTRACTS['router'])
            
            tx_data = self.router_contract.encodeABI(
                fn_name='exactInput',
                args=[(
                    path,
                    self.address if to_token != 'ETH' else '0x0000000000000000000000000000000000000002',
                    amount_wei,
                    min_amount_out
                )]
            )
            
            full_data = [tx_data]
            
            if from_token == 'ETH' or to_token == 'ETH':
                tx_additional_data = self.router_contract.encodeABI(
                    fn_name='unwrapWETH9' if from_token != 'ETH' else 'refundETH',
                    args=[
                        min_amount_out,
                        self.address
                    ] if from_token != 'ETH' else None
                )

                full_data.append(tx_additional_data)
            
            tx_params = await self.get_tx_data(value=amount_wei if from_token == 'ETH' else 0)
            
            tx = await self.router_contract.functions.multicall(full_data).build_transaction(tx_params)
            
            tx_status = await self.execute_transaction(tx)
            
            if swap_reverse:
                await async_sleep(5, 15, logs=False)
                return await self.swap(to_token, from_token, 0.01, 0.01, decimal, True, 100, 100, False)
            else:
                return tx_status

        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False