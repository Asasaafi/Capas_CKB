<!-- <script setup>
import { ref } from "vue"

const search = ref("")
const typeFilter = ref("All Types")
</script>

<template>
  <div class="container">

    <h1>Calculation History</h1>
    <p>View and manage all previously performed calculations</p>

    <div class="filter-wrapper">

      <input
        class="search"
        type="text"
        v-model="search"
        placeholder="Search for part number, file, or name"
      />

      <select class="filter" v-model="typeFilter">
        <option>All Types</option>
        <option>Storage Calculation</option>
        <option>MHE Calculation</option>
        <option>Manpower Calculation</option>
      </select>

    </div>

    <div class="history-box">

      <div class="history-content">
        <div class="icon">↻</div>
        <h3>No History Available</h3>
        <p>Perform a calculation to view the history</p>
      </div>

    </div>

  </div>
</template>

<style scoped>
.container{
  padding:20px 40px;
  max-width:1100px;
  margin:0 auto;
}

h1{
  margin-bottom:8px;
}

p{
  margin-bottom:24px;
  color:#666;
}

.filter-wrapper{
  display:flex;
  align-items:center;
  gap:20px;
  padding:14px 20px;
  border:1px solid #dcdcdc;
  border-radius:10px;
  background:#fff;
  width:100%;
}

.search{
  flex:2;
  padding:10px 14px;
  border-radius:20px;
  border:1px solid #dcdcdc;
  background:#f5f5f5;
  font-size:14px;
}

.filter{
  flex:1;
  padding:10px 14px;
  border-radius:20px;
  border:1px solid #dcdcdc;
  background:#f3f4f6;
  font-size:14px;
  cursor:pointer;
}

.history-box{
  margin-top:28px;
  width:100%;
  border:1px solid #cfcfcf;
  border-radius:8px;
  padding:50px 20px;
  text-align:center;
}

.icon{
  font-size:26px;
  margin-bottom:8px;
}

.history-content h3{
  margin-bottom:4px;
}

.history-content p{
  color:#888;
}
</style> -->