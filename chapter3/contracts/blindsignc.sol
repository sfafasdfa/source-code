// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract blindsignc{
    uint256 [80][1024*1024] text;
    event a(uint key, uint dex);

    function blindsignmethod(
        uint[80] memory _pubkey,
        uint _index
    ) external {
        uint i = 0;
        for(i=0;i<80;i++)
        {
            text[i][_index] = _pubkey[i];
            emit a(_pubkey[i], _index);

        }
        
    }
    function get()external view returns(uint256[80] memory){
        return text[0];
    }

    
}