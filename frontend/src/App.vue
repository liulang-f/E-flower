<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* 全局样式，或者引入其他样式 */
@import './assets/styles/global.css';

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f7f7f7;
}
</style>
