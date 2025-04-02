// FlowerGrid.vue - 花卉网格组件
<template>
  <div class="flower-grid">
    <h2 class="grid-title">热门花卉</h2>
    <div class="filters">
      <span class="filter-label">排序方式:</span>
      <div class="sort-options">
        <button
            class="sort-btn"
            :class="{ active: sortOption === 'sales' }"
            @click="$emit('changeSort', 'sales')">
          销量
        </button>
        <button
            class="sort-btn"
            :class="{ active: sortOption === 'price' }"
            @click="$emit('changeSort', 'price')">
          价格
        </button>
        <button
            class="sort-btn"
            :class="{ active: sortOption === 'created_at' }"
            @click="$emit('changeSort', 'created_at')">
          最新
        </button>
      </div>
    </div>
    <div class="grid-container">
      <FlowerCardHotView
          v-for="(flower, index) in flowers"
          :key="flower.id"
          :flower="flower"
          :rank="index + rankOffset"
      />
    </div>
  </div>
</template>

<script setup>
import FlowerCardHotView from "@/components/FlowerCardHotView.vue";

defineProps({
  flowers: {
    type: Array,
    required: true
  },
  rankOffset: {
    type: Number,
    default: 1
  },
  sortOption: {
    type: String,
    default: 'sales'
  }
});

defineEmits(['changeSort']);
</script>

<style scoped>
.flower-grid {
  padding: 20px;
}

.grid-title {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.filters {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 16px;
  margin-right: 10px;
  color: #555;
}

.sort-options {
  display: flex;
  gap: 10px;
}

.sort-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.sort-btn:hover {
  background-color: #f5f5f5;
}

.sort-btn.active {
  background-color: #ff4757;
  color: white;
  border-color: #ff4757;
}

.grid-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    gap: 10px;
  }

  .filter-label {
    margin-bottom: 5px;
  }
}
</style>