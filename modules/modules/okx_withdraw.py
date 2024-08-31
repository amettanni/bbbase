import base64
from datetime import datetime
import hmac
import random
import aiohttp

from modules.account import Account
from settings import OKXSettings
from utils.utils import async_sleep
from utils.config import BASE_TOKENS


class OKXWithdraw(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)

        self.symbol = OKXSettings.SYMBOL
        self.amount = round(random.uniform(OKXSettings.AMOUNT_WITHDRAW[0], OKXSettings.AMOUNT_WITHDRAW[1]), 6)
        self.fee = OKXSettings.FEE
        self.chain = OKXSettings.CHAIN
        self.api_key = OKXSettings.API_KEY
        self.secret_key = OKXSettings.SECRET_KEY
        self.passphrase = OKXSettings.PASSPHRASE
        self.dest = 4
    
    async def wait_until_change_balance(self):
        _, init_balance_wei = _, current_balance_wei = await self.get_balance(
            BASE_TOKENS[self.symbol] if self.symbol != 'ETH' else None
        )
        
        self.log_send(f'Awaiting to credit funds to wallet.')
        
        while init_balance_wei == current_balance_wei:
            await async_sleep(10, 10, logs=False)
            _, current_balance_wei = await self.get_balance(
                BASE_TOKENS[self.symbol] if self.symbol != 'ETH' else None
            )
        
        self.log_send(f'Tokens ${self.symbol} has been successfully credited.', status='success')
    
    async def make_http_request(self, url, method, headers=None, params=None, data=None, timeout=10):
        async with aiohttp.ClientSession() as session:
            kwargs = {"url": url, "method": method, "timeout": timeout}
                
            if headers:
                kwargs["headers"] = headers
            
            if params:
                kwargs["params"] = params
            
            if data:
                kwargs["data"] = data
            
            async with session.request(**kwargs) as response:
                return await response.json()

    async def get_data(self, request_path, body, method):
        def signature(timestamp: str, method: str, request_path: str, secret_key: str, body: str):
            message = timestamp + method.upper() + request_path + body
            mac = hmac.new(
                bytes(secret_key, encoding="utf-8"),
                bytes(message, encoding="utf-8"),
                digestmod="sha256",
            )
            d = mac.digest()
            return base64.b64encode(d).decode("utf-8")

        dt_now = datetime.utcnow()
        ms = str(dt_now.microsecond).zfill(6)[:3]
        timestamp = f"{dt_now:%Y-%m-%dT%H:%M:%S}.{ms}Z"

        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature(timestamp, method, request_path, self.secret_key, body),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            'x-simulated-trading': '0'
        }

        return headers

    async def withdraw(self, amount_withdraw: float = 0, wait_until_credited: bool = False):
        self.amount = amount_withdraw if amount_withdraw != 0 else self.amount
        
        try:
            body = {
                "ccy": self.symbol,
                "amt": self.amount,
                "fee": self.fee,
                "dest": self.dest,
                "chain": f"{self.symbol}-{self.chain}",
                "toAddr": self.address
            }

            headers = await self.get_data(request_path='/api/v5/asset/withdrawal', method='POST', body=str(body))
            result = await self.make_http_request("https://www.okx.cab/api/v5/asset/withdrawal",data=str(body), method="POST", headers=headers)

            if result['code'] == '0':
                self.log_send(f'Successfully withdraw {self.amount} {self.symbol} from OKX.', status='success')
                
                if wait_until_credited: await self.wait_until_change_balance()
                
                return True
            else:
                e = result['msg']
                self.log_send(f'Error occurred when withdraw {self.amount} {self.symbol} with OKX: {e}', status='error')
                return False

        except Exception as e:
            self.log_send(f'Error occurred when withdraw {self.amount} {self.symbol} with OKX: {e}', status='error')
            return False