<template>
  <div class="flower-item" @click="goToFlowerDetail(flower.id)">
    <!-- 花卉图片 -->
    <img :src="'/api/img/' + flower.name" :alt="flower.name" class="flower-image" />

    <!-- 花卉信息 -->
    <div class="flower-info">
      <h3 class="flower-name">{{ flower.name }}</h3>

      <!-- 标签展示 -->
      <div class="flower-tags">
        <span v-for="(tag, index) in flower.tags" :key="index" class="flower-tag">
          {{ tag }}
        </span>
      </div>

      <!-- 价格展示 -->
      <div class="flower-price">
        <span v-if="discountPrice !== null" class="original-price">¥{{ flower.price.toFixed(2) }}</span>
        <span class="final-price">¥{{ discountPrice !== null ? discountPrice.toFixed(2) : flower.price?.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "FlowerItem",
  props: {
    flower: {
      type: Object,
      required: true
    }
  },
  computed: {
    // 折扣价逻辑：前端计算更灵活
    discountPrice() {
      if (this.flower.discount !== undefined && this.flower.discount !== null) {
        return this.flower.price * this.flower.discount;
      }
      return null;
    }
  },
  methods: {
    goToFlowerDetail(flowerId) {
      this.$router.push(`/flowers/${flowerId}`);
    },
  },
}
</script>

<style scoped>
/* 卡片样式 */
.flower-item {
  border: 1px solid #eee;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  cursor: pointer;
  background: #fff;
}

.flower-item:hover {
  transform: translateY(-5px);
}

/* 图片样式 */
.flower-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

/* 信息展示 */
.flower-info {
  padding: 10px;
  text-align: center;
}

/* 标签 */
.flower-tags {
  margin: 5px 0;
}

.flower-tag {
  display: inline-block;
  margin: 2px;
  padding: 2px 8px;
  background: #f1f1f1;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

/* 价格 */
.flower-price {
  margin-top: 10px;
  font-size: 16px;
  color: #333;
}

/* 原价带删除线 */
.original-price {
  text-decoration: line-through;
  color: #999;
  margin-right: 8px;
}

/* 折后价 */
.final-price {
  font-size: 18px;
  color: #e74c3c;
  font-weight: bold;
}
</style>