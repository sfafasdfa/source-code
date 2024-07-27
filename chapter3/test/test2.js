const { ethers } = require('hardhat');
const {mimcSpongecontract} = require('circomlibjs')
const {generateCommitment,calculateMerkleRootAndZKProof} = require("zk-merkle-tree")
const { assert} = require("chai")
const SEED = "mimcsponge";
const BlindSignature = require("./rsablind.cjs");
// the default verifier is for 20 levels, for different number of levels, you need a new verifier circuit
const TREE_LEVELS = 20;
describe("cs Smart contract test", () => {
    let zkpc, ringsignc, blindsignc
    beforeEach(async () => {
        const signers = await ethers.getSigners()
        const MiMCSponge = new ethers.ContractFactory(mimcSpongecontract.abi, mimcSpongecontract.createCode(SEED, 220), signers[0])
        const mimcsponge = await MiMCSponge.deploy()
        const Verifier = await ethers.getContractFactory("Verifier");
        const verifier = await Verifier.deploy();
        const ZKPC = await ethers.getContractFactory("zkpc");
        zkpc = await ZKPC.deploy(TREE_LEVELS, mimcsponge.address, verifier.address);
        const RING = await ethers.getContractFactory("ringsignc");
        ringsignc = await RING.deploy();
        const BLIND = await ethers.getContractFactory("blindsignc");
        blindsignc = await BLIND.deploy();
    });
    it("test one", async () => {//zkp
        //generate 3 commit
        
        const signers = await ethers.getSigners()
        let i;
        for(i=0;i<5;i++){

          const commitment1 = await generateCommitment()
          await zkpc.connect(signers[1]).zkmethod(i, commitment1.commitment)
          const cd1 = await calculateMerkleRootAndZKProof(zkpc.address, signers[1], TREE_LEVELS, commitment1, "keys/Verifier.zkey")   
        }
        
    });

    it("test two", async ()=>{//lrs
        const signers = await ethers.getSigners()
        
        let j;
        for(j=0;j<5;j++)
        {
          let i;
          arr = []
          for(i=0;i<80;i++){
            let max =100000
            let min =0
            let range = max-min
            let random = Math.random()
            let result = min+Math.round(random*range)
            arr.push(result)
          }
          for(i=0;i<10;i++){
            await ringsignc.connect(signers[1]).ringsignmethod(arr,0)
            await ringsignc.connect(signers[1]).get()
            await ringsignc.connect(signers[1]).ringsignmethod(arr,0)
            await ringsignc.connect(signers[1]).get()
          }
        }
        

    })
    it("test three", async ()=>{//blindc
        const signers = await ethers.getSigners()
        let j;
        for(j=0;j<5;j++){
          let i;
          arr = []
          for(i=0;i<80;i++){
            let max =100000
            let min =0
            let range = max-min
            let random = Math.random()
            let result = min+Math.round(random*range)
            arr.push(result)
          }
          for(i=0;i<10;i++){
            await blindsignc.connect(signers[1]).blindsignmethod(arr,0)
            await blindsignc.connect(signers[1]).get()
            await blindsignc.connect(signers[1]).blindsignmethod(arr,0)
            await blindsignc.connect(signers[1]).get()
            const Bob = {
                key: BlindSignature.keyGeneration({ b: 512 }),
                blinded: null,
                unblinded: null,
                message: null,
              };
              
            const Alice = {
                message: 'Hello Chaum!',
                N: null,
                E: null,
                r: null,
                signed: null,
                unblinded: null,
              };
              
              // Alice wants Bob to sign a message without revealing it's contents.
              // Bob can later verify he did sign the message
              
            console.log('Message:', Alice.message);
              
              // Alice gets N and E variables from Bob's key
            Alice.N = Bob.key.keyPair.n.toString();
            Alice.E = Bob.key.keyPair.e.toString();
              
              // N, E
            const { blinded, r } = BlindSignature.blind({
                message: Alice.message,
                N: Alice.N,
                E: Alice.E,
            }); // Alice blinds message
            Alice.r = r;
              
              // Alice sends blinded to Bob
            Bob.blinded = blinded;
              
              // N, D (P, Q)
            const signed = BlindSignature.sign({
                blinded: Bob.blinded,
                key: Bob.key,
            }); // Bob signs blinded message
              
              // Bob sends signed to Alice
            Alice.signed = signed;
              
              // N
            const unblinded = BlindSignature.unblind({
                signed: Alice.signed,
                N: Alice.N,
                r: Alice.r,
              }); // Alice unblinds
            Alice.unblinded = unblinded;
              
              // Alice verifies
              // N, E
            const result = BlindSignature.verify({
                unblinded: Alice.unblinded,
                N: Alice.N,
                E: Alice.E,
                message: Alice.message,
              });
            if (result) {
                console.log('Alice: Signatures verify!');
            } else {
                console.log('Alice: Invalid signature');
            }
              
              // Alice sends Bob unblinded signature and original message
            Bob.unblinded = Alice.unblinded;
            Bob.message = Alice.message;
              
              // Bob verifies
              // N, D
            const result2 = BlindSignature.verify2({
                unblinded: Bob.unblinded,
                key: Bob.key,
                message: Bob.message,
              });
            if (result2) {
                console.log('Bob: Signatures verify!');
            }else {
                console.log('Bob: Invalid signature');
            }
        }

        }
        
        
          


        })
});