<script setup>
import { ref } from 'vue'
import { saveAs } from 'file-saver'
import { useRouter } from "vue-router"

const router = useRouter()
const step1 = new URL('../../assets/step1.png', import.meta.url).href
const step2 = new URL('../../assets/step2.png', import.meta.url).href
const step3 = new URL('../../assets/step3.png', import.meta.url).href

const fileInput = ref(null)
const selectedFileName = ref('No file uploaded yet')
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
</script>

<template>
  <div class="upload-container">
    <h1>Upload File Excel</h1>
    <p class="subtitle">
      Upload a CSV file to calculate storage requirements and cost estimation
    </p>

    <div class="steps">
      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <img :src="step1" alt="Step 1" />
          </div>
          <div>
            <h3>Step 1</h3>
            <p>Download Template</p>
          </div>
        </div>
        <button class="primary-btn" @click="downloadTemplate">Download Template</button>
      </div>

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <img :src="step2" alt="Step 2" />
          </div>
          <div>
            <h3>Step 2</h3>
            <p>Fill in Item Data</p>
          </div>
        </div>
        <p class="step2-note">Open the template and fill in the required columns</p>
      </div>

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <img :src="step3" alt="Step 3" />
          </div>
          <div>
            <h3>Step 3</h3>
            <p>Upload File</p>
          </div>
        </div>
        <button class="primary-btn" @click="openBrowser">Open Browser</button>
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
      <div>
        <p class="no-file">{{ selectedFileName }}</p>
        <small></small>
      </div>
      <button class="primary-btn browser-btn" @click="calculatePrediction">
        Calculate Prediction
      </button>
    </div>

    <div v-if="predictions.length > 0" class="download-box">
      <p class="download-text">File processed successfully! {{ predictions.length }} items have been calculated.</p>
      <button class="primary-btn" @click="downloadResult">
        Download Result
      </button>
    </div>
  </div>

  <div v-if="predictions.length > 0" class="preview-box">
  <h3>Preview Result</h3>

  <div class="preview-table">
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

<div class="help-button" @click="goToStorage">
  ?
</div>
</template>

<style scoped>
.upload-container {
  padding: 20px 40px;
}

h1 {
  margin-bottom: 8px;
}

.download-box {
  margin-top: 25px;
  text-align: center;
  background: #f7f7f7;
  border-radius: 10px;
  padding: 20px;
}

.download-text {
  font-weight: 600;
  color: #026766;
  margin-bottom: 12px;
}

.subtitle {
  color: #777;
  margin-bottom: 25px;
}

.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 25px;
  width: 100%;
}

.step-card {
  background: #fff;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.step-header {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
  align-items: center;
}

.step-card h3 {
  margin: 0;
  font-size: 14px;
  color: #026766;
}

.step-card p {
  margin: 2px 0;
  font-weight: 600;
}

.icon-box {
  width: 50px;
  height: 50px;
  background-color: #026766;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-box img {
  width: 32px;
  height: 32px;
  display: block;
}

.step2-note {
  text-align: center;
  font-size: 13px;
  color: #555;
  margin-top: auto;
  margin-bottom: 10px;
}

.primary-btn {
  background-color: #026766;
  color: #fff;
  border: none;
  height: 42px;
  width: 90%;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
  display: block;
  margin: 0 auto;
  font-weight: 500;
}

.primary-btn:hover {
  background-color: #014f4e;
}

.browser-btn {
  width: 308px;
  margin-left: 0;
  margin-right: 11px;
}

.upload-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f7f7f7;
  border-radius: 10px;
  padding: 18px;
  border: 1px solid #ddd;
}

.preview-box {
  margin-top: 25px;
}

.preview-box h3 {
  margin-bottom: 10px;
}

.preview-table {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.preview-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.preview-table th {
  background: #026766;
  color: white;
  position: sticky;
  top: 0;
}

.preview-table th,
.preview-table td {
  padding: 8px;
  border-bottom: 1px solid #eee;
  text-align: center;
}

.preview-table tr:hover {
  background: #f5f5f5;
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
}

.no-file {
  font-weight: 600;
}

.download-box {
  margin-top: 20px;
  text-align: center;
}
</style>