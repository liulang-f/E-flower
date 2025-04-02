<template>
    <Header/>
  <!-- 背景图片 -->
  <div
      class="flower-detail-background"
      :style="{ backgroundImage: `url(http://localhost:5000/img/${flower.name})` }"
  >
  </div>


  <!-- 主内容 -->
  <div class="flower-detail-container" v-if="flag">
    <!-- 上半部分：图片和信息 -->
    <el-row :gutter="20" class="flower-detail-row">
      <!-- 左侧：图片展示 -->
      <el-col :span="12" class="flower-image-col">
        <div class="flower-image">
          <el-image
              :src="'http://localhost:5000/img/' + flower.name"
              :alt="flower.name"
              fit="contain"
              class="flower-img"
          />
        </div>
      </el-col>

      <!-- 右侧：花卉信息 -->
      <el-col :span="12" class="flower-info-col">
        <div class="flower-info">
          <h1 class="flower-name">{{ flower.name || '加载中...' }}</h1>

          <!-- 标签 -->
          <div class="flower-tags">
            <TagItem v-for="tag in flower.tags || []" :key="tag" :tag="tag" />
          </div>

          <!-- 价格 -->
          <div class="flower-price">
            <span v-if="discountPrice !== null" class="original-price">¥{{ flower.price?.toFixed(2) }}</span>
            <span class="final-price">¥{{ discountPrice !== null ? discountPrice.toFixed(2) : flower.price?.toFixed(2) }}</span>
          </div>

          <!-- 额外信息 -->
          <div class="flower-meta">
            <span><strong>上架时间：</strong>{{ formatDate(flower.created_at) }}</span>
            <span><strong>已售：</strong>{{ flower.sales || 0 }} 朵</span>
            <span><strong>库存：</strong>{{ flower.stock || 0 }} 朵</span>
          </div>

          <!-- 花朵介绍 -->
          <div class="flower-description">
            <h3>花朵介绍</h3>
            <p>{{ flower.description || '暂无介绍' }}</p>
          </div>

          <!-- 活动介绍 -->
          <div class="flower-promotion">
            <h3>活动介绍</h3>
            <p>{{ flower.promotion || '暂无活动' }}</p>
          </div>

          <!-- 数量选择 -->
          <div class="quantity-container">
            <label for="quantity">数量：</label>
            <el-input-number v-model="quantity" :min="1" :max="flower.stock || 1" />
          </div>

          <!-- 购物按钮 -->
          <div class="action-buttons">
            <el-button type="primary" class="add-cart-btn" @click="addCart">加入购物车</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>

  <!-- 分割线 -->
  <el-divider />

  <!-- 推荐花卉 -->
  <div v-if="flag">
    <FlowerSection title="相关推荐" :flowers="recommendedFlowers"></FlowerSection>
  </div>

  <Footer/>
</template>


<script>
import TagItem from "@/components/TagItem.vue";
import FlowerSection from "@/components/FlowerSection.vue";
import {getFlowerDetail, gethotFlowers} from "@/api/flower";
import Header from '@/components/Header.vue';
import Footer from "@/components/Footer.vue";
import {addToCart} from "@/api/cart.js"

import {ElButton, ElCol, ElDivider, ElImage, ElInputNumber, ElMessage, ElRow} from 'element-plus';


export default {
  name: "FlowerDetail",
  components: { FlowerSection, TagItem,ElImage,Header,Footer,ElMessage,
    ElButton,
    ElInputNumber,
    ElDivider,
    ElRow,
    ElCol, },
  data() {
    return {
      flower: {},
      recommendedFlowers: [],
      quantity: 1,
      flag:false,
    };
  },
  computed: {
    discountPrice() {
      if (this.flower.discount !== undefined && this.flower.discount !== null) {
        return this.flower.price * this.flower.discount;
      }
      return null;
    }
  },
  methods: {

    async addCart() {
      // 检查是否选择了鲜花和数量
      if (!this.flower || !this.quantity) {
        ElMessage.warning('请选择鲜花和数量');
        return;
      }

      // 调用 addToCart 方法，不处理返回值
      await addToCart(this.flower.id, this.quantity);
    },

    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    },async loadFlowerDetail(flowerId) {
      try {
        this.flower = await getFlowerDetail(flowerId);
        this.recommendedFlowers = (await gethotFlowers()).flowers;
      } catch (error) {
        console.error('加载花卉详情失败:', error);
      }
    }
  },async created() {
    // 移除这里的请求，交给 watch 处理
    this.flag = true;
  },
  watch: {
    '$route.params.flowerId': {
      immediate: true, // 首次加载时自动执行
      async handler(newId) {
        try {
          this.flower = await getFlowerDetail(newId);
          this.recommendedFlowers = (await gethotFlowers()).flowers;
        } catch (error) {
          console.error("加载花卉详情失败:", error);
        }
      }
    }
  }
}
</script>


<style scoped>
/* 页面整体布局 */
  /* 背景图片 */
.flower-detail-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(8px); /* 背景虚化 */
  opacity: 0.5; /* 背景透明度 */
  z-index: -1; /* 确保背景在内容下方 */
}

/* 主容器 */
.flower-detail-container {
  position: relative;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.7); /* 半透明背景 */
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  max-width: 1000px; /* 限制最大宽度 */
}

/* 图片区域 */
.flower-image-col {
  padding: 20px;
}

.flower-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.flower-img {
  max-width: 100%;
  max-height: 400px; /* 控制图片最大高度 */
  border-radius: 8px;
}

/* 信息区域 */
.flower-info-col {
  padding: 20px;
}

.flower-name {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 10px;
}

.flower-tags {
  margin: 10px 0;
}

.flower-price {
  margin: 20px 0;
}

.original-price {
  text-decoration: line-through;
  color: #999;
  margin-right: 10px;
}

.final-price {
  font-size: 1.5rem;
  color: #f56c6c;
}

.flower-meta {
  margin: 20px 0;
  display: flex;
  gap: 20px; /* 已售、库存等信息在同一行 */
  color: #666;
}

.flower-description,
.flower-promotion {
  margin: 20px 0;
}

.flower-description h3,
.flower-promotion h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
}

.flower-description p,
.flower-promotion p {
  color: #666;
  line-height: 1.6;
}

.quantity-container {
  margin: 20px 0;
}

.action-buttons {
  margin-top: 20px;
}

.add-cart-btn {
  width: 100%;
  background-color: #f56c6c;
  border: none;
  transition: background-color 0.3s ease;
}

.add-cart-btn:hover {
  background-color: #e65a5a;
}
</style>