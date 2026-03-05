<template>
  <div class="container">
    <h1>Bulk Calculation</h1>
    <p>Generate pallet and warehouse space estimation based on item specifications</p>

    <div class="card" ref="bulkSection">
      <h3>Bulk Information</h3>

      <label>Number Parts</label>
      <input v-model="form.numberParts" placeholder="e.g. 2530-01-244443" />

      <label>Total Goods (tons)</label>
      <input v-model.number="form.totalGoods" placeholder="e.g. 500" />

      <div class="row">
        <div class="field">
          <label>Weight Per Item (kg)</label>
          <input v-model.number="form.weightPerItem" placeholder="e.g. 5" />
        </div>

        <div class="field">
          <label>Volume Per Item (m³)</label>
          <input v-model.number="form.volumePerItem" placeholder="e.g. 0.03" />
        </div>
      </div>

      <label>Max Pallet Stacking</label>
      <input v-model.number="form.maxStacking" placeholder="e.g. 3" />

      <label>Pallet Size (m²)</label>
      <input v-model.number="form.palletSize" placeholder="e.g. 1.44" />

      <label>Gangway Allowance (%)</label>
      <input v-model.number="form.gangway" placeholder="e.g. 30" />

      <button class="btn" @click="calculate">
        Calculate Prediction
      </button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Calculation Result</h3>

      <div class="result-group">
        <label>Total Pallets</label>
        <input :value="result.totalPallets" readonly />

        <label>Floor Pallet Positions</label>
        <input :value="result.floorPositions" readonly />

        <label>Net Pallet Area (m²)</label>
        <input :value="result.netArea" readonly />

        <label>Gangway Area</label>
        <input :value="result.gangwayArea" readonly />

        <label>Total Warehouse Area</label>
        <input :value="result.totalArea" readonly />
      </div>

      <button class="btn try-btn" @click="resetForm">
        Try Again
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const showResult = ref(false)
const resultSection = ref(null)
const bulkSection = ref(null)

const initialFormState = {
  numberParts: '',
  totalGoods: '',
  weightPerItem: '',
  volumePerItem: '',
  maxStacking: '',
  palletSize: '',
  gangway: ''
}

const form = ref({ ...initialFormState })

const result = ref({
  totalPallets: '',
  floorPositions: '',
  netArea: '',
  gangwayArea: '',
  totalArea: ''
})

function warehouseCalculation(data) {

  const {
    totalGoods,
    weightPerItem,
    volumePerItem,
    maxStacking,
    palletSize,
    gangway
  } = data

  const inputs = [
    totalGoods,
    weightPerItem,
    volumePerItem,
    maxStacking,
    palletSize
  ]

  if (inputs.some(x => !x || x <= 0)) {
    alert("Semua input harus lebih dari 0")
    return null
  }

  const totalGoodsKg = totalGoods * 1000
  const totalItems = totalGoodsKg / weightPerItem

  // asumsi sederhana:
  // (rule-based)
  const palletVolumeCapacity = 1.5
  const itemsPerPallet = Math.floor(palletVolumeCapacity / volumePerItem)

  if (itemsPerPallet <= 0) {
    alert("Volume barang terlalu besar untuk pallet")
    return null
  }

  const totalPallets = totalItems / itemsPerPallet
  const floorPositions = totalPallets / maxStacking
  const netArea = floorPositions * palletSize
  const gangwayArea = netArea * (gangway / 100)
  const totalArea = netArea + gangwayArea

  return {
    totalPallets: totalPallets.toFixed(2),
    floorPositions: floorPositions.toFixed(2),
    netArea: netArea.toFixed(2),
    gangwayArea: gangwayArea.toFixed(2),
    totalArea: totalArea.toFixed(2)
  }
}

const calculate = async () => {

  const computed = warehouseCalculation(form.value)

  if (!computed) return

  result.value = computed

  showResult.value = true
  await nextTick()

  resultSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const resetForm = async () => {
  showResult.value = false
  form.value = { ...initialFormState }

  result.value = {
    totalPallets: '',
    floorPositions: '',
    netArea: '',
    gangwayArea: '',
    totalArea: ''
  }

  await nextTick()
  bulkSection.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

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
  max-width: 600px;
  margin: 30px auto;
  padding: 24px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

label {
  display: block;
  font-size: 14px;
  color: #000;
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

.row {
  display: flex;
  gap: 15px;
}

.field {
  flex: 1;
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
  transition: 0.2s;
}

.btn:hover {
  background: #014f4f;
}

.result-section {
  max-width: 600px;
  margin: 40px auto;
  padding: 10px;
  animation: fadeIn 0.4s ease-in-out;
}

.result-group input {
  margin-bottom: 12px;
}

@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }
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