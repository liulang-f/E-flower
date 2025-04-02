<template>
  <div class="user-management-container">
    <!-- 顶部标题和搜索栏 -->
    <div class="header">
      <h2><i class="el-icon-user-solid"></i> 用户管理</h2>
      <div class="search-bar">
        <el-input
            v-model="searchQuery"
            placeholder="搜索用户名或手机号"
            clearable
            @clear="handleSearch"
            @keyup.enter.native="handleSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
      </div>
    </div>

    <!-- 用户表格 -->
    <el-table
        :data="users"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
        :fit="true"
    >
      <!-- 用户头像列 -->
      <el-table-column label="头像" width="100" align="center">
        <template #default="{ row }">
          <el-avatar
              :size="50"
              :src="`/api/img/avatar/${row.username}`"
          />
        </template>
      </el-table-column>

      <!-- 用户名 -->
      <el-table-column prop="username" label="用户名" width="120"/>

      <!-- 手机号 -->
      <el-table-column prop="phone" label="手机号" width="150" />

      <!-- VIP等级 -->
      <el-table-column label="VIP等级" width="150" align="center">
        <template #default="{ row }">
          <el-tag :type="getVipTagType(row.vip)">
            {{ getVipText(row.vip) }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- 总消费 -->
      <el-table-column prop="sales" label="总消费(元)" width="120" sortable :sort-by="row => parseFloat(row.consumption)">
        <template #default="{ row }">
          {{ row.consumption.toFixed(2) }}
        </template>
      </el-table-column>

      <!-- 创建时间 -->
      <el-table-column prop="created_at" label="注册时间" width="200" sortable>
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>

      <!-- 用户角色 -->
      <el-table-column prop="role" label="角色" width="150" align="center">
        <template #default="{ row }">
          <el-tag :type="row.role === 'admin' ? 'danger' : 'success'">
            {{ row.role === 'admin' ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- 操作列 -->
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button
              size="small"
              type="primary"
              @click="showUserDetail(row)"
              :icon="View"
          >详情</el-button
          >
          <el-button
              size="small"
              type="warning"
              @click="handleResetPassword(row.id)"
              :icon="Refresh"
          >重置密码</el-button
          >
          <el-button
              size="small"
              type="danger"
              @click="handleDeleteUser(row.id)"
              :icon="Delete"
          >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页控件 -->
    <div class="pagination">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalUsers"
      />
    </div>

    <!-- 用户详情弹窗 -->
    <el-dialog
        v-model="detailDialogVisible"
        title="用户详情"
        width="70%"
        top="5vh"
    >
      <el-tabs v-model="activeTab">
        <!-- 基本信息标签页 -->
        <el-tab-pane label="基本信息" name="basic">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="用户名">
              {{ currentUser.username }}
            </el-descriptions-item>
            <el-descriptions-item label="手机号">
              {{ currentUser.phone }}
            </el-descriptions-item>
            <el-descriptions-item label="VIP等级">
              <el-tag :type="getVipTagType(currentUser.vip)">
                {{ getVipText(currentUser.vip) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="总消费">
              ¥{{ currentUser.consumption.toFixed(2) }}
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
              {{ formatDate(currentUser.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="头像">
              <el-avatar
                  :size="100"
                  :src="`/api/img/avatar/${currentUser.username}`"
              />
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>

        <!-- 订单记录标签页 -->
        <el-tab-pane label="订单记录" name="orders">
          <el-table
              :data="currentUser.orders"
              border
              style="width: 100%"
              max-height="500"
              v-loading="ordersLoading"
          >
            <el-table-column prop="id" label="订单号" width="180" />
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getOrderStatusTagType(row.status)">
                  {{ getOrderStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="总价" width="120">
              <template #default="{ row }">
                ¥{{ row.total_price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="下单时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                    size="small"
                    type="primary"
                    @click="viewOrderDetails(row)"
                >详情</el-button
                >
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
              small
              layout="prev, pager, next"
              :total="totalOrders"
              :page-size="ordersPageSize"
              :current-page="ordersCurrentPage"
              @current-change="handleOrdersPageChange"
              style="margin-top: 15px;"
          />
        </el-tab-pane>

        <!-- 地址信息标签页 -->
        <el-tab-pane label="地址信息" name="addresses">
          <el-table :data="currentUser.addresses" border style="width: 100%">
            <el-table-column prop="address" label="地址详情" />
            <el-table-column label="是否默认" width="120" align="center">
              <template #default="{ row }">
                <el-tag v-if="row.is_default" type="success">默认地址</el-tag>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" align="center">
              <template #default="{ row }">
                <el-button
                    size="small"
                    type="primary"
                    plain
                    v-if="!row.is_default"
                    @click="setDefaultAddress(row.id)"
                >设为默认</el-button
                >
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>

      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关 闭</el-button>
      </span>
    </el-dialog>

    <!-- 订单详情弹窗 -->
    <AdminOrderDetailDialog
        v-model="orderDetailVisible"
        :order-id="selectedOrderId"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {getUserList} from "@/api/auth.js";
import {Delete, Refresh, Search, View,} from '@element-plus/icons-vue'
import {changeUserAddr, delUser, GetUserInf, getUserOrders, reSetPwd} from "@/api/admin.js";
import AdminOrderDetailDialog from "@/components/AdminComp/AdminOrderDetailDialog.vue";

export default {
  name: 'UserManagement',
  components: {
    AdminOrderDetailDialog
  },
  computed: {
    Delete() {
      return Delete
    },
    Refresh() {
      return Refresh
    },
    View() {
      return View
    },
    Search() {
      return Search
    }
  },
  setup() {
    const users = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const totalUsers = ref(0)
    const detailDialogVisible = ref(false)
    const currentUser = ref({})
    const activeTab = ref('basic')
    const orderDetailVisible = ref(false)
    const selectedOrderId = ref('')
    const ordersLoading = ref(false)
    const ordersCurrentPage = ref(1)
    const ordersPageSize = ref(10)
    const totalOrders = ref(0)

    const setDefaultAddress = async (id)=>{
      await changeUserAddr(currentUser.value.id, id)
      await fetchUsers()
    }

    // 获取用户列表
    const fetchUsers = async () => {
      try {
        const params = ({
          page: currentPage.value,
          pageSize: pageSize.value,
          search: searchQuery.value
        })
        const resp = await getUserList(params)
        users.value = resp.users
        totalUsers.value = resp.total
        loading.value = false

      } catch (error) {
        ElMessage.error('获取用户列表失败')
      }
    }

    // 获取用户订单
    const fetchUserOrders = async (userId) => {
      try {
        ordersLoading.value = true
        const params = {
          page: ordersCurrentPage.value,
          pageSize: ordersPageSize.value,
          userId:userId
        }
        const resp = await getUserOrders(params)
        currentUser.value.orders = resp.orders
        totalOrders.value = resp.total
      } catch (error) {
        ElMessage.error('获取用户订单失败')
      } finally {
        ordersLoading.value = false
      }
    }

    // 搜索用户
    const handleSearch = () => {
      currentPage.value = 1
      fetchUsers()
    }

    // 重置密码
    const handleResetPassword = async (userId) => {
      await ElMessageBox.confirm('确定要重置该用户的密码为"12345678"吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })

      await reSetPwd(userId)
    }

    // 删除用户
    const handleDeleteUser = async (userId) => {
      try {
        await ElMessageBox.confirm('确定要删除该用户吗?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'error'
        })
        await delUser(userId)
        await fetchUsers()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除用户失败')
        }
      }
    }

    // 显示用户详情
    const showUserDetail = async (user) => {
      try {
        currentUser.value = await GetUserInf(user.id)
        detailDialogVisible.value = true
        // 默认加载第一页订单
        await fetchUserOrders(user.id)
      } catch (error) {
        ElMessage.error('获取用户详情失败')
      }
    }

    // 查看订单详情
    const viewOrderDetails = (order) => {
      selectedOrderId.value = order.id
      orderDetailVisible.value = true
    }

    // 订单分页处理
    const handleOrdersPageChange = async (page) => {
      ordersCurrentPage.value = page
      await fetchUserOrders(currentUser.value.id)
    }

    // 切换标签页
    const handleTabChange = (tab) => {
      if (tab === 'orders' && currentUser.value.id && (!currentUser.value.orders || currentUser.value.orders.length === 0)) {
        fetchUserOrders(currentUser.value.id)
      }
    }

    // 分页处理
    const handleSizeChange = async (val) => {
      pageSize.value = val
      await fetchUsers()
    }

    const handleCurrentChange = async (val) => {
      currentPage.value = val
      await fetchUsers()
    }

    // 辅助函数
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const getVipTagType = (vipLevel) => {
      const types = ['primary', 'success', 'warning', 'danger']
      return types[vipLevel] || ''
    }

    const getVipText = (vipLevel) => {
      const texts = ['普通会员', '白银会员', '黄金会员', '钻石会员']
      return texts[vipLevel] || '普通会员'
    }

    const getOrderStatusTagType = (status) => {
      const map = {
        pending: 'info',
        paid: 'primary',
        shipped: 'warning',
        completed: 'success',
        cancelled: 'danger'
      }
      return map[status] || ''
    }

    const getOrderStatusText = (status) => {
      const map = {
        pending: '待支付',
        paid: '已支付',
        shipped: '已发货',
        completed: '已完成',
        cancelled: '已取消'
      }
      return map[status] || status
    }

    onMounted(async () => {
      try {
        await fetchUsers();
      } catch (error) {
        console.error('Error in fetchUsers:', error);
        ElMessage.error('获取用户列表失败');
      }
    });

    return {
      users,
      loading,
      searchQuery,
      currentPage,
      pageSize,
      totalUsers,
      detailDialogVisible,
      currentUser,
      activeTab,
      orderDetailVisible,
      selectedOrderId,
      ordersLoading,
      ordersCurrentPage,
      ordersPageSize,
      totalOrders,
      handleSearch,
      handleResetPassword,
      handleDeleteUser,
      showUserDetail,
      viewOrderDetails,
      handleSizeChange,
      handleCurrentChange,
      handleOrdersPageChange,
      handleTabChange,
      formatDate,
      getVipTagType,
      getVipText,
      getOrderStatusTagType,
      getOrderStatusText,
      setDefaultAddress,
    }
  }
}
</script>

<style scoped>
.user-management-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  width: 300px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-avatar {
  background-color: #f5f7fa;
}

.el-tag {
  margin-right: 5px;
}

.el-descriptions {
  margin-top: 20px;
}

.el-tabs {
  margin-top: -20px;
}

.order-detail {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 10px;
}

.order-summary-row {
  margin-top: 20px;
  text-align: right;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.price-item {
  margin-bottom: 8px;
}

.price-item.total {
  font-weight: bold;
  font-size: 1.1em;
}

.price-label {
  display: inline-block;
  width: 120px;
  text-align: right;
  margin-right: 15px;
}

.price-value {
  display: inline-block;
  width: 100px;
  text-align: right;
}

.flower-info {
  display: flex;
  align-items: center;
}

.text-muted {
  color: #999;
  font-size: 0.8em;
}

.image-error {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  color: #ccc;
}
</style>