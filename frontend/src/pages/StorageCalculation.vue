<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const goToBulking = () => {
  router.push("/storage/bulking")
}

const goToUpload = () => {
  router.push("/storage/upload")
}
</script>

<template>
  <div class="guide-container">

    <div class="header">
      <h1>Storage Planning</h1>
      <p>
        Estimate warehouse storage requirements based on item dimensions,
        weight, and storage configuration. Choose a calculation method below
        to begin the analysis.
      </p>
    </div>

    <div class="guide-cards">

      <div class="card" @click="goToBulking">
        <div class="card-icon">📦</div>

        <h3>Bulk Calculation</h3>

        <p>
          Calculate storage requirements for individual items based on
          <strong>item dimensions</strong>, <strong>weight</strong>,
          and <strong>pallet stacking rules</strong>.
        </p>

        <ul>
          <li>Manual item input</li>
          <li>Pallet capacity estimation</li>
          <li>Warehouse area calculation</li>
        </ul>

        <span class="card-action">Start Calculation →</span>
      </div>

      <div class="card" @click="goToUpload">
        <div class="card-icon">📄</div>

        <h3>File Upload Calculation</h3>

        <p>
          Upload a dataset to automatically calculate storage requirements
          for multiple items using predefined templates.
        </p>

        <ul>
          <li>Download Excel template</li>
          <li>Upload item dataset</li>
          <li>Automatic storage prediction</li>
        </ul>

        <span class="card-action">Start Calculation →</span>
      </div>

    </div>

  </div>
</template>

<style scoped>

.guide-container{
  max-width:1100px;
  margin:auto;
  padding:40px 20px;
}

.header{
  text-align:center;
  margin-bottom:40px;
}

.header h1{
  font-size:32px;
  margin-bottom:10px;
}

.header p{
  color:#555;
  max-width:700px;
  margin:auto;
  line-height:1.6;
}

.guide-cards{
  display:flex;
  gap:30px;
  justify-content:center;
  flex-wrap:wrap;
}

.card{
  background:white;
  width:420px;
  padding:30px;

  border-radius:12px;
  border:1px solid #e6e6e6;

  box-shadow:0 6px 18px rgba(0,0,0,0.05);

  cursor:pointer;

  transition:0.25s;
}

.card:hover{
  transform:translateY(-6px);
  box-shadow:0 12px 25px rgba(0,0,0,0.08);
  border-color:#026766;
}

.card-icon{
  font-size:32px;
  margin-bottom:10px;
}

.card h3{
  margin-bottom:10px;
}

.card p{
  color:#555;
  line-height:1.5;
  margin-bottom:15px;
}

.card ul{
  padding-left:18px;
  margin-bottom:20px;
  color:#444;
}

.card li{
  margin-bottom:6px;
  font-size:14px;
}

.card-action{
  color:#026766;
  font-weight:600;
}
</style>