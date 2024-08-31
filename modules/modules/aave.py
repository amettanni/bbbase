from modules.account import Account
from utils.config import AAVE_CONTRACTS, AAVE_ABI
from utils.utils import async_sleep
from utils.wrappers import check_gas
from settings import MainSettings as SETTINGS


class Aave(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.aave_contract = self.get_contract(AAVE_CONTRACTS['main'], AAVE_ABI)
        self.aave_weth = self.get_contract(AAVE_CONTRACTS['aave_weth'])
    
    async def get_deposit_amount(self):
        amount = await self.aave_weth.functions.balanceOf(self.address).call()
        return amount

    @check_gas
    async def deposit(
        self,
        min_amount: float,
        max_amount: float,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
        withdraw: bool
    ):
        try:
            await self.withdraw()
        except Exception as e:
            pass
        try:
            self.log_send(f'Deposit on Aave.')

            if all_amount:
                amount_wei, _ = await self.get_percent_amount('ETH', min_percent, max_percent)
            else:
                amount_wei, _ = await self.get_random_amount('ETH', min_amount, max_amount, decimal)
            
            tx_data = await self.get_tx_data(value=amount_wei)
            
            tx = await self.aave_contract.functions.depositETH(
                self.w3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
                self.address,
                0
            ).build_transaction(tx_data)
            
            tx_status = await self.execute_transaction(tx)
            
            if withdraw:
                await async_sleep(SETTINGS.LANDINGS_SLEEP[0], SETTINGS.LANDINGS_SLEEP[1], logs=False)
                return await self.withdraw()
            else:
                return tx_status
        
        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False
    
    @check_gas
    async def withdraw(self):
        try:
            amount_wei = await self.get_deposit_amount()
            
            if amount_wei > 0:
                self.log_send('Make withdraw from Aave.')

                await self.approve(amount_wei, "0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7", AAVE_CONTRACTS['main'])

                tx_data = await self.get_tx_data()

                tx = await self.aave_contract.functions.withdrawETH(
                    self.w3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98d1c5"),
                    amount_wei,
                    self.address
                ).build_transaction(tx_data)

                return await self.execute_transaction(tx)

            else:
                self.log_send(f'Deposit on Aave not found.', status='error')
                return False
        
        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False