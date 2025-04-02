import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from "@/routes/index.js";

const API_BASE_URL = '/api/auth';

// 获取 token 的函数不需要异步
export const getLocalToken = () => {
    const jwtToken = localStorage.getItem('jwtToken');
    if (!jwtToken) {
        ElMessage.error("未找到登录信息，请重新登录！");
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

export const login = async (username, password) => {
    try {
        const response = await authClient.post('/login', { username, password });
        localStorage.setItem('jwtToken', response.access_token);
        await router.push('/');
    } catch (error) {
        throw error;
    }
};

export const register = async (username, password, phone) => {
    try {
        const response = await authClient.post('/register', { username, password, phone }); // 注意这里应该是/register而不是/login
        localStorage.setItem('jwtToken', response.access_token);
        await router.push('/');
    } catch (error) {
        throw error;
    }
};

// 其他需要认证的API保持不变
export const checkAuth = async() => {
    try {
        const jwtToken = localStorage.getItem('jwtToken');
        let Authorization = null
        if (jwtToken) {
           Authorization = `Bearer ${jwtToken}`;
        }

        const response = await authClient.get('/checkAuth',{
            headers:{
                Authorization:Authorization
            }
        });

        return {
            isAuthenticated: true,
            user: {
                username: response.username,
                avatar: `/api/img/avator/${response.username}`,
            },
            carts: response.carts,
            isAdmin: response.isAdmin,
        };
    } catch (error) {
    }
};

export const logoutAuth = async() => {
    try {
        await apiClient.get('/logout');
        localStorage.removeItem('jwtToken');
        await router.push('/');
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const getAuth = async() => {
    try {
        return  await apiClient.post('/getAuth');
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const updateAddress = async (addrid,addr,is_default) => {
    try {
        await apiClient.post('/upAddress',{addrid,addr,is_default});
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const delAddress = async (addrid) => {
    try {
        await apiClient.post('/delAddress',{addrid});
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const addAddr = async (addr) => {
    try {
        return  await apiClient.post('/addAddress',{addr});
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};


export const updateAuth = async({ name = '', oldpwd = '', newpwd = '', phone = '' } = {}) => {
    try {

        // 校验 name
        const nameRegex = /^[a-zA-Z0-9\u4e00-\u9fa5]{2,10}$/; // 2-10个字符，支持字母、数字和中文
        if (name && !nameRegex.test(name)) {
            ElMessage.error("用户名必须为2-10个字符，支持字母、数字和中文。");
            return;
        }

        // 校验 newpwd
        const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>?/~`]{8,12}$/; // 8-12个字符，支持字母、数字和特殊字符
        if (newpwd && !passwordRegex.test(newpwd)) {
            ElMessage.error("密码必须为8-12个字符，支持字母、数字和特殊字符。");
            return;
        }

        // 校验 phone
        const phoneRegex = /^1[3-9]\d{9}$/; // 中国大陆手机号码格式
        if (phone && !phoneRegex.test(phone)) {
            ElMessage.error("手机号码格式不正确。");
            return;
        }

        await apiClient.post('/updateAuth',{ name, oldpwd, newpwd, phone });

    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const uploadAvatar = async (formData) => {
    try {
        return  await apiClient.post('/uploadAvatar', {formData},{
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};

export const getUserList = async(params) => {
    try {
        return await apiClient.get('/getUserList', {params});
    } catch (error) {
        // 错误已经在拦截器中处理，这里可以选择是否继续抛出
        throw error;
    }
};