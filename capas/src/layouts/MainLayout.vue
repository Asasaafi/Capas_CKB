<template>
  <div class="layout">
    <Sidebar />
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  background-color: #f5f7fa;
  padding: 20px;
}
</style>