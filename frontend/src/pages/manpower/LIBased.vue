<script setup>
import { ref, nextTick } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const showResult = ref(false)
const resultSection = ref(null)
const liSection = ref(null)

const mode = ref("daily")

const form = ref({
  liInbound: "",
  liOutbound: ""
})

const result = ref({
  totalMain: 0,
  totalBackup: 0,
  totalAll: 0,
  perDay: 0
})

// daily (exact sklearn coefficients)
function calcDaily(liInbound, liOutbound) {
  const INTERCEPT = 7.819727891156468
  const COEF_INBOUND = 0.00993197
  const COEF_OUTBOUND = 0.03508503

  const rawPred =
    INTERCEPT +
    (COEF_INBOUND * liInbound) +
    (COEF_OUTBOUND * liOutbound)

  const totalMain = Math.ceil(rawPred)
  const totalBackup = Math.ceil(totalMain * 0.10)

  return {
    totalMain,
    totalBackup,
    totalAll: totalMain + totalBackup,
    perDay: null
  }
}

// monthly (exact sklearn coefficients)
const intercept = 36.66679822099945
const coefInbound = -0.00083654
const coefOutbound = 0.00078005

function calcMonthly(inbound, outbound) {
  const rawPred =
    intercept +
    (coefInbound * inbound) +
    (coefOutbound * outbound)

  const totalMain = Math.max(0, Math.round(rawPred))
  const totalBackup = Math.round(totalMain * 0.10)
  const totalAll = totalMain + totalBackup

  const workingDays = 26
  const perDay = Math.ceil(totalAll / workingDays)

  return {
    totalMain,
    totalBackup,
    totalAll,
    perDay
  }
}

function manpowerCalculation() {
  const liInbound = Number(form.value.liInbound)
  const liOutbound = Number(form.value.liOutbound)

  if (isNaN(liInbound) || isNaN(liOutbound) || liInbound <= 0 || liOutbound <= 0) {
    alert("Inbound and outbound values must be filled and must be valid numbers")
    return false
  }

  const res = mode.value === "monthly"
    ? calcMonthly(liInbound, liOutbound)
    : calcDaily(liInbound, liOutbound)

  result.value = res
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
  form.value = {
    liInbound: "",
    liOutbound: ""
  }

  result.value = {
    totalMain: 0,
    totalBackup: 0,
    totalAll: 0,
    perDay: 0
  }

  await nextTick()
  liSection.value?.scrollIntoView({ behavior: "smooth" })
}

const switchMode = (m) => {
  mode.value = m
  showResult.value = false

  form.value = {
    liInbound: "",
    liOutbound: ""
  }

  result.value = {
    totalMain: 0,
    totalBackup: 0,
    totalAll: 0,
    perDay: 0
  }
}
</script>

<template>
  <div class="container">
    <h1>LI-Based Manpower Planning</h1>
    <p>Estimate workforce requirements based on LI volume</p>

    <div class="card" ref="liSection">

      <div class="toggle-group">
        <button
          :class="['toggle-btn', { active: mode === 'daily' }]"
          @click="switchMode('daily')"
        >
          Per Day
        </button>
        <button
          :class="['toggle-btn', { active: mode === 'monthly' }]"
          @click="switchMode('monthly')"
        >
          Monthly
        </button>
      </div>

      <h3>Activity Information</h3>

      <div class="field">
        <label>{{ mode === 'monthly' ? 'Inbound (LI/Month)' : 'Inbound (LI/Day)' }}</label>
        <input
          type="number"
          v-model="form.liInbound"
          :placeholder="mode === 'monthly' ? 'e.g. 14063' : 'e.g. 500'"
          @keyup.enter="$refs.outboundInput.focus()"
        />
      </div>

      <div class="field">
        <label>{{ mode === 'monthly' ? 'Outbound (LI/Month)' : 'Outbound (LI/Day)' }}</label>
        <input
          type="number"
          v-model="form.liOutbound"
          :placeholder="mode === 'monthly' ? 'e.g. 23580' : 'e.g. 600'"
          ref="outboundInput"
          @keyup.enter="calculate"
        />
      </div>

      <button class="btn" @click="calculate">Calculate Manpower</button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Estimation Result</h3>

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

.toggle-group {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.toggle-btn {
  flex: 1;
  padding: 8px;

  border: 1px solid #dcdcdc;
  border-radius: 6px;
  background: #f5f5f5;

  color: #555;
  font-weight: 500;
  cursor: pointer;

  transition: 0.2s;
}

.toggle-btn.active {
  background: #026766;
  color: #fff;
  border-color: #026766;
}

.toggle-btn:hover:not(.active) {
  background: #e8f4f4;
  border-color: #026766;
  color: #026766;
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