<template>
  <Header/>
  <div class="orders-container">
    <h1 class="page-title">我的订单</h1>

    <!-- 订单筛选和搜索区域 -->
    <div class="filter-section">
      <div class="status-filters">
        <button
            v-for="status in statusOptions"
            :key="status.value"
            :class="['status-btn', currentStatus === status.value ? 'active' : '']"
            @click="filterByStatus(status.value)"
        >
          {{ status.label }}
        </button>
      </div>

      <div class="search-section">
        <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="搜索订单号..."
            class="search-input"
        />
      </div>
    </div>

    <!-- 订单列表 -->
    <div class="orders-list" v-if="orders.length > 0">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <div class="order-info">
            <span class="order-id">订单号: {{ order.id }}</span>
            <span class="order-date">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="order-status" :class="getStatusClass(order.status)">
            {{ getStatusText(order.status) }}
          </div>
        </div>

        <div class="order-brief">
          <div class="order-address">
            <i class="fa fa-map-marker"></i>
            <span>{{ order.address }}</span>
          </div>
          <div class="order-flower-count">
            <i class="fa fa-shopping-basket"></i>
            <span>{{ order.flower_count }} 种花卉</span>
          </div>
          <div class="order-price">
            <i class="fa fa-yen-sign"></i>
            <span>{{ formatPrice(order.total_price) }}</span>
          </div>
        </div>

        <div class="order-actions">
          <button class="btn view-btn" @click="viewOrderDetail(order.id)">查看详情</button>
          <button v-if="order.status === 'pending'" class="btn pay-btn" @click="handlePayment(order.id)">
            去支付
          </button>
          <button v-if="order.status === 'pending'" class="btn cancel-btn" @click="cancelOrder(order.id)">
            取消订单
          </button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <p>暂无订单记录</p>
      <router-link to="/" class="btn shop-btn">去购物</router-link>
    </div>

    <!-- 分页控件 -->
    <div class="pagination" v-if="totalPages > 1">
      <!-- 上一页按钮 -->
      <button
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
          class="page-btn prev-btn"
          title="上一页"
      >
        <font-awesome-icon icon="fa-solid fa-chevron-left" />
      </button>

      <!-- 首页按钮（当不在第一页时显示） -->
      <span
          v-if="currentPage !== 1 && totalPages > 5"
          @click="changePage(1)"
          class="page-num"
          title="首页"
      >
    1
  </span>

      <!-- 省略号（如果第一页和起始页之间有间隔） -->
      <span v-if="displayedPages.length > 0 && displayedPages[0] > 2" class="page-ellipsis">...</span>

      <!-- 中间页码 -->
      <span
          v-for="page in displayedPages"
          :key="page"
          :class="['page-num', currentPage === page ? 'active' : '']"
          @click="changePage(page)"
      >
    {{ page }}
  </span>

      <!-- 省略号（如果结束页和最后一页之间有间隔） -->
      <span v-if="displayedPages.length > 0 && displayedPages[displayedPages.length - 1] < totalPages - 1" class="page-ellipsis">...</span>

      <!-- 尾页按钮（当不在最后一页时显示） -->
      <span
          v-if="currentPage !== totalPages && totalPages > 5"
          @click="changePage(totalPages)"
          class="page-num"
          title="尾页"
      >
    {{ totalPages }}
  </span>

      <!-- 下一页按钮 -->
      <button
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
          class="page-btn next-btn"
          title="下一页"
      >
        <font-awesome-icon icon="fa-solid fa-chevron-right" />
      </button>
    </div>

    <!-- 订单详情对话框 -->
    <div v-if="showOrderDetail" class="modal-overlay" @click.self="closeOrderDetail">
      <div class="modal-container">
        <div class="modal-header">
          <h2>订单详情</h2>
          <button class="close-btn" @click="closeOrderDetail">×</button>
        </div>

        <div class="modal-content" v-if="orderDetail">
          <div class="detail-header">
            <div class="detail-id">订单号: {{ orderDetail.order_id }}</div>
            <div class="detail-status" :class="getStatusClass(orderDetail.status)">
              {{ getStatusText(orderDetail.status) }}
            </div>
          </div>

          <div class="detail-info">
            <div class="info-item">
              <span class="info-label">下单时间:</span>
              <span class="info-value">{{ formatDate(orderDetail.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">收货地址:</span>
              <span class="info-value">{{ orderDetail.address }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">订单总价:</span>
              <span class="info-value price">{{ formatPrice(orderDetail.total_price) }} <small>配送费十元</small> </span>
            </div>
          </div>

          <div class="items-list">
            <h3>订单商品</h3>
            <div class="item-card" v-for="item in orderDetail.items" :key="item.flower_id">
              <div class="item-img">
                <img :src="`api/img/${item.flower_name}`" :alt="item.flower_name">
              </div>
              <div class="item-details">
                <div class="item-name">{{ item.flower_name }}</div>
                <div class="item-desc">{{ item.flower_description }}</div>
                <div class="item-price-info">
                  <div class="unit-price">单价: {{ formatPrice(item.flower_price) }}</div>
                  <div class="quantity">数量: {{ item.flower_quantity }}</div>
                  <div class="total-item-price">小计: {{ formatPrice(item.flower_price * item.flower_quantity) }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="order-timeline">
            <h3>订单进度</h3>
            <div class="timeline">
              <div
                  v-for="(step, index) in orderTimeline"
                  :key="index"
                  :class="['timeline-step', isStepCompleted(step.status) ? 'completed' : '']"
              >
                <div class="step-icon">
                  <font-awesome-icon :icon="step.icon" />
                </div>
                <div class="step-content">
                  <div class="step-title">{{ step.title }}</div>
                  <div class="step-time" v-if="isStepCompleted(step.status)">
                    {{ index === 0 ? formatDate(orderDetail.created_at) : '处理中' }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-actions">
            <button
                v-if="orderDetail.status === 'pending'"
                class="btn pay-btn"
                @click="handlePayment(orderDetail.order_id)"
            >
              去支付
            </button>
            <button
                v-if="orderDetail.status === 'pending'"
                class="btn cancel-btn"
                @click="cancelOrderFromDetail(orderDetail.order_id)"
            >
              取消订单
            </button>
            <button
                v-if="['shipped', 'completed'].includes(orderDetail.status)"
                class="btn track-btn"
            >
              查看物流
            </button>
            <button
                v-if="orderDetail.status === 'completed'"
                class="btn refund-btn"
                @click="applyRefund(orderDetail.order_id)"
            >
              申请退款
            </button>
            <button
                v-if="orderDetail.status === 'completed'"
                class="btn review-btn"
            >
              评价订单
            </button>
          </div>
        </div>

        <div v-else class="loading-spinner">
          <i class="fa fa-spinner fa-spin"></i>
          <span>加载中...</span>
        </div>
      </div>
    </div>

    <!-- 确认对话框 -->
    <div v-if="showConfirmDialog" class="confirm-dialog-overlay">
      <div class="confirm-dialog">
        <div class="confirm-header">
          <h3>{{ confirmDialogTitle }}</h3>
        </div>
        <div class="confirm-content">
          {{ confirmDialogMessage }}
        </div>
        <div class="confirm-actions">
          <button class="btn cancel-btn" @click="closeConfirmDialog">取消</button>
          <button class="btn confirm-btn" @click="confirmAction">确认</button>
        </div>
      </div>
    </div>
  </div>
  <!-- 支付弹窗 -->
  <PayCard
      :show="showPaymentModal"
      :total-amount="currentOrderAmount"
      :order-id="currentOrderId"
      @close="showPaymentModal = false"
      @payment-success="handlePaymentSuccess"
  />
  <Footer/>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { delOrder, getOrders, getOrderDetail } from "@/api/order.js";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import PayCard from "@/components/PayCard.vue";

export default {
  name: 'OrdersPage',
  components: {FontAwesomeIcon, Header, Footer,PayCard},
  setup() {
    // 状态变量
    const orders = ref([]);
    const currentPage = ref(1);
    const pageSize = ref(4); // 控制每页显示的订单数量
    const totalPages = ref(0);
    const totalOrders = ref(0);
    const currentStatus = ref('');
    const searchQuery = ref('');
    const isLoading = ref(false);

    // 支付弹窗相关
    const showPaymentModal = ref(false);
    const currentOrderId = ref('');
    const currentOrderAmount = ref(0);

    // 订单详情相关
    const showOrderDetail = ref(false);
    const orderDetail = ref(null);

    // 确认对话框相关
    const showConfirmDialog = ref(false);
    const confirmDialogTitle = ref('');
    const confirmDialogMessage = ref('');
    const confirmCallback = ref(null);

    // 状态选项
    const statusOptions = [
      { value: '', label: '全部订单' },
      { value: 'pending', label: '待付款' },
      { value: 'paid', label: '已付款' },
      { value: 'shipped', label: '配送中' },
      { value: 'completed', label: '已完成' }
    ];

    // 订单时间线
    const orderTimeline = [
      {
        status: 'pending',
        title: '待付款',
        icon: 'fa-solid fa-clock' // 替换为 Font Awesome 6 图标
      },
      {
        status: 'paid',
        title: '已付款',
        icon: 'fa-solid fa-circle-check' // 替换为 Font Awesome 6 图标
      },
      {
        status: 'shipped',
        title: '配送中',
        icon: 'fa-solid fa-truck-fast' // 替换为 Font Awesome 6 图标
      },
      {
        status: 'completed',
        title: '已完成',
        icon: 'fa-solid fa-flag-checkered' // 替换为 Font Awesome 6 图标
      }
    ];

    // 计算属性：显示的页码
    const displayedPages = computed(() => {
      const range = [];
      const maxPagesToShow = 5;

      // 根据总页数和当前页计算显示范围
      if (totalPages.value <= maxPagesToShow) {
        // 总页数少于或等于最大显示数，显示所有页码
        for (let i = 1; i <= totalPages.value; i++) {
          range.push(i);
        }
      } else {
        // 总页数大于最大显示数，需要计算显示哪些页码

        // 计算中间的页码范围
        const middlePagesCount = maxPagesToShow - 2; // 减去首尾两页
        const halfMiddleCount = Math.floor(middlePagesCount / 2);

        let startPage = Math.max(2, currentPage.value - halfMiddleCount);
        let endPage = Math.min(totalPages.value - 1, startPage + middlePagesCount - 1);

        // 如果结束页接近尾页，调整起始页
        if (endPage >= totalPages.value - 1) {
          endPage = totalPages.value - 1;
          startPage = Math.max(2, endPage - middlePagesCount + 1);
        }

        // 如果起始页接近首页，调整结束页
        if (startPage <= 2) {
          startPage = 2;
          endPage = Math.min(totalPages.value - 1, startPage + middlePagesCount - 1);
        }

        // 填充页码数组
        for (let i = startPage; i <= endPage; i++) {
          range.push(i);
        }
      }

      return range;
    });

    // 初始化加载数据
    onMounted(() => {
      fetchOrders();
    });

    // 获取订单列表
    const fetchOrders = async () => {
      try {
        isLoading.value = true;
        const response = await getOrders(currentPage.value, pageSize.value,currentStatus.value,searchQuery.value);
        orders.value = response.orders;
        totalPages.value = response.total_pages;
        totalOrders.value = response.total_orders;
      } catch (error) {
        console.error('获取订单列表失败:', error);
        // 这里可以添加错误提示
      } finally {
        isLoading.value = false;
      }
    };

    // 获取订单详情
    const fetchOrderDetail = async (orderId) => {
      try {
        const response = await getOrderDetail(orderId);
        orderDetail.value = response;
      } catch (error) {
        console.error('获取订单详情失败:', error);
        // 这里可以添加错误提示
      }
    };

    // 切换页码
    const changePage = (page) => {
      if (page === currentPage.value) return;
      currentPage.value = page;
      fetchOrders();
    };

    // 根据状态筛选
    const filterByStatus = (status) => {
      currentStatus.value = status;
      currentPage.value = 1;
      fetchOrders();
    };

    // 处理搜索
    const handleSearch = () => {
      // 这里可以添加防抖
      fetchOrders();
    };

    // 查看订单详情
    const viewOrderDetail = (orderId) => {
      fetchOrderDetail(orderId);
      showOrderDetail.value = true;
    };

    // 关闭订单详情
    const closeOrderDetail = () => {
      showOrderDetail.value = false;
      orderDetail.value = null;
    };

    // 处理支付
    const handlePayment = (orderId) => {
      // 查找订单总价
      const order = orders.value.find(o => o.id === orderId);
      if (order) {
        currentOrderId.value = orderId;
        currentOrderAmount.value = order.total_price;
        showPaymentModal.value = true;
      }
    };

    // 处理支付成功
    const handlePaymentSuccess = (paymentInfo) => {
      fetchOrders();
      closeOrderDetail();
    };

    // 取消订单
    const cancelOrder = (orderId) => {
      showConfirmDialog.value = true;
      confirmDialogTitle.value = '取消订单';
      confirmDialogMessage.value = '确定要取消这个订单吗？取消后不可恢复。';

      confirmCallback.value = async () => {
        try {
          await delOrder(orderId);
          // 如果当前页没有订单了且不是第一页，则返回上一页
          if (orders.value.length === 1 && currentPage.value > 1) {
            currentPage.value -= 1;
          }
          // 刷新订单列表
          await fetchOrders();
          closeConfirmDialog();
        } catch (error) {
          console.error('取消订单失败:', error);
        }
      };
    };

    // 从详情页取消订单
    const cancelOrderFromDetail = (orderId) => {
      showConfirmDialog.value = true;
      confirmDialogTitle.value = '取消订单';
      confirmDialogMessage.value = '确定要取消这个订单吗？取消后不可恢复。';
      confirmCallback.value = async () => {
        try {
          await delOrder(orderId);
          // 关闭详情页并刷新订单列表
          closeOrderDetail();
          fetchOrders();
          closeConfirmDialog();
        } catch (error) {
          console.error('取消订单失败:', error);
          // 这里可以添加错误提示
        }
      };
    };

    // 申请退款
    const applyRefund = (orderId) => {
      showConfirmDialog.value = true;
      confirmDialogTitle.value = '申请退款';
      confirmDialogMessage.value = '确定要申请退款吗？';
      confirmCallback.value = () => {
        // 这里添加退款逻辑
        console.log('申请退款:', orderId);
        closeConfirmDialog();
      };
    };

    // 关闭确认对话框
    const closeConfirmDialog = () => {
      showConfirmDialog.value = false;
      confirmDialogTitle.value = '';
      confirmDialogMessage.value = '';
      confirmCallback.value = null;
    };

    // 确认操作
    const confirmAction = () => {
      if (confirmCallback.value) {
        confirmCallback.value();
      }
    };


    // 格式化日期
    const formatDate = (timestamp) => {
      if (!timestamp) return '';
      const date = new Date(timestamp);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    };

    // 格式化价格
    const formatPrice = (price) => {
      return `¥${parseFloat(price).toFixed(2)}`;
    };

    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待付款',
        'paid': '已付款',
        'shipped': '配送中',
        'completed': '已完成'
      };
      return statusMap[status] || status;
    };

    // 获取状态类名
    const getStatusClass = (status) => {
      return `status-${status}`;
    };

    // 判断步骤是否完成
    const isStepCompleted = (stepStatus) => {
      const statusOrder = ['pending', 'paid', 'shipped', 'completed'];
      const currentStatusIndex = statusOrder.indexOf(orderDetail.value?.status);
      const stepStatusIndex = statusOrder.indexOf(stepStatus);

      return currentStatusIndex >= stepStatusIndex;
    };

    return {
      orders,
      currentPage,
      pageSize,
      totalPages,
      totalOrders,
      currentStatus,
      searchQuery,
      isLoading,
      showOrderDetail,
      orderDetail,
      showConfirmDialog,
      confirmDialogTitle,
      confirmDialogMessage,
      statusOptions,
      orderTimeline,
      displayedPages,
      fetchOrders,
      fetchOrderDetail,
      changePage,
      filterByStatus,
      handleSearch,
      viewOrderDetail,
      closeOrderDetail,
      handlePayment,
      cancelOrder,
      cancelOrderFromDetail,
      applyRefund,
      closeConfirmDialog,
      confirmAction,
      formatDate,
      formatPrice,
      getStatusText,
      getStatusClass,
      isStepCompleted,
      showPaymentModal,
      currentOrderId,
      currentOrderAmount,
      handlePaymentSuccess,
    };
  }
};
</script>

<style scoped>
.orders-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Microsoft YaHei', sans-serif;
}

.page-title {
  color: #333;
  font-size: 28px;
  margin-bottom: 24px;
  text-align: center;
}

/* 筛选区域样式 */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.status-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.status-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 20px;
  background-color: #f5f5f5;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.status-btn:hover {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-btn.active {
  background-color: #4caf50;
  color: white;
}

.search-section {
  flex-grow: 1;
  max-width: 300px;
}

.search-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #4caf50;
}

/* 订单列表样式 */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.order-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.order-id {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.order-date {
  font-size: 13px;
  color: #999;
}

.order-status {
  font-size: 14px;
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: 500;
}

.status-pending {
  background-color: #fff3e0;
  color: #ff9800;
}

.status-paid {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-shipped {
  background-color: #e3f2fd;
  color: #2196f3;
}

.status-completed {
  background-color: #f5f5f5;
  color: #757575;
}

.order-brief {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.order-brief > div {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.order-brief i {
  color: #4caf50;
}

.order-price {
  font-weight: 600;
  color: #f44336 !important;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-btn {
  background-color: #f5f5f5;
  color: #666;
}

.view-btn:hover {
  background-color: #e0e0e0;
}

.pay-btn {
  background-color: #ff9800;
  color: white;
}

.pay-btn:hover {
  background-color: #f57c00;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #f44336;
}

.cancel-btn:hover {
  background-color: #ffebee;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 20px;
  text-align: center;
}

.empty-img {
  width: 120px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.empty-state p {
  color: #999;
  margin-bottom: 20px;
  font-size: 16px;
}

.shop-btn {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
}

.shop-btn:hover {
  background-color: #43a047;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  margin-top: 20px;
}

.page-btn {
  width: 36px;
  height: 36px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn:not(:disabled):hover {
  background-color: #f5f5f5;
  border-color: #4caf50;
  color: #4caf50;
}

.page-num {
  min-width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.page-num.active {
  background-color: #4caf50;
  color: white;
}

.page-num:not(.active):hover {
  background-color: #f5f5f5;
  color: #4caf50;
}

.page-ellipsis {
  padding: 0 5px;
  color: #999;
}

/* 订单详情对话框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* container整体*/

.modal-container {
  background-color: white;
  border-radius: 10px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  scroll-behavior: smooth;
  scrollbar-width: thin;
}

.modal-container::-webkit-scrollbar {
  width: 6px;
}

.modal-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/*上面是整体*/

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 10;
}

.modal-header h2 {
  font-size: 20px;
  color: #333;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #f44336;
}

.modal-content {
  padding: 20px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.detail-id {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.detail-info {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  margin-bottom: 10px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  width: 80px;
  color: #999;
  flex-shrink: 0;
}

.info-value {
  flex-grow: 1;
  color: #333;
}

.info-value.price {
  color: #f44336;
  font-weight: 600;
}

.items-list {
  margin-bottom: 25px;
}

.items-list h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.item-card {
  display: flex;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
}

.item-img {
  width: 80px;
  height: 80px;
  border-radius: 5px;
  overflow: hidden;
  margin-right: 15px;
  flex-shrink: 0;
}

.item-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-details {
  flex-grow: 1;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.item-desc {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-price {
  font-size: 15px;
  color: #f44336;
  font-weight: 600;
}

.order-timeline {
  margin-bottom: 25px;
}

.order-timeline h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.timeline {
  display: flex;
  justify-content: space-between;
  position: relative;
  padding: 0 10px;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 25px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #ddd;
  z-index: 1;
}

.timeline-step {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  width: 25%;
}

.step-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: white;
  border: 2px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  transition: all 0.3s;
}

.step-icon i {
  font-size: 20px;
  color: #ddd;
  transition: all 0.3s;
}

.timeline-step.completed .step-icon {
  border-color: #4caf50;
  background-color: #e8f5e9;
}

.timeline-step.completed .step-icon i {
  color: #4caf50;
}

.step-content {
  text-align: center;
  width: 100%;
}

.step-title {
  font-size: 13px;
  color: #666;
  margin-bottom: 5px;
}

.step-time {
  font-size: 12px;
  color: #999;
}

.detail-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 30px;
  flex-wrap: wrap;
}

.track-btn {
  background-color: #2196f3;
  color: white;
}

.track-btn:hover {
  background-color: #1976d2;
}

.refund-btn {
  background-color: #f5f5f5;
  color: #ff9800;
}

.refund-btn:hover {
  background-color: #fff3e0;
}

.review-btn {
  background-color: #4caf50;
  color: white;
}

.review-btn:hover {
  background-color: #43a047;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
  color: #666;
}

.loading-spinner i {
  font-size: 40px;
  color: #4caf50;
  margin-bottom: 15px;
}

/* 确认对话框样式 */
.confirm-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
}

.confirm-dialog {
  background-color: white;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.confirm-header {
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.confirm-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.confirm-content {
  padding: 20px;
  color: #666;
  font-size: 15px;
}

.confirm-actions {
  display: flex;
  border-top: 1px solid #f0f0f0;
}

.confirm-actions button {
  flex: 1;
  padding: 12px;
  border: none;
  background: none;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.confirm-actions .cancel-btn {
  border-right: 1px solid #f0f0f0;
  color: #666;
}

.confirm-actions .cancel-btn:hover {
  background-color: #f5f5f5;
}

.confirm-actions .confirm-btn {
  color: #f44336;
  font-weight: 500;
}

.confirm-actions .confirm-btn:hover {
  background-color: #ffebee;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .order-brief {
    grid-template-columns: 1fr 1fr;
  }

  .filter-section {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-section {
    width: 100%;
    max-width: none;
    margin-top: 10px;
  }

  .timeline {
    flex-wrap: wrap;
  }

  .timeline-step {
    width: 50%;
    margin-bottom: 20px;
  }

  .timeline::before {
    display: none;
  }
}

@media (max-width: 480px) {
  .order-brief {
    grid-template-columns: 1fr;
  }

  .order-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .order-actions button {
    margin-bottom: 8px;
  }

  .timeline-step {
    width: 100%;
  }
}
/*新加*/
.item-price-info {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}

.unit-price, .quantity {
  font-size: 14px;
  color: #666;
}

.total-item-price {
  font-size: 15px;
  color: #f44336;
  font-weight: 600;
}

@media (max-width: 480px) {
  .item-price-info {
    flex-direction: column;
    gap: 5px;
  }
}

.item-card {
  display: flex;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}


</style>