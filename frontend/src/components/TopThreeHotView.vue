<template>
  <div class="top-three-banner">
    <h2 class="banner-title">花店之星 <span class="highlight">TOP 3</span></h2>
    <div class="top-three-container">
      <div class="second-place podium">
        <FlowerCardHotView :flower="topFlowers[1]" :rank="2" />
      </div>
      <div class="first-place podium">
        <FlowerCardHotView :flower="topFlowers[0]" :rank="1" />
        <div class="crown">👑</div>
      </div>
      <div class="third-place podium">
        <FlowerCardHotView :flower="topFlowers[2]" :rank="3" />
      </div>
    </div>
  </div>
</template>

<script setup>
import FlowerCardHotView from "@/components/FlowerCardHotView.vue";

defineProps({
  topFlowers: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.top-three-banner {
  margin-bottom: 50px;
  padding: 30px 0;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  border-radius: 15px;
  position: relative;
  overflow: hidden;
}

.banner-title {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #333;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.highlight {
  color: #ff4757;
  position: relative;
  display: inline-block;
}

.highlight::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #ff4757;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
    transform: scaleX(0.9);
  }
  50% {
    opacity: 1;
    transform: scaleX(1.1);
  }
  100% {
    opacity: 0.6;
    transform: scaleX(0.9);
  }
}

.top-three-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 15px;
  padding: 0 20px;
}

.podium {
  position: relative;
  transition: transform 0.3s ease;
}

.podium:hover {
  transform: translateY(-10px);
}

.first-place {
  z-index: 3;
}

.second-place,
.third-place {
  transform: scale(0.9);
  z-index: 2;
}

.crown {
  position: absolute;
  top: -35px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 40px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-10px);
  }
  100% {
    transform: translateX(-50%) translateY(0);
  }
}
</style>