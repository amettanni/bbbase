from modules.account import Account
from modules.modules.okx_withdraw import OKXWithdraw


class OKXTopUp(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.str_proxy = proxy

    async def calculate_amount(self, amount: float):
        
        _, balance_wei = await self.get_balance()
        amount_wei = self.w3.to_wei(amount, 'ether')
        
        if amount_wei > balance_wei:
            required_balance_wei = amount_wei - balance_wei
            required_balance_eth = round(self.w3.from_wei(required_balance_wei, 'ether'), 6)
            return required_balance_eth
        
        else:
            return False
    
    async def okx_withdraw(self, account_id: int, key: str, amount_withdraw: float, wait_balance: bool):
        okx_withdraw = OKXWithdraw(account_id, key, self.str_proxy)
        await okx_withdraw.withdraw(amount_withdraw, wait_balance)
    
    async def top_up_balance(self, amount: float, wait_balance: bool):
        required_balance_eth = await self.calculate_amount(amount)
        
        if required_balance_eth:
            await self.okx_withdraw(self.account_id, self.private_key, required_balance_eth, wait_balance)
        
        else:
            return self.log_send(f'The account already has the requested balance: {required_balance_eth}!')