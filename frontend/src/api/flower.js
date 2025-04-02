import axios from 'axios';
import router from '@/routes';
import {ElMessage} from 'element-plus';

const API_BASE_URL = '/api/flower'; // 后端接口地址

// 获取 token 的函数不需要异步
export const getLocalToken = () => {
    const jwtToken = localStorage.getItem('jwtToken');
    if (!jwtToken) {
        router.push('/login');
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

// 创建一个不需要 token 的 axios 实例用于登录/注册
const authClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器，统一添加 token（仅对需要认证的请求）
apiClient.interceptors.request.use(config => {
    const token = getLocalToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// 响应拦截器，统一处理错误（共享错误处理）
const setupResponseInterceptor = (instance) => {
    instance.interceptors.response.use(response => {
        if (response.data?.message) {
            ElMessage.success(response.data.message);
        }
        return response.data;
    }, error => {
        if (error.response?.data?.message) {
            ElMessage.error(error.response.data.message);
        }
        return Promise.reject(error);
    });
};

// 为两个实例设置响应拦截器
setupResponseInterceptor(apiClient);
setupResponseInterceptor(authClient);

// 获取轮播图数据
export const getCarouselImages =async () =>{
    try {
        return await authClient.get('/showFlowers')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}


export const gethotFlowers =async () =>{
    try {
        return await authClient.get('/hotFlowers')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}

export const getdiscountFlowers =async () =>{
    try {
        return await authClient.get('/discountFlowers')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}

export const getFlowerDetail =async (flowerId) =>{
    try {
        return await authClient.get( `/flowers/${flowerId}`)
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}

export const fetchTags =async (flowerId) =>{
    try {
        return await authClient.get( `/tags`)
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}

// 获取花卉列表
// API示例：GET /api/flowers
// 支持分页、搜索、筛选、排序，返回格式为 { items: [], totalPages: 10 }
export const fetchFlowers =async (params) =>{
    try {
        return await authClient.get( '/flowers',{ params })
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}

export const addFlowerAdmin = async (formData) => {
    try {
        return await apiClient.post('/addFlower', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
}

export const updateFlowerAdmin = async (id, formData) => {
    try {
        return await apiClient.put(`/updateFlower/${id}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    } catch (error) {
        throw error;
    }
}

export const delFlowerAdmin = async (id) => {
    try {
        return await apiClient.delete(`/delFlowerAdmin`, {
            data: { id: id },
        });
    } catch (error) {
        throw error;
    }
}

