<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const images = [
  new URL('../assets/warehouse1.jpeg', import.meta.url).href,
  new URL('../assets/warehouse2.jpeg', import.meta.url).href,
  new URL('../assets/warehouse3.jpeg', import.meta.url).href
]

const currentIndex = ref(0)
let intervalId

const goTo = (index) => {
  currentIndex.value = index
}

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % images.length
}

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length
}

const resetTimer = () => {
  clearInterval(intervalId)
  intervalId = setInterval(nextSlide, 4000)
}

const handleNext = () => { nextSlide(); resetTimer() }
const handlePrev = () => { prevSlide(); resetTimer() }
const handleDot  = (i) => { goTo(i);   resetTimer() }

onMounted(() => {
  intervalId = setInterval(nextSlide, 4000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <div class="dashboard">

    <div class="hero-wrap">

      <div
        v-for="(img, i) in images"
        :key="i"
        class="slide"
        :class="{ active: i === currentIndex }"
        :style="{ backgroundImage: `url(${img})` }"
      />

      <div class="overlay" />

      <button class="nav left" @click="handlePrev">&#8249;</button>
      <button class="nav right" @click="handleNext">&#8250;</button>

      <div class="dots">
        <span
          v-for="(_, i) in images"
          :key="i"
          class="dot"
          :class="{ active: i === currentIndex }"
          @click="handleDot(i)"
        />
      </div>

    </div>

    <div class="hero-bottom">
      <div class="text-left">
        <p class="eyebrow">Welcome to</p>
        <h1>CAPAS <span class="capas">SYSTEM</span></h1>
      </div>

      <div class="divider-line" />

      <div class="text-right">
        <p>All-in-one solution for fast calculations<br />&amp;<br />predicted warehouse planning</p>
        <span class="tag">Warehouse Intelligence Platform</span>
      </div>
    </div>

  </div>
</template>

<style scoped>
.dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.hero-wrap {
  position: relative;
  flex: 3;
  overflow: hidden;
  background: #0d1f1f;
}

.slide {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transform: scale(1.04);
  transition: opacity 0.9s ease, transform 0.9s ease;
}

.slide.active {
  opacity: 1;
  transform: scale(1);
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.08) 0%,
    rgba(0, 0, 0, 0.45) 100%
  );
  pointer-events: none;
}

.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: white;
  font-size: 22px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.nav:hover {
  background: rgba(2, 103, 102, 0.75);
  border-color: #026766;
}

.left  { left: 20px }
.right { right: 20px }

.dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  align-items: center;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot.active {
  background: white;
  width: 22px;
  border-radius: 4px;
}

.hero-bottom {
  flex: 1;
  min-height: 130px;
  background: #026766;
  border-top: 5px solid #D1C48A;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 60px;
  position: relative;
  overflow: hidden;
  gap: 40px;
}

.hero-bottom::before {
  content: "";
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 24px,
    rgba(255, 255, 255, 0.02) 24px,
    rgba(255, 255, 255, 0.02) 48px
  );
  pointer-events: none;
}

.text-left {
  position: relative;
  flex-shrink: 0;
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 3px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 6px;
  text-transform: uppercase;
  font-weight: 400;
}

.text-left h1 {
  font-size: 34px;
  font-weight: 800;
  letter-spacing: 2px;
  line-height: 1;
  color: white;
  margin: 0;
}

.capas {
  position: relative;
  display: inline-block;
}

.capas::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 100%;
  height: 3px;
  background: #FFCB3D;
  border-radius: 2px;
}

.divider-line {
  width: 1px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}

.text-right {
  text-align: right;
  position: relative;
  max-width: 380px;
}

.text-right p {
  font-size: 15px;
  font-weight: 300;
  line-height: 1.8;
  letter-spacing: 0.4px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.tag {
  display: inline-block;
  margin-top: 10px;
  font-size: 10px;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 3px 12px;
  border-radius: 20px;
}
</style>