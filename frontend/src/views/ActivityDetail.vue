<template>
  <Header/>
  <div class="promotion-detail-page">
    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
    </div>

    <div v-else-if="!promotion" class="promotion-not-found">
      <h2>未找到该活动信息</h2>
      <button class="back-btn" @click="goBack">返回活动列表</button>
    </div>

    <div v-else class="promotion-content">
      <!-- 活动头部信息 -->
      <div class="promotion-header">
        <button class="back-btn" @click="goBack">
          <span class="back-icon">←</span> 返回活动列表
        </button>

        <h1>{{ promotion.title }}</h1>

        <div class="promotion-meta">
          <div class="promotion-period">
            <span class="label">活动时间：</span>
            <span class="value">{{ formatDate(promotion.start_time) }} - {{ formatDate(promotion.end_time) }}</span>
          </div>

          <div v-if="promotion.discount" class="promotion-discount">
            <span class="discount-tag">{{ promotion.discount }}折</span>
          </div>
        </div>

        <div class="promotion-description">
          <p>{{ promotion.description }}</p>
        </div>

        <div class="promotion-tags">
          <span
              v-for="(tag, index) in promotion.tags"
              :key="index"
              class="promotion-tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>

      <!-- 使用花卉展示组件 -->
      <flower-container
          :promotion-id="promotionId"
          :title="`${promotion.title}活动下的所有花卉产品`"
      />
    </div>
  </div>
  <Footer/>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import FlowerContainer from '@/components/FlowerContainer.vue';
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

const route = useRoute();
const router = useRouter();
const promotionId = ref(parseInt(route.params.promotionId));
const isLoading = ref(true);
const promotion = ref(null);

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
};

// 获取促销活动详情
const fetchPromotionDetail = async () => {
  isLoading.value = true;
  try {
    const response = await fetch(`/api/promotion/promotions/${promotionId.value}`);
    if (!response.ok) {
      throw new Error('获取活动数据失败');
    }
    const data = await response.json();
    promotion.value = data;
  } catch (error) {
    console.error('获取活动详情失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 返回上一页
const goBack = () => {
  router.push('/activity');
};

onMounted(() => {
  if (!promotionId.value) {
    router.push('/activity');
    return;
  }
  fetchPromotionDetail();
});
</script>

<style scoped>
.promotion-detail-page {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 5rem 0;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(248, 181, 193, 0.3);
  border-radius: 50%;
  border-top-color: #f8b5c1;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.promotion-not-found {
  text-align: center;
  padding: 5rem 0;
  color: #888;
}

.promotion-header {
  background-color: #fff;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.back-btn {
  background: transparent;
  border: none;
  color: #f8b5c1;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0;
  margin-bottom: 1.5rem;
}

.back-icon {
  margin-right: 0.5rem;
  font-weight: bold;
}

.promotion-header h1 {
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.promotion-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.promotion-period {
  color: #666;
}

.label {
  font-weight: 500;
}

.discount-tag {
  background-color: #f8b5c1;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-weight: 500;
}

.promotion-description {
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.promotion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.promotion-tag {
  font-size: 0.9rem;
  padding: 0.4rem 1rem;
  background-color: #f9f9f9;
  border-radius: 2rem;
  color: #666;
}

.promotion-not-found .back-btn {
  background-color: #f8b5c1;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  display: inline-block;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .promotion-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>