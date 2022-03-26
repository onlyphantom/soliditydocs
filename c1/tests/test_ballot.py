import pytest
from brownie import Ballot, accounts, convert, reverts


proposals = [1007, 1014, 1021]


@pytest.fixture
def ballot(scope="module"):
    byte_proposals = [convert.to_bytes(p) for p in proposals]
    return Ballot.deploy(byte_proposals, {"from": accounts[0]})


def test_correct_chairperson(ballot):
    assert ballot.chairperson() == accounts[0]


def test_has_proposals(ballot):
    assert convert.to_int(ballot.proposals(0)[0]) == proposals[0]
    assert convert.to_int(ballot.proposals(1)[0]) == proposals[1]
    assert convert.to_int(ballot.proposals(2)[0]) == proposals[2]


def test_rights_to_vote_admin(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    _, _, weight, _ = ballot.voters(accounts[1])
    assert weight == 1


def test_rights_to_vote_nonadmin(ballot):
    with reverts():
        ballot.giveRightToVote(accounts[2], {"from": accounts[1]})
    assert ballot.voters(accounts[2])[2] == 0


def test_rights_to_vote_hasvoted(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    ballot.vote(0, {"from": accounts[1]})

    with reverts():
        ballot.giveRightToVote(accounts[1], {"from": accounts[0]})


def test_rights_to_vote_hasrights(ballot):

    with reverts():
        ballot.giveRightToVote(accounts[0], {"from": accounts[0]})

    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    with reverts():
        ballot.giveRightToVote(accounts[1], {"from": accounts[0]})


def test_delegates_has_voted(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[2], {"from": accounts[0]})
    ballot.vote(0, {"from": accounts[1]})

    with reverts():
        ballot.delegate(accounts[2], {"from": accounts[1]})


def test_delegates_toself(ballot):
    with reverts():
        ballot.delegate(accounts[0], {"from": accounts[0]})


def test_delegates_toloop(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[2], {"from": accounts[0]})
    ballot.delegate(accounts[2], {"from": accounts[1]})

    with reverts():
        ballot.delegate(accounts[1], {"from": accounts[2]})


def test_delegates_noweights(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})

    with reverts():
        ballot.delegate(accounts[2], {"from": accounts[1]})


def test_delegates_success_setstate(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[2], {"from": accounts[0]})

    ballot.delegate(accounts[2], {"from": accounts[1]})
    delegate, vote, weight, voted = ballot.voters(accounts[1])
    assert voted == True
    assert delegate == accounts[2]


def test_delegates_success_notvoted(ballot):
    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[2], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[3], {"from": accounts[0]})
    ballot.delegate(accounts[3], {"from": accounts[1]})
    ballot.delegate(accounts[3], {"from": accounts[2]})
    _, _, weight, _ = ballot.voters(accounts[3])
    assert weight == 3


def test_delegates_success_hasvoted(ballot):

    PROPOSAL = 2

    ballot.giveRightToVote(accounts[1], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[2], {"from": accounts[0]})
    ballot.giveRightToVote(accounts[3], {"from": accounts[0]})

    ballot.vote(PROPOSAL, {"from": accounts[2]})

    ballot.delegate(accounts[2], {"from": accounts[1]})
    ballot.delegate(accounts[2], {"from": accounts[3]})

    _, votecount = ballot.proposals(PROPOSAL)
    assert votecount == 3
