from brownie import SimpleStorage, accounts


def main():
    ss = SimpleStorage.deploy({"from": accounts[0]})
    print(ss)
