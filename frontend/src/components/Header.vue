<template>
  <div>
    <header class="header-fixed">
      <div class="container">
        <div class="header-left">
          <!-- 返回按钮 -->
          <button @click="goBack" class="back-button" v-if="canGoBack">
            <FontAwesomeIcon icon="arrow-left" />
            <span>返回</span>
          </button>

          <div class="logo">
            <img src="@/assets/images/logo.png" alt="花店Logo" />
            <span class="logo-text">花<span class="accent">语</span></span>
          </div>
        </div>

        <nav class="nav">
          <ul>
            <li :class="{ active: $route.path === '/' }"><router-link to="/">首页</router-link></li>
            <li :class="{ active: $route.path === '/flowers' }"><router-link to="/flowers">全部鲜花</router-link></li>
            <li :class="{ active: $route.path === '/activity' }"><router-link to="/activity">活动专区</router-link></li>
            <li :class="{ active: $route.path === '/hot' }"><router-link to="/hot">热销专区</router-link></li>
<!--            <li :class="{ active: $route.path === '/gifts' }"><router-link to="/gifts">礼品专区</router-link></li>-->
<!--            <li :class="{ active: $route.path === '/flower-knowledge' }"><router-link to="/flower-knowledge">花语知识</router-link></li>-->
          </ul>
        </nav>

        <div class="header-right">
          <div class="search-box">
            <input type="text" placeholder="想要点什么？" v-model="searchQuery" />
            <button @click="handleSearch">
              <FontAwesomeIcon icon="search" />
            </button>
          </div>

          <div class="cart-icon" v-if="isAuthenticated">
            <router-link to="/cart" :class="{ active: $route.path === '/cart' }">
              <FontAwesomeIcon icon="shopping-cart" />
              <span class="cart-count" v-if="cartCount > 0">{{ cartCount > 99 ? '99+' : cartCount }}</span>
            </router-link>
          </div>

          <div v-if="isAuthenticated" class="user-menu-container" @mouseover="ddChange" @mouseleave="changeShowDown">
            <div class="user-info">
              <img :src="user.avatar" alt="用户头像" class="avatar" />
              <span class="username">{{ user.username }}</span>
              <FontAwesomeIcon icon="chevron-down" class="dropdown-icon" />
            </div>
            <div>
            <ul v-if="showDropdown" class="dropdown-menu" @mouseover="ddChange" @mouseleave="changeShowDown">
              <li><router-link to="/controller" v-if="isAdmin"><FontAwesomeIcon icon="list-alt" /> 控制台</router-link></li>
              <li><router-link to="/authinfo"><FontAwesomeIcon icon="user" /> 个人信息</router-link></li>
              <li><router-link to="/orders"><FontAwesomeIcon icon="list-alt" /> 我的订单</router-link></li>
              <li><a href="#" @click.stop.prevent="handleLogout"><FontAwesomeIcon icon="sign-out-alt" /> 退出</a></li>
            </ul>
            </div>
          </div>

          <div v-else class="login-button">
            <a href="/login">登录 / 注册</a>
          </div>
        </div>
      </div>
    </header>
    <!-- 在 header 标签之后添加 -->
    <div class="header-placeholder"></div>
  </div>
</template>

<script>
import { checkAuth, logoutAuth } from '@/api/auth.js';

export default {
  name: 'Header',
  data() {
    return {
      isAuthenticated: false,
      user: {
        username: '',
        avatar: '',
      },
      showDropdown: false,
      searchQuery: null,
      isScrolled: false,
      canGoBack: false,
      cartCount: 0,
      timeoutId : null,
      isAdmin: false,
    };
  },
  async created() {
    await this.checkUserAuth();
    this.canGoBack = window.history.length > 1;
  },

  methods: {
    async checkUserAuth() {
      try {
        const authResult = await checkAuth();
        if (authResult.isAuthenticated) {
          this.isAuthenticated = true;
          this.user.username = authResult.user.username;
          this.user.avatar = authResult.user.avatar;
          this.cartCount = authResult.carts;
          this.isAdmin = authResult.isAdmin;
        }
      } catch (error) {

      }
    },

    async handleLogout() {
      try {
        await logoutAuth();
        this.isAuthenticated = false;
        this.user = { username: '', avatar: '' };
        this.$router.push('/');
      } catch (error) {
        console.error('退出登录失败:', error);
      }
    },

    handleSearch() {
      if (this.searchQuery) {
        this.$router.push({
          path: '/flowers',
          query: { search: this.searchQuery }
        });
      }
    },

    goBack() {
      this.$router.go(-1);
    },

    changeShowDown() {
      // 如果已经有延迟操作在进行，先取消它
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
      }

      // 设置一个新的延迟操作
      this.timeoutId = setTimeout(() => {
        this.showDropdown = false;
      }, 500); // 1000毫秒后执行
    },

    // 取消改变showDropdown的延迟操作
    ddChange() {
      this.showDropdown = true;
      if (this.timeoutId) {
        clearTimeout(this.timeoutId); // 取消延迟操作
        this.timeoutId = null; // 清除timeoutId
      }
    },
  },
};
</script>

<style scoped>
/* 固定样式简化 */
/* header固定样式 */
.header-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #ffffff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

/* 占位div样式 - 固定高度 */
.header-placeholder {
  height: 90px; /* 与header高度保持一致 */
  width: 100%;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

/* Logo 样式增强 */
.logo {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.logo img {
  height: 36px;
  margin-right: 8px;
  transition: transform 0.3s ease;
}

.logo:hover img {
  transform: scale(1.05);
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  color: #333;
  letter-spacing: 1px;
}

.accent {
  color: #e74c3c;
}

/* 返回按钮 */
.back-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: #555;
  font-size: 14px;
  margin-right: 15px;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-button:hover {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.back-button span {
  margin-left: 5px;
}

/* 导航样式优化 */
.nav {
  margin: 0 auto;
}

.nav ul {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0;
}

.nav li {
  margin: 0 12px;
  position: relative;
}

.nav a {
  text-decoration: none;
  color: #555;
  font-weight: 500;
  font-size: 15px;
  padding: 8px 4px;
  display: block;
  transition: all 0.3s ease;
}

.nav a:hover {
  color: #e74c3c;
}

.nav li.active a {
  color: #e74c3c;
  font-weight: 600;
}

.nav li.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #e74c3c;
  border-radius: 3px;
}

/* 搜索框样式优化 */
.search-box {
  display: flex;
  align-items: center;
  margin-right: 15px;
  position: relative;
}

.search-box input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  width: 180px;
  transition: all 0.3s ease;
  font-size: 14px;
}

.search-box input:focus {
  width: 220px;
  border-color: #e74c3c;
  outline: none;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.search-box button {
  position: absolute;
  right: 10px;
  padding: 6px;
  background: none;
  color: #888;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.search-box button:hover {
  color: #e74c3c;
}

/* 购物车图标 */
.cart-icon {
  margin: 0 15px;
  position: relative;
}

.cart-icon a {
  color: #555;
  font-size: 18px;
  transition: color 0.3s ease;
}

.cart-icon a:hover, .cart-icon a.active {
  color: #e74c3c;
}

.cart-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #e74c3c;
  color: white;
  font-size: 11px;
  font-weight: bold;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 用户菜单容器 - 新增 */
.user-menu-container {
  position: relative;
}

/* 用户信息样式优化 */
.user-info {
  position: relative;
  display: flex;
  align-items: center;
  padding: 5px;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.user-info:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e74c3c;
}

.username {
  margin: 0 8px;
  font-weight: 500;
  font-size: 14px;
  color: #444;
}

.dropdown-icon {
  font-size: 12px;
  color: #888;
}

/* 下拉菜单样式优化 */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  list-style: none;
  margin: 0;
  padding: 8px 0;
  min-width: 120px;
  z-index: 1001;
  opacity: 0;
  transform: translateY(10px);
  animation: fadeIn 0.3s ease forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-menu::before {
  content: '';
  position: absolute;
  top: -6px;
  right: 20px;
  width: 12px;
  height: 12px;
  background-color: #fff;
  transform: rotate(45deg);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  border-left: 1px solid rgba(0, 0, 0, 0.05);
}

.dropdown-menu li {
  margin: 0;
}

.dropdown-menu a {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  text-decoration: none;
  color: #444;
  font-size: 14px;
  transition: all 0.2s ease;
}

.dropdown-menu a:hover {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.dropdown-menu a svg {
  margin-right: 8px;
  width: 16px;
}

/* 登录按钮 */
.login-button a {
  display: inline-block;
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  font-weight: 500;
  border-radius: 20px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.login-button a:hover {
  background-color: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .nav a {
    font-size: 14px;
  }

  .nav li {
    margin: 0 8px;
  }

  .search-box input {
    width: 150px;
  }
}

@media (max-width: 768px) {
  .container {
    flex-wrap: wrap;
  }

  .nav {
    order: 3;
    width: 100%;
    margin-top: 15px;
    overflow-x: auto;
  }

  .nav ul {
    padding-bottom: 5px;
  }

  .search-box input {
    width: 120px;
  }

  .username {
    display: none;
  }
}
</style>