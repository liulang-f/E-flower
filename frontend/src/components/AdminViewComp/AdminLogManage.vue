<template>
  <div class="log-management">
    <h2>系统日志管理</h2>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="操作人员">
          <el-input
              v-model="filterForm.username"
              placeholder="请输入用户名"
              clearable
          />
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select
              v-model="filterForm.operation"
              placeholder="请选择操作类型"
              clearable
              style="width: 200px"
          >
            <el-option label="新增" value="add" />
            <el-option label="删除" value="delete" />
            <el-option label="修改" value="update" />
            <el-option label="查询" value="query" />
            <el-option label="系统自动" value="system" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 日志表格 -->
    <div class="log-table">
      <el-table
          :data="logData"
          border
          style="width: 100%"
          v-loading="loading"
      >
        <el-table-column prop="username" label="操作人员" width="120" />
        <el-table-column prop="operation" label="操作类型" width="120">
          <template #default="{row}">
            <el-tag :type="getOperationType(row.operation)">
              {{ formatOperation(row.operation) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="操作详情" />
        <el-table-column prop="operation_time" label="操作时间" width="180" sortable>
          <template #default="{row}">
            {{ formatTime(row.operation_time) }}
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          :total="total"
          :current-page="currentPage"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import {getLogs} from "@/api/admin.js";
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const logData = ref([])
    const loading = ref(false)
    const total = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(10)

    const filterForm = ref({
      username: '',
      operation: ''
    })

    // 获取日志数据
    const fetchLogs = async () => {
      try {
        loading.value = true
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          username: filterForm.value.username,
          operation: filterForm.value.operation
        }

        const response = await getLogs(params)
        logData.value = response.items
        total.value = response.total
      } catch (error) {
        ElMessage.error('获取日志失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 筛选处理
    const handleFilter = () => {
      currentPage.value = 1
      fetchLogs()
    }

    // 重置筛选
    const resetFilter = () => {
      filterForm.value = {
        username: '',
        operation: ''
      }
      handleFilter()
    }

    // 分页大小变化
    const handleSizeChange = (val) => {
      pageSize.value = val
      fetchLogs()
    }

    // 当前页变化
    const handleCurrentChange = (val) => {
      currentPage.value = val
      fetchLogs()
    }

    // 格式化操作类型
    const formatOperation = (operation) => {
      const map = {
        'add': '新增',
        'delete': '删除',
        'update': '修改',
        'query': '查询',
        'system': '系统自动'
      }
      return map[operation] || operation
    }

    // 获取操作类型对应的标签样式
    const getOperationType = (operation) => {
      const map = {
        'add': 'success',
        'delete': 'danger',
        'update': 'warning',
        'query': 'info',
        'system': ''
      }
      return map[operation] || ''
    }

    // 格式化时间
    const formatTime = (time) => {
      return new Date(time).toLocaleString()
    }

    onMounted(() => {
      fetchLogs()
    })

    return {
      logData,
      loading,
      total,
      currentPage,
      pageSize,
      filterForm,
      handleFilter,
      resetFilter,
      handleSizeChange,
      handleCurrentChange,
      formatOperation,
      getOperationType,
      formatTime
    }
  }
}
</script>

<style scoped>
.log-management {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

.filter-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.log-table {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.el-tag {
  margin-right: 5px;
}
</style>