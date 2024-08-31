from modules.account import Account
from utils.config import RUBYSCORE_CONTRACTS, RUBYSCORE_ABI


class RubyScore(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.rubyscore_contract = self.get_contract(RUBYSCORE_CONTRACTS['vote'], RUBYSCORE_ABI)
        
    async def vote(self):
        try:
            self.log_send('Vote on RubyScore.')
            
            amount_wei, _ = await self.get_random_amount("ETH", 0.000002, 0.0000035, 8)
            
            tx_data = await self.get_tx_data(value=amount_wei)
            
            tx = await self.rubyscore_contract.functions.vote().build_transaction(tx_data)
            
            return await self.execute_transaction(tx)

        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False