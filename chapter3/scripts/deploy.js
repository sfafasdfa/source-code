import * as fs from 'fs'
import pkg from 'hardhat';
const { ethers } = pkg;
import { mimcSpongecontract } from 'circomlibjs'

const SEED = "mimcsponge";
const TREE_LEVELS = 20;

async function main() {
    const signers = await ethers.getSigners()
    console.log(signers)
    const MiMCSponge = new ethers.ContractFactory(mimcSpongecontract.abi, mimcSpongecontract.createCode(SEED, 220), signers[0])
    const mimcsponge = await MiMCSponge.deploy()
    console.log(`MiMC sponge hasher address: ${mimcsponge.address}`)

    const Verifier = await ethers.getContractFactory("Verifier");
    const verifier = await Verifier.deploy();
    console.log(`Verifier address: ${verifier.address}`)

    const Oracle = await ethers.getContractFactory("Oracle");
    const oracle = await Oracle.deploy();
    console.log(`Oracle address: ${oracle.address}`)

    const Crowdsensing = await ethers.getContractFactory("ZKTreeVote");
    const crowdsensing = await Crowdsensing.deploy(TREE_LEVELS, mimcsponge.address, verifier.address, oracle.address);
    console.log(`Crowdsensing address: ${crowdsensing.address}`)

    // add the 2nd hardhat account as a validator
    await crowdsensing.registerValidator("0x6Ef6EC1efB273C4E6AeE218519d36Bd82cb770b2")

    fs.writeFileSync("static/contracts.json", JSON.stringify({
        mimc: mimcsponge.address,
        verifier: verifier.address,
        oracle:oracle.address,
        Crowdsensing: crowdsensing.address
    }))
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});