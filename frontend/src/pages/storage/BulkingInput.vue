<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from "vue-router"

const router        = useRouter()
const showResult    = ref(false)
const resultSection = ref(null)
const bulkSection   = ref(null)

const initialFormState = {
  numberParts   : '',
  totalGoods    : '',
  weightPerItem : '',
  itemPerPallet : '',
  length        : '',
  width         : '',
  height        : '',
  maxStacking   : '',
  gangway       : ''
}

const form = ref({ ...initialFormState })

const calculationMethod = ref("item")

const result = ref({
  itemsPerPallet : '',
  totalPallets   : '',
  floorPositions : '',
  netArea        : '',
  gangwayArea    : '',
  totalArea      : ''
})

function warehouseCalculation(data) {
  const {
    totalGoods,
    weightPerItem,
    itemPerPallet,
    length,
    width,
    height,
    maxStacking,
    gangway
  } = data

  const palletLength    = 1.2
  const palletWidth     = 1.2
  const palletArea      = palletLength * palletWidth
  const maxPalletLoadKg = 800

  const totalGoodsKg = totalGoods * 1000
  const totalItems   = totalGoodsKg / weightPerItem

  let itemsPerPallet = 0

  if (calculationMethod.value === "item") {
    if (!itemPerPallet || itemPerPallet <= 0) {
      alert("Items per pallet must be greater than 0")
      return null
    }
    itemsPerPallet = itemPerPallet
  }

  if (calculationMethod.value === "dimension") {
    if (!length || !width) {
      alert("Length and width must be filled")
      return null
    }

    const lengthM = length / 100
    const widthM  = width / 100

    const maxItemsByWeight = maxPalletLoadKg / weightPerItem
    const maxItemsByArea   = palletArea / (lengthM * widthM)

    itemsPerPallet = Math.floor(Math.min(maxItemsByWeight, maxItemsByArea))

    if (itemsPerPallet <= 0) {
      alert("Item size is too large for the pallet")
      return null
    }
  }

  const totalPallets   = totalItems / itemsPerPallet
  const floorPositions = totalPallets / maxStacking

  const netArea     = floorPositions * palletArea
  const gangwayArea = netArea * (gangway / 100)
  const totalArea   = netArea + gangwayArea

  return {
    itemsPerPallet,
    totalPallets   : Number(totalPallets.toFixed(2)),
    floorPositions : Number(floorPositions.toFixed(2)),
    netArea        : Number(netArea.toFixed(2)),
    gangwayArea    : Number(gangwayArea.toFixed(2)),
    totalArea      : Number(totalArea.toFixed(2))
  }
}

const calculate = async () => {
  const computed = warehouseCalculation(form.value)
  if (!computed) return

  result.value     = computed
  showResult.value = true

  await nextTick()
  resultSection.value?.scrollIntoView({ behavior: 'smooth' })
}

const resetForm = async () => {
  showResult.value       = false
  form.value             = { ...initialFormState }
  calculationMethod.value = "item"

  result.value = {
    itemsPerPallet : '',
    totalPallets   : '',
    floorPositions : '',
    netArea        : '',
    gangwayArea    : '',
    totalArea      : ''
  }

  await nextTick()
  bulkSection.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="container">
    <h1>Bulk Calculation</h1>
    <p>Generate pallet and warehouse space estimation based on item specifications</p>

    <div class="card" ref="bulkSection">
      <h3>Bulk Information</h3>

      <label>Number Parts</label>
      <input v-model="form.numberParts" placeholder="e.g. 2530-01-244443" />

      <label>Total Goods (tons)</label>
      <input type="number" v-model.number="form.totalGoods" placeholder="e.g. 2100" />

      <label>Weight Per Item (kg)</label>
      <input type="number" v-model.number="form.weightPerItem" placeholder="e.g. 25" />

      <label>Calculation Method</label>
      <select v-model="calculationMethod">
        <option value="item">Items per Pallet</option>
        <option value="dimension">Item Dimensions</option>
      </select>

      <div v-if="calculationMethod === 'item'">
        <label>Items per Pallet</label>
        <input
          type="number"
          v-model.number="form.itemPerPallet"
          placeholder="e.g. 20"
        />
      </div>

      <div v-if="calculationMethod === 'dimension'" class="dimension-row">
        <div class="field">
          <label>Length (cm)</label>
          <input
            type="number"
            v-model.number="form.length"
            placeholder="e.g. 60"
          />
        </div>

        <div class="field">
          <label>Width (cm)</label>
          <input
            type="number"
            v-model.number="form.width"
            placeholder="e.g. 14"
          />
        </div>

        <div class="field">
          <label>Height (cm)</label>
          <input
            type="number"
            v-model.number="form.height"
            placeholder="e.g. 7"
          />
        </div>
      </div>

      <label>Max Pallet Stacking</label>
      <input
        type="number"
        v-model.number="form.maxStacking"
        placeholder="e.g. 2"
      />

      <label>Gangway Allowance (%)</label>
      <input
        type="number"
        v-model.number="form.gangway"
        placeholder="e.g. 30"
      />

      <button class="btn" @click="calculate">
        Calculate Prediction
      </button>
    </div>

    <div v-if="showResult" ref="resultSection" class="result-section">
      <h3>Calculation Result</h3>

      <div class="result-group">
        <label>Items per Pallet</label>
        <input :value="result.itemsPerPallet" readonly />

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

  <div class="help-button" @click="$router.push('/storage')">
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

.dimension-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 15px;
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
}

.btn:hover {
  background: #014f4f;
}

.result-section {
  max-width: 600px;
  margin: 40px auto;
  padding: 10px;
  animation: fadeIn .4s ease-in-out;
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
}

@media (max-width: 768px) {
  .dimension-row {
    grid-template-columns: 1fr;
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