<template>
  <span class="tag" @click="goToTagPage">{{ tag }}</span>
</template>

<script>
export default {
  name: "TagItem",
  props: { tag: String },
  methods: {
    goToTagPage() {
      this.$router.push({ path: '/flowers', query: { tags: this.tag } });
    }
  }
};
</script>

<style scoped>
.tag {
  display: inline-block;
  background: #f1f1f1;
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 14px;
  color: #333;
  margin-right: 5px;
  cursor: pointer;
}

.tag:hover {
  background: #e74c3c;
  color: white;
}
</style>