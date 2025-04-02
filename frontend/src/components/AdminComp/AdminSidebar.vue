<template>
  <aside :class="['admin-sidebar', { 'collapsed': !isCollapsed }]">
    <div class="sidebar-header">
      <h3 v-if="isCollapsed">功能一览</h3>
      <font-awesome-icon v-else :icon="['fas', 'tree']" class="collapsed-icon" />
    </div>

    <nav class="sidebar-nav">
      <ul>
        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminDashboardContent' }">
          <a href="#" @click="selectComponent('AdminDashboardContent')">
            <font-awesome-icon :icon="['fas', 'tachometer-alt']" />
            <span v-if="isCollapsed">仪表盘</span>
          </a>
        </li>
        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminFlowerManage' }">
          <a href="#" @click="selectComponent('AdminFlowerManage')">
            <font-awesome-icon :icon="['fas', 'shopping-bag']" />
            <span v-if="isCollapsed">商品管理</span>
          </a>
        </li>
        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminOrderManage' }">
          <a href="#" @click="selectComponent('AdminOrderManage')">
            <font-awesome-icon :icon="['fas', 'receipt']" />
            <span v-if="isCollapsed">订单管理</span>
          </a>
        </li>
        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminUserManage' }">
          <a href="#" @click="selectComponent('AdminUserManage')">
            <font-awesome-icon :icon="['fas', 'users']" />
            <span v-if="isCollapsed">用户管理</span>
          </a>
        </li>
        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminPromotionManage' }">
          <a href="#" @click="selectComponent('AdminPromotionManage')">
            <font-awesome-icon :icon="['fas', 'percent']" />
            <span v-if="isCollapsed">促销活动</span>
          </a>
        </li>

        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminLogManage' }">
          <a href="#" @click="selectComponent('AdminLogManage')">
            <font-awesome-icon :icon="['fas', 'file-alt']" />
            <span v-if="isCollapsed">日志管理</span>
          </a>
        </li>

        <li class="nav-item" :class="{ 'active': currentComponent === 'AdminSettingManage' }">
          <a href="#" @click="selectComponent('AdminSettingManage')">
            <font-awesome-icon :icon="['fas', 'cog']" />
            <span v-if="isCollapsed">系统设置</span>
          </a>
        </li>
        <li class="nav-item" :class="{ 'active': currentComponent === 'SupportComponent' }">
          <a href="#" @click="selectComponent('SupportComponent')">
            <font-awesome-icon :icon="['fas', 'headset']" />
            <span v-if="isCollapsed">客户支持</span>
          </a>
        </li>
      </ul>
    </nav>

    <div class="sidebar-footer">
      <button @click="toggleCollapse" class="collapse-btn">
        <font-awesome-icon :icon="['fas', !isCollapsed ? 'chevron-right' : 'chevron-left']" />
        <span v-if="isCollapsed">收起</span>
      </button>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'AdminSidebar',
  props: {
    currentComponent: {
      type: String,
      default: 'AdminDashboardContent'
    }
  },
  data() {
    return {
      isCollapsed: false
    }
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
      this.$emit('sidebar-collapsed', this.isCollapsed);
    },
    selectComponent(componentName) {
      this.$emit('select-component', componentName);
    }
  }
}
</script>

<style scoped>
.admin-sidebar {
  width: 180px;
  height: 100vh;
  background: linear-gradient(to bottom, #4a6b57, #3a5547);
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  padding-top: 60px;
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  box-shadow: 3px 0 10px rgba(0, 0, 0, 0.1);
}

.admin-sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.sidebar-header h3 {
  margin: 0;
  color: white;
  font-size: 1.2rem;
  white-space: nowrap;
  font-weight: 500;
  letter-spacing: 1px;
}

.collapsed-icon {
  font-size: 1.5rem;
  color: white;
}

.sidebar-nav {
  padding: 15px 0;
  flex-grow: 1.8;
  overflow-y: auto;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin:auto;
  border-radius: 0 30px 30px 0;
  overflow: hidden;
  width: 95%;
}

.nav-item a {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
  white-space: nowrap;
  border-radius: 0 30px 30px 0;
}

.nav-item a:hover, .nav-item.active a {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateX(5px);
}

.nav-item svg {
  margin-right: 15px;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.admin-sidebar.collapsed .nav-item svg {
  margin: auto;
}

.sidebar-footer {
  padding: 10px 0;
  flex-grow: 1;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.collapse-btn {
  background: none;
  border: none;
  color: white;
  width: 100%;
  padding: 10px 20px;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s;
  margin: auto;
}

.collapse-btn:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.collapse-btn svg {
  margin-right: 20px;
}

.admin-sidebar.collapsed .collapse-btn span {
  display: none;
}

.admin-sidebar.collapsed .collapse-btn svg {
  margin-right: 0;
  margin-left: 18px;
}

.admin-sidebar.collapsed .nav-item svg {
  margin-right: 0;
  font-size: 1.3rem;
  display: block;
  text-align: center;
  width: 100%;
}

/* 移动端样式 */
@media (max-width: 768px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar:not(.collapsed) {
    transform: translateX(0);
    width: 250px;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  }

  .sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    transition: opacity 0.3s;
  }
}
</style>