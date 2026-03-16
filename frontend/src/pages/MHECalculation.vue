<script setup>
import { ref, nextTick } from "vue"

const showResult = ref(false)
const resultSection = ref(null)
const formSection = ref(null)

const uomRows = ref([{ id: 1, uom: "ton", qty: "" }])
let nextId = 2

const result = ref({ summary: [], totals: {} })

const mheRules = {
  ton: [
    [1,      50,      [["Forklift 3T", 2], ["Forklift 5T", 2]]],
    [51,     200,     [["Forklift 3T", 3], ["Forklift 5T", 2], ["Forklift 16T", 1]]],
    [201,    500,     [["Forklift 5T", 2], ["Forklift 16T", 1], ["Crane", 1]]],
    [501,    2000,    [["Forklift 16T", 2]]],
    [2001,   9999999, [["Crane", 1], ["Telehandler", 1], ["Stacker", 1]]]
  ],
  liter: [
    [1,      100000,  [["Handpallet", 4], ["Forklift 3T", 3], ["Drum Grabber", 1]]],
    [100001, 300000,  [["Forklift 3T", 3], ["Forklift 5T", 1], ["Drum Grabber", 2], ["Handpallet", 4]]],
    [300001, 600000,  [["Forklift 3T", 4], ["Handpallet", 5], ["Drum Grabber", 3], ["Forklift 5T", 2]]]
  ],
  line_item: [
    [1,     5000,  [["Handpallet", 2], ["Troli", 2]]],
    [5001,  10000, [["Handpallet", 3], ["Troli", 3], ["Forklift 3T", 1], ["Reach Truck", 1]]],
    [10001, 25000, [["Reach Truck", 2], ["Forklift 3T", 3], ["Handpallet", 4], ["Troli Tingkat", 5]]],
    [25001, 50000, [["Forklift 3T", 4], ["Reach Truck", 4], ["Handpallet", 5], ["Troli Tingkat", 10]]]
  ],
  cbm: [
    [1,   50,  [["Handpallet", 1], ["Troli", 1]]],
    [51,  200, [["Forklift 3T / Reach Truck", 1], ["Handpallet", 1]]],
    [201, 500, [["Forklift 3T / 5T", 1], ["Pallet Mover", 1], ["Handpallet", 2], ["Troli", 4]]]
  ]
}

const uomLabels = { ton: "Ton", liter: "Liter", line_item: "Line Item", cbm: "CBM" }
const uomBadgeClass = { ton: "badge-ton", liter: "badge-liter", line_item: "badge-line-item", cbm: "badge-cbm" }

function getIcon(name) {
  const n = name.toLowerCase()

  if (n.includes("forklift") || n.includes("fl")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="8" y="30" width="30" height="18" rx="3" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="38" y="20" width="5" height="28" rx="1.5" fill="#026766"/>
      <rect x="38" y="20" width="16" height="3" rx="1.5" fill="#026766"/>
      <rect x="43" y="23" width="3" height="16" rx="1" fill="#80c4c4"/>
      <rect x="8" y="34" width="6" height="10" rx="1" fill="#026766" opacity=".3"/>
      <circle cx="16" cy="50" r="5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="16" cy="50" r="2" fill="white"/>
      <circle cx="32" cy="50" r="5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="32" cy="50" r="2" fill="white"/>
      <rect x="4" y="36" width="6" height="4" rx="1" fill="#026766" opacity=".5"/>
    </svg>`

  if (n.includes("reach truck") || n.includes("rt ")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="28" width="24" height="20" rx="3" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="34" y="12" width="4" height="36" rx="1.5" fill="#026766"/>
      <rect x="38" y="12" width="14" height="2.5" rx="1" fill="#026766"/>
      <rect x="38" y="14" width="3" height="20" rx="1" fill="#80c4c4"/>
      <rect x="6" y="38" width="6" height="3" rx="1" fill="#026766" opacity=".4"/>
      <circle cx="17" cy="50" r="5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="17" cy="50" r="2" fill="white"/>
      <circle cx="30" cy="50" r="5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="30" cy="50" r="2" fill="white"/>
    </svg>`

  if (n.includes("handpallet") || n.includes("hand pallet")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="22" width="36" height="10" rx="2" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="14" y="32" width="4" height="16" rx="1.5" fill="#026766"/>
      <rect x="38" y="32" width="4" height="16" rx="1.5" fill="#026766"/>
      <rect x="18" y="32" width="20" height="3" rx="1" fill="#80c4c4"/>
      <rect x="24" y="16" width="4" height="8" rx="1.5" fill="#026766"/>
      <rect x="20" y="12" width="12" height="6" rx="2" fill="#026766" opacity=".7"/>
      <circle cx="16" cy="50" r="4" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="40" cy="50" r="4" fill="#026766" stroke="white" stroke-width="1.5"/>
    </svg>`

  if (n.includes("crane")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="44" width="20" height="8" rx="2" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="18" y="14" width="4" height="30" rx="1.5" fill="#026766"/>
      <line x1="20" y1="14" x2="50" y2="18" stroke="#026766" stroke-width="2" stroke-linecap="round"/>
      <line x1="50" y1="18" x2="50" y2="36" stroke="#026766" stroke-width="2" stroke-linecap="round"/>
      <rect x="44" y="36" width="12" height="8" rx="2" fill="#80c4c4" stroke="#026766" stroke-width="1.5"/>
      <line x1="22" y1="16" x2="20" y2="44" stroke="#026766" stroke-width="1.5" stroke-dasharray="3 2"/>
      <circle cx="14" cy="54" r="3.5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="26" cy="54" r="3.5" fill="#026766" stroke="white" stroke-width="1.5"/>
    </svg>`

  if (n.includes("troli") || n.includes("trolley")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="14" y="20" width="28" height="8" rx="2" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="14" y="30" width="28" height="8" rx="2" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="12" y="18" width="4" height="24" rx="1.5" fill="#026766"/>
      <rect x="8" y="14" width="4" height="6" rx="1.5" fill="#026766" opacity=".5"/>
      <circle cx="18" cy="50" r="4.5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="38" cy="50" r="4.5" fill="#026766" stroke="white" stroke-width="1.5"/>
    </svg>`

  if (n.includes("stacker")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="12" y="30" width="22" height="18" rx="3" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="34" y="16" width="4" height="32" rx="1.5" fill="#026766"/>
      <rect x="34" y="16" width="14" height="3" rx="1.5" fill="#026766"/>
      <rect x="38" y="19" width="3" height="14" rx="1" fill="#80c4c4"/>
      <circle cx="18" cy="50" r="4.5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="30" cy="50" r="4.5" fill="#026766" stroke="white" stroke-width="1.5"/>
    </svg>`

  if (n.includes("pallet mover")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="8" y="26" width="40" height="10" rx="2" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <rect x="12" y="36" width="4" height="12" rx="1.5" fill="#026766"/>
      <rect x="36" y="36" width="4" height="12" rx="1.5" fill="#026766"/>
      <rect x="16" y="36" width="20" height="3" rx="1" fill="#80c4c4"/>
      <rect x="44" y="28" width="6" height="20" rx="1.5" fill="#026766" opacity=".5"/>
      <circle cx="14" cy="50" r="4" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="38" cy="50" r="4" fill="#026766" stroke="white" stroke-width="1.5"/>
    </svg>`

  if (n.includes("drum")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="32" cy="36" rx="14" ry="18" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <ellipse cx="32" cy="18" rx="14" ry="5" fill="#026766" opacity=".3"/>
      <ellipse cx="32" cy="54" rx="14" ry="5" fill="#026766" opacity=".3"/>
      <rect x="18" y="18" width="3" height="36" fill="#80c4c4" opacity=".6"/>
      <rect x="28" y="10" width="8" height="4" rx="1.5" fill="#026766"/>
    </svg>`

  if (n.includes("telehandler")) return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="32" width="32" height="16" rx="3" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <line x1="24" y1="32" x2="54" y2="16" stroke="#026766" stroke-width="3" stroke-linecap="round"/>
      <rect x="50" y="10" width="10" height="8" rx="1.5" fill="#80c4c4" stroke="#026766" stroke-width="1.5"/>
      <circle cx="14" cy="50" r="5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="14" cy="50" r="2" fill="white"/>
      <circle cx="30" cy="50" r="5" fill="#026766" stroke="white" stroke-width="1.5"/>
      <circle cx="30" cy="50" r="2" fill="white"/>
    </svg>`

  return `
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="12" y="18" width="40" height="32" rx="3" fill="#c8e6e6" stroke="#026766" stroke-width="1.5"/>
      <line x1="12" y1="30" x2="52" y2="30" stroke="#026766" stroke-width="1.5"/>
      <line x1="32" y1="18" x2="32" y2="50" stroke="#026766" stroke-width="1.5"/>
    </svg>`
}

function addRow() {
  uomRows.value.push({ id: nextId++, uom: "ton", qty: "" })
}

function removeRow(id) {
  uomRows.value = uomRows.value.filter(r => r.id !== id)
}

function getMHE(uom, qty) {
  const rules = mheRules[uom]
  if (!rules) return []
  let selected = null
  for (const [minQ, , alat] of rules) {
    if (qty >= minQ) selected = alat
  }
  return selected || []
}

const calculate = async () => {
  for (const row of uomRows.value) {
    if (!row.uom) { alert("Please select a UOM type for all rows."); return }
    if (!row.qty || Number(row.qty) <= 0) { alert("Please enter a valid quantity for all rows."); return }
  }

  const summary = []
  const totals = {}

  for (const row of uomRows.value) {
    const qty = Number(row.qty)
    const alatList = getMHE(row.uom, qty)
    alatList.forEach(([alat, jumlah]) => {
      totals[alat] = (totals[alat] || 0) + jumlah
    })
    summary.push({ uom: row.uom, qty, alatList })
  }

  result.value = { summary, totals }
  showResult.value = true
  await nextTick()
  resultSection.value?.scrollIntoView({ behavior: "smooth" })
}

const resetForm = async () => {
  showResult.value = false
  uomRows.value = [{ id: 1, uom: "ton", qty: "" }]
  nextId = 2
  result.value = { summary: [], totals: {} }
  await nextTick()
  formSection.value?.scrollIntoView({ behavior: "smooth" })
}

const totalUnits = () => Object.values(result.value.totals).reduce((s, v) => s + v, 0)
const totalTypes = () => Object.keys(result.value.totals).length
</script>

<template>
  <div class="container">

    <div class="page-header">
      <h1>MHE Planning Calculator</h1>
      <p>Get equipment recommendations based on your warehouse handling UOM</p>
    </div>

    <div class="card" ref="formSection">
      <h3>Handling Input</h3>

      <div
        v-for="row in uomRows"
        :key="row.id"
        class="uom-row"
      >
        <div class="field">
          <label>UOM Type</label>
          <select v-model="row.uom">
            <option value="ton">Ton</option>
            <option value="liter">Liter</option>
            <option value="line_item">Line Item</option>
            <option value="cbm">CBM</option>
          </select>
        </div>

        <div class="field">
          <label>Quantity</label>
          <input
            type="number"
            v-model="row.qty"
            placeholder="e.g. 150"
            min="1"
          />
        </div>

        <button
          class="btn-remove"
          @click="removeRow(row.id)"
          :disabled="uomRows.length === 1"
          title="Remove"
        >
          ×
        </button>
      </div>

      <button class="btn-add" @click="addRow">
        <span class="plus-icon">+</span> Add UOM
      </button>

      <button class="btn" @click="calculate">
        Calculate MHE Requirements
      </button>
    </div>

    <div v-if="showResult" ref="resultSection" class="card result-section">
      <h3>MHE Recommendation Result</h3>

      <div class="info-bar">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
          <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        {{ result.summary.length }} UOM processed —
        {{ totalTypes() }} equipment types, {{ totalUnits() }} units total
      </div>

      <table class="detail-table">
        <thead>
          <tr>
            <th>UOM</th>
            <th>Qty</th>
            <th>Recommended Equipment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in result.summary" :key="i">
            <td>
              <span :class="['badge', uomBadgeClass[item.uom]]">
                {{ uomLabels[item.uom] }}
              </span>
            </td>
            <td>{{ item.qty.toLocaleString("id-ID") }}</td>
            <td>
              <span v-for="([alat, jumlah], j) in item.alatList" :key="j">
                {{ alat }} <strong>({{ jumlah }})</strong>
                <span v-if="j < item.alatList.length - 1">, </span>
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="divider" />
      <p class="section-label">Total Equipment Needed</p>

      <div class="equip-grid">
        <div
          v-for="([nama, qty]) in Object.entries(result.totals)"
          :key="nama"
          class="equip-card"
        >
          <div class="equip-icon" v-html="getIcon(nama)" />
          <div class="equip-info">
            <div class="equip-qty">{{ qty }}</div>
            <div class="equip-unit">unit</div>
            <div class="equip-name">{{ nama }}</div>
          </div>
        </div>
      </div>

      <button class="btn-outline" @click="resetForm">
        Calculate Again
      </button>
    </div>

  </div>
</template>

<style scoped>
.container {
  padding: 32px 40px;
}

.page-header {
  margin-bottom: 28px;
}

.page-header h1 {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
}

.page-header p {
  margin-bottom: 20px;
  color: #555;
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
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 28px;
  margin-bottom: 24px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.card h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 18px;
}

.uom-row {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 8px;
  align-items: end;
  margin-bottom: 8px;
}

.field {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 14px;
  margin: 0 0 5px;
}

input,
select {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
}

input:focus,
select:focus {
  outline: none;
  border-color: #026766;
  box-shadow: 0 0 0 2px rgba(2, 103, 102, 0.1);
}

.btn-remove {
  height: 38px;
  width: 38px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  background: transparent;
  color: #aaa;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.btn-remove:hover:not(:disabled) {
  background: #fff0f0;
  border-color: #f09595;
  color: #a32d2d;
}

.btn-remove:disabled {
  opacity: 0.25;
  cursor: not-allowed;
}

.btn-add {
  width: 100%;
  padding: 9px;
  border: 1px dashed #b0d4d4;
  border-radius: 8px;
  background: transparent;
  color: #026766;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-add:hover {
  background: #f0faf9;
  border-color: #026766;
}

.plus-icon {
  font-size: 18px;
  line-height: 1;
}

.btn {
  width: 100%;
  padding: 11px;
  background: #026766;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 14px;
}

.btn:hover {
  background: #014f4f;
}

.btn-outline {
  width: 100%;
  padding: 11px;
  background: transparent;
  color: #026766;
  border: 1px solid #026766;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 10px;
}

.btn-outline:hover {
  background: #f0faf9;
}

.info-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f0faf9;
  border: 1px solid #9fe1cb;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 12px;
  color: #0f6e56;
  margin-bottom: 16px;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin-bottom: 4px;
}

.detail-table th {
  text-align: left;
  padding: 7px 4px;
  color: #888;
  font-weight: 400;
  font-size: 12px;
  border-bottom: 1px solid #e8e8e8;
}

.detail-table td {
  padding: 8px 4px;
  color: #444;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
}

.badge {
  display: inline-block;
  font-size: 11px;
  padding: 2px 9px;
  border-radius: 20px;
  font-weight: 500;
}

.badge-ton        { background: #E6F1FB; color: #0C447C; }
.badge-liter      { background: #EAF3DE; color: #3B6D11; }
.badge-line-item  { background: #FAEEDA; color: #854F0B; }
.badge-cbm        { background: #EEEDFE; color: #3C3489; }

.divider {
  height: 1px;
  background: #ebebeb;
  margin: 18px 0;
}

.section-label {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 14px;
}

.equip-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 12px;
  margin-bottom: 6px;
}

.equip-card {
  background: #f4fbfa;
  border: 1px solid #c4e0df;
  border-radius: 10px;
  padding: 16px 14px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.equip-icon {
  flex-shrink: 0;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.equip-icon :deep(svg) {
  width: 54px;
  height: 54px;
}

.equip-info {
  flex: 1;
  min-width: 0;
}

.equip-qty {
  font-size: 28px;
  font-weight: 700;
  color: #026766;
  line-height: 1;
}

.equip-unit {
  font-size: 11px;
  color: #888;
  margin-top: 1px;
}

.equip-name {
  font-size: 12px;
  color: #333;
  margin-top: 5px;
  font-weight: 500;
  line-height: 1.4;
}

.result-section {
  animation: fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 500px) {
  .container { padding: 20px 16px; }
  .uom-row { grid-template-columns: 1fr 1fr auto; gap: 6px; }
  .equip-grid { grid-template-columns: 1fr 1fr; }
}
</style>