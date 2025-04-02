<template>
  <div class="settings-container">
    <h2 class="settings-title">系统设置</h2>
    <div class="settings-card">
      <el-table :data="settings" style="width: 100%" border stripe>
        <el-table-column prop="key" label="设置项" width="200">
          <template #default="{ row }">
            <span class="setting-key">{{ formatKey(row.key) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="value" label="当前值">
          <template #default="{ row }">
            <div v-if="isBooleanSetting(row.key)">
              <el-switch
                  v-model="row.value"
                  :active-value="1"
                  :inactive-value="0"
                  @change="updateSetting(row.id, row.value)"
              />
              <span class="status-text">
                {{ row.value ? '已开启' : '已关闭' }}
              </span>
            </div>
            <div v-else class="numeric-setting">
              <el-input-number
                  v-model="row.value"
                  :min="1"
                  :max="1000"
                  @change="updateSetting(row.id, row.value)"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="描述" width="300">
          <template #default="{ row }">
            <span class="setting-description">{{ row.description }}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {adGetSettings, adUpdateSetting} from "@/api/admin.js";

const settings = ref([])

// 获取设置
const getSettings = async () => {
  settings.value = await adGetSettings()
}

// 更新设置
const updateSetting = async (id, value) => {
  await adUpdateSetting(id,value)
  await getSettings()
}

// 辅助函数
const isBooleanSetting = (key) => {
  return key === '自动接单' || key === '自动删除过期活动'
}

const formatKey = (key) => {
  return key
}

onMounted(() => {
  getSettings()
})
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.settings-title {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  font-weight: 600;
}

.settings-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.setting-key {
  font-weight: 500;
  color: #409eff;
}

.status-text {
  margin-left: 10px;
  color: #666;
}

.numeric-setting {
  width: 150px;
}

.setting-description {
  color: #888;
  font-size: 0.9em;
}
</style>