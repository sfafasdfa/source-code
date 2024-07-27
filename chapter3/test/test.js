const { ethers } = require('hardhat');
const {mimcSpongecontract} = require('circomlibjs')
const {generateCommitment,calculateMerkleRootAndZKProof} = require("zk-merkle-tree")
const { assert} = require("chai")
const SEED = "mimcsponge";

// the default verifier is for 20 levels, for different number of levels, you need a new verifier circuit
const TREE_LEVELS = 20;
describe("cs Smart contract test", () => {
    let cs, commitment1, commitment2, commitment3
    beforeEach(async () => {
        //deploy contracts
        const signers = await ethers.getSigners()
        const MiMCSponge = new ethers.ContractFactory(mimcSpongecontract.abi, mimcSpongecontract.createCode(SEED, 220), signers[0])
        const mimcsponge = await MiMCSponge.deploy()
        console.log(`MiMC sponge hasher address: ${mimcsponge.address}`)
        const Verifier = await ethers.getContractFactory("Verifier");
        const verifier = await Verifier.deploy();
        console.log(`Verifier address: ${verifier.address}`)
        const Crowdsensing = await ethers.getContractFactory("cs");
        cs = await Crowdsensing.deploy(TREE_LEVELS, mimcsponge.address, verifier.address);
        console.log(`cs address: ${cs.address}`)
        // register 3 workers
        await cs.connect(signers[0]).registerValidator(signers[1].address)
        await cs.connect(signers[0]).registerValidator(signers[2].address)
        await cs.connect(signers[0]).registerValidator(signers[3].address)
        //generate 3 commit
        commitment1 = await generateCommitment()
        commitment2 = await generateCommitment()
        commitment3 = await generateCommitment()
        console.log(`commit1: ${commitment1.commitment.toString()}`)
        console.log(`commit2: ${commitment2.commitment.toString()}`)
        console.log(`commit3: ${commitment3.commitment.toString()}`)
    });
    it("Test the full process", async () => {
        const signers = await ethers.getSigners()
        // register 3 commit      
        await cs.connect(signers[1]).registerCommitment(1, commitment1.commitment)       
        await cs.connect(signers[2]).registerCommitment(2, commitment2.commitment)    
        await cs.connect(signers[3]).registerCommitment(3, commitment3.commitment)
        // calculate zkp
        const cd1 = await calculateMerkleRootAndZKProof(cs.address, signers[1], TREE_LEVELS, commitment1, "keys/Verifier.zkey")     
        const cd2 = await calculateMerkleRootAndZKProof(cs.address, signers[2], TREE_LEVELS, commitment2, "keys/Verifier.zkey")
        const cd3 = await calculateMerkleRootAndZKProof(cs.address, signers[3], TREE_LEVELS, commitment3, "keys/Verifier.zkey")
        console.log(`cd1: ${cd1.proof_a.toString()},${cd1.proof_b.toString()},${cd1.proof_c.toString()}`)
        console.log(`cd2: ${cd2.proof_a.toString()},${cd2.proof_b.toString()},${cd2.proof_c.toString()}`)
        console.log(`cd3: ${cd3.proof_a.toString()},${cd3.proof_b.toString()},${cd3.proof_c.toString()}`)
        //register zkp
        await cs.connect(signers[4]).anoregis(cd1.nullifierHash, cd1.root, cd1.proof_a, cd1.proof_b, cd1.proof_c)
        await cs.connect(signers[5]).anoregis(cd2.nullifierHash, cd2.root, cd2.proof_a, cd2.proof_b, cd2.proof_c)
        await cs.connect(signers[6]).anoregis(cd3.nullifierHash, cd3.root, cd3.proof_a, cd3.proof_b, cd3.proof_c)
        //show anoregister results
        const result1 = await cs.showano(signers[4].address)
        const result2 = await cs.showano(signers[5].address)
        const result3 = await cs.showano(signers[6].address)
        console.log(`ano1: ${result1.toString()}`)
        console.log(`ano2: ${result2.toString()}`)
        console.log(`ano3: ${result3.toString()}`)  
    });

    it("test one", async ()=>{
        const signers = await ethers.getSigners()
        //verify 1 unregistered worker register commit
        const commitment4 = await generateCommitment()
        await cs.connect(signers[7]).registerCommitment(7, commitment4.commitment)
    })
    it("test two", async ()=>{    
        const signers = await ethers.getSigners()
        //verify 2 use a used commit to register commit
        await cs.connect(signers[1]).registerCommitment(1, commitment1.commitment)
        await cs.connect(signers[0]).registerValidator(signers[7].address)
        await cs.connect(signers[7]).registerCommitment(7, commitment1.commitment)
    })
    it("test three", async ()=>{
        const signers = await ethers.getSigners()
        //verify 3 use a used commit to register ano
        await cs.connect(signers[3]).registerCommitment(3, commitment3.commitment)
        const cd3 = await calculateMerkleRootAndZKProof(cs.address, signers[3], TREE_LEVELS, commitment3, "keys/Verifier.zkey")
        await cs.connect(signers[6]).anoregis(cd3.nullifierHash, cd3.root, cd3.proof_a, cd3.proof_b, cd3.proof_c)
        await cs.connect(signers[8]).anoregis(cd3.nullifierHash, cd3.root, cd3.proof_a, cd3.proof_b, cd3.proof_c)
    })
});