<script setup>
import { ref, nextTick } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const showResult = ref(false)
const resultSection = ref(null)
const literSection = ref(null)

const form = ref({
  inbound: "",
  outbound: ""
})

const result = ref({
  totalLiter: 0,
  totalMain: 0,
  totalBackup: 0,
  totalAll: 0
})

// linear regression
// X (liter)    = [87269, 97119.07, 94616.71, 104219]
// Y (manpower) = [30, 29, 31, 31]
const trainingX = [87269, 97119.07, 94616.71, 104219]
const trainingY = [30, 29, 31, 31]

function trainLinearRegression(x, y) {
  const n = x.length
  const meanX = x.reduce((a, b) => a + b, 0) / n
  const meanY = y.reduce((a, b) => a + b, 0) / n

  let num = 0, den = 0
  for (let i = 0; i < n; i++) {
    num += (x[i] - meanX) * (y[i] - meanY)
    den += (x[i] - meanX) ** 2
  }

  const slope = num / den
  const intercept = meanY - slope * meanX
  return { slope, intercept }
}

const { slope, intercept } = trainLinearRegression(trainingX, trainingY)

function manpowerCalculation() {
  const inbound = Number(form.value.inbound)
  const outbound = Number(form.value.outbound)

  if (isNaN(inbound) || isNaN(outbound) || inbound <= 0 || outbound <= 0) {
    alert("Inbound dan outbound harus diisi dengan angka valid")
    return false
  }

  const totalLiter = inbound + outbound
  const totalMain = Math.round(slope * totalLiter + intercept)
  const totalBackup = Math.round(totalMain * 0.10)
  const totalAll = totalMain + totalBackup

  result.value = {
    totalLiter,
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
  form.value = { inbound: "", outbound: "" }
  result.value = { totalLiter: 0, totalMain: 0, totalBackup: 0, totalAll: 0 }

  await nextTick()
  literSection.value?.scrollIntoView({ behavior: "smooth" })
}
</script>

<template>
  <div class="container">
    <h1>Liter-Based Manpower Planning</h1>
    <p>Estimate workforce requirements based on liter volume</p>

    <div class="card" ref="literSection">
      <h3>Activity Information</h3>

      <div class="field">
        <label>Inbound (liter)</label>
        <input
          type="number"
          v-model="form.inbound"
          placeholder="e.g. 48323"
          @keyup.enter="$refs.outboundInput.focus()"
        />
      </div>

      <div class="field">
        <label>Outbound (liter)</label>
        <input
          type="number"
          v-model="form.outbound"
          placeholder="e.g. 38946"
          ref="outboundInput"
          @keyup.enter="calculate"
        />
      </div>

      <button class="btn" @click="calculate">Calculate Manpower</button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Estimation Result</h3>

      <div class="result-meta">
        <span>Total Liter: {{ result.totalLiter.toLocaleString('id-ID') }}</span>
      </div>

      <div class="metrics">
        <div class="metric-card">
          <p class="metric-label">Main Manpower</p>
          <p class="metric-value">{{ result.totalMain }}</p>
          <p class="metric-unit">people</p>
        </div>

        <div class="metric-card">
          <p class="metric-label">Backup (10%)</p>
          <p class="metric-value">{{ result.totalBackup }}</p>
          <p class="metric-unit">people</p>
        </div>
      </div>

      <div class="metric-total">
        <div>
          <p class="total-label">Total Manpower</p>
          <p class="total-sub">Main + Backup</p>
        </div>

        <div class="total-right">
          <span class="total-value">{{ result.totalAll }}</span>
          <span class="total-unit"> people</span>
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

input {
  width: 100%;
  padding: 8px 10px;
  margin-bottom: 12px;
  border-radius: 6px;
  border: 1px solid #dcdcdc;
  box-sizing: border-box;
}

input:focus {
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
  background: #fff;
  max-width: 500px;
  margin: 30px auto;
  padding: 24px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  animation: fadeIn 0.4s ease-in-out;
}

.result-meta {
  margin-bottom: 16px;
}

.result-meta span {
  display: inline-block;
  font-size: 12px;
  background: #f5f5f5;
  padding: 4px 10px;
  border-radius: 20px;
}

.metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.metric-card {
  background: #f8f8f8;
  padding: 14px;
  border-radius: 8px;
}

.metric-label {
  font-size: 12px;
  color: #666;
}

.metric-value {
  font-size: 28px;
  font-weight: 500;
}

.metric-unit {
  font-size: 13px;
  color: #888;
}

.metric-total {
  background: #026766;
  border-radius: 8px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.metric-card:hover {
  background: #e9f7f7;
  transform: translateY(-2px);
  transition: 0.2s;
}

.total-label {
  color: white;
}

.total-sub {
  color: rgba(255,255,255,0.7);
  font-size: 12px;
}

.total-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  text-align: right;
  gap: 4px;
}

.total-value {
  font-size: 30px;
  color: white;
  line-height: 1;
}

.total-unit {
  color: rgba(255,255,255,0.8);
  align-self: center;
}

.help-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 50px;
  height: 50px;
  background: #026766;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 6px 12px rgba(0,0,0,0.2);
  transition: 0.2s;
}

.help-button:hover {
  background: #014f4f;
  transform: scale(1.05);
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