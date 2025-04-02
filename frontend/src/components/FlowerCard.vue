<template>
  <div class="flower-card">
    <div class="card-image" @click="goToFlowerDetail(flower.id)">
      <img :src="'/api/img/' + flower.name" :alt="flower.name">
      <div class="discount-badge" v-if="hasDiscount">
        {{ discountPercentage }}% OFF
      </div>
    </div>

    <div class="card-content">
      <h3 class="flower-name">{{ flower.name }}</h3>

      <div class="price-container">
        <span class="current-price">¥{{ currentPrice }}</span>
        <span class="original-price" v-if="hasDiscount">¥{{ flower.price }}</span>
      </div>

      <p class="flower-description">{{ flower.description }}</p>

      <div class="flower-meta">
        <div class="sales-count">
          <i class="fas fa-shopping-cart"></i>
          已售 : {{ flower.sales }}
        </div>
      </div>

      <div class="tags-container">
        <tag-item
            v-for="(tag, index) in flower.tags" :key="index" :tag="tag"
        ></tag-item>
      </div>

      <button class="add-to-cart-button" @click="addCart(flower.id)">
        <i class="fas fa-plus"></i> 加入购物车
      </button>
    </div>
  </div>
</template>

<script>
import TagItem from './TagItem.vue';
import {addToCart} from "@/api/cart.js";

export default {
  name: 'FlowerCard',
  components: {
    TagItem
  },
  props: {
    flower: {
      type: Object,
      required: true
    }
  },
  computed: {
    // 是否有折扣
    hasDiscount() {
      return this.flower.discount && this.flower.discount < 1; // discount < 1 表示有折扣
    },
    // 折扣百分比
    discountPercentage() {
      if (!this.hasDiscount) return 0;
      return Math.round((1 - this.flower.discount) * 100); // 计算折扣百分比
    },
    // 当前价格（折扣后的价格）
    currentPrice() {
      if (this.hasDiscount) {
        return (this.flower.price * this.flower.discount).toFixed(2); // 计算折扣后的价格
      }
      return this.flower.price.toFixed(2); // 无折扣时显示原价
    }
  },
  methods: {
    goToFlowerDetail(flowerId) {
      this.$router.push(`/flowers/${flowerId}`);
    },
    addCart(flowerid){
      addToCart(flowerid,1);
    }
  },

};
</script>

<style scoped>
.flower-card {
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.flower-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.flower-card:hover .card-image img {
  transform: scale(1.1);
}

.discount-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff7675;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}

.card-content {
  padding: 15px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.flower-name {
  margin: 0 0 10px;
  font-size: 18px;
  color: #333;
}

.price-container {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-price {
  font-size: 18px;
  font-weight: bold;
  color: #ff7675;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.flower-description {
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.flower-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 13px;
  color: #888;
}

.sales-count i {
  margin-right: 5px;
  color: #ff7675;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
}

.add-to-cart-button {
  margin-top: auto;
  padding: 8px 0;
  background-color: #ff7675;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.add-to-cart-button:hover {
  background-color: #e84393;
}
</style>