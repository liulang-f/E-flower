<template>
  <Header/>
  <div class="hot-view">
    <div class="page-header">
      <h1 class="main-title">
        <span class="fire-icon">🔥</span> 热销花卉 <span class="fire-icon">🔥</span>
      </h1>
      <p class="subtitle">发现我们最受欢迎的鲜花，为你的特别时刻增添色彩</p>
    </div>

    <div class="content-container">
      <TopThreeHotView v-if="topThree.length === 3" :topFlowers="topThree" />

      <FlowerGridHotVIew
          :flowers="remainingFlowers"
          :rankOffset="4"
          :sortOption="sortBy"
          @changeSort="changeSort"
      />
    </div>
  </div>
  <Footer/>
</template>

<script setup>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import TopThreeHotView from "@/components/TopThreeHotView.vue";
import FlowerGridHotVIew from "@/components/FlowerGridHotVIew.vue";

const loading = ref(true);
const flowers = ref([]);
const sortBy = ref('sales');
const sortOrder = ref('desc');

// 获取热销花卉数据
const fetchHotFlowers = async () => {
  loading.value = true;
  try {
    const response = await axios.get('api/flower/flowers', {
      params: {
        sort_by: sortBy.value,
        order: sortOrder.value,
        per_page: 20  // 获取前30朵热销花卉
      }
    });

    flowers.value = response.data.flowers;
  } catch (error) {
    console.error('获取热销花卉失败:', error);
  } finally {
    loading.value = false;
  }
};

// 排序变更
const changeSort = (option) => {
  sortBy.value = option;
  fetchHotFlowers();
};

// 计算前三名花卉
const topThree = computed(() => {
  return flowers.value.slice(0, 3);
});

// 计算剩余的花卉
const remainingFlowers = computed(() => {
  return flowers.value.slice(3);
});

onMounted(() => {
  fetchHotFlowers();
});
</script>

<style scoped>
.hot-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.main-title {
  font-size: 42px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  position: relative;
  display: inline-block;
}

.fire-icon {
  display: inline-block;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.subtitle {
  font-size: 18px;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.content-container {
  margin-top: 30px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .main-title {
    font-size: 32px;
  }

  .subtitle {
    font-size: 16px;
  }
}
</style>