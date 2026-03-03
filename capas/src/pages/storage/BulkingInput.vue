<template>
  <div class="container">
    <h1>Bulk Calculation</h1>
    <p>Calculate prediction for a single item.</p>

    <div class="card">
      <h3>Bulk Information</h3>

      <input placeholder="Number Parts" />
      <input placeholder="Total Goods (tons)" />

      <div class="row">
        <input placeholder="Weight Per Item (kg)" />
        <input placeholder="Volume Per Item (m³)" />
      </div>

      <input placeholder="Max Pallet Stacking" />
      <input placeholder="Pallet Size (m²)" />
      <input placeholder="Gangway Allowance (%)" />

      <button class="btn">Calculate Prediction</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  background: white;
  padding: 30px;
  border-radius: 10px;
}

.card {
  max-width: 500px;
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

input {
  width: 100%;
  padding: 8px;
  margin: 8px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.row {
  display: flex;
  gap: 10px;
}

.btn {
  width: 100%;
  padding: 10px;
  background: #0f1b2d;
  color: white;
  border: none;
  border-radius: 5px;
  margin-top: 10px;
  cursor: pointer;
}
</style>