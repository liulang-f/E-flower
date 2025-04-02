import axios from 'axios';
import router from '@/routes';
import {ElMessage} from 'element-plus';

const API_BASE_URL = '/api/admin';

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

export const getBaseData = async () => {
    try {
        return await apiClient.get('/getBaseInfo')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const getSalesTrend = async () => {
    try {
        return await apiClient.get('/getSalesTrend')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};
export const getTopFlweor = async () => {
    try {
        return await apiClient.get('/getTopFlower')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};
export const getRencentOrder = async () => {
    try {
        return await apiClient.get('/getTenOrder')
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};
export const reSetPwd = async (user_id) => {
    try {
        return await apiClient.post('/reSetPwd', { user_id })
    } catch (error) {
        throw error;
    }
};
export const delUser = async (user_id) => {
    try {
        return await apiClient.delete(`/delUser?user_id=${user_id}`);
    } catch (error) {
        throw error;
    }
};
export const GetUserInf = async (user_id) => {
    try {
        return await apiClient.get(`/getUserInf`,{params:{user_id}});
    } catch (error) {
        throw error;
    }
};
export const getUserOrders = async (params) => {
    try {
        return await apiClient.get(`/getUserOrders`,{params});
    } catch (error) {
        throw error;
    }
};
export const changeUserAddr = async (userId,addrId) => {
    try {
        return await apiClient.post(`/changeUserAddr`,{userId,addrId});
    } catch (error) {
        throw error;
    }
};
export const adminAllPromotions = async (params) => {
    try {
        return await apiClient.get(`/getAllPro`,{params});
    } catch (error) {
        throw error;
    }
};
export const flowersPro = async (promotion_id) => {
    try {
        return await apiClient.get(`/flowersPro`,{
            params:{promotion_id}
        });
    } catch (error) {
        throw error;
    }
};
export const allProTags = async () => {
    try {
        return await apiClient.get(`/allProTags`);
    } catch (error) {
        throw error;
    }
};

export const adminAddPro = async (params) => {
    try {
        return await apiClient.post(`/addPro`,params);
    } catch (error) {
        throw error;
    }
};

export const adminUpdatePro = async (params) => {
    try {
        return await apiClient.post(`/updatePro`,params);
    } catch (error) {
        throw error;
    }
};

export const adminDelPro = async (id) => {
    try {
        return await apiClient.post(`/delPro`, {id});
    } catch (error) {
        throw error;
    }
};

export const getLogs = async (params) => {
    try {
        return await apiClient.get(`/logs`, {params});
    } catch (error) {
        throw error;
    }
};

export const adGetSettings = async () => {
    try {
        return await apiClient.get(`/settings`);
    } catch (error) {
        throw error;
    }
};

export const adUpdateSetting = async (id,value) => {
    try {
        return await apiClient.put(`/updateSetting`,{id,value});
    } catch (error) {
        throw error;
    }
};


