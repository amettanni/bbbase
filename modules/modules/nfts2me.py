import random

from modules.account import Account
from utils.config import NFTS2ME_ABI
from utils.wrappers import check_gas


class NFT2ME(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)

    @check_gas
    async def mint_nft(self, contracts: list):
        try:
            self.log_send(f'Mint NFT on NFTS2ME.')

            contract = self.get_contract(random.choice(contracts), NFTS2ME_ABI)

            tx_data = await self.get_tx_data()

            tx = await contract.functions.mint(1).build_transaction(tx_data)

            return await self.execute_transaction(tx)

        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False