<script setup>
import { ref, computed } from 'vue'
import { saveAs } from 'file-saver'
import { useRouter } from "vue-router"

const router = useRouter()

const fileInput = ref(null)
const selectedFileName = ref(null)
const selectedFile = ref(null)
const predictions = ref([])

const downloadTemplate = () => {
  const link = document.createElement('a')
  link.href = '/template_storage.xlsx'
  link.download = 'template_storage.xlsx'
  link.click()
}

const openBrowser = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    selectedFileName.value = file.name
  }
}

const calculatePrediction = async () => {
  if (!selectedFile.value) {
    alert("Please upload file first")
    return
  }
  const formData = new FormData()
  formData.append("file", selectedFile.value)
  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData
    })
    const data = await response.json()
    console.log("Backend Response:", data)
    predictions.value = data.predictions
    alert("Prediction success!")
  } catch (error) {
    console.error("Upload error:", error)
    alert("Prediction failed!")
  }
}

const goToStorage = () => {
  router.push("/storage")
}

const downloadResult = () => {
  if (predictions.value.length === 0) {
    alert("No prediction to download")
    return
  }
  const headers = Object.keys(predictions.value[0])
  const csvRows = [
    headers.join(','),
    ...predictions.value.map(row =>
      headers.map(h => `"${row[h]}"`).join(',')
    )
  ]
  const csvString = csvRows.join('\n')
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
  saveAs(blob, 'predictions.csv')
}

const storageSummary = computed(() => {
  const summary = {}
  predictions.value.forEach(item => {
    const type  = item["Storage Type"]
    const level = item["Level"]
    const key   = `${type}-${level}`
    if (!summary[key]) {
      summary[key] = { storageType: type, level, units: 0, cost: 0 }
    }
    summary[key].units += Number(item["Units Needed"] || 0)
    summary[key].cost  += Number(item["Total Cost"]   || 0)
  })
  return Object.values(summary)
})
</script>

<template>
  <div class="page-header">
    <h1>File Upload Calculation</h1>
    <p class="subtitle">Upload a CSV or Excel file to calculate storage requirements and cost estimation</p>
  </div>

  <div class="upload-container">

    <div class="steps">

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
          </div>
          <div class="step-meta">
            <span class="step-num">Step 01</span>
            <span class="step-title">Download Template</span>
          </div>
        </div>
        <p class="step-note">Download the Excel template and use it as your data input format.</p>
        <button class="primary-btn" @click="downloadTemplate">Download Template</button>
      </div>

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"/>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
            </svg>
          </div>
          <div class="step-meta">
            <span class="step-num">Step 02</span>
            <span class="step-title">Fill in Item Data</span>
          </div>
        </div>
        <p class="step-note">Open the template and fill in the required columns: part number, quantity, weight, Growth Indicator, and dimensions.</p>
      </div>

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </div>
          <div class="step-meta">
            <span class="step-num">Step 03</span>
            <span class="step-title">Upload File</span>
          </div>
        </div>
        <p class="step-note">Select your completed file and click Calculate to run the prediction.</p>
        <button class="primary-btn" @click="openBrowser">Browse File</button>
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          accept=".csv,.xlsx"
          @change="handleFileChange"
        />
      </div>

    </div>

    <div class="upload-box">
      <div class="file-info">
        <div class="file-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
        </div>
        <div>
          <div class="file-name">{{ selectedFileName ?? 'No file uploaded yet' }}</div>
          <div class="file-hint">Accepted formats: .csv, .xlsx</div>
        </div>
      </div>
      <button class="calc-btn" @click="calculatePrediction">Calculate Prediction</button>
    </div>

    <div v-if="predictions.length > 0" class="success-box">
      <div class="success-text">
        <svg viewBox="0 0 24 24" fill="none" stroke="#0f6e56" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        File processed successfully! {{ predictions.length }} items have been calculated.
      </div>
      <button class="dl-btn" @click="downloadResult">Download Result</button>
    </div>

    <div v-if="storageSummary.length > 0" class="section">
      <p class="section-title">Storage Requirement Summary</p>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr>
              <th>Storage Type</th>
              <th>Level</th>
              <th>Total Units Needed</th>
              <th>Total Cost</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in storageSummary" :key="index">
              <td>{{ row.storageType }}</td>
              <td>{{ row.level }}</td>
              <td>{{ row.units }}</td>
              <td>Rp {{ row.cost.toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <div v-if="predictions.length > 0" class="preview-section">
    <p class="section-title">
      Preview Result
      <span class="section-sub">(showing first 20 rows)</span>
    </p>
    <div class="preview-scroll">
      <table>
        <thead>
          <tr>
            <th>Part Number</th>
            <th>Quantity</th>
            <th>Weight (kg)</th>
            <th>Growth Indicator</th>
            <th>Dimension (cm)</th>
            <th>Storage Type</th>
            <th>Level</th>
            <th>Units Needed</th>
            <th>Total Cost</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in predictions.slice(0, 20)" :key="index">
            <td>{{ row["Part Number"] }}</td>
            <td>{{ row["Quantity"] }}</td>
            <td>{{ row["Weight (kg)"] }}</td>
            <td>{{ row["Growth Indicator"] }}</td>
            <td>{{ row["Dimension (cm)"] }}</td>
            <td>{{ row["Storage Type"] }}</td>
            <td>{{ row["Level"] }}</td>
            <td>{{ row["Units Needed"] }}</td>
            <td>{{ row["Total Cost"] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="help-button" @click="goToStorage">?</div>

</template>

<style scoped>
.upload-container {
  padding: 0 40px 32px;
  max-width: 960px;
  margin: 0 auto;
}

.page-header {
  padding: 32px 40px 20px;
}

h1 {
  font-size: 24px;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

p {
  margin-bottom: 20px;
  color: #555;
}

.subtitle {
  color: #777;
  font-size: 14px;
  margin-bottom: 28px;
}

.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.step-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 14px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
  overflow: hidden;
}

.step-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #026766;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.icon-box {
  width: 46px;
  height: 46px;
  background: #026766;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-box svg {
  width: 22px;
  height: 22px;
}

.step-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: left;
}

.step-num {
  font-size: 11px;
  font-weight: 600;
  color: #026766;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.step-title {
  font-size: 14px;
  font-weight: 700;
  color: #111;
}

.step-note {
  font-size: 13px;
  color: #888;
  line-height: 1.6;
  flex: 1;
}

.primary-btn {
  background: #026766;
  color: #fff;
  border: none;
  height: 40px;
  width: 100%;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: background 0.2s;
}

.primary-btn:hover {
  background: #014f4e;
}

.upload-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 14px 20px;
  gap: 16px;
  margin-bottom: 14px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-icon {
  width: 38px;
  height: 38px;
  background: #f0faf9;
  border: 1px solid #c8e6e5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.file-icon svg {
  width: 17px;
  height: 17px;
}

.file-name {
  font-size: 13px;
  font-weight: 600;
  color: #444;
}

.file-hint {
  font-size: 11px;
  color: #aaa;
  margin-top: 2px;
}

.calc-btn {
  background: #026766;
  color: #fff;
  border: none;
  height: 40px;
  padding: 0 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  transition: background 0.2s;
  flex-shrink: 0;
}

.calc-btn:hover {
  background: #014f4e;
}

.success-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f0faf9;
  border: 1px solid #9fe1cb;
  border-radius: 12px;
  padding: 12px 20px;
  margin-bottom: 20px;
}

.success-text {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #0f6e56;
}

.success-text svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.dl-btn {
  background: #026766;
  color: #fff;
  border: none;
  height: 36px;
  padding: 0 18px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  transition: background 0.2s;
  flex-shrink: 0;
}

.dl-btn:hover {
  background: #014f4e;
}

.section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 15px;
  font-weight: 700;
  color: #111;
  margin-bottom: 12px;
}

.section-sub {
  font-size: 12px;
  color: #aaa;
  font-weight: 400;
  margin-left: 6px;
}

.tbl-wrap,
.preview-scroll {
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  overflow: hidden;
}

.preview-scroll {
  max-height: 280px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

thead tr {
  background: #026766;
}

thead th {
  color: white;
  padding: 10px 14px;
  text-align: center;
  font-weight: 500;
  font-size: 12px;
  letter-spacing: 0.3px;
}

.preview-scroll thead th {
  position: sticky;
  top: 0;
}

tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid #f0f0f0;
  color: #444;
  text-align: center;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover td {
  background: #f8fffe;
}

.preview-section {
  padding: 0 40px 32px;
  max-width: 960px;
  margin: 0 auto;
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
  font-size: 22px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
  transition: background 0.2s, transform 0.2s;
}

.help-button:hover {
  background: #014f4e;
  transform: scale(1.05);
}
</style>