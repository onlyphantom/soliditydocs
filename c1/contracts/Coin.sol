// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Coin {
    // state variable
    address public minter;
    mapping(address => uint256) public balances;

    event Sent(address from, address to, uint256 amount);

    constructor() {
        minter = msg.sender;
    }

    // creates coins out of thin air
    // make sure only minter gets to called this. Otherwise, bad tokenomics.
    function mint(address _receiver, uint256 _amount) public {
        // this should only be called by the creator of this coin
        require(msg.sender == minter);

        balances[_receiver] += _amount; // overflow: 2 ^ 256 - 1
    }

    error InsufficientBalance(uint256 requested, uint256 bal_available);

    function send(address _receiver, uint256 _amount) public {
        // check that the sender does indeed have the amount specified
        require(balances[msg.sender] >= _amount, "Not enough balance.");
        // alternative
        // if (balances[msg.sender] < _amount) {
        //     revert InsufficientBalance({
        //         requested: _amount,
        //         bal_available: balances[msg.sender]
        //     });
        // }

        balances[msg.sender] -= _amount;
        balances[_receiver] += _amount;
        emit Sent(msg.sender, _receiver, _amount);
    }
}
