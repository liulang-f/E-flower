<template>
  <el-dialog
      v-model="visible"
      :title="`订单详情 - #${orderData.id || ''}`"
      width="70%"
      top="5vh"
      @open="loadOrderDetail"
  >
    <div v-if="orderData.id" class="order-detail">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusTagType(orderData.status)">
            {{ getStatusText(orderData.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="下单时间">
          {{ formatDateTime(orderData.createdAt) }}
        </el-descriptions-item>
        <el-descriptions-item label="用户姓名">
          {{ orderData.username }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ orderData.phone }}
        </el-descriptions-item>
        <el-descriptions-item label="配送地址">
          {{ orderData.address }}
        </el-descriptions-item>
        <el-descriptions-item label="订单备注">
          <el-input
              v-model="orderData.remark"
              type="textarea"
              :rows="2"
              placeholder="暂无备注"
              :disabled="true"
          />
        </el-descriptions-item>
      </el-descriptions>

      <el-divider/>

      <h4>商品清单</h4>
      <el-table
          :data="orderData.items"
          border
          style="width: 100%"
          max-height="200"
      >
        <el-table-column label="商品" width="250">
          <template #default="{row}">
            <div class="flower-info">
              <el-image
                  :src="`api/img/${row.flower_name}`"
                  fit="cover"
                  style="width: 60px; height: 60px; margin-right: 10px;"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><el-icon-picture /></el-icon>
                  </div>
                </template>
              </el-image>

              <div>
                <div>{{ row.flower_name }}</div>
                <div class="text-muted">{{ row.flower_description }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="originalPrice" label="原价" width="180">
          <template #default="{row}">
            ¥{{ row.flower_original_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="price" label="成交价" width="180">
          <template #default="{row}">
            ¥{{ row.flower_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="数量" width="180">
          <template #default="{row}">
            {{ row.flower_quantity.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="小计" width="180">
          <template #default="{row}">
            ¥{{ (row.flower_price * row.flower_quantity).toFixed(2) }}
          </template>
        </el-table-column>
      </el-table>

      <div class="order-summary-row">
        <div class="price-item">
          <span class="price-label">商品总价:</span>
          <span class="price-value">¥{{ calculateSubtotal().toFixed(2) }}</span>
        </div>
        <div class="price-item">
          <span class="price-label">运费:</span>
          <span class="price-value">¥10.00</span>
        </div>
        <div class="price-item total">
          <span class="price-label">实付金额:</span>
          <span class="price-value">¥{{ (calculateSubtotal() + 10).toFixed(2) }}</span>
        </div>
      </div>
    </div>

    <div v-else class="loading-detail">
      <el-skeleton :rows="5" animated />
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button
            type="success"
            :disabled="orderData.status !== 'paid'"
            @click="$emit('ship-order', orderData)"
        >
          <font-awesome-icon icon="truck" class="mr-1"/>
          接单发货
        </el-button>
        <el-button
            type="danger"
            :disabled="orderData.status!=='paid'"
            @click="$emit('cancel-order', orderData)"
        >
          <font-awesome-icon icon="times" class="mr-1"/>
          取消订单
        </el-button>
        <el-button @click="visible = false">
          关闭
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture as ElIconPicture } from '@element-plus/icons-vue'
import { getOrderDetail } from "@/api/order.js"

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  orderId: {
    type: [String, Number], // 允许 orderId 为字符串或数字
    default: ''
  }
});

const emit = defineEmits([
  'update:modelValue',
  'ship-order',
  'cancel-order'
])

const visible = ref(false)
const loadingDetail = ref(false)
const orderData = ref({
  id: '',
  username: '',
  phone: '',
  totalPrice: 0,
  status: '',
  createdAt: '',
  address: '',
  remark: '',
  items: []
})

// 同步外部 modelValue 变化
watch(() => props.modelValue, (val) => {
  visible.value = val
})

// 同步内部 visible 变化到外部
watch(visible, (val) => {
  emit('update:modelValue', val)
})

// 加载订单详情
const loadOrderDetail = async () => {
  if (!props.orderId) return

  try {
    loadingDetail.value = true
    const orderDetail = await getOrderDetail(props.orderId)
    orderData.value = {
      id: orderDetail.order_id,
      username: orderDetail.username,
      phone: orderDetail.phone,
      totalPrice: orderDetail.total_price,
      status: orderDetail.status,
      createdAt: orderDetail.created_at,
      address: orderDetail.address,
      remark: orderDetail.remark,
      items: orderDetail.items
    }
  } catch (error) {
    ElMessage.error('获取订单详情失败')
  } finally {
    loadingDetail.value = false
  }
}

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

const calculateSubtotal = () => {
  if (!orderData.value?.items) return 0
  return orderData.value.items.reduce(
      (sum, item) => sum + (item.flower_price * item.flower_quantity),
      0
  )
}
</script>

<style scoped>
.order-detail {
  padding: 0 10px;
}

/* 商品清单表格优化 */
.order-detail .el-table {
  margin: 20px 0;
}

.flower-info {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.flower-info .el-image {
  width: 80px;
  height: 80px;
  margin-right: 15px;
  border-radius: 4px;
  border: 1px solid #eee;
}

.flower-info > div {
  flex: 1;
}

.flower-info div:first-child {
  font-weight: 500;
  margin-bottom: 5px;
}

.text-muted {
  color: #909399;
  font-size: 12px;
}

.image-error {
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
}

.image-error .el-icon {
  font-size: 24px;
}

/* 操作按钮区域优化 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding: 15px 0 0;
  border-top: 1px solid #ebeef5;
}

.mr-1 {
  margin-right: 5px;
}

/* 描述列表优化 */
.el-descriptions {
  margin-bottom: 20px;
}

.el-descriptions-item__label {
  width: 100px;
}

/* 价格汇总区块优化 */
.order-summary-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.price-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.price-item.total {
  padding-left: 20px;
  border-left: 1px solid #dcdfe6;
}

.price-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 4px;
}

.price-value {
  font-size: 16px;
  font-weight: 500;
  color: #606266;
}

.price-item.total .price-value {
  font-size: 18px;
  font-weight: 600;
  color: #409EFF;
}

/* 加载状态优化 */
.loading-detail {
  padding: 20px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .order-summary-row {
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
  }

  .price-item {
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }

  .price-item.total {
    padding-left: 0;
    border-left: none;
    padding-top: 10px;
    border-top: 1px dashed #dcdfe6;
    margin-top: 5px;
  }
}
</style>