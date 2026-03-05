<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const images = [
  new URL('../assets/warehouse1.jpeg', import.meta.url).href,
  new URL('../assets/warehouse2.jpeg', import.meta.url).href,
  new URL('../assets/warehouse3.jpeg', import.meta.url).href
]

const currentIndex = ref(0)

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % images.length
}

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length
}

let intervalId
onMounted(() => {
  intervalId = setInterval(nextSlide, 4000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <div class="dashboard">

    <div class="hero-image-container">
      <img
        :src="images[currentIndex]"
        class="hero-image"
      />

      <button class="nav left" @click="prevSlide">‹</button>
      <button class="nav right" @click="nextSlide">›</button>
    </div>

    <div class="hero-text">
      <div class="text-left">
        <h1>
          WELCOME TO
            <span class="capas">CAPAS</span>
        </h1>
      </div>
      <div class="text-right">
        <p>
          All-in-one solution for fast calculations <br />
          & <br />
          predicted warehouse planning
        </p>
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

.hero-image-container {
  position: relative;
  flex: 3;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-text {
  flex: 1;
  background: 
    linear-gradient(
      to right,
      rgba(2,103,102,0.95),
      rgba(2,103,102,0.85)
    ),
    url('../assets/effect.png');
    
  background-size: cover;
  background-position: center;
  background-blend-mode: overlay;

  border-top: 6px solid #D1C48A;

  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 60px;
}

.hero-text p {
  font-size: 15px;
  line-height: 1.6;
}

.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  font-size: 45px;
  color: white;
  cursor: pointer;
  transition: 0.2s;
}

.nav:hover {
  color: #026766;
}

.left {
  left: 20px;
}

.text-left h1 {
  font-size: 40px;
  font-weight: 700;
  margin: 0;
  letter-spacing: 1px;
}

.right {
  right: 20px;
}

.text-right {
  text-align: right;
  max-width: 420px;
}

.text-right p {
  margin: 0;
  font-size: 18px;
  line-height: 1.7;
  font-weight: 300;
  letter-spacing: 0.5px;
}

.capas {
  position: relative;
  font-weight: 700;
}

.capas::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 100%;
  height: 4px;
  background-color: #FFCB3D;
}

</style>