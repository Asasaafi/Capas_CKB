<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const goToLI       = () => router.push("/manpower/li")
const goToActivity = () => router.push("/manpower/activity")
</script>

<template>
  <div class="guide-container">

    <div class="guide-header">
      <div class="badge">
        <!-- Users icon -->
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        Workforce Estimation
      </div>
      <h1>Manpower Planning</h1>
      <p>
        Estimate workforce requirements based on warehouse workload and operational
        activities. Choose a calculation method below to begin the analysis.
      </p>
    </div>

    <div class="cards">

      <div class="card" @click="goToLI">
        <div class="card-top">
          <div class="card-icon-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"/>
              <line x1="12" y1="20" x2="12" y2="4"/>
              <line x1="6"  y1="20" x2="6"  y2="14"/>
            </svg>
          </div>
          <span class="card-num">01</span>
        </div>

        <h3>LI-Based Calculation</h3>
        <p>
          Estimate manpower requirements based on the total
          <strong>Line Items (LI)</strong> handled in warehouse <strong class="">Part Management</strong> operations.
          Suitable for quick workload estimation when total handling volume is known.
        </p>

        <ul class="card-features">
          <li>Fast manpower estimation</li>
          <li>Based on total handling load</li>
          <li>Suitable for planning scenarios</li>
        </ul>

        <span class="card-action">
          Start Calculation
          <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </span>
      </div>

      <div class="card" @click="goToActivity">
        <div class="card-top">
          <div class="card-icon-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="#026766" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
            </svg>
          </div>
          <span class="card-num">02</span>
        </div>

        <h3>Activity-Based Calculation</h3>
        <p>
          Calculate manpower based on specific warehouse activities such as
          <strong>Goods Receipt (GR)</strong>, <strong>Goods Issue (GI)</strong>,
          and <strong>Stock Transfer (ST)</strong>.
        </p>

        <ul class="card-features">
          <li>More detailed manpower analysis</li>
          <li>Based on operational activity workload</li>
          <li>Suitable for operational planning</li>
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