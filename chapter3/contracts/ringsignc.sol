// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract ringsignc{
    uint256 [80][1024*1024] pubkey;
    event a(uint key, uint dex);

    function ringsignmethod(
        uint256[80] memory _pubkey,
        uint256 _index
    ) external {
        uint i = 0;
        for(i=0;i<80;i++)
        {
            pubkey[i][_index] = _pubkey[i];
            emit a(_pubkey[i], _index);
        }
        
    }
    function get()external view returns(uint256[80] memory){
        return pubkey[0];
    }
}