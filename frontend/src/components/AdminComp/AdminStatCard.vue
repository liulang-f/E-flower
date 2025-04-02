<template>
  <div class="stats-card" :class="type">
    <div class="card-icon">
      <font-awesome-icon :icon="icon" />
    </div>
    <div class="card-content">
      <h3>{{ title }}</h3>
      <p class="value">{{ value }}</p>
      <p class="change" :class="changeType">
        <font-awesome-icon :icon="changeIcon" />
        {{ change }} <span>vs yesterday</span>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsCard',
  props: {
    title: String,
    value: [String, Number],
    change: [String, Number],
    icon: Array,
    type: String
  },
  computed: {
    changeType() {
      return this.change >= 0 ? 'positive' : 'negative';
    },
    changeIcon() {
      return this.change >= 0 ? ['fas', 'arrow-up'] : ['fas', 'arrow-down'];
    }
  }
}
</script>

<style scoped>
.stats-card {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
  font-size: 1.5rem;
  color: white;
}

.stats-card.orders .card-icon {
  background-color: #ff6b6b;
}

.stats-card.users .card-icon {
  background-color: #48dbfb;
}

.stats-card.revenue .card-icon {
  background-color: #1dd1a1;
}

.stats-card.stock .card-icon {
  background-color: #feca57;
}

.card-content h3 {
  margin: 0 0 5px 0;
  font-size: 1rem;
  color: #6c757d;
  font-weight: 500;
}

.value {
  margin: 0 0 5px 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: #343a40;
}

.change {
  margin: 0;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.change.positive {
  color: #28a745;
}

.change.negative {
  color: #dc3545;
}

.change svg {
  margin-right: 5px;
}

.change span {
  color: #6c757d;
  margin-left: 5px;
}
</style>