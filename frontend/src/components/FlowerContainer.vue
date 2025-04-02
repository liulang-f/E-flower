<template>
  <div class="flower-container">
    <h2 v-if="title" class="container-title">{{ title }}</h2>

    <div class="filters" v-if="showFilters">
      <div class="search-bar">
        <input
            type="text"
            v-model="searchKeyword"
            placeholder="搜索花卉..."
            @keyup.enter="applyFilters"
        />
        <button class="search-btn" @click="applyFilters">搜索</button>
      </div>

      <div class="filter-options">
        <div class="sort-group">
          <span class="label">排序：</span>
          <div class="sort-buttons">
            <button
                v-for="option in sortOptions"
                :key="option.field"
                :class="['sort-btn', isSortActive(option.field) ? 'active' : '']"
                @click="toggleSort(option.field)"
            >
              {{ option.label }}
              <span v-if="isSortActive(option.field)" class="sort-icon">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </button>
          </div>
        </div>

        <div class="price-filter">
          <span class="label">价格：</span>
          <div class="price-inputs">
            <input
                type="number"
                v-model="minPrice"
                placeholder="最低"
                min="0"
            />
            <span class="price-separator">-</span>
            <input
                type="number"
                v-model="maxPrice"
                placeholder="最高"
                min="0"
            />
            <button class="price-btn" @click="applyFilters">确定</button>
          </div>
        </div>
      </div>

      <div class="tag-filter" v-if="availableTags.length > 0">
        <span class="label">标签：</span>
        <div class="tag-buttons">
          <button
              class="tag-btn"
              :class="{ active: selectedTags.length === 0 }"
              @click="clearTags"
          >
            全部
          </button>
          <button
              v-for="tag in availableTags"
              :key="tag"
              class="tag-btn"
              :class="{ active: selectedTags.includes(tag) }"
              @click="toggleTag(tag)"
          >
            {{ tag }}
          </button>
        </div>
      </div>

    </div>

    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
    </div>

    <div v-else-if="flowers.length === 0" class="no-flowers">
      <p>暂无相关花卉产品</p>
    </div>

    <div v-else class="flower-grid">
      <flower-card
          v-for="flower in flowers"
          :key="flower.id"
          :flower="flower"
      ></flower-card>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button
          class="page-btn first"
          :disabled="currentPage === 1"
          @click="changePage(1)"
      >
        首页
      </button>
      <button
          class="page-btn prev"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
      >
        上一页
      </button>

      <div class="page-numbers">
        <button
            v-for="page in displayedPages"
            :key="page"
            :class="['page-number', currentPage === page ? 'active' : '']"
            @click="changePage(page)"
        >
          {{ page }}
        </button>
      </div>

      <button
          class="page-btn next"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
      <button
          class="page-btn last"
          :disabled="currentPage === totalPages"
          @click="changePage(totalPages)"
      >
        末页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import FlowerCard from "@/components/FlowerCard.vue";

const props = defineProps({
  promotionId: {
    type: Number,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  showFilters: {
    type: Boolean,
    default: true
  }
});

// 数据状态
const isLoading = ref(false);
const flowers = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const perPage = ref(8); // 每页显示8条数据

// 筛选和排序状态
const searchKeyword = ref('');
const selectedTags = ref([]);
const minPrice = ref('');
const maxPrice = ref('');
const sortField = ref('');
const sortOrder = ref('desc');
const availableTags = ref([]);

// 排序选项
const sortOptions = [
  { label: '价格', field: 'price' },
  { label: '销量', field: 'sales' },
  { label: '上架时间', field: 'created_at' }
];

// 检查排序字段是否激活
const isSortActive = (field) => {
  return sortField.value === field;
};

// 切换排序方式
const toggleSort = (field) => {
  if (sortField.value === field) {
    // 如果已经选中该字段，则切换排序方向
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    // 否则选中该字段，默认降序排列
    sortField.value = field;
    sortOrder.value = 'desc';
  }

  currentPage.value = 1;
  fetchFlowers();
};

// 切换标签选择
const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag);
  if (index > -1) {
    selectedTags.value.splice(index, 1);
  } else {
    selectedTags.value.push(tag);
  }

  currentPage.value = 1;
  fetchFlowers();
};

// 清除所有已选标签
const clearTags = () => {
  selectedTags.value = [];
  currentPage.value = 1;
  fetchFlowers();
};

// 应用筛选条件
const applyFilters = () => {
  currentPage.value = 1;
  fetchFlowers();
};

// 分页逻辑
const changePage = (page) => {
  currentPage.value = page;
  fetchFlowers();
};

// 计算要显示的页码范围
const displayedPages = computed(() => {
  const range = [];
  const totalDisplay = 5; // 显示5个页码按钮

  let start = Math.max(1, currentPage.value - Math.floor(totalDisplay / 2));
  let end = Math.min(totalPages.value, start + totalDisplay - 1);

  // 调整起始位置以保证显示正确数量的页码
  if (end - start + 1 < totalDisplay) {
    start = Math.max(1, end - totalDisplay + 1);
  }

  for (let i = start; i <= end; i++) {
    range.push(i);
  }

  return range;
});

// 获取花卉数据
const fetchFlowers = async () => {
  isLoading.value = true;
  try {
    // 构建查询参数
    const params = new URLSearchParams();
    params.append('page', currentPage.value);
    params.append('per_page', perPage.value);

    if (searchKeyword.value) {
      params.append('search', searchKeyword.value);
    }

    if (selectedTags.value.length > 0) {
      params.append('tags', selectedTags.value.join(','));
    }

    if (minPrice.value) {
      params.append('min_price', minPrice.value);
    }

    if (maxPrice.value) {
      params.append('max_price', maxPrice.value);
    }

    if (sortField.value) {
      params.append('sort_by', sortField.value);
      params.append('order', sortOrder.value);
    }

    if (props.promotionId) {
      params.append('promotionId', props.promotionId);
    }

    // 发送API请求获取花卉数据
    const url = `/api/flower/flowers?${params.toString()}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error('获取花卉数据失败');
    }

    const data = await response.json();
    flowers.value = data.flowers;
    totalPages.value = data.pages;
    currentPage.value = data.current_page;

    // 如果是第一次加载且没有可用标签，则从另一个API获取可用标签
    if (availableTags.value.length === 0) {
      availableTags.value = data.tags;
    }
  } catch (error) {
    console.error('获取花卉数据失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 监听促销ID变化
watch(() => props.promotionId, (newVal) => {
  if (newVal) {
    resetFilters();
    fetchFlowers();
  }
});

// 重置所有筛选条件
const resetFilters = () => {
  currentPage.value = 1;
  searchKeyword.value = '';
  selectedTags.value = [];
  minPrice.value = '';
  maxPrice.value = '';
  sortField.value = '';
  sortOrder.value = 'desc';
};

onMounted(() => {
  if (props.promotionId) {
    fetchFlowers();
  }
});
</script>

<style scoped>
.flower-container {
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.container-title {
  font-size: 1.5rem;
  color: #333;
  padding: 1.5rem 2rem;
  margin: 0;
  border-bottom: 1px solid #f0f0f0;
}

.filters {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-bar {
  display: flex;
  width: 100%;
  max-width: 500px;
}

.search-bar input {
  flex: 1;
  padding: 0.6rem 1rem;
  border: 1px solid #ddd;
  border-right: none;
  border-radius: 4px 0 0 4px;
  font-size: 0.9rem;
}

.search-btn {
  padding: 0.6rem 1.2rem;
  background-color: #f8b5c1;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #f69bab;
}

.filter-options {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.sort-group {
  display: flex;
  align-items: center;
}

.sort-buttons {
  display: flex;
  gap: 0.5rem;
}

.label {
  color: #666;
  margin-right: 0.5rem;
  font-weight: 500;
}

.sort-btn {
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.sort-btn:hover {
  border-color: #f8b5c1;
  color: #f8b5c1;
}

.sort-btn.active {
  background-color: #f8b5c1;
  color: white;
  border-color: #f8b5c1;
}

.sort-icon {
  margin-left: 0.3rem;
}

.price-filter {
  display: flex;
  align-items: center;
}

.price-inputs {
  display: flex;
  align-items: center;
}

.price-inputs input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.price-separator {
  margin: 0 0.5rem;
  color: #666;
}

.price-btn {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f8b5c1;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.price-btn:hover {
  background-color: #f69bab;
}

.tag-filter {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.tag-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-btn {
  background: transparent;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 0.3rem 0.8rem;
  font-size: 0.85rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tag-btn:hover {
  border-color: #f8b5c1;
  color: #f8b5c1;
}

.tag-btn.active {
  background-color: #f8b5c1;
  color: white;
  border-color: #f8b5c1;
}

.flower-grid {
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 每行4条数据 */
  gap: 1.5rem;
  background-color: #fafafa;
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 4rem 0;
  background-color: #fafafa;
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

.no-flowers {
  text-align: center;
  padding: 4rem 0;
  color: #888;
  background-color: #fafafa;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1.5rem;
  gap: 0.5rem;
  border-top: 1px solid #f0f0f0;
}

.page-btn {
  padding: 0.5rem 0.8rem;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.page-btn:hover:not(:disabled) {
  border-color: #f8b5c1;
  color: #f8b5c1;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.3rem;
}

.page-number {
  min-width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 1px solid #ddd;
  background-color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-number:hover {
  border-color: #f8b5c1;
  color: #f8b5c1;
}

.page-number.active {
  background-color: #f8b5c1;
  color: white;
  border-color: #f8b5c1;
}

@media (max-width: 1200px) {
  .flower-grid {
    grid-template-columns: repeat(3, 1fr); /* 中等屏幕3条数据一行 */
  }
}

@media (max-width: 900px) {
  .flower-grid {
    grid-template-columns: repeat(2, 1fr); /* 小屏幕2条数据一行 */
  }

  .filter-options {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 600px) {
  .flower-grid {
    grid-template-columns: 1fr; /* 超小屏幕1条数据一行 */
    padding: 1.5rem 1rem;
  }

  .filters {
    padding: 1rem;
  }

  .pagination {
    flex-wrap: wrap;
  }
}
</style>