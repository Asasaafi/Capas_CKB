<script setup>
import { ref, nextTick } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const showResult = ref(false)
const resultSection = ref(null)
const formSection = ref(null)

const form = ref({ totalLI: "" })
const result = ref({ main: 0, backup: 0, total: 0 })
const errors = ref({ li: false })

const LI_TRAIN = [7313, 3525, 15715, 9507, 20430, 12359, 16067, 20887, 27153, 26558, 34526, 44884, 58349]
const MP_TRAIN = [30, 18, 21, 32, 39, 34, 38, 43, 50, 45, 52, 61, 72]

function linearRegression(xArr, yArr) {
  const n = xArr.length
  const xMean = xArr.reduce((a, b) => a + b, 0) / n
  const yMean = yArr.reduce((a, b) => a + b, 0) / n

  let num = 0
  let den = 0

  for (let i = 0; i < n; i++) {
    num += (xArr[i] - xMean) * (yArr[i] - yMean)
    den += (xArr[i] - xMean) ** 2
  }

  return {
    slope: num / den,
    intercept: yMean - (num / den) * xMean
  }
}

const { slope, intercept } = linearRegression(LI_TRAIN, MP_TRAIN)

function manpowerCalculation() {
  const totalLI = Number(form.value.totalLI)

  errors.value.li = isNaN(totalLI) || totalLI <= 0
  if (errors.value.li) return false

  const mp = Math.round(slope * totalLI + intercept)
  const backup = Math.ceil(mp * 0.10)

  result.value = {
    main: mp,
    backup,
    total: mp + backup
  }

  return true
}

const calculate = async () => {
  if (!manpowerCalculation()) return

  showResult.value = true
  await nextTick()
  resultSection.value?.scrollIntoView({ behavior: "smooth" })
}

const resetForm = async () => {
  showResult.value = false
  form.value = { totalLI: "" }
  result.value = { main: 0, backup: 0, total: 0 }
  errors.value = { li: false }

  await nextTick()
  formSection.value?.scrollIntoView({ behavior: "smooth" })
}
</script>

<template>
  <div class="container">
    <h1>Site management Manpower Planning</h1>
    <p>Estimate workforce requirements based on total line items (LI)</p>

    <div class="card" ref="formSection">
      <h3>Activity Information</h3>

      <div class="field">
        <label>Total Line Item (LI)</label>
        <input
          type="number"
          v-model="form.totalLI"
          placeholder="e.g. 58349"
          :class="{ error: errors.li }"
          @keyup.enter="calculate"
        />
        <span class="err-msg" v-if="errors.li">
          Please enter a valid line item value
        </span>
      </div>

      <button class="btn" @click="calculate">Calculate Manpower</button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Estimation Result</h3>

      <div class="result-meta">
        <span>LI: {{ Number(form.totalLI).toLocaleString('id-ID') }}</span>
      </div>

      <div class="metrics">
        <div class="metric-card">
          <p class="metric-label">Main Manpower</p>
          <p class="metric-value">{{ result.main }}</p>
          <p class="metric-unit">people</p>
        </div>

        <div class="metric-card">
          <p class="metric-label">Backup (10%)</p>
          <p class="metric-value">{{ result.backup }}</p>
          <p class="metric-unit">people</p>
        </div>
      </div>

      <div class="metric-total">
        <div>
          <p class="total-label">Total Manpower</p>
          <p class="total-sub">Main + Backup</p>
        </div>

        <div class="total-right">
          <span class="total-value">{{ result.total }}</span>
          <span class="total-unit"> people</span>
        </div>
      </div>

      <button class="btn" @click="resetForm">Try Again</button>
    </div>
  </div>

  <div class="help-button" @click="router.push('/manpower')">?</div>
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

.card,
.result-section {
  background: #fff;
  max-width: 500px;
  margin: 30px auto;
  padding: 24px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.field {
  margin-bottom: 14px;
}

label {
  display: block;
  font-size: 14px;
  margin: 8px 0 4px;
}

input {
  width: 100%;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #dcdcdc;
  box-sizing: border-box;
}

input.error {
  border-color: #e74c3c;
}

.err-msg {
  font-size: 12px;
  color: #e74c3c;
}

.btn,
.btn-outline {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  margin-top: 10px;
}

.btn {
  background: #026766;
  color: #fff;
  border: none;
}

.btn-outline {
  background: transparent;
  color: #026766;
  border: 1px solid #026766;
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
  cursor: pointer;
}
</style>