// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.9.0;

contract SimpleStorage {
    // state variables
    // declare a state variable called storedData of type uint of 256 bits
    uint256 storedData;
    // declare another variable called 'unlocked' (true / false), default to false
    bool unlocked = false;
    // signed integer
    int256 count = 5;
    // type of address, it's a hard coded value that cannot be modified because it
    // is a constant
    address constant storageOwner = 0x3C79c6d6faB7f0811aA34fe95fA63e8787775Bf3;
    bytes1 xyz = 0x5f;

    mapping(address => uint256) public storeCredits;

    constructor() {
        set(3);
    }

    function queryCredits(address _keyAddr) public view returns (uint256) {
        return storeCredits[_keyAddr];
    }

    // this will incur some transaction fee; currency in ether (1 ether = 1e18 wei)
    function set(uint256 _x) public {
        storedData = _x;
        storeCredits[msg.sender] += _x;
    }

    function get() public view returns (uint256) {
        return storedData;
    }
}
