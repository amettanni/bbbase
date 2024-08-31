import asyncio
import random
from typing import Callable
from loguru import logger

from utils.modules import *
from utils.utils import async_sleep, remove_wallet_from_files
from settings import MainSettings as SETTINGS
from utils.wrappers import repeats


async def start_tasks(data: list, module: Callable = None):
    tasks = []

    for account in data:
        await run_main_proccesses(account.get('id'), account.get('key'), account.get('proxy'), module)

    #     tasks.append(
    #         asyncio.create_task(run_main_proccesses(account.get('id'), account.get('key'), account.get('proxy'), module))
    #     )

    # await asyncio.gather(*tasks)


async def run_main_proccesses(account_id: int, key: str, proxy: str, module: Callable = None):
    await async_sleep(
        SETTINGS.START_PERIOD[0], SETTINGS.START_PERIOD[1],
        True, account_id, key, 'before starting work'
    )
    
    if module:
        await run_module(module, account_id, key, proxy)
    
    else:
        if not SETTINGS.CUSTOM_ROUTES_MODULES:
            raise ValueError(f'Enter your modules to CUSTOM_ROUTES_MODULES in the settings.')
        
        # for route in SETTINGS.CUSTOM_ROUTES_MODULES:
        #     choiced_module = random.choice(route)
        #     if not choiced_module: continue
            
        #     await run_module(eval(choiced_module), account_id, key, proxy)

        choiced_route = random.choice(SETTINGS.CUSTOM_ROUTES_MODULES)
        for module in choiced_route:
            if not module: continue
            
            await run_module(eval(module), account_id, key, proxy)
    
    if SETTINGS.REMOVE_WALLET: remove_wallet_from_files(key, proxy)


async def run_check_balance(data: list):
    tasks = []

    for account in data:
        tasks.append(
            asyncio.create_task(check_balance(account.get('id'), account.get('key'), account.get('proxy')))
        )
    
    all_balances = sum(await asyncio.gather(*tasks))

    logger.success(f'💰 Balance of all accounts in Base: {round(all_balances, 6)} $ETH.')


@repeats
async def run_module(module: Callable, account_id: int, key: str, proxy: str):
    succcess_bridge = await module(account_id, key, proxy)
    if not succcess_bridge: return False
    return True