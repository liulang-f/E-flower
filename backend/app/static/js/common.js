/**
 * common.js - 全站通用JavaScript
 */

// DOM 准备就绪后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化用户状态
    initUserState();

    // 返回顶部按钮
    initBackToTop();

    // 初始化退出登录按钮
    initLogoutButton();
});

/**
 * 初始化用户状态 - 登录/未登录状态切换
 */
function initUserState() {
    // 检查是否已登录
    const isLoggedIn = checkLoginStatus();
    const userActions = document.getElementById('userActions');

    if (!userActions) return;

    if (isLoggedIn) {
        // 已登录，显示用户菜单，隐藏登录注册按钮
        userActions.querySelector('.logged-in').style.display = 'flex';
        userActions.querySelector('.not-logged-in').style.display = 'none';

        // 更新用户信息
        updateUserInfo();

        // 更新购物车数量
        updateCartCount();
    } else {
        // 未登录，显示登录注册按钮，隐藏用户菜单
        userActions.querySelector('.logged-in').style.display = 'none';
        userActions.querySelector('.not-logged-in').style.display = 'flex';
    }
}

/**
 * 检查登录状态
 * @returns {boolean} 是否已登录
 */
function checkLoginStatus() {
    // 从本地存储或Cookie中获取登录状态
    // 这里仅作演示，实际应使用更安全的方式处理登录凭证
    const token = localStorage.getItem('userToken');
    return !!token;
}

/**
 * 更新用户信息
 */
function updateUserInfo() {
    // 从本地存储或通过API获取用户信息
    const userInfo = getUserInfo();

    // 更新用户名和头像
    if (userInfo) {
        const userMenu = document.querySelector('.user-menu');
        if (!userMenu) return;

        const usernameEl = userMenu.querySelector('.username');
        const avatarEl = userMenu.querySelector('.user-avatar');

        if (usernameEl && userInfo.username) {
            usernameEl.textContent = userInfo.username;
        }

        if (avatarEl && userInfo.avatar) {
            avatarEl.src = userInfo.avatar;
        }
    }
}

/**
 * 获取用户信息
 * @returns {Object|null} 用户信息对象
 */
function getUserInfo() {
    // 从本地存储或Cookie中获取用户信息
    // 这里仅作演示，实际应通过API获取最新用户数据
    try {
        const userInfoStr = localStorage.getItem('userInfo');
        return userInfoStr ? JSON.parse(userInfoStr) : null;
    } catch (e) {
        console.error('获取用户信息失败', e);
        return null;
    }
}

/**
 * 更新购物车数量
 */
function updateCartCount() {
    // 从本地存储或通过API获取购物车数量
    const cartCount = getCartCount();

    // 更新购物车数量显示
    const cartCountEl = document.querySelector('.cart-count');
    if (cartCountEl && cartCount !== null) {
        cartCountEl.textContent = cartCount;
    }
}

/**
 * 获取购物车数量
 * @returns {number} 购物车商品数量
 */
function getCartCount() {
    // 从本地存储或Cookie中获取购物车数量
    // 这里仅作演示，实际应通过API获取最新购物车数据
    try {
        const cart = localStorage.getItem('cart');
        if (!cart) return 0;

        const cartItems = JSON.parse(cart);
        if (Array.isArray(cartItems)) {
            return cartItems.reduce((total, item) => total + (item.quantity || 0), 0);
        }
        return 0;
    } catch (e) {
        console.error('获取购物车数量失败', e);
        return 0;
    }
}

/**
 * 初始化返回顶部按钮
 */
function initBackToTop() {
    const backToTop = document.getElementById('backToTop');
    if (!backToTop) return;

    // 滚动事件处理
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });

    // 点击事件处理
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * 初始化退出登录按钮
 */
function initLogoutButton() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (!logoutBtn) return;

    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        logout();
    });
}

/**
 * 退出登录
 */
function logout() {
    // 清除本地存储中的登录信息
    localStorage.removeItem('userToken');
    localStorage.removeItem('userInfo');
    // 可能需要调用API通知服务器用户退出

    // 刷新页面或跳转到首页
    window.location.href = 'index.html';
}

/**
 * 格式化日期时间
 * @param {Date|string|number} date 日期对象、字符串或时间戳
 * @param {string} format 格式字符串，默认为 'YYYY-MM-DD HH:mm:ss'
 * @returns {string} 格式化后的日期时间字符串
 */
function formatDateTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
    const d = new Date(date);

    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');

    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 格式化价格
 * @param {number} price 价格
 * @param {string} currency 货币符号，默认为 '¥'
 * @returns {string} 格式化后的价格字符串
 */
function formatPrice(price, currency = '¥') {
    return `${currency}${parseFloat(price).toFixed(2)}`;
}

/**
 * 计算剩余时间
 * @param {Date|string|number} endTime 结束时间
 * @returns {Object|null} 剩余时间对象 {days, hours, minutes, seconds}
 */
function calculateTimeRemaining(endTime) {
    const end = new Date(endTime).getTime();
    const now = new Date().getTime();
    const diff = end - now;

    if (diff <= 0) return null;

    // 计算剩余天数、小时、分钟和秒
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    return { days, hours, minutes, seconds };
}

/**
 * 处理API请求
 * @param {string} url API地址
 * @param {Object} options 请求选项
 * @returns {Promise} 请求Promise
 */
async function apiRequest(url, options = {}) {
    try {
        // 设置默认选项
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        // 合并选项
        const requestOptions = { ...defaultOptions, ...options };

        // 添加认证token（如果已登录）
        const token = localStorage.getItem('userToken');
        if (token) {
            requestOptions.headers.Authorization = `Bearer ${token}`;
        }

        // 发送请求
        const response = await fetch(url, requestOptions);

        // 检查响应状态
        if (!response.ok) {
            throw new Error(`API请求失败: ${response.status} ${response.statusText}`);
        }

        // 解析JSON响应
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

/**
 * 添加到购物车
 * @param {number} flowerId 花卉ID
 * @param {number} quantity 数量
 * @returns {Promise} 添加结果Promise
 */
async function addToCart(flowerId, quantity = 1) {
    // 检查登录状态
    if (!checkLoginStatus()) {
        // 未登录跳转到登录页
        window.location.href = 'login.html?redirect=' + encodeURIComponent(window.location.href);
        return;
    }

    try {
        // 请求API添加到购物车
        // 实际使用时应调用后端API
        // const result = await apiRequest('/api/cart/add', {
        //     method: 'POST',
        //     body: JSON.stringify({ flowerId, quantity })
        // });

        // 这里模拟添加到本地购物车
        addToLocalCart(flowerId, quantity);

        // 更新购物车数量显示
        updateCartCount();

        // 显示添加成功提示
        showMessage('添加到购物车成功！');

        return true;
    } catch (error) {
        console.error('添加到购物车失败:', error);
        showMessage('添加到购物车失败，请重试', 'error');
        return false;
    }
}

/**
 * 添加到本地购物车（仅供演示）
 * @param {number} flowerId 花卉ID
 * @param {number} quantity 数量
 */
function addToLocalCart(flowerId, quantity = 1) {
    try {
        // 获取当前购物车
        let cart = localStorage.getItem('cart');
        cart = cart ? JSON.parse(cart) : [];

        // 检查商品是否已在购物车中
        const existingItemIndex = cart.findIndex(item => item.flowerId === flowerId);

        if (existingItemIndex >= 0) {
            // 商品已存在，增加数量
            cart[existingItemIndex].quantity += quantity;
        } else {
            // 商品不存在，添加新项
            cart.push({ flowerId, quantity });
        }

        // 保存回本地存储
        localStorage.setItem('cart', JSON.stringify(cart));
    } catch (e) {
        console.error('添加到本地购物车失败', e);
    }
}

/**
 * 显示消息提示
 * @param {string} message 消息内容
 * @param {string} type 消息类型：'success'(默认)、'error'、'warning'、'info'
 * @param {number} duration 显示时长（毫秒），默认3000
 */
function showMessage(message, type = 'success', duration = 3000) {
    // 创建消息元素
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    messageEl.innerHTML = `
        <div class="message-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : type === 'warning' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    // 添加到页面
    document.body.appendChild(messageEl);

    // 显示动画
    setTimeout(() => {
        messageEl.classList.add('show');
    }, 10);

    // 一段时间后隐藏
    setTimeout(() => {
        messageEl.classList.remove('show');
        messageEl.addEventListener('transitionend', function() {
            document.body.removeChild(messageEl);
        });
    }, duration);
}

// 导出公共函数（如果需要模块化）
// export {
//     formatDateTime,
//     formatPrice,
//     calculateTimeRemaining,
//     apiRequest,
//     addToCart,
//     showMessage
// };