<template>
  <div class="home">
    <Header />

    <!-- 轮播图 -->
    <div class="carousel-container">
      <div class="carousel-background"></div> <!-- 背景图容器 -->
      <Carousel v-model="currentSlide" :items-to-show="3" :wrapAround="true" :autoplay="5000">
        <Slide v-for="(image, index) in carouselImages" :key="index" @click="goToFlowerDetail(image.id)">
          <div
              class="carousel-slide"
              :class="{
              'carousel-slide-left': index === currentSlide - 1 || (currentSlide === 0 && index === carouselImages.length - 1),
              'carousel-slide-center': index === currentSlide,
              'carousel-slide-right': index === currentSlide + 1 || (currentSlide === carouselImages.length - 1 && index === 0),
            }"
          >
            <img :src="image.image_path" alt="轮播图" class="carousel-image" />
            <div class="carousel-title">{{ image.name }}</div>
          </div>
        </Slide>
      </Carousel>
    </div>

    <!-- 热销花朵 -->
    <FlowerSection :title="'热销花朵'" :flowers="hotFlowers" />
    <!-- 优惠花朵 -->
    <FlowerSection :title="'优惠花朵'" :flowers="discountFlowers" />

    <Footer />
  </div>
</template>

<script>
import { Carousel, Slide } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import FlowerSection from "@/components/FlowerSection.vue";

import { gethotFlowers, getdiscountFlowers, getCarouselImages } from '@/api/flower';

export default {
  components: {
    Header,
    Footer,
    Carousel,
    Slide,
    FlowerSection
  },
  data() {
    return {
      currentSlide: 0,
      carouselImages: [],
      hotFlowers: [],
      discountFlowers: [],
    };
  },
  methods: {
    goToFlowerDetail(flowerId) {
      this.$router.push(`/flowers/${flowerId}`);
    },
  },
  async created() {
    const baseUrl = 'http://localhost:5000/img/';
    const carouselResponse = await getCarouselImages();
    this.carouselImages = carouselResponse.flowers.map(flower => ({
      id: flower.id,
      image_path: baseUrl + flower.name,
      name: flower.name,
    }));
    const hotResponse = await gethotFlowers();
    this.hotFlowers = hotResponse.flowers;
    const discountResponse = await getdiscountFlowers();
    this.discountFlowers = discountResponse.flowers;
  },
};
</script>

<style scoped>
.home {
  padding: 20px;
}

/* 轮播图样式 */
.carousel-container {
  margin: 40px auto; /* 上下留白，水平居中 */
  width: 80%; /* 缩小轮播图区块宽度 */
  max-width: 800px; /* 设置最大宽度，避免过大 */
  position: relative; /* 相对定位，用于背景图 */
  border-radius: 15px; /* 圆角 */
  overflow: hidden; /* 隐藏超出部分 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* 阴影 */
}

.carousel-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/bg-lb.png'); /* 替换为你的背景图路径 */
  background-size: cover; /* 背景图覆盖整个容器 */
  background-position: center; /* 背景图居中 */
  filter: blur(10px); /* 模糊效果 */
  z-index: 0; /* 置于底层 */
}

.carousel-slide {
  transition: transform 0.5s ease, opacity 0.5s ease;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%; /* 确保每张图片宽度一致 */
  height: 200px; /* 缩小高度，适应小图片 */
  z-index: 1; /* 置于背景图之上 */
}

.carousel-slide-left {
  transform: translateX(-50%) scale(0.8);
  opacity: 0.6;
}

.carousel-slide-center {
  transform: scale(1.2);
  opacity: 1;
}

.carousel-slide-right {
  transform: translateX(50%) scale(0.8);
  opacity: 0.6;
}

.carousel-image {
  width: 100%; /* 图片宽度占满容器 */
  height: 100%; /* 图片高度占满容器 */
  object-fit: contain; /* 保持图片比例，防止变形 */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.carousel-slide:hover{
  transform: scale(1);
}

.carousel-title {
  position: absolute;
  bottom: 10px; /* 调整文字位置 */
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 16px; /* 缩小字体大小 */
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  background-color: rgba(0, 0, 0, 0.5); /* 添加背景色，确保文字清晰 */
  padding: 5px 10px;
  border-radius: 5px;
}
</style>