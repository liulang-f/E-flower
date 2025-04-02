import axios from 'axios';
import router from '@/routes';
import { ElMessage } from 'element-plus'; // 引入提示组件

const API_BASE_URL = '/api/cart'; // 后端接口地址

// 添加购物车
export const addToCart = async (flower_id, quantity) => {
    try {
        // 从本地存储中获取 JWT Token
        const token = localStorage.getItem('jwtToken');
        if (!token) {
            // 如果没有 Token，显示提示信息
            ElMessage.warning('请先登录');
            await router.push('/login');
            return 0
        }

        // 调用后端接口
        const response = await axios.post(
            `${API_BASE_URL}/add`, // 后端接口地址
            { flower_id, quantity }, // 请求体
            {
                headers: {
                    Authorization: `Bearer ${token}`, // 在请求头中携带 Token
                },
            }
        );

        // 如果添加成功，返回成功信息
        if (response.status === 200) {
            // 使用后端返回的 message
            ElMessage.success(response.data.message);
        } else {
            // 如果后端返回失败，显示提示信息
            ElMessage.error(response.data.message);
        }

    } catch (error) {
        // 如果请求失败，显示提示信息
        ElMessage.error('添加失败，请稍后重试');
    }
};

export const getCarts = async () => {
    try {
        // 获取 JWT Token
        const jwtToken = localStorage.getItem('jwtToken');
        if (!jwtToken) {
            ElMessage.error("操作失败！");
            window.location.reload(); // 仅刷新当前页面
            return;
        }

        // 发送请求
        const response = await axios.get(
            `${API_BASE_URL}/getCarts`, // URL
            {
                timeout: 5000, // 超时时间
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            }
        );

        // 处理响应
        if (response.status === 200 || response.status === 201) {
            if (response.data?.message) {
                ElMessage.success(response.data.message);
            }
            return response.data; // 返回完整的响应数据
        }else {
            ElMessage.error(response.data.message)
        }
    } catch (error) {
        // 错误处理
        throw error;
    }
};

export const delCart = async (cart_id) => {
    try {
        // 获取 JWT Token
        const jwtToken = localStorage.getItem('jwtToken');
        if (!jwtToken) {
            ElMessage.error("操作失败！");
            window.location.reload(); // 仅刷新当前页面
            return;
        }

        // 发送请求
        const response = await axios.post(
            `${API_BASE_URL}/remove`, // URL
            {cart_id},
            {
                timeout: 5000, // 超时时间
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            }
        );

        // 处理响应
        if (response.status === 200 || response.status === 201) {
            if (response.data?.message) {
                ElMessage.success(response.data.message);
            }
            return response.data; // 返回完整的响应数据
        }else {
            ElMessage.error(response.data.message)
        }
    } catch (error) {
        // 错误处理
        throw error;
    }
};


export const updateCart = async (flower_id, quantity) => {
    try {
        // 从本地存储中获取 JWT Token
        const token = localStorage.getItem('jwtToken');
        if (!token) {
            // 如果没有 Token，显示提示信息
            ElMessage.warning('请先登录');
            await router.push('/login');
            return 0
        }

        // 调用后端接口
        const response = await axios.put(
            `${API_BASE_URL}/update`, // 后端接口地址
            { flower_id, quantity }, // 请求体
            {
                headers: {
                    Authorization: `Bearer ${token}`, // 在请求头中携带 Token
                },
            }
        );

        if (response.status !== 200) {
            // 使用后端返回的 message
            ElMessage.error(response.data.message);
        }

    } catch (error) {
        // 如果请求失败，显示提示信息
        ElMessage.error('修改，请稍后重试');
    }
};

export const clearUserCart = async () => {
    try {
        // 获取 JWT Token
        const jwtToken = localStorage.getItem('jwtToken');
        if (!jwtToken) {
            ElMessage.error("操作失败！");
            window.location.reload(); // 仅刷新当前页面
            return;
        }

        // 发送请求
        const response = await axios.get(
            `${API_BASE_URL}/clear`, // URL
            {
                timeout: 5000, // 超时时间
                headers: {
                    Authorization: `Bearer ${jwtToken}`,
                },
            }
        );

        // 处理响应
        if (response.status === 200 || response.status === 201) {
            if (response.data?.message) {
                ElMessage.success(response.data.message);
            }
            return response.data; // 返回完整的响应数据
        }else {
            ElMessage.error(response.data.message)
        }
    } catch (error) {
        // 错误处理
        throw error;
    }
};