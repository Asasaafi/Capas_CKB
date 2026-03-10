<script setup>
import { ref, nextTick } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const showResult = ref(false)
const resultSection = ref(null)
const formSection = ref(null)

const form = ref({
  site: "",
  totalLI: ""
})

const result = ref({
  main: 0,
  backup: 0,
  total: 0
})

const gr_percent = 0.01
const gi_percent = 0.005
const slope = 0.043031
const intercept = 7.550311
const st_formula = li => (li * 2) / 12 / 24

function manpowerCalculation() {
  const site = form.value.site
  const totalLI = Number(form.value.totalLI)

  if (!site) {
    alert("Site location must be selected")
    return false
  }
  if (isNaN(totalLI) || totalLI <= 0) {
    alert("Total Line Item must be valid")
    return false
  }

  // Hitung activity (GR, GI, ST)
  const li_gr = totalLI * gr_percent
  const li_gi = totalLI * gi_percent
  const li_st = st_formula(totalLI)

  // Hitung manpower per activity
  const mp_gr = Math.round(slope * li_gr + intercept)
  const mp_gi = Math.round(slope * li_gi + intercept)
  const mp_st = Math.round(slope * li_st + intercept)

  const mp_total = mp_gr + mp_gi + mp_st
  const backup = Math.ceil(mp_total * 0.10)
  const total = mp_total + backup

  result.value = {
    main: mp_total,
    backup: backup,
    total: total
  }

  return true
}

const calculate = async () => {
  const success = manpowerCalculation()
  if (!success) return

  showResult.value = true
  await nextTick()
  resultSection.value?.scrollIntoView({ behavior: "smooth" })
}

const goToManpower = () => {
  router.push("/manpower")
}

const resetForm = async () => {
  showResult.value = false
  form.value = { site: "", totalLI: "" }
  result.value = { main: 0, backup: 0, total: 0 }
  await nextTick()
  formSection.value?.scrollIntoView({ behavior: "smooth" })
}
</script>

<template>
  <div class="container">
    <h1>Manpower Activity Planning</h1>
    <p>Estimate workforce requirements based on warehouse activities.</p>

    <div class="card" ref="formSection">
      <h3>Activity Information</h3>

      <div class="field">
        <label>Site Location</label>
        <select v-model="form.site">
          <option value="">Select Site</option>
          <option value="BSI">BSI</option>
          <option value="PANI">PANI</option>
        </select>
      </div>

      <div class="field">
        <label>Total Line Item (LI)</label>
        <input
          type="number"
          v-model="form.totalLI"
          placeholder="e.g. 7313"
        />
      </div>

      <button class="btn" @click="calculate">
        Calculate Manpower
      </button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Manpower Result</h3>

      <div class="result-group">
        <div class="field">
          <label>Main Manpower</label>
          <input :value="result.main" readonly />
        </div>

        <div class="field">
          <label>Backup Manpower (10%)</label>
          <input :value="result.backup" readonly />
        </div>

        <div class="field">
          <label>Total Manpower</label>
          <input :value="result.total" readonly />
        </div>
      </div>

      <button class="btn try-btn" @click="resetForm">
        Try Again
      </button>
    </div>
  </div>

  <div class="help-button" @click="goToManpower">
    ?
  </div>
</template>

<style scoped>
.container {
  padding: 20px 40px;
}

h1 {
  margin-bottom: 8px;
}

p {
  margin-bottom: 20px;
  color: #555;
}

.card {
  background: #fff;
  max-width: 500px;
  margin: 30px auto;
  padding: 24px;

  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

label {
  display: block;
  font-size: 14px;
  margin: 8px 0 4px;
}

input,
select {
  width: 100%;
  padding: 8px 10px;
  margin-bottom: 12px;

  border-radius: 6px;
  border: 1px solid #dcdcdc;
  box-sizing: border-box;
}

input:focus,
select:focus {
  outline: none;
  border-color: #026766;
  box-shadow: 0 0 0 2px rgba(2,103,102,0.1);
}

.btn {
  width: 100%;
  padding: 10px;

  background: #026766;
  color: #fff;

  border: none;
  border-radius: 6px;
  margin-top: 10px;

  cursor: pointer;
  font-weight: 500;
}

.btn:hover {
  background: #014f4f;
}

.result-section {
  max-width: 500px;
  margin: 40px auto;
  animation: fadeIn 0.4s ease-in-out;
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

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>