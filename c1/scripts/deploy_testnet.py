from brownie import Ballot, accounts, convert, config

proposals = [1030, 1031, 1032, 1033]
byte_proposals = [convert.to_bytes(p) for p in proposals]

account = accounts.add(config["keys"]["private_key"])


def main():
    ballot = Ballot.deploy(
        byte_proposals,
        {"from": account},
        publish_source=config["networks"]["rinkeby"]["verify"],
    )
    print(f"Successfully deployed Ballot contract to: {ballot.address}")
