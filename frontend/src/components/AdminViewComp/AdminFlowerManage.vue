<template>
  <div class="flower-management-container">
    <div class="header">
      <h2>花卉商品管理</h2>
      <el-button type="primary" @click="handleAddFlower">
        <el-icon><Plus /></el-icon> 添加花卉
      </el-button>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="filter-container">
      <el-input
          v-model="searchQuery"
          placeholder="搜索花卉名称或描述"
          class="search-input"
          clearable
          @clear="handleSearchClear"
          @keyup.enter="fetchFlowersN"
      >
        <template #append>
          <el-button :icon="Search" @click="fetchFlowersN" />
        </template>
      </el-input>

      <el-select
          v-model="filterTag"
          placeholder="按标签筛选"
          clearable
          class="filter-select"
          @change="fetchFlowersN"
      >
        <el-option
            v-for="tag in allTags"
            :key="tag"
            :label="tag"
            :value="tag"
        />
      </el-select>

      <el-select
          v-model="filterStock"
          placeholder="按库存筛选"
          clearable
          class="filter-select"
          @change="fetchFlowersN"
      >
        <el-option label="库存充足(>50)" value="50" />
        <el-option label="库存紧张(>10)" value="10" />
        <el-option label="缺货(=0)" value="0" />
      </el-select>
    </div>

    <!-- 商品表格 -->
    <el-table
        :data="flowers"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
        class="flower-table"
    >
      <el-table-column label="花卉图片" width="120">
        <template #default="{ row }">
          <el-image
              :src="'api/img/'+row.name"
              fit="cover"
              preview-teleported
              class="flower-image"
          />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="花卉名称" width="150" sortable />
      <el-table-column prop="price" label="价格(元)" width="120" sortable>
        <template #default="{ row }">
          <span v-if="row.promotion" style="text-decoration: line-through; color: #999">
            {{ row.price }}
          </span>
          <span :style="{ color: row.promotion ? '#f56c6c' : 'inherit' }">
            {{ row.promotion ? (row.price * row.promotion.discount).toFixed(2) : row.price }}
          </span>
          <el-tag v-if="row.promotion" size="small" type="danger" style="margin-left: 5px">
            促销中
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="100" sortable>
        <template #default="{ row }">
          <el-tag :type="getStockTagType(row.stock)">
            {{ row.stock }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sales" label="销量" width="100" sortable />
      <el-table-column label="标签" width="200">
        <template #default="{ row }">
          <el-tag
              v-for="tag in row.tags"
              :key="tag"
              size="small"
              style="margin-right: 5px"
          >
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">
            <el-icon><Edit /></el-icon> 编辑
          </el-button>
          <el-popconfirm
              title="确定要删除这个花卉吗？"
              @confirm="handleDelete(row.id)"
          >
            <template #reference>
              <el-button size="small" type="danger">
                <el-icon><Delete /></el-icon> 删除
              </el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="fetchFlowersN"
          @current-change="fetchFlowersN"
      />
    </div>

    <!-- 编辑/添加花卉对话框 -->
    <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="50%"
        :close-on-click-modal="false"
    >
      <el-form
          :model="currentFlower"
          :rules="flowerRules"
          ref="flowerForm"
          label-width="100px"
      >
        <el-form-item label="花卉名称" prop="name">
          <el-input v-model="currentFlower.name" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number
              v-model="currentFlower.price"
              :min="0"
              :precision="2"
              :step="0.1"
          />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number v-model="currentFlower.stock" :min="0" />
        </el-form-item>



        <!-- 修改后的图片上传部分 -->
        <el-form-item label="花卉图片" prop="image">
          <el-upload
              class="avatar-uploader"
              action="#"
              :show-file-list="false"
              :auto-upload="false"
              :on-change="handleImageChange"
              accept="image/*"
          >
            <img
                v-if="currentFlower.imageFile"
                :src="currentFlower.imageFile"
                class="avatar"
            />
            <el-icon v-else class="avatar-uploader-icon">
              <Plus />
            </el-icon>
          </el-upload>

          <!-- 裁剪对话框 -->
          <el-dialog
              v-model="cropDialogVisible"
              title="图片裁剪"
              width="600px"
              append-to-body
          >
            <div class="cropper-container">
              <vue-cropper
                  ref="cropper"
                  :img="uploadedImage"
                  :autoCrop="true"
                  :fixed="true"
                  :fixedNumber="[1, 1]"
                  :centerBox="true"
                  :info="true"
                  mode="contain"
              />
            </div>
            <template #footer>
        <span class="dialog-footer">
          <el-button @click="cropDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmCrop">确认裁剪</el-button>
        </span>
            </template>
          </el-dialog>
        </el-form-item>


        <el-form-item label="标签" prop="tags">
          <el-select
              v-model="currentFlower.tagsArray"
              multiple
              filterable
              allow-create
              placeholder="请选择或输入标签"
              style="width: 100%"
          >
            <el-option
                v-for="tag in allTags"
                :key="tag"
                :label="tag"
                :value="tag"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="促销活动" prop="promotion_id">
          <el-select
              v-model="currentFlower.promotion_id"
              placeholder="选择促销活动"
              clearable
              style="width: 100%"
              @change="handlePromotionChange"
          >
            <el-option
                v-for="promotion in availablePromotions"
                :key="promotion.id"
                :label="`${promotion.title} (${promotion.discount * 10}折)`"
                :value="promotion.id"
            />
          </el-select>
          <div v-if="selectedPromotion" class="promotion-info">
            <p>活动时间: {{ formatDate(selectedPromotion.start_time) }} 至 {{ formatDate(selectedPromotion.end_time) }}</p>
            <p>活动描述: {{ selectedPromotion.description }}</p>
          </div>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
              v-model="currentFlower.description"
              type="textarea"
              :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm"> 确认 </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
// 图片上传前验证
import {allPromotionDet} from "@/api/promotion.js";
import {ref, computed, onMounted, watch} from 'vue'
import {
  Search,
  Edit,
  Delete,
  Plus
} from '@element-plus/icons-vue'
import {addFlowerAdmin, delFlowerAdmin, fetchFlowers, fetchTags, updateFlowerAdmin} from "@/api/flower.js";
import {ElMessage} from "element-plus";
import 'vue-cropper/dist/index.css'
import { VueCropper } from 'vue-cropper'

// 新增的状态
const cropDialogVisible = ref(false)
const cropper = ref(null)
const uploadedImage = ref('')

// 数据状态
const flowers = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const filterTag = ref([])
const filterStock = ref('')
const allTags = ref([])
const availablePromotions = ref([])

// 对话框状态
const dialogVisible = ref(false)
// const dialogTitle = ref('')
const currentFlower = ref({
  id: null,
  name: '',
  price: 0,
  stock: 0,
  imageFile: '',
  description: '',
  tags: '',
  tagsArray: [],
  promotion_id: null,
})
const selectedPromotion = ref(null)
const flowerForm = ref(null)

// 表单验证规则
const flowerRules = {
  name: [
    { required: true, message: '请输入花卉名称', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value <= 0) {
          callback(new Error('价格必须大于零'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ],
  stock: [
    { required: true, message: '请输入库存', trigger: 'blur' },
    { pattern: /^[1-9]\d*$/, message: '库存必须是大于零的整数', trigger: 'blur' }
  ]
};

// 计算属性
const dialogTitle = computed(() => {
  return currentFlower.value.id ? '编辑花卉信息' : '添加新花卉'
})

// 生命周期钩子
onMounted(() => {
  fetchFlowersN()
  fetchPromotions()
})

// Add this watch
watch(cropDialogVisible, (newVal) => {
  if (newVal) {
    console.log('Crop dialog opened, image data:', uploadedImage.value ? 'exists' : 'missing')
    // Give DOM time to render
    setTimeout(() => {
      console.log('Cropper reference after timeout:', cropper.value)
    }, 300)
  }
})


// 修改后的方法
const handleImageChange = (file) => {
  const isImage = file.raw.type.startsWith('image/');
  const isLt2M = file.raw.size / 1024 / 1024 < 2;

  if (!isImage) {
    ElMessage.error('只能上传图片文件!');
    return false;
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!');
    return false;
  }

  // 读取文件为DataURL
  const reader = new FileReader();
  reader.onload = (e) => {
    console.log('Image loaded successfully');
    uploadedImage.value = e.target.result;
    // 直接设置currentFlower.imageFile，防止裁剪失败
    currentFlower.value.imageFile = e.target.result;
    cropDialogVisible.value = true;
  };
  reader.readAsDataURL(file.raw);
  return false;
}

const confirmCrop = () => {
  console.log('Confirming crop, cropper ref:', cropper.value);
  if (!cropper.value) {
    ElMessage.error('裁剪器未正确初始化');
    return;
  }

  cropper.value.getCropData((data) => {
    console.log('Cropped data received:', data ? 'success' : 'failed');
    currentFlower.value.imageFile = data;
    // 添加这行确保图片被正确设置
    console.log('Image set to currentFlower:', currentFlower.value.imageFile ? 'success' : 'failed');
    cropDialogVisible.value = false;
  });
}


// 修改提交方法
const submitForm = async () => {
  try {
    await flowerForm.value.validate();

    console.log('Form validation passed');

    const formData = new FormData();
    // 添加表单字段
    formData.append('name', currentFlower.value.name);
    formData.append('price', currentFlower.value.price);
    formData.append('stock', currentFlower.value.stock);
    formData.append('description', currentFlower.value.description);

    // 处理标签 - 转换为JSON字符串
    if (currentFlower.value.tagsArray && currentFlower.value.tagsArray.length > 0) {
      formData.append('tags', JSON.stringify(currentFlower.value.tagsArray));
    }

    // 添加促销ID（如果有）
    if (currentFlower.value.promotion_id) {
      formData.append('promotion_id', currentFlower.value.promotion_id);
    }


    if (currentFlower.value.imageFile) {
      let imageBlob = null;

      if (currentFlower.value.imageFile.startsWith('data:')) {
        imageBlob = dataURLtoBlob(currentFlower.value.imageFile);
      } else if (currentFlower.value.imageFile.startsWith('api/img/')) {
        // 这是编辑模式下的已有图片，需要先获取
        try {
          const response = await fetch(currentFlower.value.imageFile);
          imageBlob = await response.blob();
        } catch (error) {
        }
      }

      if (imageBlob) {
        // 使用随机文件名避免缓存问题
        const filename = `${currentFlower.value.name || 'flower'}_${Date.now()}.png`;
        formData.append('image', imageBlob, filename);
        console.log('Image added to FormData with filename:', filename);
      } else {
        ElMessage.error('图片处理失败，请重新选择图片');
        return;
      }
    } else {
      // 新增模式下必须有图片
      if (!currentFlower.value.id) {
        ElMessage.error('请选择并裁剪花卉图片');
        return;
      }
    }

    // 根据是编辑还是新增选择不同的API
    if (currentFlower.value.id) {
      await updateFlowerAdmin(currentFlower.value.id, formData);
    } else {
      await addFlowerAdmin(formData);
    }

    dialogVisible.value = false;
    await fetchFlowersN(); // 刷新列表
  } catch (error) {
    console.error('表单提交失败:', error);
    // 打印更详细的错误信息
    ElMessage.error(error.message || '操作失败');
  }
}

// 重写 dataURLtoBlob 函数，确保它能正确处理 DataURL
const dataURLtoBlob = (dataurl) => {
  try {
    // 确保 dataurl 是字符串
    if (typeof dataurl !== 'string') {
      console.error('dataURLtoBlob: input is not a string', dataurl);
      return null;
    }

    // 确保 dataurl 是 DataURL 格式
    if (!dataurl.startsWith('data:')) {
      console.error('dataURLtoBlob: input is not a DataURL', dataurl);
      return null;
    }

    const arr = dataurl.split(',');
    if (arr.length !== 2) {
      console.error('dataURLtoBlob: invalid DataURL format');
      return null;
    }

    // 获取 MIME 类型
    const mime = arr[0].match(/:(.*?);/);
    if (!mime || !mime[1]) {
      console.error('dataURLtoBlob: cannot extract MIME type');
      return null;
    }

    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }

    console.log('Blob created successfully with MIME type:', mime[1]);
    return new Blob([u8arr], { type: mime[1] });
  } catch (error) {
    console.error('dataURLtoBlob error:', error);
    return null;
  }
}


// 方法
const fetchFlowersN = async () => {
  loading.value = true
  try {
    // 这里替换为实际的API调用
      const params = {
        page: currentPage.value,
        per_page: pageSize.value,
        search: searchQuery.value,
        tags: filterTag.value,
        stock: filterStock.value
      };

    const rpdata = await fetchFlowers(params)

    flowers.value = rpdata.flowers
    total.value = rpdata.totalflower
    allTags.value = await fetchTags()
    // 模拟数据
    // flowers.value = mockFlowers
    // total.value = mockFlowers.length
  } catch (error) {
    console.error('获取花卉数据失败:', error)
    ElMessage.error('获取花卉数据失败')
  } finally {
    loading.value = false
  }
}

const fetchPromotions = async () => {
  try {
    availablePromotions.value = await allPromotionDet();
  } catch (error) {
    console.error('获取促销活动失败:', error)
    ElMessage.error('获取促销活动失败')
  }
}

const handleSearchClear = () => {
  searchQuery.value = ''
  fetchFlowersN()
}


const handleEdit = (flower) => {
  currentFlower.value = {
    ...flower,
    tagsArray: flower.tags,
    imageFile: `api/img/${flower.name}`,
  }

  if (flower.promotion_id) {
    selectedPromotion.value = availablePromotions.value.find(
        p => p.id === flower.promotion_id
    )
  } else {
    selectedPromotion.value = null
  }

  dialogVisible.value = true
}


const handleAddFlower = () => {
  currentFlower.value = {
    id: null,
    name: '',
    price: 0,
    stock: 0,
    imageFile: '',
    description: '',
    tags: '',
    tagsArray: [],
    promotion_id: null
  }
  selectedPromotion.value = null
  dialogVisible.value = true
}

const handleDelete = async (id) => {
  await delFlowerAdmin(id)
}

const handlePromotionChange = (promotionId) => {
  selectedPromotion.value = availablePromotions.value.find(
      p => p.id === promotionId
  )
}

const getStockTagType = (stock) => {
  if (stock === 0) return 'danger'
  if (stock < 10) return 'warning'
  return 'success'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

</script>

<style scoped>
/* 新增裁剪容器样式 */
.cropper-container {
  width: 100%;
  height: 400px;
}


.flower-management-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-container {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 150px;
}

.flower-table {
  margin-bottom: 20px;
}

.flower-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.promotion-info {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

.promotion-info p {
  margin: 5px 0;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100px;
  height: 100px;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}

</style>