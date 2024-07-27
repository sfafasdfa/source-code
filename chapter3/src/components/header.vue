<template>
    <header>
        <el-row :gutter="20">
            <el-col :span="16">
                <div class="grid-content ep-bg-purple">
                    <h1 class="title">
                        MCS平台
                    </h1>
                </div>/></el-col>
            <el-col :span="8">
                <div class="grid-content ep-bg-purple">
                        <el-botton @click = "registerValidator">{{account}}</el-botton>
                </div>/>
            </el-col>
        </el-row>
    </header>
  </template>
  
  <script lang="ts">
  import {ref, onMounted, toRefs, defineComponent} from 'vue'
  import { ethers } from 'ethers'
  import { Component, Vue } from "vue-facing-decorator";
  const abi = [
    {
      "inputs": [
        {
          "internalType": "uint32",
          "name": "_levels",
          "type": "uint32"
        },
        {
          "internalType": "contract IHasher",
          "name": "_hasher",
          "type": "address"
        },
        {
          "internalType": "contract IVerifier",
          "name": "_verifier",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_oracele",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "bytes32",
          "name": "commitment",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "internalType": "uint32",
          "name": "leafIndex",
          "type": "uint32"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "Commit",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "FIELD_SIZE",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "ROOT_HISTORY_SIZE",
      "outputs": [
        {
          "internalType": "uint32",
          "name": "",
          "type": "uint32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "ZERO_VALUE",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_x",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_y",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_reward",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_time",
          "type": "string"
        }
      ],
      "name": "addtotasklist",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "name": "commitments",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "currentRootIndex",
      "outputs": [
        {
          "internalType": "uint32",
          "name": "",
          "type": "uint32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_i",
          "type": "uint256"
        }
      ],
      "name": "deletetask",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "filledSubtrees",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getLastRoot",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getcurrentwkcoord",
      "outputs": [
        {
          "components": [
            {
              "internalType": "address",
              "name": "name",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "x",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "y",
              "type": "uint256"
            }
          ],
          "internalType": "struct Crowdsensing.worker[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_nullifier",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_root",
          "type": "uint256"
        },
        {
          "internalType": "uint256[2]",
          "name": "_proof_a",
          "type": "uint256[2]"
        },
        {
          "internalType": "uint256[2][2]",
          "name": "_proof_b",
          "type": "uint256[2][2]"
        },
        {
          "internalType": "uint256[2]",
          "name": "_proof_c",
          "type": "uint256[2]"
        }
      ],
      "name": "getreward",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "gettasklistinfo",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "name",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "x",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "y",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "reward",
              "type": "uint256"
            },
            {
              "internalType": "string",
              "name": "time",
              "type": "string"
            }
          ],
          "internalType": "struct Crowdsensing.task[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_left",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_right",
          "type": "uint256"
        }
      ],
      "name": "hashLeftRight",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "hasher",
      "outputs": [
        {
          "internalType": "contract IHasher",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_root",
          "type": "bytes32"
        }
      ],
      "name": "isKnownRoot",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "levels",
      "outputs": [
        {
          "internalType": "uint32",
          "name": "",
          "type": "uint32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "nextIndex",
      "outputs": [
        {
          "internalType": "uint32",
          "name": "",
          "type": "uint32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "name": "nullifiers",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_uniqueHash1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_commitment1",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "_pubkey",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_confirm",
          "type": "uint256"
        }
      ],
      "name": "registerCommitment1",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_uniqueHash2",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_commitment2",
          "type": "uint256"
        }
      ],
      "name": "registerCommitment2",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_validator",
          "type": "address"
        }
      ],
      "name": "registerValidator",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_x",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_y",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_nullifier",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_root",
          "type": "uint256"
        },
        {
          "internalType": "uint256[2]",
          "name": "_proof_a",
          "type": "uint256[2]"
        },
        {
          "internalType": "uint256[2][2]",
          "name": "_proof_b",
          "type": "uint256[2][2]"
        },
        {
          "internalType": "uint256[2]",
          "name": "_proof_c",
          "type": "uint256[2]"
        }
      ],
      "name": "registermission",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "roots",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "tasklist",
      "outputs": [
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "x",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "y",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reward",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "time",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_name",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_x",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_y",
          "type": "uint256"
        }
      ],
      "name": "updatetrajectory",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "validators",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "verifier",
      "outputs": [
        {
          "internalType": "contract IVerifier",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "i",
          "type": "uint256"
        }
      ],
      "name": "zeros",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    }
  ];
  @Component
  export default class header extends Vue{
  account = ref("认证");
  async mounted(){
    if((window as any).ethereum === "undefined"){
      alert("请安装metamask");
    }
    else{
      this.account = await this.getAccount();
    }
    (window as any).ethereum.on("accountsChanged", this.accountchange());
  }

  async getAccount() {
    const provider = new ethers.providers.Web3Provider((window as any).ethereum);
    const accounts = await provider.send("eth_requestAccounts", []);
    return accounts[0];
  }
  async accountchange(){
    this.account = await this.getAccount();
  }
  async registerValidator(){
    const provider = new ethers.providers.Web3Provider((window as any).ethereum);
    const account = await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner(account[0]);
    const contracts = await (await fetch("contracts.json")).json();
    const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
    await contract.registerValidator(await this.getAccount());
  }
  }
  
  </script>