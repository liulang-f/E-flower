<!-- components/Breadcrumb.vue -->
<template>
  <div class="breadcrumb">
    <div
        v-for="(item, index) in items"
        :key="index"
        class="breadcrumb-item"
    >
      <router-link
          v-if="index < items.length - 1"
          :to="item.path"
          class="breadcrumb-link"
      >
        {{ item.title }}
      </router-link>
      <span v-else class="breadcrumb-text">{{ item.title }}</span>

      <i
          v-if="index < items.length - 1"
          class="fas fa-chevron-right breadcrumb-separator"
      ></i>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Breadcrumb',
  props: {
    items: {
      type: Array,
      required: true,
      validator: (value) => {
        // 验证数组中的每个对象都有title和path属性
        return value.every(item =>
            typeof item === 'object' &&
            'title' in item &&
            'path' in item
        )
      }
    }
  }
}
</script>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumb-link {
  color: #666;
  text-decoration: none;
  transition: color 0.3s;
}

.breadcrumb-link:hover {
  color: #4CAF50;
}

.breadcrumb-text {
  color: #999;
}

.breadcrumb-separator {
  font-size: 10px;
  color: #ccc;
  margin: 0 8px;
}
</style>