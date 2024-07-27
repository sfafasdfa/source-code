<template>
  <main role="main" class="container">
    <div style="padding-top: 7rem" class="d-none d-lg-block"></div>
    <div class="row justify-content-md-center">
      <div class="col-lg-4">
        <div class="text-center vstack gap-3">
                  
          <button class="btn btn-info" @click="getcomit">
            get commitment
          </button>
          <h1>Your commitment</h1>  
          <img :src="qrcodeDataUrl"/>
          <div
            v-if="commitment"
            v-html="splitTwoLines(commitment.commitment)"
          ></div>

          <button class="btn btn-info" @click="copyToClipboard">
            Copy to clipboard
          </button>
          <button class="btn btn-danger" @click="resetCommitment">
            Reset commitment
          </button>
          <a href="#/" class="btn btn-primary">Back</a>
        </div>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { Component, Vue } from "vue-facing-decorator";
import {generateCommitment} from 'zk-merkle-tree';
import QRCode from "qrcode";
import copyToClipboard from "copy-to-clipboard";

@Component
export default class VoterRegistration extends Vue {
  public commitment:  any = "";
  public qrcodeDataUrl: any = "";

  
  async getcomit(){
    console.log("1");
    this.commitment = JSON.parse(localStorage.getItem("zktree-vote-commitment"));
    console.log(this.commitment);
    console.log("2");
    if (!this.commitment) {
      var comit =  await generateCommitment();
      var tempjson = {commitment:comit.commitment.toString(),
        nullifier:comit.nullifier.toString(),
        nullifierHash:comit.nullifierHash.toString(),
        secret: comit.secret.toString(),
      }
      this.commitment = tempjson
      localStorage.setItem(
        "zktree-vote-commitment",
        JSON.stringify(this.commitment)
      );
      console.log(this.commitment);
      
    }
    console.log("3");
    this.qrcodeDataUrl =  await QRCode.toDataURL(this.commitment.commitment);
  }

  splitTwoLines(text: string) {
    if(text){
      const half = text.length / 2;
      return (
      text.substring(0, half) + "<br/>" + text.substring(half + 1, text.length));
      }
    }
    

  public copyToClipboard() {
    copyToClipboard(this.commitment.commitment);
    alert("Successfully copied to the clipboard");
  }

  public resetCommitment() {
    localStorage.removeItem("zktree-vote-commitment");
    window.location.reload();
  }
}
</script>