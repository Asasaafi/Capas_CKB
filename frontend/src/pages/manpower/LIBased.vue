<script setup>
import { ref, nextTick } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const showResult = ref(false)
const resultSection = ref(null)
const liSection = ref(null)

const form = ref({
  liInbound: "",
  liOutbound: ""
})

const result = ref({
  totalMain: 0,
  totalBackup: 0,
  totalAll: 0
})

function manpowerCalculation() {
  const liInbound = Number(form.value.liInbound)
  const liOutbound = Number(form.value.liOutbound)

  if (isNaN(liInbound) || isNaN(liOutbound) || liInbound <= 0 || liOutbound <= 0) {
    alert("Inbound and outbound values must be filled and must be valid numbers")
    return false
  }

  const inboundBase = 500
  const outboundBase = 600

  const inboundRoles = {
    "Ops Forklift": 1,
    "Admin": 1,
    "Warehouse Checker (Tetap)": 2,
    "Warehouse Checker (Harian)": 8
  }

  const outboundRoles = {
    "Ops Forklift": 1,
    "Admin": 7,
    "Warehouse Picker": 6,
    "Warehouse Checker": 10,
    "Warehouse Handover": 2
  }

  const roleTotals = {}

  // Hitung inbound
  for (const role in inboundRoles) {
    const main = (liInbound / inboundBase) * inboundRoles[role]
    roleTotals[role] = (roleTotals[role] || 0) + main
  }

  // Hitung outbound
  for (const role in outboundRoles) {
    const main = (liOutbound / outboundBase) * outboundRoles[role]
    roleTotals[role] = (roleTotals[role] || 0) + main
  }

  let totalMain = 0
  let totalBackup = 0

  // Pembulatan per role + cadangan 1
  for (const role in roleTotals) {
    const mainCeil = Math.ceil(roleTotals[role])
    const backup = 1

    totalMain += mainCeil
    totalBackup += backup
  }

  const totalAll = totalMain + totalBackup

  result.value = {
    totalMain,
    totalBackup,
    totalAll
  }

  return true
}

const goToManpower = () => {
  router.push("/manpower")
}

const calculate = async () => {
  const success = manpowerCalculation()
  if (!success) return

  showResult.value = true
  await nextTick()
  resultSection.value?.scrollIntoView({ behavior: "smooth" })
}

const resetForm = async () => {
  showResult.value = false
  form.value = { liInbound: "", liOutbound: "" }
  result.value = { totalMain: 0, totalBackup: 0, totalAll: 0 }

  await nextTick()
  liSection.value?.scrollIntoView({ behavior: "smooth" })
}
</script>

<template>
  <div class="container">
    <h1>LI-Based Manpower Planning</h1>
    <p>Estimate workforce requirements based on LI volume.</p>

    <div class="card" ref="liSection">
      <h3>Activity Information</h3>

      <div class="field">
        <label>Inbound Line Item (LI/Day)</label>
        <input type="number" v-model="form.liInbound" placeholder="e.g. 1000" />
      </div>

      <div class="field">
        <label>Outbound Line Item (LI/Day)</label>
        <input type="number" v-model="form.liOutbound" placeholder="e.g. 1200" />
      </div>

      <button class="btn" @click="calculate">Calculate Manpower</button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Total Manpower</h3>

      <div class="result-group">
        <div class="field">
          <label>Main Manpower</label>
          <input :value="result.totalMain" readonly />
        </div>
        <div class="field">
          <label>Backup Manpower</label>
          <input :value="result.totalBackup" readonly />
        </div>
        <div class="field">
          <label>Total Manpower</label>
          <input :value="result.totalAll" readonly />
        </div>
      </div>

      <button class="btn try-btn" @click="resetForm">Try Again</button>
    </div>
  </div>

  <div class="help-button" @click="goToManpower">
    ?
  </div>
</template>

<style scoped>

.container{
  padding:20px 40px;
}

h1{
  margin-bottom:8px;
}

p{
  margin-bottom:20px;
  color:#555;
}

.card{
  background:#fff;
  max-width:500px;
  margin:30px auto;
  padding:24px;

  border:1px solid #e0e0e0;
  border-radius:10px;

  box-shadow:0 4px 12px rgba(0,0,0,0.05);
}

label{
  display:block;
  font-size:14px;
  margin:8px 0 4px;
}

input{
  width:100%;
  padding:8px 10px;
  margin-bottom:12px;

  border-radius:6px;
  border:1px solid #dcdcdc;
  box-sizing:border-box;
}

input:focus{
  outline:none;
  border-color:#026766;
  box-shadow:0 0 0 2px rgba(2,103,102,0.1);
}

.btn{
  width:100%;
  padding:10px;

  background:#026766;
  color:#fff;

  border:none;
  border-radius:6px;
  margin-top:10px;

  cursor:pointer;
  font-weight:500;
}

.btn:hover{
  background:#014f4f;
}

.result-section{
  max-width:500px;
  margin:40px auto;
  animation:fadeIn 0.4s ease-in-out;
}

.result-group input{
  margin-bottom:12px;
}

.help-button{
  position:fixed;
  bottom:30px;
  right:30px;

  width:50px;
  height:50px;

  background:#026766;
  color:white;

  border-radius:50%;

  display:flex;
  align-items:center;
  justify-content:center;

  font-size:24px;
  font-weight:bold;

  cursor:pointer;

  box-shadow:0 6px 12px rgba(0,0,0,0.2);

  transition:0.2s;
}

.help-button:hover{
  background:#014f4f;
  transform:scale(1.05);
}

@keyframes fadeIn{
  from{
    opacity:0;
    transform:translateY(20px);
  }
  to{
    opacity:1;
    transform:translateY(0);
  }
}
</style>