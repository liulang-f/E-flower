// FlowerCard.vue - 可复用的花卉卡片组件
<template>
  <div class="flower-card" :class="{ 'top-three': rank <= 3 }">
    <div v-if="rank <= 3" class="rank-badge" :class="`rank-${rank}`">
      <span>{{ rank }}</span>
    </div>
    <div v-else class="normal-rank">{{ rank }}</div>
    <div class="flower-image-container" @click="goToDetail(flower.id)">
      <img :src="`api/img/${flower.name}`" :alt="flower.name" class="flower-image" />
      <div v-if="flower.discount" class="discount-badge">
        {{ Math.round((1 - flower.discount) * 100) }}% OFF
      </div>
    </div>
    <div class="flower-info">
      <h3 class="flower-name">{{ flower.name }}</h3>
      <div class="price-container">
        <span v-if="flower.discount" class="original-price">¥{{ flower.price.toFixed(2) }}</span>
        <span class="current-price">¥{{ (flower.price * (flower.discount || 1)).toFixed(2) }}</span>
      </div>
      <div class="tags-container">
        <span v-for="(tag, index) in flower.tags" :key="index" class="tag">{{ tag }}</span>
      </div>
      <div class="sales-info">
        已售出 {{ flower.sales }} 份
      </div>
      <button class="order-button" @click="add_to_cart(flower.id)">立即下单</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { addToCart } from '@/api/cart.js';

const router = useRouter();

defineProps({
  flower: {
    type: Object,
    required: true
  },
  rank: {
    type: Number,
    required: true
  }
});

// 跳转到花朵详情页面
const goToDetail = (flowerId) => {
  router.push(`/flowers/${flowerId}`);
};

// 添加到购物车
const add_to_cart = (flowerId) => {
  try {
    addToCart(flowerId, 1);
  } catch (error) {
    console.error('添加到购物车失败:', error);
  }
};
</script>

<style scoped>
.flower-card {
  position: relative;
  width: 280px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  background-color: #fff;
  margin: 15px;
}

.flower-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.top-three {
  border: 2px solid transparent;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
}

.rank-1 {
  background: linear-gradient(135deg, gold, #ffd700);
  color: #000;
}

.rank-2 {
  background: linear-gradient(135deg, silver, #c0c0c0);
  color: #000;
}

.rank-3 {
  background: linear-gradient(135deg, #cd7f32, #b87333);
  color: #fff;
}

.rank-badge {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  z-index: 10;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid white;
}

.normal-rank {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  z-index: 1;
}

.flower-image-container {
  position: relative;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
}

.flower-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.flower-card:hover .flower-image {
  transform: scale(1.05);
}

.discount-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff4757;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 14px;
}

.flower-info {
  padding: 15px;
}

.flower-name {
  margin: 0 0 10px;
  font-size: 18px;
  font-weight: 600;
}

.price-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.original-price {
  text-decoration: line-through;
  color: #777;
  font-size: 14px;
  margin-right: 8px;
}

.current-price {
  color: #ff4757;
  font-size: 20px;
  font-weight: bold;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 10px;
  gap: 5px;
}

.tag {
  background-color: #f0f0f0;
  color: #555;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.sales-info {
  color: #777;
  font-size: 14px;
  margin-bottom: 12px;
}

/* 立即下单按钮 */
.order-button {
  width: 100%;
  padding: 10px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.order-button:hover {
  background-color: #ff2c40;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 71, 87, 0.3);
}

.order-button:active {
  transform: translateY(0);
}

/* 为前三名添加闪光效果 */
.top-three {
  position: relative;
  overflow: hidden;
}

.top-three::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    transform: rotate(30deg) translate(-100%, -100%);
  }
  100% {
    transform: rotate(30deg) translate(100%, 100%);
  }
}
</style>