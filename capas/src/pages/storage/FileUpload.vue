<template>
  <div class="container">
    <h1>Upload File Excel</h1>
    <p>Upload CSV for Calculation</p>

    <div class="steps">
      <div class="step">Step 1<br />Download Template</div>
      <div class="step">Step 2<br />Fill Item Data</div>
      <div class="step">Step 3<br />Upload File</div>
    </div>

    <div class="upload-box">
      No file uploaded yet
      <button class="btn">Open Browser</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  background: white;
  padding: 30px;
  border-radius: 10px;
}

.steps {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.step {
  flex: 1;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 10px;
  text-align: center;
}

.upload-box {
  padding: 20px;
  border: 1px dashed #aaa;
  border-radius: 10px;
  text-align: center;
}

.btn {
  margin-top: 10px;
  padding: 8px 15px;
  background: #0f1b2d;
  color: white;
  border: none;
  border-radius: 5px;
}
</style>