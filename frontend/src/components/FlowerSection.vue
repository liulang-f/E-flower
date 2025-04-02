<template>
  <section class="section-container">
    <h2 class="section-title">{{ title }}</h2>
    <div class="flower-grid">
      <FlowerItem
          v-for="flower in flowers"
          :key="flower.id"
          :flower="flower"
      />
    </div>
  </section>

</template>

<script>
import FlowerItem from './FlowerItem.vue'; // 假设你已经有一个 FlowerItem 组件

export default {
  name: 'FlowerSection',
  components: {
    FlowerItem
  },
  props: {
    title: {
      type: String,
      required: true
    },
    flowers: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
/* 保持原有的样式 */
.section-container {
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  width: 80%;
}

.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.flower-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 每行显示 4 朵花 */
  gap: 20px;
}
</style>