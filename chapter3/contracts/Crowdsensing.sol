// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "zk-merkle-tree/contracts/ZKTree.sol";
import "./oracle.sol";
contract Crowdsensing is ZKTree {
    address public owner;
    mapping(address => bool) public validators;
    mapping(uint256 => bool) uniqueHashes;
    mapping(address => bool) registerstate1;
    mapping(address => bool) registerstate2;
    address oracle;
    struct worker{
        address name;
        uint x;
        uint y;
    }
    worker[] workerlist;
    mapping(address => bool) currentworkerstate;

    struct coord {
        uint x;
        uint y;
    }
    mapping(address => coord[]) trajectory;
    mapping(address => coord) currentcoord;
    constructor(
        uint32 _levels,
        IHasher _hasher,
        IVerifier _verifier,
        address _oracele
    ) ZKTree(_levels, _hasher, _verifier) {
        owner = msg.sender;
        oracle = _oracele;
    }
    //1share 2task register 3 register commit 4second register & register reward 5 up and down task

    //register task
    struct task {
        string name;
        uint x;
        uint y;
        uint reward;
        string time;
    }
    task[] public tasklist;

    function addtotasklist(string memory _name, uint _x,uint  _y, uint _reward, string memory _time) external{
        require(msg.sender==owner,"only owner can add task");
        tasklist.push(task({name:_name,x:_x,y:_y,reward:_reward,time:_time}));
    }
    function deletetask(uint256 _i) external{
        require(msg.sender==owner,"only owner can delete task");
        require(_i<tasklist.length,"out of index");
        for(uint256 i = _i;i<tasklist.length-1;i++){
            tasklist[i] = tasklist[i+1];
        }
        tasklist.pop();
    }
    function gettasklistinfo() external view returns (task[] memory){
        return tasklist;
    }


    //validator & commit
    function registerValidator(address _validator) external {
        //require(msg.sender == owner, "Only owner can add validator!");
        validators[_validator] = true;
    }

    function registerCommitment1(
        uint256 _uniqueHash1,
        uint256 _commitment1,
        string memory _pubkey,
        uint256 _confirm
    ) external {
        require(validators[msg.sender], "Only validator can commit!");
        require(!registerstate1[msg.sender],"only once");
        require(
            !uniqueHashes[_uniqueHash1],
            "This unique hash 1 is already used!"
        );


        _commit(bytes32(_commitment1));
        uniqueHashes[_uniqueHash1] = true;
        Oracle(oracle).register(msg.sender,_pubkey,_uniqueHash1,_confirm);
        registerstate1[msg.sender] = true;
    }

    
    function registerCommitment2(
        uint256 _uniqueHash2,
        uint256 _commitment2
    ) external {
        require(currentworkerstate[msg.sender],"you are not in this task set");
        require(!registerstate2[msg.sender],"only once");

        require(
            !uniqueHashes[_uniqueHash2],
            "This unique hash 2 is already used!"
        );

        _commit(bytes32(_commitment2));
        uniqueHashes[_uniqueHash2] = true;
        registerstate2[msg.sender] = true;
    }


    function registermission(
        uint _x,
        uint _y,
        uint256 _nullifier,
        uint256 _root,
        uint[2] memory _proof_a,
        uint[2][2] memory _proof_b,
        uint[2] memory _proof_c
    ) external {
        
        require(!currentworkerstate[msg.sender],"You have already registered!");
        require(Oracle(oracle).getconfirm(msg.sender),"not register in oracle");
        _nullify(
            bytes32(_nullifier),
            bytes32(_root),
            _proof_a,
            _proof_b,
            _proof_c
        );
        workerlist.push(worker({name:msg.sender,x:_x,y:_y}));
        currentworkerstate[msg.sender] = true;
        trajectory[msg.sender].push(coord({x:_x,y:_y}));
        currentcoord[msg.sender] = coord({x:_x,y:_y});
    }
    
    function updatetrajectory(address  _name, uint _x, uint _y) external{
        trajectory[_name].push(coord({x:_x,y:_y}));
        currentcoord[_name] = coord({x:_x,y:_y});
    }
    function getcurrentwkcoord() external view returns(worker[] memory){
        worker[] memory currentwk = new worker[](workerlist.length);
        for(uint i =0; i<workerlist.length; i++)
        {
            address cname = workerlist[i].name;
            currentwk[i] = worker({name:cname,x:currentcoord[cname].x,y:currentcoord[cname].y});
        }
        return currentwk;
    }
    function getreward(
        uint256 _nullifier,
        uint256 _root,
        uint[2] memory _proof_a,
        uint[2][2] memory _proof_b,
        uint[2] memory _proof_c
    ) external returns(uint) {
        _nullify(
            bytes32(_nullifier),
            bytes32(_root),
            _proof_a,
            _proof_b,
            _proof_c
        );
        return 1;
    }
}