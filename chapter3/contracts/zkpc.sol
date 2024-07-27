// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "zk-merkle-tree/contracts/ZKTree.sol";
contract zkpc is ZKTree {
    address public owner;
    mapping(uint256 => bool) uniqueHashes;
    constructor(
        uint32 _levels,
        IHasher _hasher,
        IVerifier _verifier
    ) ZKTree(_levels, _hasher, _verifier) {
        owner = msg.sender;

    }


    function zkmethod(
        uint256 _uniqueHash,
        uint256 _commitment
    ) external {
        require(
            !uniqueHashes[_uniqueHash],
            "This unique hash is already used!"
        );
        _commit(bytes32(_commitment));
        uniqueHashes[_uniqueHash] = true;
    }

}

