from modules.account import Account
from utils.config import WETH_ABI, BASE_TOKENS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class WrapETH(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.weth_contract = self.get_contract(BASE_TOKENS['WETH'], WETH_ABI)
    
    @check_gas
    async def wrap_eth(
        self,
        min_amount: float,
        max_amount: float,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
        unwrap_eth: bool
    ):
        try:

            try:
                self.log_send('Firstly Unwrap $ETH.')
                unwrap_tx_status = await self.unwrap_eth()
                await async_sleep(5, 15, logs=False)
                if unwrap_tx_status:
                    return unwrap_tx_status
            except Exception as unwrap_err:
                self.log_send(f'Error in module «{__class__.__name__}». Can not unwrap ETH: {unwrap_err}', status='error')

            self.log_send('Wrap $ETH.')

            if all_amount:
                amount_wei, _ = await self.get_percent_amount('ETH', min_percent, max_percent)
            else:
                amount_wei, _ = await self.get_random_amount('ETH', min_amount, max_amount, decimal)
            
            tx_data = await self.get_tx_data(value=amount_wei)
            
            tx = await self.weth_contract.functions.deposit().build_transaction(tx_data)
            
            tx_status = await self.execute_transaction(tx)
            
            if unwrap_eth:
                await async_sleep(5, 15, logs=False)
                return await self.unwrap_eth()
            else:
                return tx_status

        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False

    @check_gas
    async def unwrap_eth(self):
        self.log_send('Unwrap all $WETH.')

        _, balance_wei = await self.get_balance(BASE_TOKENS['WETH'])

        tx_data = await self.get_tx_data()

        tx = await self.weth_contract.functions.withdraw(balance_wei).build_transaction(tx_data)

        return await self.execute_transaction(tx)