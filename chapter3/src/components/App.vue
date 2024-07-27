<template>
  <div class="common-layout">
    <el-container>
      <el-header><Header></Header></el-header>
      <el-container>
        <el-aside width="200px"><Aside></Aside></el-aside>
        <el-main><router-view></router-view></el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

import Header from "./header.vue";
import Aside from "./aside.vue"
import { defineComponent } from "vue";




export default defineComponent({
  name: "App",
  components: { 
    Header, 
    Aside, 
  }
});
</script>

<style>
  html,
  body{
    height: 100%;
    margin: 0;
    border: 0;
    padding: 0;
  }
</style>

