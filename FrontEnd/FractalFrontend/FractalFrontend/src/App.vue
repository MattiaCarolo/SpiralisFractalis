<template>
  <div id="app">
    <Fractals />
  </div>
</template>
<script>
import Fractals from "./components/Fractals.vue";
export default {
  name: "App",
  components: {
    Fractals,
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>