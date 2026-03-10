<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const goToLI = () => {
  router.push("/manpower/li")
}

const goToActivity = () => {
  router.push("/manpower/activity")
}
</script>

<template>
  <div class="guide-container">

    <div class="header">
      <h1>Manpower Planning</h1>
      <p>
        Estimate workforce requirements based on warehouse workload and operational
        activities. Choose a calculation method below to begin the analysis.
      </p>
    </div>

    <div class="guide-cards">
      <div class="card" @click="goToLI">
        <div class="card-icon">📦</div>

        <h3>LI-Based Calculation</h3>

        <p>
          Estimate manpower requirements based on the total
          <strong>Line Items (LI)</strong> handled in warehouse operations.
          This method is suitable for quick workload estimation when the
          total handling volume is known.
        </p>

        <ul>
          <li>Fast manpower estimation</li>
          <li>Based on total handling load</li>
          <li>Suitable for planning scenarios</li>
        </ul>

        <span class="card-action">Start Calculation →</span>
      </div>

      <div class="card" @click="goToActivity">
        <div class="card-icon">⚙️</div>

        <h3>Activity-Based Calculation</h3>

        <p>
          Calculate manpower based on specific warehouse activities such as
          <strong>Goods Receipt (GR)</strong>, <strong>Goods Issue (GI)</strong>,
          and <strong>Stock Transfer (ST)</strong>.
        </p>

        <ul>
          <li>More detailed manpower analysis</li>
          <li>Based on operational activity workload</li>
          <li>Suitable for operational planning</li>
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