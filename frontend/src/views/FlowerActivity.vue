<template>
  <Header/>
  <div class="activity-page">
    <div class="activity-header">
      <h1>'花语'精选活动</h1>
      <div class="filter-options">
        <button
            class="filter-btn"
            :class="{ 'active': activeTag === 'all' }"
            @click="setActiveTag('all')"
        >
          全部活动
        </button>
        <button
            v-for="tag in availableTags"
            :key="tag"
            :class="['filter-btn', activeTag === tag ? 'active' : '']"
            @click="setActiveTag(tag)"
        >
          {{ tag }}
        </button>
      </div>
    </div>

    <div class="activity-container">
      <div
          v-for="promotion in promotions"
          :key="promotion.id"
          class="activity-block"
      >
        <div class="activity-info">
          <div class="activity-title-section">
            <h2>{{ promotion.title }}</h2>
            <span class="activity-date">{{ formatDate(promotion.start_time) }} - {{ formatDate(promotion.end_time) }}</span>
          </div>
          <div class="activity-description">
            <p>{{ promotion.description }}</p>
            <div class="activity-tags">
              <span
                  v-for="(tag, index) in promotion.tags"
                  :key="index"
                  class="activity-tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>

        <div class="flower-grid" v-if="promotionFlowers[promotion.id]">
          <flower-card
              v-for="flower in promotionFlowers[promotion.id]"
              :key="flower.id"
              :flower="flower"
          ></flower-card>
        </div>
        <div v-else class="loading-flowers">
          <div class="spinner"></div>
        </div>

        <div class="activity-footer">
          <button class="view-more-btn" @click="viewAllPromotionFlowers(promotion.id)">
            查看更多
          </button>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
    </div>

    <div v-if="!isLoading && promotions.length === 0" class="no-activities">
      <p>暂无活动，敬请期待~</p>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button
          class="page-btn prev"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button
          class="page-btn next"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
  <Footer/>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import { fetchFlowers } from "@/api/flower.js"
import FlowerCard from "@/components/FlowerCard.vue";

const router = useRouter();

// 数据状态
const isLoading = ref(false);
const promotions = ref([]);
const promotionFlowers = reactive({});  // 存储每个活动的花朵，格式为 {promotionId: [flowers]}
const currentPage = ref(1);
const totalPages = ref(1);
const activeTag = ref('all');
const availableTags = ref([]);  // 所有可用的标签

// 方法
const fetchPromotions = async () => {
  isLoading.value = true;
  try {
    // 根据标签筛选活动
    let url = `/api/promotion/promotions?page=${currentPage.value}`;
    if (activeTag.value !== 'all') {
      url += `&tag=${activeTag.value}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    promotions.value = data.promotions;
    totalPages.value = data.pages;
    currentPage.value = data.current_page;

    // 更新可用的标签列表
    if (data.tags && Array.isArray(data.tags)) {
      availableTags.value = data.tags;
    }

    // 获取每个活动的花朵
    for (const promotion of promotions.value) {
      fetchPromotionFlowers(promotion.id);
    }
  } catch (error) {
    console.error('获取活动数据失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 获取某个活动下的花朵
const fetchPromotionFlowers = async (promotionId) => {
  try {
    // 构造请求参数
    const params = {
      promotionId: promotionId,
      per_page: 8
    };

    // 调用 fetchFlowers 方法获取数据
    const data = await fetchFlowers(params);

    // 使用 Vue 的响应式更新方式
    promotionFlowers[promotionId] = data.flowers;
  } catch (error) {
    console.error(`获取活动 ${promotionId} 的花朵数据失败:`, error);
  }
};

const setActiveTag = (tag) => {
  activeTag.value = tag;
  currentPage.value = 1;
  fetchPromotions();
};

const changePage = (page) => {
  currentPage.value = page;
  fetchPromotions();
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;
};

const viewAllPromotionFlowers = (promotionId) => {
  router.push(`/promotion/${promotionId}`);
};

// 生命周期钩子
onMounted(() => {
  fetchPromotions();
});
</script>

<style scoped>
.activity-page {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.activity-header {
  margin-bottom: 2rem;
  text-align: center;
}

.activity-header h1 {
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.filter-options {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
}

.filter-btn {
  padding: 0.6rem 1.2rem;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 2rem;
  color: #666;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  border-color: #f8b5c1;
  color: #f8b5c1;
}

.filter-btn.active {
  background-color: #f8b5c1;
  color: #fff;
  border-color: #f8b5c1;
}

.activity-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.activity-block {
  border: 1px solid #eaeaea;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.activity-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.activity-info {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f0f0f0;
}

.activity-title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.activity-title-section h2 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.activity-date {
  font-size: 0.9rem;
  color: #888;
}

.activity-description {
  color: #666;
  line-height: 1.6;
}

.activity-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.activity-tag {
  font-size: 0.8rem;
  padding: 0.3rem 0.8rem;
  background-color: #f9f9f9;
  border-radius: 1rem;
  color: #666;
}

.flower-grid {
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  background-color: #fafafa;
}

.loading-flowers {
  padding: 3rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fafafa;
  min-height: 200px;
}

.activity-footer {
  padding: 1rem 2rem;
  display: flex;
  justify-content: center;
  border-top: 1px solid #f0f0f0;
}

.view-more-btn {
  padding: 0.6rem 2rem;
  background-color: transparent;
  border: 1px solid #f8b5c1;
  border-radius: 2rem;
  color: #f8b5c1;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-more-btn:hover {
  background-color: #f8b5c1;
  color: #fff;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(248, 181, 193, 0.3);
  border-radius: 50%;
  border-top-color: #f8b5c1;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.no-activities {
  text-align: center;
  padding: 3rem 0;
  color: #888;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2.5rem;
  gap: 1rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: #f8b5c1;
  color: #f8b5c1;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}

@media (max-width: 768px) {
  .activity-title-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .flower-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    padding: 1.5rem;
  }
}
</style>