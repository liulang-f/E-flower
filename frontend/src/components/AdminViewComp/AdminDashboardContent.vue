<template>
  <div class="admin-main">
    <div class="container-fluid" v-if="baseData">
      <h2 class="page-title">仪表盘概览</h2>

      <!-- Stats Cards Row -->
      <div class="stats-row">
        <div class="stat-card">
          <AdminStatCard
              title="今日订单"
              :value="baseData.today_orders"
              :change="baseData.order_percentage"
              :icon="['fas', 'shopping-cart']"
              type="orders"
          />
        </div>
        <div class="stat-card">
          <AdminStatCard
              title="新增用户"
              :value="baseData.today_users"
              :change="baseData.user_percentage"
              :icon="['fas', 'users']"
              type="users"
          />
        </div>
        <div class="stat-card">
          <AdminStatCard
              title="今日收益"
              :value="baseData.today_sales"
              :change="baseData.sales_percentage"
              :icon="['fas', 'dollar-sign']"
              type="revenue"
          />
        </div>
        <div class="stat-card">
          <AdminStatCard
              title="库存预警"
              :value="baseData.low_stock_flowers"
              :change="0"
              :icon="['fas', 'exclamation-triangle']"
              type="stock"
          />
        </div>
      </div>

      <!-- 第一行图表 -->
      <div class="chart-row">
        <div class="chart-item">
          <div class="chart-card">
            <h3>订单量走势图/7日</h3>
            <AdminSalesChart />
          </div>
        </div>
        <div class="chart-item">
          <div class="chart-card">
            <h3>热销榜单/15</h3>
            <AdminTopFlowersChart />
          </div>
        </div>
      </div>

      <!-- 第二行图表 -->
      <div class="chart-row">
        <div class="chart-item">
          <div class="chart-card">
            <h3>最新订单</h3>
            <AdminRecentOrder/>
          </div>
        </div>

        <div class="chart-item">
          <div class="chart-card">
            <h3>系统活动</h3>
            <AdminSystemActivitiesTable />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminStatCard from "@/components/AdminComp/AdminStatCard.vue";
import AdminSalesChart from "@/components/AdminComp/AdminSalesChart.vue";
import AdminSystemActivitiesTable from "@/components/AdminComp/AdminSystemActivitiesTable.vue";
import AdminTopFlowersChart from "@/components/AdminComp/AdminTopFlowersChart.vue";
import AdminRecentOrder from "@/components/AdminComp/AdminRecentOrder.vue";
import {getBaseData} from "@/api/admin.js";

export default {
  name: 'AdminDashboardContent',
  components: {
    AdminStatCard,
    AdminSalesChart,
    AdminSystemActivitiesTable,
    AdminTopFlowersChart,
    AdminRecentOrder
  },
  created() {
    this.fetchBaseData();
  },

  data(){
    return{
      baseData: null,
    }
  },

  methods:{
    async fetchBaseData() {
      this.baseData = await getBaseData();
    }
  }

}
</script>

<style scoped>
.admin-main {
  width: 100%;
}

.page-title {
  color: #4a6b57;
  margin-bottom: 25px;
  font-weight: 600;
  position: relative;
  padding-bottom: 10px;
}

.page-title:after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #4a6b57;
  border-radius: 3px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  min-height: 120px;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 25px;
}

.chart-card {
  background-color: white;
  border-radius: 12px;
  padding: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  height: 100%;
  min-height: 350px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin-top: 0;
  color: #4a6b57;
  font-size: 1.2rem;
  margin-bottom: 20px;
  font-weight: 600;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}
</style>