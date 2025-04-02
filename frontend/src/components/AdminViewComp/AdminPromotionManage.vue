<template>
  <div class="promotion-management">
    <div class="header">
      <h2>活动管理</h2>
      <el-button type="primary" @click="handleAdd">新增活动</el-button>
    </div>

    <!-- 活动列表表格 -->
    <el-table
        :data="promotions"
        border
        style="width: 100%"
        v-loading="loading"
        :row-style="{height: '60px'}"
    >
      <el-table-column prop="title" label="活动标题" width="100"></el-table-column>
      <el-table-column label="折扣率" width="100">
        <template #default="{row}">
          {{ (row.discount * 10) + '折' }}
        </template>
      </el-table-column>

      <el-table-column prop="description" label="活动介绍" width="150"></el-table-column>

      <el-table-column prop="start_time" label="开始时间" width="180">
        <template #default="{row}">
          {{ row.start_time }}
        </template>
      </el-table-column>
      <el-table-column prop="end_time" label="结束时间" width="180">
        <template #default="{row}">
          {{ row.end_time }}
        </template>
      </el-table-column>
      <el-table-column label="标签" width="150">
        <template #default="{row}">
          <el-tag v-for="tag in row.tags" :key="tag" style="margin-right: 5px;">
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="关联花卉" width="200">
        <template #default="{row}">
          <div class="flower-list">
            <template v-if="flowerMap[row.id] && flowerMap[row.id].length > 0">
              <el-popover placement="right" trigger="hover" width="300">
                <template #reference>
                  <el-button type="text">查看关联花卉({{ flowerMap[row.id].length }})</el-button>
                </template>
                <div class="popover-flower-list">
                  <div v-for="flower in flowerMap[row.id]" :key="flower.flower_id" class="flower-item">
                    <img :src="`api/img/${flower.flower_name}`" :alt="flower.flower_name" class="flower-image">
                    <span>{{ flower.flower_name }}</span>
                  </div>
                </div>
              </el-popover>
            </template>
            <span v-else>暂无关联花卉</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{row}">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div class="pagination">
      <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          :page-sizes="[10, 20, 50, 100]"
          @size-change="loadPromotions"
          @current-change="loadPromotions"
      />
    </div>

    <!-- 新增/编辑活动对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="50%">
      <el-form :model="currentPromotion" label-width="100px" ref="promotionForm">
        <el-form-item label="活动标题" prop="title" required>
          <el-input v-model="currentPromotion.title" maxlength="10" show-word-limit></el-input>
        </el-form-item>
        <el-form-item label="折扣率" prop="discount" required>
          <el-input-number
              v-model="currentPromotion.discount"
              :min="0.1"
              :max="0.9"
              :step="0.1"
              controls-position="right"
          ></el-input-number>
          <span class="discount-text">{{ (currentPromotion.discount * 10) + '折' }}</span>
        </el-form-item>
        <el-form-item label="活动时间" prop="timeRange">
          <el-date-picker
              v-model="timeRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              value-format="YYYY-MM-DD HH:mm:ss"
              @change="handleTimeRangeChange"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="活动标签" prop="tags">
          <div class="tag-management">
            <el-select
                v-model="selectedTag"
                filterable
                allow-create
                placeholder="选择或创建标签"
                @change="handleTagChange"
            >
              <el-option
                  v-for="tag in allTags"
                  :key="tag"
                  :label="tag"
                  :value="tag"
              ></el-option>
            </el-select>
            <div class="selected-tags">
              <el-tag
                  v-for="tag in currentTags"
                  :key="tag"
                  closable
                  @close="removeTag(tag)"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="活动描述" prop="description">
          <el-input
              v-model="currentPromotion.description"
              type="textarea"
              :rows="3"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  adminAllPromotions, allProTags, flowersPro,
  adminAddPro, adminUpdatePro, adminDelPro,
} from "@/api/admin.js";

export default {
  name: 'PromotionManagement',
  setup() {
    // 活动数据
    const promotions = ref([])
    const flowerMap = ref({})

    // 分页相关
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)

    // 所有标签
    const allTags = ref([])

    // 加载状态
    const loading = ref(false)

    // 对话框相关
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增活动')
    const currentPromotion = ref({
      id: null,
      title: '',
      discount: 0.7,
      start_time: '',
      end_time: '',
      tags: [],
      description: ''
    })
    const timeRange = ref([])
    const currentTags = ref([])
    const selectedTag = ref('')
    const promotionForm = ref(null)

    const handleTimeRangeChange = (val) => {
      if (val && val.length === 2) {
        timeRange.value = val;
      } else {
        timeRange.value = [];
      }
    };

    // 加载活动数据
    const loadPromotions = async () => {
      loading.value = true
      try {
        const response = await adminAllPromotions({
          page: currentPage.value,
          size: pageSize.value
        })

        promotions.value = response.promotions || []
        total.value = response.total || 0

        // 加载关联花卉
        await loadFlowersForPromotions()
      } catch (error) {
        ElMessage.error('加载活动数据失败: ' + (error.message || error))
        console.error('加载活动数据失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 为所有活动加载关联花卉
    const loadFlowersForPromotions = async () => {
      const newFlowerMap = {}

      await Promise.all(promotions.value.map(async promotion => {
        try {
          const flowers = await flowersPro(promotion.id)
          newFlowerMap[promotion.id] = flowers || []
        } catch (error) {
          console.error(`加载活动 ${promotion.id} 的花卉失败`, error)
          newFlowerMap[promotion.id] = []
        }
      }))

      flowerMap.value = newFlowerMap
    }

    // 处理标签变化
    const handleTagChange = (tag) => {
      if (tag && !currentTags.value.includes(tag)) {
        currentTags.value.push(tag)
        if (!allTags.value.includes(tag)) {
          allTags.value.push(tag)
        }
      }
      selectedTag.value = ''
    }

    // 移除标签
    const removeTag = (tag) => {
      currentTags.value = currentTags.value.filter(t => t !== tag)
    }

    // 打开新增对话框
    const handleAdd = () => {
      dialogTitle.value = '新增活动'
      currentPromotion.value = {
        id: null,
        title: '',
        discount: 0.7,
        start_time: '',
        end_time: '',
        tags: [],
        description: ''
      }
      timeRange.value = []
      currentTags.value = []
      dialogVisible.value = true

      nextTick(() => {
        promotionForm.value?.resetFields()
      })
    }

    // 打开编辑对话框
    const handleEdit = (promotion) => {
      dialogTitle.value = '编辑活动'
      currentPromotion.value = {
        ...promotion,
        tags: promotion.tags ? promotion.tags : []
      }
      timeRange.value = [promotion.start_time, promotion.end_time]
      currentTags.value = [...currentPromotion.value.tags]
      dialogVisible.value = true
    }

    // 删除活动
    const handleDelete = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除此活动吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        await adminDelPro(id)
        await loadPromotions()
      } catch (error) {
        if (error !== 'cancel') {

        }
      }
    }

    // 验证时间范围
    const validateTimeRange = () => {
      if (!timeRange.value || timeRange.value.length !== 2) {
        ElMessage.warning('请选择完整的时间范围');
        return false;
      }

      const [start, end] = timeRange.value;

      // 确保时间字符串有效
      if (!start || !end) {
        ElMessage.warning('时间格式不正确');
        return false;
      }

      // 验证时间顺序
      if (new Date(start) >= new Date(end)) {
        ElMessage.warning('结束时间必须晚于开始时间');
        return false;
      }

      return true;
    };


    // 提交表单
    const submitForm = async () => {
      try {
        // 验证表单
        await promotionForm.value.validate();

        // 验证标签
        if (currentTags.value.length === 0) {
          ElMessage.warning('请至少添加一个标签');
          return;
        }

        // 验证时间范围
        if (!validateTimeRange()) {
          return;
        }

        // 准备提交数据
        const formData = {
          ...currentPromotion.value,
          start_time: timeRange.value[0],
          end_time: timeRange.value[1],
          tags: currentTags.value.join(',')
        };

        if (formData.id) {
          // 更新活动
          await adminUpdatePro(formData);
        } else {
          // 新增活动
          await adminAddPro(formData);
        }

        // 重新加载数据
        await loadPromotions();
        dialogVisible.value = false;
      } catch (error) {
        if (error.name !== 'Cancel') {
          ElMessage.error(`操作失败: ${error.message || '未知错误'}`);
        }
      }
    };

    // 初始化加载数据
    onMounted(async () => {
      try {
        await Promise.all([
          loadPromotions(),
          (async () => {
            try {
              allTags.value = await allProTags()
            } catch (error) {
              console.error('加载标签失败:', error)
              allTags.value = []
            }
          })()
        ])
      } catch (error) {
        console.error('初始化失败:', error)
      }
    })

    return {
      promotions,
      flowerMap,
      allTags,
      loading,
      dialogVisible,
      dialogTitle,
      currentPromotion,
      timeRange,
      currentTags,
      selectedTag,
      promotionForm,
      currentPage,
      pageSize,
      total,
      handleTagChange,
      removeTag,
      handleAdd,
      handleEdit,
      handleDelete,
      submitForm,
      loadPromotions,
      handleTimeRangeChange,
    }
  }
}
</script>

<style scoped>
.promotion-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.flower-list {
  display: flex;
  align-items: center;
}

.popover-flower-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.flower-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80px;
}

.flower-image {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.tag-management {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.discount-text {
  margin-left: 10px;
  color: #f56c6c;
  font-weight: bold;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>