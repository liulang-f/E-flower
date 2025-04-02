<template>
  <header class="admin-header">
    <div class="header-left">
      <h1 class="logo">我的商店</h1>
    </div>
    <div class="header-right">
      <div class="notifications">
        <font-awesome-icon :icon="['fas', 'bell']" />
        <span class="badge">3</span>
      </div>
      <div class="admin-profile" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
        <img src="@/assets/images/admin-avatar.png" alt="Admin" class="avatar" />
        <span class="admin-name">Admin</span>
        <font-awesome-icon :icon="['fas', 'chevron-down']" :class="{ 'rotate-icon': showDropdown }" />

        <transition name="fade">
          <div v-if="showDropdown" class="dropdown-menu">
            <button class="dropdown-item" @click="goToStore">
              <font-awesome-icon :icon="['fas', 'shop']" class="item-icon" />
              返回商店
            </button>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script>
import routes from "@/routes/index.js";
export default {
  name: 'AdminHeader',
  data() {
    return {
      showDropdown: false
    }
  },
  methods: {
    goToStore() {
      // 这里添加导航到商店的逻辑
      routes.push('/')
      this.showDropdown = false;
    }
  }
}
</script>

<style scoped>
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1002;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  color: #4a6b57;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  position: relative;
}

.notifications {
  position: relative;
  margin-right: 25px;
  font-size: 1.2rem;
  color: #5a5a5a;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -5px;
  right: -10px;
  background-color: #ff4757;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.7rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.admin-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  padding: 5px 10px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.admin-profile:hover {
  background-color: #f5f5f5;
}

.avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  margin-right: 10px;
}

.admin-name {
  margin-right: 8px;
  font-weight: 500;
}

.rotate-icon {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 180px;
  z-index: 1000;
  overflow: hidden;
  margin-top: 5px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 10px 15px;
  background: none;
  border: none;
  text-align: left;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
  color: #4a6b57;
}

.item-icon {
  margin-right: 10px;
  color: #4a6b57;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>