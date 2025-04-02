<template>
  <div class="admin-order-manage">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" class="mb-4">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <font-awesome-icon icon="shopping-cart" size="2x" class="text-primary"/>
            <div>
              <span>今日订单</span>
              <h3>{{ stats.todayOrders }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <font-awesome-icon icon="clock" size="2x" class="text-warning"/>
            <div>
              <span>待处理</span>
              <h3>{{ stats.pendingOrders }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <font-awesome-icon icon="truck" size="2x" class="text-success"/>
            <div>
              <span>配送中</span>
              <h3>{{ stats.shippingOrders }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <font-awesome-icon icon="yen-sign" size="2x" class="text-danger"/>
            <div>
              <span>今日收入</span>
              <h3>¥{{ stats.todayIncome }}</h3>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索和筛选区域 -->
    <el-card class="mb-4">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="输入订单号" clearable/>
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 100px">
            <el-option label="待付款" value="pending"/>
            <el-option label="已付款" value="paid"/>
            <el-option label="配送中" value="shipped"/>
            <el-option label="已完成" value="completed"/>
            <el-option label="已取消" value="cancelled"/>
          </el-select>
        </el-form-item>
        <el-form-item label="下单时间">
          <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <font-awesome-icon icon="search" class="mr-1"/>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <font-awesome-icon icon="redo" class="mr-1"/>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 订单表格 -->
    <el-card>
      <div class="table-actions mb-3">
        <el-button type="danger" :disabled="!selectedOrders.length" @click="batchCancel">
          <font-awesome-icon icon="times-circle" class="mr-1"/>
          批量取消
        </el-button>
        <el-button type="success" :disabled="!selectedOrders.length" @click="batchShip">
          <font-awesome-icon icon="truck" class="mr-1"/>
          批量接单
        </el-button>
        <el-button type="info" @click="exportOrders">
          <font-awesome-icon icon="file-export" class="mr-1"/>
          导出订单
        </el-button>
      </div>

      <el-table
          :data="orderList"
          border
          stripe
          style="width: 100%"
          @sort-change="handleSortChange"
          @selection-change="handleSelectionChange"
          v-loading="loading"
      >
        <el-table-column type="selection" width="55"/>
        <el-table-column prop="id" label="订单号" width="180" sortable="custom"/>
        <el-table-column prop="username" label="用户" width="120"/>
        <el-table-column prop="total_price" label="总金额" width="120" sortable="custom">
          <template #default="{row}">
            ¥{{ row.totalPrice.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{row}">
            <el-tag :type="getStatusTagType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" width="180" sortable="custom">
          <template #default="{row}">
            {{ formatDateTime(row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column prop="address" label="配送地址" min-width="200" show-overflow-tooltip/>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{row}">
            <el-button size="small" @click="showOrderDetail(row)">
              <font-awesome-icon icon="eye"/>
              详情
            </el-button>
            <el-dropdown @command="handleCommand($event, row)" trigger="click">
              <el-button size="small">
                <font-awesome-icon icon="ellipsis-v"/>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="ship" :disabled="row.status !== 'paid'">
                    <font-awesome-icon icon="truck" class="mr-1"/>
                    接单发货
                  </el-dropdown-item>
                  <el-dropdown-item command="cancel" :disabled="row.status!=='paid'">
                    <font-awesome-icon icon="times" class="mr-1"/>
                    取消订单
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided :disabled="row.status!=='completed'">
                    <font-awesome-icon icon="trash" class="mr-1 text-danger"/>
                    删除订单
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
          class="mt-4"
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
    </el-card>

    <!-- 订单详情弹窗组件 -->
    <AdminOrderDetailDialog
        v-model="detailDialogVisible"
        :order-id="currentOrderId"
        @ship-order="shipOrder"
        @cancel-order="cancelOrder"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {adminOrderStatus, delOrder, getAllOrders, getBaseOrderInf} from "@/api/order.js"
import AdminOrderDetailDialog from "@/components/AdminComp/AdminOrderDetailDialog.vue";

// 数据状态
const orderList = ref([])
const selectedOrders = ref([])
const detailDialogVisible = ref(false)
const loading = ref(false)
const oneOrderL = ref([])
const currentOrderId = ref('')

const stats = ref({
  todayOrders: 0,
  pendingOrders: 0,
  shippingOrders: 0,
  todayIncome: 0
})

const searchForm = ref({
  orderId: '',
  status: '',
  dateRange: []
})

const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const sortOptions = ref({
  prop: 'created_at',
  order: 'descending'
})

// 辅助函数
const getStatusTagType = (status) => {
  const map = {
    pending: 'warning',
    paid: 'primary',
    shipped: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return map[status] || ''
}

const getStatusText = (status) => {
  const map = {
    pending: '待付款',
    paid: '已付款',
    shipped: '配送中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

const formatDateTime = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

// 事件处理
const handleSearch = async () => {
  pagination.value.currentPage = 1
  await fetchOrders()
}

const resetSearch = () => {
  searchForm.value = {
    orderId: '',
    status: '',
    dateRange: []
  }
  handleSearch()
}

const handleSortChange = ({ prop, order }) => {
  sortOptions.value = { prop, order }
  fetchOrders()
}

const handleSizeChange = (val) => {
  pagination.value.pageSize = val
  fetchOrders()
}

const handleCurrentChange = (val) => {
  pagination.value.currentPage = val
  fetchOrders()
}

const handleSelectionChange = (selection) => {
  selectedOrders.value = selection.map(item => item.id)
}

const handleCommand = (command, row) => {
  switch (command) {
    case 'ship':
      shipOrder(row)
      break
    case 'cancel':
      cancelOrder(row)
      break
    case 'delete':
      deleteOrder(row)
      break
  }
}

// 显示订单详情
const showOrderDetail = (order) => {
  currentOrderId.value = order.id
  detailDialogVisible.value = true
}

// 订单操作
const shipOrder = async (order) => {
  try {
    await ElMessageBox.confirm('确认接单发货吗?', '提示', {
      type: 'warning'
    })
    oneOrderL.value.push(order.id)
    await adminOrderStatus(oneOrderL.value,'shipped')
    order.status = 'shipped'
    await fetchOrders()
    oneOrderL.value = []
  } catch (error) {
    console.log('取消操作')
  }
}

const cancelOrder = async (order) => {
  try {
    await ElMessageBox.confirm('确认取消此订单吗?', '提示', {
      type: 'warning'
    })
    oneOrderL.value.push(order.id)
    await adminOrderStatus(oneOrderL.value, 'cancelled')
    order.status = 'cancelled'
    await fetchOrders()
    oneOrderL.value = []
  } catch (error) {
    console.log('取消操作')
  }
}

const deleteOrder = async (order) => {
  try {
    await ElMessageBox.confirm('确认删除此订单吗?此操作不可恢复!', '警告', {
      type: 'error'
    })
    await delOrder(order.id)
    orderList.value = orderList.value.filter(item => item.id !== order.id)
  } catch (error) {
    // 取消操作
  }
}

const batchShip = async () => {
  try {
    await ElMessageBox.confirm(`确认批量接单 ${selectedOrders.value.length} 个订单吗?`, '提示', {
      type: 'warning'
    })
    await adminOrderStatus(selectedOrders.value, 'shipped')
    orderList.value.forEach(order => {
      if (selectedOrders.value.includes(order.id) && order.status === 'paid') {
        order.status = 'shipped'
      }
    })
    selectedOrders.value = []
  } catch (error) {
    // 取消操作
  }
}

const batchCancel = async () => {
  try {
    await ElMessageBox.confirm(`确认批量取消 ${selectedOrders.value.length} 个订单吗?`, '提示', {
      type: 'warning'
    })
    await adminOrderStatus(selectedOrders.value,'cancelled')
    orderList.value.forEach(order => {
      if (selectedOrders.value.includes(order.id) && 'paid'===order.status) {
        order.status = 'cancelled'
      }
    })
    selectedOrders.value = []
  } catch (error) {
    console.log('取消操作')
  }
}

const exportOrders = () => {
  ElMessage.info('导出功能开发中')
}

// 数据获取
const fetchOrders = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.value.currentPage,
      pageSize: pagination.value.pageSize,
      sort: sortOptions.value.prop,
      order: sortOptions.value.order
    }

    if(searchForm.value.status){
      params['status'] = searchForm.value.status
    }
    if(searchForm.value.orderId){
      params['orderId'] = searchForm.value.orderId
    }
    if (searchForm.value.dateRange?.length === 2) {
      params['dateRange[]'] = searchForm.value.dateRange
    }

    const OrderDatas = await getAllOrders(params)
    orderList.value = OrderDatas.orders
    pagination.value.total = OrderDatas.total
    updateStats()
  } catch (error) {
    ElMessage.error('获取订单列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const updateStats = async () => {
  const countO = await getBaseOrderInf()
  stats.value = {
    todayOrders: countO.todaycount,
    pendingOrders: countO.todayclcount,
    shippingOrders: countO.todaypscount,
    todayIncome: countO.todayincome
  }
}

// 初始化
onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.admin-order-manage {
  padding: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-card span {
  color: #888;
  font-size: 14px;
}

.stat-card h3 {
  margin: 5px 0 0;
  font-size: 24px;
}

.text-primary {
  color: #409EFF;
}

.text-success {
  color: #67C23A;
}

.text-warning {
  color: #E6A23C;
}

.text-danger {
  color: #F56C6C;
}

.text-muted {
  color: #909399;
  font-size: 12px;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.mb-3 {
  margin-bottom: 15px;
}

.mb-4 {
  margin-bottom: 20px;
}

.mt-4 {
  margin-top: 20px;
}

.mr-1 {
  margin-right: 5px;
}
</style>