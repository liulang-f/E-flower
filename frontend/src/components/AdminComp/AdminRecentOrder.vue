<template>
  <div class="orders-container">
    <h3 class="title">最近10条订单</h3>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="orders.length === 0" class="no-orders">暂无订单数据</div>
    <table v-else class="orders-table">
      <thead>
      <tr>
        <th>购买者</th>
        <th>下单时间</th>
        <th>总金额</th>
        <th>地址</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="order in orders" :key="order.id">
        <td>{{ order.username }}</td>
        <td>{{ formatDate(order.created_at) }}</td>
        <td>¥{{ order.total_price.toFixed(2) }}</td>
        <td>{{ order.address }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import {getRencentOrder} from "@/api/admin.js";

export default {
  name: 'RecentOrdersList',
  setup() {
    const orders = ref([]);
    const loading = ref(true);

    const fetchRecentOrders = async () => {
      orders.value = await getRencentOrder();
      loading.value = false;
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString().slice(0,5);
    };

    onMounted(() => {
      fetchRecentOrders();
    });

    return {
      orders,
      loading,
      formatDate
    };
  }
};
</script>

<style scoped>
.orders-container {
  height: 300px;
  width: 95%;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.title {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #333;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.orders-table th, .orders-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.orders-table th {
  font-weight: 500;
  color: #666;
  background-color: #fafafa;
}

.loading, .no-orders {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #999;
}
</style>
