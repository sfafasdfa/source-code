// SPDX-License-Identifier: GPL-3.0
 
pragma solidity ^0.8.17;
 
/**
 * @title Oracle
 * @dev Store & retrieve value in a variable
 */
contract Oracle {
 
    event LogRegister(address, string);//niming dizhi he duiying de mimi
    mapping(address => bool) registerinfos;//yongyu jilu nimingdizhi shifou youxiao
    mapping(uint256 => uint256) uniquetoconfirm;//uniquehash to comfirm
    mapping(uint256 => address) uniquetoaddress;
    mapping(uint256 => string) uniquetoencrypted;
    string[] pubkeys;
    struct hashsec {
        uint256 uhash;
        string secret;
    }
    hashsec[] hashseclist;
    function register(address _wk,string memory _pubkey, uint256 _uniquehash, uint256 _confirmhash) public {
        uniquetoconfirm[_uniquehash] = _confirmhash;
        uniquetoaddress[_uniquehash] = _wk;
        pubkeys.push(_pubkey);
    }

    function workerrequest(string memory _encyptedaddress, uint256 _uniquehash, uint256 _confirm) public {
        bytes32 hashresult = sha256(abi.encodePacked(_confirm));
        bytes32 temp = bytes32(uniquetoconfirm[_uniquehash]);
        require(temp == hashresult,"not match");
        require(bytes(uniquetoencrypted[_uniquehash]).length == 0,"have been used");
        uniquetoencrypted[_uniquehash] = _encyptedaddress;
        hashseclist.push(hashsec({uhash:_uniquehash,secret:_encyptedaddress}));
    }
    
    function servercallback(address _addr, string memory _infos) public {
        registerinfos[_addr] = true;
        emit LogRegister(_addr, _infos);
    }
    function getcount() public view returns(uint){
        return pubkeys.length;
    }
    function getsecret() public view returns(hashsec[] memory){
        return hashseclist;
    }
    function getconfirm(address _addr) public view returns(bool){
        return registerinfos[_addr];
    }
}
