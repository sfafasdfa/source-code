<template>
    <el-col span="8">
    <el-card shadow="always">
        <el-button class="btn btn-info" @click="getcomit1">
            获取账号承诺
        </el-button>
        <el-button class="btn btn-danger" @click="resetCommitment1">
            重置账号承诺
        </el-button>
        <el-button @click="showcommit1">
            显示账号承诺
        </el-button>
        <el-button @click="registercommit1">
            登记账号承诺
        </el-button>
        <el-dialog v-model="showdialog1" @close="dialogClose1">
        <h1>你的承诺</h1>  
          <img :src="qrcodeDataUrl1"/>
          <div
            v-if="commitment1"
            v-html="splitTwoLines(commitment1.commitment)"
          ></div>
        </el-dialog>
    </el-card>
    </el-col>
    <el-col span="8">
    <el-card shadow="always">
        <el-button class="btn btn-info" @click="getcomit2">
            获取账号承诺
        </el-button>
        <el-button class="btn btn-danger" @click="resetCommitment2">
            重置账号承诺
        </el-button>
        <el-button @click="showcommit2">
            显示账号承诺
        </el-button>
        <el-button @click="registercommit2">
            登记账号承诺
        </el-button>
        <el-dialog v-model="showdialog2" @close="dialogClose2">
            <h1>你的承诺</h1>  
          <img :src="qrcodeDataUrl2"/>
          <div
            v-if="commitment2"
            v-html="splitTwoLines(commitment2.commitment)"
          ></div>
        </el-dialog>

    </el-card>
    </el-col>
    <el-col span="8">
    <el-card shadow="always">
        <el-button class="btn btn-info" @click="getkey">
            获取公私钥
        </el-button>
        <el-button class="btn btn-info" @click="getsecret">
            获取注册秘密
        </el-button>
        <el-button class="btn btn-info" @click="showkeys">
            显示密钥
        </el-button>
        <el-button class="btn btn-info" @click="showsec">
            显示秘密
        </el-button>
        <el-button class="btn btn-info" @click="resetkeysec">
            重置密钥和秘密
        </el-button>
        <el-button class="btn btn-info" @click="calloracle">
            同步身份
        </el-button>
        <el-dialog v-model="showdialog3" @close="dialogClose3">
            <h1>你的密钥</h1>
            <el-col span="12">
              <el-row><h2>公钥</h2></el-row>
              <el-row><img :src="qrcodeDataUrl3"></img></el-row>
            </el-col>
              <el-row><h2>私钥</h2></el-row>
              <el-row><img :src="qrcodeDataUrl4"></img></el-row>
            <el-col span="12">

            </el-col>
          </el-dialog>
          <el-dialog v-model="showdialog4" @close="dialogClose4">
            <el-row><h1>你的秘密</h1> </el-row>
            <el-row>值：{{ this.sec.value }}</el-row>
            <el-row>哈希：</el-row>
          <div
            v-if="this.sec"
            v-html="splitTwoLines(this.sec.hash)"
          ></div>
        </el-dialog>
    </el-card>
    </el-col>
</template>
<script lang="ts">
import { Component, Vue } from "vue-facing-decorator";
import { ref } from 'vue';
import {generateCommitment} from 'zk-merkle-tree';
import QRCode from "qrcode";
import crypto from 'crypto';
import * as ethers from "ethers";
import { concat } from "ethers/lib/utils";
const oraclepubkey = "";
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
const abi2 = [
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "LogRegister",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_addr",
          "type": "address"
        }
      ],
      "name": "getconfirm",
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
      "name": "getcount",
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
      "name": "getsecret",
      "outputs": [
        {
          "components": [
            {
              "internalType": "uint256",
              "name": "uhash",
              "type": "uint256"
            },
            {
              "internalType": "string",
              "name": "secret",
              "type": "string"
            }
          ],
          "internalType": "struct Oracle.hashsec[]",
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
          "internalType": "address",
          "name": "_wk",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "_pubkey",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_uniquehash",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_confirmhash",
          "type": "uint256"
        }
      ],
      "name": "register",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_addr",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "_infos",
          "type": "string"
        }
      ],
      "name": "servercallback",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_encyptedaddress",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_uniquehash",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_confirm",
          "type": "uint256"
        }
      ],
      "name": "workerrequest",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ];
@Component
export default class commit extends Vue{
    public commitment1:  any = "";
    public qrcodeDataUrl1: any = "";
    public commitment2:  any = "";
    public qrcodeDataUrl2: any = "";
    public qrcodeDataUrl3: any = "";
    public qrcodeDataUrl4: any = "";
    public showdialog1 = ref(false);
    public showdialog2 = ref(false);
    public showdialog3 = ref(false);
    public showdialog4 = ref(false);
    public keys: any = "";
    public sec: any ="";
    splitTwoLines(text: string) {
    if(text){
        const half = text.length / 2;
        return (text.substring(0, half) + "<br/>" + text.substring(half + 1, text.length));
        }
    }
    splitFourLines(text: string) {
    if(text){
        const half = text.length / 2;
        return (this.splitTwoLines(text.substring(0, half)) + "<br/>" + this.splitTwoLines(text.substring(half + 1, text.length)));
        }
    }
    async getcomit1(){
    this.commitment1 = JSON.parse(localStorage.getItem("registercommit"));
    if (!this.commitment1) {
      var comit =  await generateCommitment();
      var tempjson = {commitment:comit.commitment.toString(),
        nullifier:comit.nullifier.toString(),
        nullifierHash:comit.nullifierHash.toString(),
        secret: comit.secret.toString(),
      }
      this.commitment1 = tempjson
      localStorage.setItem(
        "registercommit",
        JSON.stringify(this.commitment1)
      );
      console.log(this.commitment1);
      
    }
    this.qrcodeDataUrl1 =  await QRCode.toDataURL(this.commitment1.commitment);
    }

    async getcomit2(){
    this.commitment2 = JSON.parse(localStorage.getItem("rewardcommit"));
    console.log(this.commitment2);
    if (!this.commitment2) {
      var comit =  await generateCommitment();
      var tempjson = {commitment:comit.commitment.toString(),
        nullifier:comit.nullifier.toString(),
        nullifierHash:comit.nullifierHash.toString(),
        secret: comit.secret.toString(),
      }
      this.commitment2 = tempjson
      localStorage.setItem(
        "rewardcommit",
        JSON.stringify(this.commitment2)
      );
      
    }
    this.qrcodeDataUrl2 =  await QRCode.toDataURL(this.commitment2.commitment);
    }

    public resetCommitment1() {
    localStorage.removeItem("registercommit");
    }
    public resetCommitment2() {
    localStorage.removeItem("rewardcommit");
    }
    public showcommit1(){
      this.commitment1 = JSON.parse(localStorage.getItem("registercommit"));
      if (!this.commitment1){
        alert("还未生成承诺")
        return 
      }
      else{
        this.showdialog1 = ref(true);
      }
        
    }
    public showcommit2(){
      this.commitment2 = JSON.parse(localStorage.getItem("rewardcommit"));
      if (!this.commitment2){
        alert("还未生成承诺")
        return 
      }
      else{
        this.showdialog2 = ref(true);
      }
    }
    public dialogClose1(){
        this.showdialog1 = ref(false);
    }
    public dialogClose2(){
        this.showdialog2 = ref(false);
    }
    async registercommit1(){
      this.commitment1 = JSON.parse(localStorage.getItem("registercommit"));
      if (!this.commitment1){
        alert("还未生成承诺")
        return 
      }
      this.keys = JSON.parse(localStorage.getItem("keys"));
      if(!this.keys){
        alert("还未生成密钥");
        return
      }
      this.sec = JSON.parse(localStorage.getItem("sec"));
      if(!this.sec){
        alert("还未生成秘密");
        return
      }
      const pubkey = this.keys.publickey.toString();
      const confirm = this.sec.hash.toString();
      const provider = new ethers.providers.Web3Provider((window as any).ethereum);
      const account = await provider.send("eth_requestAccounts", []);
      const signer = provider.getSigner(account[0]);
      const contracts = await (await fetch("contracts.json")).json();
      const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
      try {
        await contract.registerCommitment1(
        11,
        this.commitment1.commitment,
        pubkey,
        confirm
        );
      } catch (e) {
        alert(e.reason);
      }
    }
    async registercommit2(){
      this.commitment2 = JSON.parse(localStorage.getItem("registercommit"));
      if (!this.commitment2){
        alert("还未生成承诺")
        return 
      }
      const provider = new ethers.providers.Web3Provider((window as any).ethereum);
      const account = await provider.send("eth_requestAccounts", []);
      const signer = provider.getSigner(account[0]);
      const contracts = await (await fetch("contracts.json")).json();
      const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
      try {
        await contract.registerCommitment2(
        111,
        this.commitment2.commitment,
        );
      } catch (e) {
        alert(e.reason);
      }
    }
    async getkey(){
        this.keys = JSON.parse(localStorage.getItem("keys"));
        if(!this.keys){
          const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
          modulusLength: 2048,
            publicKeyEncoding: {
            type: 'spki',
            format: 'pem',
            },
            privateKeyEncoding: {
            type: 'pkcs8',
            format: 'pem',
            },
            });
          var tempjson ={
              "publickey":publicKey.toString(),
              "privatekey":privateKey.toString()
            };
          this.keys = tempjson;
          localStorage.setItem(
              "keys",
              JSON.stringify(this.keys)
            );
        }
        this.qrcodeDataUrl3=  await QRCode.toDataURL(this.keys.publickey);
        this.qrcodeDataUrl4=  await QRCode.toDataURL(this.keys.privatekey);
    }
    async getsecret(){
      this.sec = JSON.parse(localStorage.getItem("sec"));
      if(!this.sec){
        const data = "123";
        const hash = crypto.createHash('sha256');
        hash.update(data);
        this.sec = {
        "value": data,
        "hash": hash.digest('hex').toString()
        };
        localStorage.setItem(
              "sec",
              JSON.stringify(this.sec)
            );
      }
      
    }
    public showkeys(){
      this.keys = JSON.parse(localStorage.getItem("keys"));
      if(!this.keys){
        alert("还未生成密钥");
        return
      }
      else{
        this.showdialog3 = ref(true);
      }
    }
    public showsec(){
      this.sec = JSON.parse(localStorage.getItem("sec"));
      if(!this.sec){
        alert("还未生成秘密");
        return
      }
      else{
        this.showdialog4 = ref(true);
      }
    }
    public dialogClose3(){
      this.showdialog3 = ref(false);
    }
    public dialogClose4(){
      this.showdialog4 = ref(false);
    }
    public resetkeysec(){
      localStorage.removeItem("keys");
      localStorage.removeItem("sec");
    }
    async calloracle(){
      this.keys = JSON.parse(localStorage.getItem("keys"));
      if(!this.keys){
        alert("还未生成密钥");
        return
      }
      this.sec = JSON.parse(localStorage.getItem("sec"));
      if(!this.sec){
        alert("还未生成秘密");
        return
      }
      const provider = new ethers.providers.Web3Provider((window as any).ethereum);
      const account = await provider.send("eth_requestAccounts", []);
      const signer = provider.getSigner(account[0]);
      const contracts = await (await fetch("contracts.json")).json();
      const contract = new ethers.Contract(contracts.oracle, abi2, signer);
      try {
        await contract.workerrequest(signer, 11, this.sec.value.toString());
        await contract.servercallback(signer,"1111");
      } catch (e) {
        alert(e.reason);
      }
    }
    
}
</script>

