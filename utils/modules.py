import random

from settings import ModulesSettings as ms
from settings import OKXSettings as OKXSETTINGS
from modules.modules.dmail import Dmail
from modules.modules.aave import Aave
from modules.modules.inch import Inch
from modules.modules.uniswap import UniSwap
from modules.modules.wrap_eth import WrapETH
from modules.modules.nfts2me import NFT2ME
from modules.modules.okx_withdraw import OKXWithdraw
from modules.modules.rubyscore import RubyScore
from modules.modules.owlto import OwlTo
from modules.modules.okx_topup import OKXTopUp
from modules.modules.tokens import Tokens
from modules.modules.balance_checker import BalanceChecker


async def okx_withdraw(account_id: int, key: str, proxy: str):
    okx_withdraw = OKXWithdraw(account_id, key, proxy)
    
    wait_balance = OKXSETTINGS.WAIT_UNTIL_BALANCE_CREDITED
    
    await okx_withdraw.withdraw(wait_until_credited=wait_balance)

async def okx_top_up(account_id: int, key: str, proxy: str):
    amount = OKXSETTINGS.BALANCE_TOP_UP
    wait_balance = OKXSETTINGS.WAIT_UNTIL_BALANCE_CREDITED
    
    okx_top_up = OKXTopUp(account_id, key, proxy)
    await okx_top_up.top_up_balance(amount, wait_balance)

async def swap_inch(account_id, key, proxy):
    from_token = ms.Inch.FROM_TOKEN
    to_token = ms.Inch.TO_TOKEN
    
    min_amount = ms.Inch.AMOUNT[0]
    max_amount = ms.Inch.AMOUNT[1]
    decimal = ms.Inch.DECIMAL
    
    all_amount = ms.Inch.USE_PERCENTS
    
    swap_reverse = ms.Inch.SWAP_REVERSE
    
    min_percent = ms.Inch.PERCENTS[0]
    max_percent = ms.Inch.PERCENTS[1]
    
    api_key = ms.Inch.API_KEY
    
    inch = Inch(account_id, key, proxy, api_key)
    await inch.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )

async def swap_uniswap(account_id, key, proxy):
    from_token = ms.UniSwap.FROM_TOKEN
    to_token = ms.UniSwap.TO_TOKEN
    
    min_amount = ms.UniSwap.AMOUNT[0]
    max_amount = ms.UniSwap.AMOUNT[1]
    decimal = ms.UniSwap.DECIMAL
    
    all_amount = ms.UniSwap.USE_PERCENTS
    
    swap_reverse = ms.UniSwap.SWAP_REVERSE
    
    min_percent = ms.UniSwap.PERCENTS[0]
    max_percent = ms.UniSwap.PERCENTS[1]
    
    uniswap = UniSwap(account_id, key, proxy)
    await uniswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )
    
async def deposit_aave(account_id, key, proxy):
    min_amount = ms.Aave.AMOUNT[0]
    max_amount = ms.Aave.AMOUNT[1]
    decimal = ms.Aave.DECIMAL
    
    all_amount = ms.Aave.USE_PERCENTS
    min_percent = ms.Aave.PERCENTS[0]
    max_percent = ms.Aave.PERCENTS[1]

    make_withdraw = ms.Aave.WITHDRAW
    
    aave = Aave(account_id, key, proxy)
    await aave.deposit(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, make_withdraw
    )
    
async def wrap_eth(account_id, key, proxy):
    min_amount = ms.WrapETH.AMOUNT[0]
    max_amount = ms.WrapETH.AMOUNT[1]
    decimal = ms.WrapETH.DECIMAL
    
    all_amount = ms.WrapETH.USE_PERCENTS
    min_percent = ms.WrapETH.PERCENTS[0]
    max_percent = ms.WrapETH.PERCENTS[1]
    
    unwrap_eth = ms.WrapETH.UNWRAP_ETH
    
    wrap_eth = WrapETH(account_id, key, proxy)
    await wrap_eth.wrap_eth(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, unwrap_eth
    )

async def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    await dmail.send_mail()

async def nfts2me_mint(account_id, key, proxy):
    nft_lists = ms.NFTs2Me.NFT_ADDRESS
    
    mint_nft = NFT2ME(account_id, key, proxy)
    await mint_nft.mint_nft(nft_lists)

async def rubyscore_vote(account_id, key, proxy):
    rubyscore = RubyScore(account_id, key, proxy)
    await rubyscore.vote()

async def owlto_checkin(account_id, key, proxy):
    owlto = OwlTo(account_id, key, proxy)
    await owlto.check_in()

async def increase_allowance(account_id, key, proxy):
    tokens = ms.Tokens.IncreaseAllowance.TOKENS
    
    min_amount = ms.Tokens.IncreaseAllowance.AMOUNT[0]
    max_amount = ms.Tokens.IncreaseAllowance.AMOUNT[1]
    decimals = ms.Tokens.IncreaseAllowance.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.increase_allowance(
        tokens, min_amount, max_amount, decimals
    )

async def approve(account_id, key, proxy):
    tokens = ms.Tokens.Approve.TOKENS
    
    min_amount = ms.Tokens.Approve.AMOUNT[0]
    max_amount = ms.Tokens.Approve.AMOUNT[1]
    decimals = ms.Tokens.Approve.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.approve_random_address(
        tokens, min_amount, max_amount, decimals
    )

async def transfer(account_id, key, proxy):
    tokens = ms.Tokens.Transfer.TOKENS
    
    min_amount = ms.Tokens.Transfer.AMOUNT[0]
    max_amount = ms.Tokens.Transfer.AMOUNT[1]
    decimals = ms.Tokens.Transfer.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.transfer(
        tokens, min_amount, max_amount, decimals
    )

async def check_balance(account_id, key, proxy):
    balance_checker = BalanceChecker(account_id, key, proxy)
    return await balance_checker.check_balance()