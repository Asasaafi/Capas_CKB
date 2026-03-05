<script setup>
const step1 = new URL('../../assets/step1.png', import.meta.url).href
const step2 = new URL('../../assets/step2.png', import.meta.url).href
const step3 = new URL('../../assets/step3.png', import.meta.url).href
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
            <img src="../../assets/step1.png" alt="Step 1" />
          </div>
          <div>
            <h3>Step 1</h3>
            <p>Download Template</p>
          </div>
        </div>
        <button class="primary-btn">Download Template</button>
      </div>

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <img src="../../assets/step2.png" alt="Step 2" />
          </div>
          <div>
            <h3>Step 2</h3>
            <p>Fill in Item Data</p>
          </div>
        </div>
        <!-- kalimat tambahan di center -->
        <p class="step2-note">Open the template and fill in the required columns</p>
      </div>

      <div class="step-card">
        <div class="step-header">
          <div class="icon-box">
            <img src="../../assets/step3.png" alt="Step 3" />
          </div>
          <div>
            <h3>Step 3</h3>
            <p>Upload File</p>
          </div>
        </div>
        <button class="primary-btn">Upload File</button>
      </div>
    </div>

    <div class="upload-box">
      <div>
        <p class="no-file">No file uploaded yet</p>
        <small>No item has been calculate</small>
      </div>
      <button class="primary-btn browser-btn">Open Browser</button>
    </div>
  </div>
</template>

<style scoped>
.upload-container {
  padding: 20px 40px;
}

h1 {
  margin-bottom: 8px;
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

/* styling khusus Step 2 */
.step2-note {
  text-align: center;
  font-size: 13px;   /* agak besar tapi tidak terlalu */
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

.no-file {
  font-weight: 600;
}
</style>