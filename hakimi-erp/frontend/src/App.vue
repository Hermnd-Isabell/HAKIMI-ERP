<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  overflow: hidden;
}

body {
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
  font-size: 13px;
  color: #12372A;
  background: linear-gradient(135deg, #FBFADA 0%, #f5f3d8 100%);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100%;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(173, 188, 159, 0.45); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(173, 188, 159, 0.7); }

::selection {
  background-color: rgba(67, 104, 80, 0.18);
  color: #12372A;
}
</style>