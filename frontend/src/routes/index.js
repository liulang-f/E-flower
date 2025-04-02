import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomeView.vue'
import FlowerDetailView from "@/views/FlowerDetailView.vue";
import LoginRegisterView from "@/views/LoginRegisterView.vue";
import FlowersView from "@/views/FlowersView.vue";
import FlowerActivity from "@/views/FlowerActivity.vue";
import ActivityDetail from "@/views/ActivityDetail.vue";
import HotView from "@/views/HotView.vue";
import AuthInfo from "@/views/AuthInfo.vue";
import CartView from "@/views/CartView.vue";
import OrderView from "@/views/OrderView.vue";
import AdminController from "@/views/AdminController.vue";

const routes = [
    {
        path: '/',
        name: '主页',
        component: HomePage
    }, {
        path: '/login',
        name: '登录注册',
        component: LoginRegisterView
    },{
        path: '/flowers',
        name: '鲜花列表',
        component: FlowersView
    },{
        path: '/activity',
        name: '活动',
        component: FlowerActivity
    },{
        path: '/promotion/:promotionId',
        name: '活动详情',
        component: ActivityDetail
    },{
        path: '/hot',
        name: '热销',
        component: HotView
    },{
        path: '/authinfo',
        name:'个人信息',
        component: AuthInfo
    },{
        path: '/cart',
        name:'购物车',
        component: CartView
    },{
        path: '/orders',
        name:'订单',
        component: OrderView
    },{
        path: '/flowers/:flowerId',
        name: '详情',
        component: FlowerDetailView,
    },{
        path: '/controller',
        name:'管理主页',
        component: AdminController,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router