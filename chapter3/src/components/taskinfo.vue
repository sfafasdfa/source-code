<template>
    <div>
      <el-row>
        <el-col span="12">
          <el-botton @click="taskadd" >taskadd</el-botton>
          <el-dialog v-model="dialog1" width="500" title="标题" draggable @close="dialogClose1">
            <el-form label-width="80">
                <el-form-item label="名称">
                    <el-input v-model="inputdata1.value.name" placeholder="请填写名称" />
                </el-form-item>
                <el-form-item label="x">
                    <el-input v-model="inputdata1.value.x" placeholder="请填写坐标x" />
                </el-form-item>
                <el-form-item label="y">
                    <el-input v-model="inputdata1.value.y" placeholder="请填写坐标y" />
                </el-form-item>
                <el-form-item label="reward">
                    <el-input v-model="inputdata1.value.reward" placeholder="请填写奖励" />
                </el-form-item>
                <el-form-item label="日期时间">
                    <el-date-picker v-model="inputdata1.value.date" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit1">添加</el-button>
                    <el-button @click="reset1">重置</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
        </el-col>
        <el-col span="12">
          <el-botton @click = "register">register</el-botton>
          <el-dialog v-model="dialog2" width="500" title="标题" draggable @close="dialogClose2">
            <el-form label-width="80">
              <el-form-item label="x">
                    <el-input v-model="inputdata2.value.x" placeholder="请填写坐标x" />
                </el-form-item>
                <el-form-item label="x">
                    <el-input v-model="inputdata2.value.y" placeholder="请填写坐标y" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit2">添加</el-button>
                    <el-button @click="reset2">重置</el-button>
                </el-form-item>
            </el-form>
          </el-dialog>
        </el-col>
      </el-row>
      <el-row>
        <el-table :data="carddata">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="x" label="横坐标" />
          <el-table-column prop="y" label="纵坐标" />
          <el-table-column prop="reward" label="奖励" />
          <el-table-column prop="date" label="时间" />
          <el-table-column label="操作">
          <template #default="scope">
        <el-button @click="deletetask(scope.$index)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</el-row>
    </div>
  </template>
  
  <script lang="ts" >
  import { ref } from 'vue'
  import { Component, Vue } from "vue-facing-decorator";
  import * as ethers from "ethers";
  import { calculateMerkleRootAndZKProof } from "zk-merkle-tree";
  const TREE_LEVELS = 20;
  const abi =[
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
  export default class taskinfo extends Vue{
  carddata = ref([]);
  dialog1 =ref(false);
  dialog2 =ref(false);
  inputdata1 = ref({
            name: '',
            x: '',
            y: '',
            reward: '',
            date: '',
            })
  inputdata2 = ref({
            x: '',
            y: '',
            })
  async mounted(){
    this.carddata.value = await this.getblockdata();
  }
  async deletetask(index:any){
    const provider = new ethers.providers.Web3Provider((window as any).ethereum);
    const account = await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner(account[0]);
    const contracts = await (await fetch("contracts.json")).json();
    const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
    try {
      await contract.deletetask(index);
    } catch (e) {
      alert(e.reason);
    }
    this.carddata = await this.getblockdata();
  }
  async getblockdata(){
    const provider = new ethers.providers.Web3Provider(
      (window as any).ethereum
    );
    await provider.send("eth_requestAccounts", []);
    const account = await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner(account[0]);
    const contracts = await (await fetch("contracts.json")).json();
    const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
    const data = await contract.gettasklistinfo();
    return data;
  }
  async taskadd(){
    this.dialog1 = ref(true);
  }
  async register(){
    this.dialog2 = ref(true);
  }
  async submit1(){
    const {name,x,y,reward,date} = this.inputdata1.value;
    if (name == ''||x == ''||y == ''||reward == ''||date == '') {
      alert("Please input complete question!");
      return;
    }
    const provider = new ethers.providers.Web3Provider((window as any).ethereum);
    const account = await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner(account[0]);
    const contracts = await (await fetch("contracts.json")).json();
    const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
    try {
      await contract.addtotasklist(
                name,
                parseInt(x),
                parseInt(y),
                parseInt(reward),
                date.toString()
            );
    } catch (e) {
      alert(e.reason);
    }
    this.dialog2 = ref(false);
    this.reset1();
  }
  async reset1(){
    this.inputdata1.value = {
            name: '',
            x: '',
            y: '',
            reward: '',
            date: '',
            };
  }
  async submit2(){
    if(this.inputdata2.value.x == ''|| this.inputdata2.value.y == ''){
      alert("Please input complete question!");
      return;
    }

    const commitment = JSON.parse(
      localStorage.getItem("registercommit")
    );
    if (!commitment) {
      alert("No commitment generated, please register!");
      return;
    }

    
    const provider = new ethers.providers.Web3Provider(
      (window as any).ethereum
    );
    await provider.send("eth_requestAccounts", []);
    const account = await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner(account[0]);
    const contracts = await (await fetch("contracts.json")).json();
    const contract = new ethers.Contract(contracts.Crowdsensing, abi, signer);
    const cd = await calculateMerkleRootAndZKProof(
      contracts.Crowdsensing,
      signer,
      TREE_LEVELS,
      commitment,
      "verifier.zkey"
    );
    try {
      await contract.registermission(
        parseInt(this.inputdata2.value.x),
        parseInt(this.inputdata2.value.y),
        cd.nullifierHash,
        cd.root,
        cd.proof_a,
        cd.proof_b,
        cd.proof_c
      );
    } catch (e) {
      alert(e.reason);
    }
    this.dialog2 = ref(false);
    this.reset2();
  }
  async reset2(){
    this.inputdata2.value = {
                x: '',
                y:''
            }
  }
  dialogClose1(){
    console.log("关闭");
  }
  dialogClose2(){
    console.log("关闭");
  }
  }
 
  
  </script>
  