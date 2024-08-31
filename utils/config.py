import json


with open('data/rpc.json', 'r') as file:
    RPC = json.load(file)
    
with open('data/erc20_abi.json', 'r') as file:
    ERC20_ABI = json.load(file)
    
with open('data/dmail/abi.json', 'r') as file:
    DMAIL_ABI = json.load(file)
    
with open('accounts.txt', 'r') as file:
    ACCOUNTS = [row.strip() for row in file]
    
with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

with open('data/weth/abi.json', "r") as file:
    WETH_ABI = json.load(file)

with open('data/mint_nft/abi.json', "r") as file:
    MINT_NFT_ABI = json.load(file)

with open('data/rubyscore/abi.json', "r") as file:
    RUBYSCORE_ABI = json.load(file)

with open('data/owlto/abi.json', "r") as file:
    OWLTO_ABI = json.load(file)

with open('data/uniswap/quoter.json', "r") as file:
    UNISWAP_QUOTER_ABI = json.load(file)

with open('data/uniswap/router.json', "r") as file:
    UNISWAP_ROUTER_ABI = json.load(file)

with open('data/aave/abi.json', "r") as file:
    AAVE_ABI = json.load(file)

with open('data/nfts2me/abi.json', "r") as file:
    NFTS2ME_ABI = json.load(file)

MAX_APPROVE = 2**256 - 1

ETH_MASK = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

DMAIL_CONTRACT = '0x47fbe95e981C0Df9737B6971B451fB15fdC989d9'

OWLTO_CONTRACT = '0xd48e3caf0d948203434646a3f3e80f8ee18007dc'

UNISWAP_CONTRACTS = {
    "router": "0x2626664c2603336E57B271c5C0b26F421741e481",
    "quoter": "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
}

AAVE_CONTRACTS = {
    'main': '0x18cd499e3d7ed42feba981ac9236a278e4cdc2ee',
    'aave_weth': '0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7',
}

RUBYSCORE_CONTRACTS = {
    "vote": "0xe10add2ad591a7ac3ca46788a06290de017b9fb4",
}

INCH_CONTRACT = {
    "router": "0x1111111254eeb25477b68fb85ed929f73a960582",
}

BASE_TOKENS = {
    "ETH": "0x4200000000000000000000000000000000000006",
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "USDBC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
}