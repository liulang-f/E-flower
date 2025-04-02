<template>
  <div class="admin-dashboard" :class="{ 'sidebar-collapsed': !isSidebarCollapsed }">
    <AdminHeader />
    <AdminSidebar
        :currentComponent="currentComponent"
        @sidebar-collapsed="handleSidebarCollapse"
        @select-component="handleComponentSelection"
    />

    <main class="admin-main">
      <div class="container-fluid">
        <component :is="currentComponent"/>
      </div>
    </main>

    <AdminFooter />
  </div>
</template>

<script>
import AdminHeader from "@/components/AdminComp/AdminHeader.vue";
import AdminSidebar from "@/components/AdminComp/AdminSidebar.vue";
import AdminFooter from "@/components/AdminComp/AdminFooter.vue";
import AdminDashboardContent from "@/components/AdminViewComp/AdminDashboardContent.vue";
import AdminFlowerManage from "@/components/AdminViewComp/AdminFlowerManage.vue";
import AdminOrderManage from "@/components/AdminViewComp/AdminOrderManage.vue";
import AdminUserManage from "@/components/AdminViewComp/AdminUserManage.vue";
import AdminPromotionManage from "@/components/AdminViewComp/AdminPromotionManage.vue";
import AdminLogManage from "@/components/AdminViewComp/AdminLogManage.vue";
import AdminSettingManage from "@/components/AdminViewComp/AdminSettingManage.vue";

export default {
  name: 'AdminController',
  components: {
    AdminHeader,
    AdminSidebar,
    AdminFooter,
    AdminDashboardContent,
    AdminFlowerManage,
    AdminOrderManage,
    AdminUserManage,
    AdminPromotionManage,
    AdminLogManage,
    AdminSettingManage,
  },
  data() {
    return {
      isSidebarCollapsed: false,
      currentComponent: 'AdminDashboardContent' // 默认显示仪表盘内容
    }
  },
  methods: {
    handleSidebarCollapse(collapsed) {
      this.isSidebarCollapsed = collapsed;
    },
    handleComponentSelection(componentName) {
      this.currentComponent = componentName;
    },
  },
}
</script>

<style scoped>
.admin-dashboard {
  padding-left: 200px;
  padding-right: 50px;
  transition: padding 0.3s ease;
  background-color: #f8f9fa;
  min-height: 100vh;
  padding-top: 60px; /* For header space */
}

.admin-dashboard.sidebar-collapsed {
  padding-left: 80px;
}

.admin-main {
  width: 100%;
}
</style>