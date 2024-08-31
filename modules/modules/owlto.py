from datetime import datetime

from modules.account import Account
from utils.config import OWLTO_CONTRACT, OWLTO_ABI


class OwlTo(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.owlto_contract = self.get_contract(OWLTO_CONTRACT, OWLTO_ABI)
        
    async def check_in(self):
        try:
            self.log_send('Check in on OwlTo.')
            
            date = int(datetime.today().strftime('%Y%m%d'))
            
            tx_data = await self.get_tx_data()
            
            tx = await self.owlto_contract.functions.checkIn(date).build_transaction(tx_data)
            
            return await self.execute_transaction(tx)

        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False