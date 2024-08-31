"""
----------------------------------------MAIN SETTINGS------------------------------------------

    MAX_GAS - 40 | Gwei Control. Maximum value of GWEI in Ethereum for software operation.

    GAS_MULTIPLAYER = 0.8 | Multiplier for MAX_GAS value.

    RANDOM_WALLETS - True | Take the wallets in random order.

    REMOVE_WALLET - True | To delete wallets after work or not. (IF NOT - SET FALSE).

    USE_PROXY - True | Use proxy or not.

    START_PERIOD = [1, 600] | The time period in which the wallets will be run.
        For example, wallets will be launched with a timer from 1 to 600 seconds after software launch.
            The first value is from, the second is to.
    
    REPEATS_PER_WALLET = 5 | The number of repetitions of each module.
    
    SLEEP_AFTER_WORK = [10, 30] | Sleeps after each module. A random number between 10 and 30 is selected.
    
    SLIPPAGE = 5 | Slippage in % for swaps.
    
    LANDINGS_SLEEP = [90, 300] | Sleep spacing for landing protocols. That's how long it will hold the money and withdraw after that time has elapsed.
    
    CUSTOM_ROUTES_MODULES = [                               |   With custom routes modules you can make your own routes.
        ['deposit_aave'],                                   |   One line - one transaction.
        ['swap_inch', 'swap_uniswap'],                      |   You can specify any number of functions on each line.
        ['wrap_eth', 'nfts2me_mint'],                       |   The software will select a random function in the list.
        ['send_mail', 'rubyscore_vote', 'owlto_checkin'],
        ['increase_allowance', 'approve', 'transfer', None]
    ]

---------------------------------------FUNCTIONS NAME------------------------------------------

    swap_inch               |   Swap on 1inch.
    swap_uniswap            |   Swap on UniSwap.
    deposit_aave            |   Supply (Redeem) Aave.
    wrap_eth                |   Wrap (Unwrap) $ETH.
    send_mail               |   Send mail via DMail.
    rubyscore_vote          |   Vote on RubyScore.
    owlto_checkin           |   Daily check in on OwlTo.
    nfts2me_mint            |   Mint on NFTs2Me.
    increase_allowance      |   Increase Allowance to random address.
    approve                 |   Approve to random address.
    transfer                |   Transfer to random address.
    okx_withdraw            |   Deposit funds to your wallet from OKX.
    okx_top_up              |   Top up wallet if the balance is less than required.

-----------------------------------------------------------------------------------------------
"""

class MainSettings:
    MAX_GAS = 100

    GAS_MULTIPLAYER = 1

    RANDOM_WALLETS = True

    REMOVE_WALLET = False

    USE_PROXY = True

    START_PERIOD = [3200, 4000]
    
    REPEATS_PER_WALLET = 1

    SLEEP_AFTER_WORK = [180, 400]

    SLIPPAGE = 1
    
    LANDINGS_SLEEP = [60, 700]

    CUSTOM_ROUTES_MODULES = [
        ['swap_uniswap'],
        ['rubyscore_vote'],
        ['owlto_checkin'],
        ['send_mail'],
        ['deposit_aave'],
        ['wrap_eth'], 
        ['swap_uniswap', 'rubyscore_vote'],
        ['swap_uniswap', 'owlto_checkin', 'wrap_eth'],
        ['swap_uniswap', 'send_mail'],
        ['swap_uniswap', 'deposit_aave'],
        ['rubyscore_vote', 'wrap_eth' 'owlto_checkin'],
        ['rubyscore_vote', 'send_mail'],
        ['wrap_eth', 'rubyscore_vote', 'deposit_aave'],
        ['owlto_checkin', 'send_mail'],
        ['owlto_checkin', 'deposit_aave'],
        ['send_mail', 'deposit_aave'],
        ['swap_uniswap', 'rubyscore_vote', 'wrap_eth', 'owlto_checkin'],
        ['swap_uniswap', 'rubyscore_vote', 'send_mail'],
        ['wrap_eth', 'swap_uniswap', 'rubyscore_vote', 'deposit_aave'],
        ['swap_uniswap', 'owlto_checkin', 'send_mail'],
        ['swap_uniswap', 'wrap_eth', 'owlto_checkin', 'deposit_aave'],
        ['rubyscore_vote', 'owlto_checkin', 'send_mail'],
        ['deposit_aave'],
        ['wrap_eth', 'rubyscore_vote', 'owlto_checkin', 'send_mail'], 
    ]

"""
----------------------------------------OKX WITHDRAW------------------------------------------

    SYMBOL = 'ETH'                      |   Data for withdraw from OKX.
    CHAIN = 'Base'                      |   You can find this data on OKX.
    FEE = 0.00004                       |   https://www.okx.com/balance/withdrawal

    AMOUNT = [0.006, 0.008]             |   Amount from and amount to withdrawal.
    
    BALANCE_TOP_UP = 0.01               |   Minimum balance for top up balance (Only for $ETH).
    
    WAIT_UNTIL_BALANCE_CREDITED = True  |   Wait until for tokens credited to move next modules.
    
    SECRET_KEY = 'YOUR_DATA'            |   Get your API data here:
    API_KEY = 'YOUR_DATA'               |   https://www.okx.com/account/my-api
    PASSPHRASE = 'YOUR_DATA'            |   Paste your secret, api keys and passphrase.

----------------------------------------------------------------------------------------------
"""

class OKXSettings:
    SYMBOL = 'ETH'
    CHAIN = 'Base'
    FEE = 0.00004

    AMOUNT_WITHDRAW = [0.0050, 0.0055]

    BALANCE_TOP_UP = 0.01
    
    WAIT_UNTIL_BALANCE_CREDITED = True

    SECRET_KEY = 'YOUR_DATA'
    API_KEY = 'YOUR_DATA'
    PASSPHRASE = 'YOUR_DATA'

"""
--------------------------------------------------MODULE SETTINGS--------------------------------------------------

    Each module has its own individual settings. Each module is labeled with the class "Module_Name".
    
    AMOUNT = [0.00035, 0.00065]     |   Amount for transactions. A random number in the interval will be used.
    
    DECIMAL = 5                     |   Decimal places for rounding for a random transaction amount.
    
    FROM_TOKEN = 'ETH'              |   Tokens for swaps.
    TO_TOKEN = 'USDC'               |   In this example, we swap $ETH to $USDC.
    
    USE_PERCENTS = False            |   Use % of balance
    
    PERCENTS = [3, 7]               |   How much % to use?
    
    SWAP_REVERSE = True             |   Doing a reverse swap for the same amount?
    
    API_KEY = 'YOUR-API-KEY'        |   Get your API key on the site for the module to work.
    
    WITHDRAW = True                 |   To withdraw liquidity from landing protocols or not.
    
    TOKENS = ['USDT', 'USDC']       |   Tokens list for work. You can choose one or several tokens.
    
    NFT_ADDRESS = [                 |   Paste NFT Contract address. You can insert more than one address.
        '0x5919F40f0d3115869882eEA8Ce491ea33bE0fF7E',
    ]

-------------------------------------------------------------------------------------------------------------------
"""

class ModulesSettings:
    
    class Aave:
        AMOUNT = [0.0005, 0.002]
        DECIMAL = 5
        
        USE_PERCENTS = True
        PERCENTS = [30, 80]
        
        WITHDRAW = True

    class UniSwap:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.002]
        DECIMAL = 5
        
        USE_PERCENTS = True
        PERCENTS = [25, 85]
        
        SWAP_REVERSE = True
    
    
    # skip
    class Inch:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.002]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        SWAP_REVERSE = True
        
        API_KEY = 'YOUR_DATA' # https://1inch.dev/portfolio-api/

    class WrapETH:
        AMOUNT = [0.0005, 0.002]
        DECIMAL = 5
        
        USE_PERCENTS = True
        PERCENTS = [10, 30]
        
        UNWRAP_ETH = True
    
    # skip or add you own NFT address contract
    class NFTs2Me:
        NFT_ADDRESS = ["0x9ca3389e003E7e9c9bB1228AD23ff335F1969Fbe", "0x7EC24C433434930Cef8d01E83656365AD334942B"]
        
    class Tokens:

        class IncreaseAllowance: # ETH not avaliable
            TOKENS = ['USDC', 'DAI', 'USDBC', 'WETH']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7
        
        class Approve: # ETH not avaliable
            TOKENS = ['USDC', 'DAI', 'USDBC', 'WETH']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7

        class Transfer:
            TOKENS = ['ETH']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7