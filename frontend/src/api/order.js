import axios from 'axios';
import router from '@/routes';
import {ElMessage} from 'element-plus';

const API_BASE_URL = '/api/order';

// 获取 token 的函数不需要异步
export const getLocalToken = () => {
    const jwtToken = localStorage.getItem('jwtToken');
    if (!jwtToken) {
        ElMessage.error("未找到登录信息，请重新登录！");
        router.push('/login'); // 更友好的方式是跳转到登录页
        throw new Error('No token found');
    }
    return jwtToken;
}

// 创建 axios 实例，统一设置基础配置
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器，统一添加 token
apiClient.interceptors.request.use(config => {
    const token = getLocalToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// 响应拦截器，统一处理错误
apiClient.interceptors.response.use(response => {
    if (response.data?.message) {
        ElMessage.success(response.data.message);
    }
    return response.data;
}, error => {
    if (error.response?.data?.message) {
        ElMessage.error(error.response.data.message);
    } else {
        ElMessage.error('请求失败，请稍后重试');
    }
    return Promise.reject(error);
});

export const addOrder = async (orderData) => {
    try {
        return await apiClient.post('/add', orderData);
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const getOrders = async (page, per_page,status="",order_id="") => {
    try {
        return await apiClient.get('/list', {
            params: {page, per_page, status, order_id}
        });
    } catch (error) {
        throw error;
    }
};

export const delOrder = async (order_id) => {
    try {
        return await apiClient.post('/delorder', {order_id});
    } catch (error) {
        throw error;
    }
};

export const getOrderDetail = async (order_id) => {
    try {
        return await apiClient.post('/orderdetail', {order_id});
    } catch (error) {
        throw error;
    }
};

export const buyFlowersNow = async (order_id) => {
    try {
        return await apiClient.post('/buyNow', {order_id});
    } catch (error) {
        throw error;
    }
};

export const getAllOrders = async (params) => {
    try {
        return await apiClient.get('/getAllOrders',{params:params});
    } catch (error) {
        throw error;
    }
};

export const getBaseOrderInf = async () => {
    try {
        return await apiClient.get('/getOrderBaseInfo');
    } catch (error) {
        throw error;
    }
};

export const adminOrderStatus = async (ids,status) => {
    try {
        return await apiClient.put('/adminOrderStatus', {ids,status});
    } catch (error) {
        throw error;
    }
};
