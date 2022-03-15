from brownie import SimpleStorage, Coin, accounts


def main():

    admin = accounts[0]
    # deployed: 0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87
    ss = SimpleStorage.deploy({"from": admin})
    # deployed: 0x602C71e4DAC47a042Ee7f46E0aee17F94A3bA0B6
    c = Coin.deploy({"from": admin})

    # perform a contract call
    ss.set(7, {"from": admin})
    ss.get()
