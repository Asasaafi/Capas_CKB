<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const goToBulking = () => router.push("/storage/bulking")
const goToUpload  = () => router.push("/storage/upload")
</script>

<template>
  <div class="guide-container">

    <div class="guide-header">
      <div class="badge">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        </svg>
        Storage Estimation
      </div>
      <h1>Storage Planning</h1>
      <p>
        Estimate warehouse storage requirements based on item dimensions,
        weight, and storage configuration. Choose a calculation method below
        to begin the analysis.
      </p>
    </div>

    <div class="cards">

      <div class="card" @click="goToBulking">
        <div class="card-top">
          <div class="card-icon-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
              <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
          </div>
          <span class="card-num">01</span>
        </div>

        <h3>Bulk Calculation</h3>
        <p>
          Estimate pallet usage and warehouse storage area for a single item.
          Choose between <strong>Items per Pallet</strong> or
          <strong>Item Dimension</strong> based calculation methods.
        </p>

        <ul class="card-features">
          <li>Manual item input</li>
          <li>Items per pallet estimation</li>
          <li>Warehouse area calculation</li>
        </ul>

        <span class="card-action">
          Start Calculation
          <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </span>
      </div>

      <div class="card" @click="goToUpload">
        <div class="card-top">
          <div class="card-icon-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </div>
          <span class="card-num">02</span>
        </div>

        <h3>File Upload Calculation</h3>
        <p>
          Upload a dataset to automatically calculate storage requirements
          for multiple items using predefined templates.
        </p>

        <ul class="card-features">
          <li>Download Excel template</li>
          <li>Upload item dataset</li>
          <li>Automatic storage prediction</li>
        </ul>

        <span class="card-action">
          Start Calculation
          <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </span>
      </div>

    </div>
  </div>
</template>

<style scoped>
.guide-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 48px 24px;
}

.guide-header {
  text-align: center;
  margin-bottom: 44px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f0faf9;
  border: 1px solid #9fe1cb;
  color: #0f6e56;
  font-size: 11px;
  font-weight: 500;
  padding: 4px 14px;
  border-radius: 20px;
  margin-bottom: 14px;
  letter-spacing: 0.5px;
}

.guide-header h1 {
  font-size: 30px;
  font-weight: 700;
  color: #111;
  margin-bottom: 10px;
}

.guide-header p {
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.7;
  font-size: 15px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 14px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #026766;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.08);
  border-color: #026766;
}

.card:hover::before {
  transform: scaleX(1);
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}

.card-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #f0faf9;
  border: 1px solid #c8e6e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon-wrap svg {
  width: 22px;
  height: 22px;
}

.card-num {
  font-size: 11px;
  font-weight: 600;
  color: #ccc;
  letter-spacing: 1px;
}

.card h3 {
  font-size: 17px;
  font-weight: 700;
  color: #111;
  margin-bottom: 10px;
}

.card p {
  font-size: 13px;
  color: #666;
  line-height: 1.65;
  margin-bottom: 18px;
}

.card-features {
  list-style: none;
  padding: 0;
  margin-bottom: 22px;
  border-top: 1px solid #f0f0f0;
  padding-top: 14px;
}

.card-features li {
  font-size: 13px;
  color: #555;
  padding: 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-features li::before {
  content: "";
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #026766;
  flex-shrink: 0;
}

.card-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #026766;
}

.card-action svg {
  width: 14px;
  height: 14px;
  transition: transform 0.2s;
}

.card:hover .card-action svg {
  transform: translateX(4px);
}
</style>