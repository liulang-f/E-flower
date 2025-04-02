<template>
  <Header/>
  <div class="flowers-view-container">
    <!-- 第一行：搜索区域 -->
    <div class="search-container">
      <div class="search-box">
        <input
            v-model="searchQuery"
            type="text"
            placeholder="想要点什么？..."
            @input="handleSearch"
        >
        <button class="search-button" @click="handleSearch">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <!-- 第二行：筛选和排序区域 -->
    <div class="filter-sort-container">
      <!-- 左侧：筛选功能区 -->
      <div class="filter-section">
        <div class="filter-title">
          <i class="fas fa-filter"></i> 筛选
        </div>

        <!-- 第一行：上架时间 + 价格区间 -->
        <div class="filter-row">
          <div class="filter-item">
            <span>上架时间：</span>
            <div class="date-picker">
              <input type="date" v-model="filterDate" @change="applyFilters" @input="handleDateInput">
            </div>
          </div>

          <div class="filter-item">
            <span>价格区间：</span>
            <div class="price-range">
              <input
                  type="number"
                  v-model="minPrice"
                  placeholder="最低价"
                  @change="applyFilters"
              >
              <span>至</span>
              <input
                  type="number"
                  v-model="maxPrice"
                  placeholder="最高价"
                  @change="applyFilters"
              >
            </div>
          </div>
        </div>

        <!-- 第二行：标签选择器 -->
        <div class="filter-item">
          <span>标签选择：</span>
          <div class="tag-selector">
            <div class="tag-options-container">
              <div class="tag-options">
                <span
                    v-for="(tag, index) in availableTags"
                    :key="index"
                    :class="['tag-option', { selected: selectedTags.includes(tag) }]"
                    @click="toggleTag(tag)"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：排序功能区 -->
      <div class="sort-section">
        <div class="sort-title">
          <i class="fas fa-sort"></i> 排序
        </div>
        <div class="sort-options">
          <button
              v-for="option in sortOptions"
              :key="option.value"
              :class="['sort-button', { active: currentSort === option.value }]"
              @click="setSortOption(option.value)"
          >
            {{ option.label }}
            <i v-if="currentSort === option.value" :class="sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down'"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 花卉列表区域 -->
    <div class="flower-grid">
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>正在加载花卉...</p>
      </div>

      <template v-else-if="flowers.length > 0">
        <flower-card
            v-for="flower in flowers"
            :key="flower.id"
            :flower="flower"
        ></flower-card>
      </template>

      <div v-else class="no-results">
        <i class="fas fa-sad-tear"></i>
        <p>没有找到符合条件的花卉，请尝试调整筛选条件</p>
      </div>
    </div>

    <!-- 底部翻页区域 -->
    <div class="pagination-container">
      <button
          class="pagination-button"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
      >
        <i class="fas fa-chevron-left"></i> 上一页
      </button>

      <div class="page-numbers">
        <button
            v-for="page in displayedPages"
            :key="page"
            :class="['page-number', { active: currentPage === page }]"
            @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </div>

      <div class="page-jump">
        <span>前往</span>
        <input
            type="number"
            v-model.number="jumpToPage"
            min="1"
            :max="totalPages"
        >
        <span>页</span>
        <button @click="goToPage(jumpToPage)">确定</button>
      </div>

      <button
          class="pagination-button"
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
      >
        下一页 <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
  <Footer/>
</template>

<script>
// FlowersView.vue - 花卉展示页面
import TagItem from '@/components/TagItem.vue';
import Header from "@/components/Header.vue";
import {fetchFlowers } from '@/api/flower'; // 引入封装的API
import Footer from "@/components/Footer.vue";
import FlowerCard from "@/components/FlowerCard.vue";

export default {
  name: 'FlowersView',
  components: {
    Footer,
    FlowerCard,
    TagItem,
    Header
  },
  data() {
    return {
      searchQuery: null,
      filterDate: null,
      minPrice: null,
      maxPrice: null,
      selectedTags: [],
      availableTags: [],
      sortOptions: [
        { label: '销量', value: 'sales' },
        { label: '价格', value: 'price' },
        { label: '库存', value: 'stock' },
        { label: '上架时间', value: 'created_at' }
      ],
      currentSort: '',
      sortDirection: 'desc',
      currentPage: 1,
      totalPages: 0,
      jumpToPage: 1,
      pageSize: 12,
      flowers: [],
      loading: false
    };
  },
  computed: {
    displayedPages() {
      const pages = [];
      const maxDisplayPages = 5;
      if (this.totalPages <= maxDisplayPages) {
        for (let i = 1; i <= this.totalPages; i++) pages.push(i);
      } else {
        if (this.currentPage <= 3) {
          for (let i = 1; i <= 5; i++) pages.push(i);
        } else if (this.currentPage >= this.totalPages - 2) {
          for (let i = this.totalPages - 4; i <= this.totalPages; i++) pages.push(i);
        } else {
          for (let i = this.currentPage - 2; i <= this.currentPage + 2; i++) pages.push(i);
        }
      }
      return pages;
    }
  },
  created() {
    this.loadFlowers();
  },

  watch: {
    '$route.query': {
      handler(newQuery) {
        // 保留传递的参数
        const { tags, search } = newQuery;

        // 重置其他筛选条件，但保留传递的参数
        this.resetFilters({ tags, search });

        // 重新加载数据
        this.loadFlowers();
      },
      immediate: true
    }
  },

  methods: {

    resetFilters({ tags = null, search = null } = {}) {
      // 清空其他筛选条件
      this.filterDate = null;
      this.minPrice = null;
      this.maxPrice = null;
      this.currentSort = null;
      this.sortDirection = 'desc';
      this.currentPage = 1;
      this.flowers = [];
      this.totalPages = 0;

      // 保留传递的参数
      this.selectedTags = tags ? [tags] : [];
      this.searchQuery = search || null;
    },

    handleDateInput(event) {
      // 检查输入框的值是否为空字符串
      if (event.target.value === '') {
        this.filterDate = null; // 如果为空字符串，将 filterDate 设置为 null
      }
    },

    toggleTag(tag) {
      if (this.selectedTags.includes(tag)) {
        this.selectedTags = this.selectedTags.filter(t => t !== tag);
      } else {
        this.selectedTags.push(tag);
      }
      this.applyFilters();
    },
    handleSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.currentPage = 1;
        this.loadFlowers();
      }, 300);
    },

    applyFilters() {
      this.currentPage = 1;
      this.loadFlowers();
    },

    setSortOption(option) {
      if (this.currentSort === option) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.currentSort = option;
        this.sortDirection = 'desc';
      }
      this.loadFlowers();
    },

    goToPage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      this.loadFlowers();
    },

    async loadFlowers() {
      this.loading = true;
      try {
        const params = {
          search: this.searchQuery,
          create_at: this.filterDate,
          min_price: this.minPrice,
          max_price: this.maxPrice,
          tags: this.selectedTags.join(','),
          sort_by: this.currentSort,
          order: this.sortDirection,
          page: this.currentPage,
          per_page: this.pageSize
        };
        const data = await fetchFlowers(params);
        this.flowers = data.flowers;
        this.totalPages = data.pages;
        this.availableTags = data.tags;
      } catch (error) {
        console.error('Failed to load flowers:', error);
      } finally {
        this.loading = false;
      }
    },
  }
};
</script>

<style scoped>
.flowers-view-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

/* 搜索区域样式 */
.search-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.search-box {
  position: relative;
  width: 60%;
  max-width: 600px;
}

.search-box input {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 30px;
  transition: all 0.3s;
  outline: none;
}

.search-box input:focus {
  border-color: #ff7675;
  box-shadow: 0 0 8px rgba(255, 118, 117, 0.3);
}

.search-button {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #ff7675;
  font-size: 18px;
  cursor: pointer;
}

/* 筛选和排序区域样式 */
.filter-sort-container {
  display: flex;
  margin-bottom: 30px;
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.filter-section {
  flex: 2;
  padding-right: 20px;
  border-right: 1px solid #e0e0e0;
}

.sort-section {
  flex: 1;
  padding-left: 20px;
}

.filter-title, .sort-title {
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
  display: flex;
  align-items: center;
}

.filter-title i, .sort-title i {
  margin-right: 8px;
  color: #ff7675;
}

/* 通用输入样式 */
.date-picker input,
.price-range input,
.tag-selector select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}

/* 价格范围样式 */
.price-range {
  display: flex;
  align-items: center;
}

.price-range input {
  width: 80px;
}

.price-range span {
  margin: 0 8px;
}

/* 通用筛选行样式 */
.filter-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.filter-item {
  display: flex;
  align-items: center;
}

.filter-item span {
  font-size: 14px;
  color: #666;
  margin-right: 10px;
}

/* 标签选择器样式 */
.tag-selector {
  width: 100%;
  overflow: hidden;
}

.tag-options-container {
  width: 600px;
  overflow-x: auto;
  white-space: nowrap;
  padding-bottom: 10px;
}

.tag-options {
  display: inline-flex;
  gap: 8px;
  padding-right: 20px;
}

.tag-option {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #fff;
  color: #666;
  flex-shrink: 0;
}

.tag-option:hover {
  border-color: #ff7675;
  color: #ff7675;
}

.tag-option.selected {
  background-color: #ff7675;
  color: white;
  border-color: #ff7675;
}

/* 排序按钮样式 */
.sort-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.sort-button {
  padding: 8px 15px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.sort-button:hover {
  border-color: #ff7675;
  color: #ff7675;
}

.sort-button.active {
  background-color: #ff7675;
  color: white;
  border-color: #ff7675;
}

/* 花卉列表样式 */
.flower-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
  min-height: 500px;
}

@media (max-width: 1200px) {
  .flower-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .flower-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .flower-grid {
    grid-template-columns: 1fr;
  }
}

/* 加载状态样式 */
.loading-container {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.loading-spinner {
  border: 4px solid rgba(255, 118, 117, 0.1);
  border-left: 4px solid #ff7675;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 无结果样式 */
.no-results {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #666;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.no-results i {
  font-size: 48px;
  color: #ff7675;
}

/* 分页样式 */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.pagination-button {
  padding: 8px 15px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.pagination-button:hover:not(:disabled) {
  background-color: #ff7675;
  color: white;
  border-color: #ff7675;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 5px;
}

.page-number {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-number:hover {
  border-color: #ff7675;
}

.page-number.active {
  background-color: #ff7675;
  color: white;
  border-color: #ff7675;
}

.page-jump {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-jump input {
  width: 50px;
  padding: 6px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-jump button {
  padding: 6px 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-jump button:hover {
  background-color: #ff7675;
  color: white;
  border-color: #ff7675;
}
</style>