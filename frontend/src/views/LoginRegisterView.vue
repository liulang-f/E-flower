<template>
  <Header/>
  <div class="login-register-container">
    <div class="form-block">
      <!-- 登录表单 -->
      <div class="login-form">
        <h2>登录</h2>
        <form @submit.prevent="login">
          <div class="form-group">
            <label for="login-username">用户名</label>
            <input type="text" id="login-username" v-model="loginForm.username" required />
          </div>
          <div class="form-group">
            <label for="login-password">密码</label>
            <input type="password" id="login-password" v-model="loginForm.password" required />
          </div>
          <button type="submit">登录</button>
        </form>
      </div>

      <!-- 注册表单 -->
      <div class="register-form">
        <h2>注册</h2>
        <form @submit.prevent="register">
          <div class="form-group">
            <label for="register-nickname">昵称</label>
            <input type="text" id="register-nickname" v-model="registerForm.nickname" @input="validateNickname" required />
            <span v-if="nicknameError" class="error">{{ nicknameError }}</span>
          </div>
          <div class="form-group">
            <label for="register-password">密码</label>
            <input type="password" id="register-password" v-model="registerForm.password" @input="validatePassword" required />
            <span v-if="passwordError" class="error">{{ passwordError }}</span>
          </div>
          <div class="form-group">
            <label for="register-phone">手机号</label>
            <input type="text" id="register-phone" v-model="registerForm.phone" @input="validatePhone" required />
            <span v-if="phoneError" class="error">{{ phoneError }}</span>
          </div>
          <!-- 验证码输入和发送按钮 -->
          <div class="form-group captcha-group">
            <label for="register-captcha">验证码</label>
            <div class="captcha-container">
              <input type="text" class="captcha-input" id="register-captcha" v-model="registerForm.captcha" required />
              <button @click.prevent="sendCaptcha" class="captcha-btn">发送验证码</button>
            </div>
          </div>
          <button type="submit">注册</button>
        </form>
      </div>

      <!-- 滑动切换块 -->
      <div class="overlay" :class="{ 'to-left': isRegister }" @click="toggleForm">
        <div class="overlay-content">
          <h3 v-if="!isRegister" class="over-titile">新朋友？</h3>
          <h3 v-else class="over-titile">老朋友？</h3>
          <p v-if="!isRegister" class="over-des">点我注册</p>
          <p v-else class="over-des">点我登录</p>
          <button>{{ isRegister ? '切换登录' : '切换注册' }}</button>
        </div>
      </div>
    </div>
  </div>
  <Footer/>
</template>

<script>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { login, register } from '@/api/auth';
import Header from '@/components/Header.vue';
import Footer from "@/components/Footer.vue";

export default {
  components: {
    Header,
    Footer,
  },
  name: 'LoginRegister',
  setup() {
    const isRegister = ref(false);

    const loginForm = ref({
      username: '',
      password: '',
    });

    const registerForm = ref({
      nickname: '',
      password: '',
      phone: '',
      captcha: '',
    });

    const nicknameError = ref('');
    const passwordError = ref('');
    const phoneError = ref('');

    // 昵称验证
    const validateNickname = () => {
      nicknameError.value =
          registerForm.value.nickname.length < 2 || registerForm.value.nickname.length > 10
              ? '昵称必须是2-10位'
              : '';
    };

    // 密码验证
    const validatePassword = () => {
      passwordError.value =
          registerForm.value.password.length < 8 || registerForm.value.password.length > 12
              ? '密码必须是8-12位'
              : '';
    };

    // 手机号验证
    const validatePhone = () => {
      const phoneRegex = /^1[3-9]\d{9}$/;
      phoneError.value = !phoneRegex.test(registerForm.value.phone) ? '手机号格式不正确' : '';
    };

    // 登录
    const handleLogin = async () => {
      if (!loginForm.value.username || !loginForm.value.password) {
        ElMessage.error('请填写完整信息');
        return;
      }
      await login(loginForm.value.username, loginForm.value.password);
    };

    // 注册
    const handleRegister = async () => {
      if (!registerForm.value.nickname || !registerForm.value.password || !registerForm.value.phone) {
        ElMessage.error('请填写完整信息');
        return;
      }

      if (nicknameError.value || passwordError.value || phoneError.value) {
        ElMessage.error('请检查填写的信息是否正确');
        return;
      }

      try {
        await register(
            registerForm.value.nickname,
            registerForm.value.password,
            registerForm.value.phone
        );
      } catch (error) {
        console.error(error);
      }
    };

    const toggleForm = () => {
      isRegister.value = !isRegister.value;
    };

    const sendCaptcha = () => {
      ElMessage.success('验证码发送成功！');
    };

    return {
      isRegister,
      loginForm,
      registerForm,
      nicknameError,
      passwordError,
      phoneError,
      validateNickname,
      validatePassword,
      validatePhone,
      toggleForm,
      login: handleLogin,
      register: handleRegister,
      sendCaptcha,
    };
  },
};
</script>


<style scoped>
/* 整体背景虚化 */
.login-register-container {
  display: flex;
  height: 100vh;
  background-size: cover;
  justify-content: center;
  align-items: center;
  position: relative; /* 确保伪元素相对于容器定位 */
}

.login-register-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('@/assets/images/bg-login.png') no-repeat center center;
  background-size: cover;
  filter: blur(2px); /* 调整模糊程度 */
  opacity: 0.8; /* 调整透明度，0是完全透明，1是不透明 */
  z-index: -1; /* 将伪元素放在容器内容的后面 */
}
/* 表单外壳 */
.form-block {
  display: flex;
  width: 800px;
  height: 500px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

/* 登录和注册表单 */
.login-form,
.register-form {
  width: 50%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 输入框和标签 */
.form-group {
  width: 90%;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  color: #bcb970;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #5454b1;
}

/* 输入框样式 */
.form-group input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: none;
  background: rgba(255, 255, 255, 0.7);
}

/* 验证码部分 */
.captcha-container {
  display: flex;
  gap: 10px;
  height: 30px;
  width: 310px;
}

.captcha-input{
  width: 50%;
  padding: 10px;
  border-radius: 5px;
  border: none;
  background: rgba(255, 255, 255, 0.7);
}

.captcha-btn {
  padding: 5px 15px;
  margin: auto;
  font-size: 0.9em;
  width: 60%;
}

/* 按钮样式 */
button {
  padding: 10px 20px;
  border: none;
  background-color: #7dcf62;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background-color: #236a0c;
}

/* 覆盖板 */
.overlay {
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.5s ease;
  overflow: hidden; /* 防止模糊溢出 */
  z-index: 2;
}

.overlay::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('@/assets/images/bg-login-1.png') no-repeat center center;
  background-size: cover;
  filter: blur(1px); /* 只对背景图片进行模糊 */
  z-index: -1; /* 将背景图片放在内容后面 */
}

.overlay.to-left {
  transform: translateX(-100%);
}

/* 错误信息 */
.error {
  color: red;
  font-size: 0.8em;
}

.over-titile{
  background: #e0e0e0;
  background: rgba(255, 255, 255, 0.7);
  text-align: center;
}

.over-des{
  background: #e0e0e0;
  background: rgba(255, 255, 255, 0.7);
  color: #9fc894;
  text-align: center;
}

.overlay-content{
  margin: auto;
}
</style>
