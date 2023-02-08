from mywallet.models import Blockchain


def generate_blockchain():
    bc_1 = {
        "network": "Real Money System Network",
        "name": "Real Money System",
        "symbol": "FIAT",
        "currency_name": "US Dollar",
        "url_rpc": "https://tok-exchange.com/",
        "url_block_explorer": "https://tok-exchange.com/explorer/",
    }

    bc_2 = {
        "network": "Binance Smart Chain Mainnet",
        "name": "Binance Smart Chain",
        "symbol": "BNB",
        "currency_name": "Binance Coin",
        "url_rpc": "https://bsc-dataseed1.binance.org/",
        "url_block_explorer": "https://bscscan.com/",
    }

    bc_3 = {
        "network": "Ethereum Mainnet",
        "name": "Etherium",
        "symbol": "ETH",
        "currency_name": "Ether",
        "url_rpc": "https://mainnet-infura.brave.com/",
        "url_block_explorer": "https://etherscan.io/",
    }

    bc_4 = {
        "network": "Bitcoin Network",
        "name": "Bitcoin EVM",
        "symbol": "BTC",
        "currency_name": "Bitcoin",
        "url_rpc": "https://connect.bitcoinevm.com/",
        "url_block_explorer": "https://explorer.bitcoinevm.com/",
    }

    try:
        Blockchain.objects.create(**bc_1)
        Blockchain.objects.create(**bc_2)
        Blockchain.objects.create(**bc_3)
        Blockchain.objects.create(**bc_4)
        print("The 4th bases Blockchain was created successfully!!")
    except Exception as e:
        print("An error occurred: %s" % e.__str__())