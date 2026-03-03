<template>
  <div class="sidebar">
    <h2>CAPAS</h2>

    <ul>
      <li>
        <router-link to="/">Dashboard</router-link>
      </li>

      <li class="menu-title">Storage Calculation</li>
      <ul class="submenu">
        <li>
          <router-link to="/storage/bulking">Bulking Input</router-link>
        </li>
        <li>
          <router-link to="/storage/upload">File Upload</router-link>
        </li>
      </ul>

      <li>
        <router-link to="/mhe">MHE Calculation</router-link>
      </li>

      <li>
        <router-link to="/manpower">Manpower Calculation</router-link>
      </li>

      <li>
        <router-link to="/history">History</router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
</script>

<style scoped>
.sidebar {
  width: 220px;
  background-color: #0f1b2d;
  color: white;
  padding: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 15px 0;
  cursor: pointer;
}

li:hover {
  color: #4ea8ff;
}

a {
  text-decoration: none;
  color: white;
}

a:hover {
  color: #4ea8ff;
}

.menu-title {
  margin-top: 15px;
  font-weight: bold;
  opacity: 0.7;
}

.submenu {
  padding-left: 15px;
  margin-bottom: 10px;
}

.submenu li {
  margin: 8px 0;
}
</style>