<template>
  <Header/>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人中心</h1>
      <p>欢迎回来，{{ userData.username}}</p>
    </div>

    <div class="tabs-container">
      <div class="tabs">
        <div
            v-for="(tab, index) in tabs"
            :key="index"
            :class="['tab', { active: activeTab === index }]"
            @click="activeTab = index"
        >
          {{ tab.name }}
        </div>
      </div>

      <!-- 个人信息管理 -->
      <div v-if="activeTab === 0" class="tab-content">
        <div class="personal-info">
          <div class="avatar-section">
            <div class="avatar-container">
              <img
                  v-if="userData.username && hasAvatar"
                  :src="`/api/img/avator/${userData.username}`"
                  alt="用户头像"
                  class="avatar"
              />
              <div v-else class="no-avatar">
                <i class="fas fa-user"></i>
                <p>暂无头像</p>
              </div>
            </div>
            <div class="upload-btn">
              <label for="avatar-upload" class="custom-file-upload">
                更换头像
              </label>
              <input
                  type="file"
                  id="avatar-upload"
                  accept="image/*"
                  @change="handleAvatarChange"
              />
            </div>
          </div>

          <div class="info-form">
            <div class="form-group">
              <label>用户名</label>
              <input v-model="tempUsername" :disabled="!editingUsername" />
              <button @click="toggleEdit('username')" class="edit-btn">
                {{ editingUsername ? '保存' : '编辑' }}
              </button>
            </div>

            <div class="form-group">
              <label>手机号码</label>
              <input v-model="tempPhone" :disabled="!editingPhone" />
              <button @click="toggleEdit('phone')" class="edit-btn">
                {{ editingPhone ? '保存' : '编辑' }}
              </button>
            </div>

            <div class="form-group password-group">
              <label>密码管理</label>
              <button @click="showPasswordModal = true" class="change-password-btn">
                修改密码
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 收货地址管理 -->
      <div v-if="activeTab === 1" class="tab-content">
        <div class="address-management">
          <h2>我的收货地址</h2>

          <div v-if="userData.address && userData.address.length > 0" class="address-list">
            <div
                v-for="addr in userData.address"
                :key="addr.id"
                :class="['address-item', { 'default-address': addr.is_default }]"
            >
              <div class="address-content">
                <p class="address-text">{{ addr.address }}</p>
                <div class="address-tags">
                  <span v-if="addr.is_default" class="default-tag">默认地址</span>
                </div>
              </div>
              <div class="address-actions">
                <button @click="editAddress(addr)" class="address-btn edit">编辑</button>
                <button @click="deleteAddress(addr.id)" class="address-btn delete">删除</button>
                <button
                    v-if="!addr.is_default"
                    @click="setDefaultAddress(addr.id,addr.address,1)"
                    class="address-btn set-default"
                >
                  设为默认
                </button>
              </div>
            </div>
          </div>

          <div v-else class="no-address">
            <p>您还没有添加收货地址</p>
          </div>

          <button @click="showAddressModal = true" class="add-address-btn">
            <i class="fas fa-plus"></i> 添加新地址
          </button>
        </div>
      </div>

      <!-- 客服交流 -->
      <div v-if="activeTab === 2" class="tab-content">
        <div class="customer-service">
          <h2>客服机器人</h2>

          <div class="chat-container">
            <div class="chat-messages" ref="chatMessages_ref">
            <div
                  v-for="(message, index) in chatMessages"
                  :key="index"
                  :class="['message', message.sender === 'user' ? 'user-message' : 'admin-message']"
              >
                <div class="message-avatar">
                  <img
                      v-if="message.sender === 'admin'"
                      src="@/assets/images/admin-avatar.png"
                      alt="客服头像"
                  />
                  <img
                      v-else-if="hasAvatar"
                      :src="`/api/img/avator/${userData.username}`"
                      alt="用户头像"
                  />
                  <div v-else class="message-no-avatar">
                    <i class="fas fa-user"></i>
                  </div>
                </div>
                <div class="message-content">
                  <p class="message-sender">{{ message.sender === 'user' ? userData.username : '客服' }}</p>
                  <p class="message-text">{{ message.text }}</p>
                  <p class="message-time">{{ message.time }}</p>
                </div>
              </div>
            </div>

            <div class="chat-input">
              <textarea
                  v-model="newMessage"
                  @keyup.enter="sendMessage"
                  placeholder="请输入您的问题..."
              ></textarea>
              <button @click="sendMessage" :disabled="!newMessage.trim()">
                发送
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 修改密码弹窗 -->
  <div v-if="showPasswordModal" class="modal-backdrop">
    <div class="modal password-modal">
      <h3>修改密码</h3>
      <div class="form-group">
        <label>原密码</label>
        <input type="password" v-model="passwordData.oldPassword" />
      </div>
      <div class="form-group">
        <label>新密码</label>
        <input type="password" v-model="passwordData.newPassword" />
      </div>
      <div class="form-group">
        <label>确认新密码</label>
        <input type="password" v-model="passwordData.confirmPassword" />
      </div>
      <div class="error-message" v-if="passwordError">
        {{ passwordError }}
      </div>
      <div class="modal-actions">
        <button @click="showPasswordModal = false" class="cancel-btn">取消</button>
        <button @click="changePassword" class="confirm-btn">确认修改</button>
      </div>
    </div>
  </div>

  <!-- 添加/编辑地址弹窗 -->
  <div v-if="showAddressModal" class="modal-backdrop">
    <div class="modal address-modal">
      <h3>{{ editingAddressId ? '编辑地址' : '添加新地址' }}</h3>
      <div class="form-group">
        <label>收货地址</label>
        <textarea v-model="addressData.address" placeholder="请输入详细地址信息"></textarea>
      </div>
      <div class="modal-actions">
        <button @click="cancelAddressEdit" class="cancel-btn">取消</button>
        <button @click="saveAddress" class="confirm-btn">
          {{ editingAddressId ? '保存修改' : '添加地址' }}
        </button>
      </div>
    </div>
  </div>
  <Footer/>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue';
import {uploadAvatar,updateAuth ,addAddr, delAddress, updateAddress, getAuth} from '@/api/auth';
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: 'UserProfile',
  components: {Header, Footer},
  setup() {
    // 标签页设置
    const tabs = [
      { name: '个人信息' },
      { name: '收货地址' },
      { name: '通用问题' }
    ];
    const activeTab = ref(0);

    // 用户数据
    const userData = reactive({
      username: '',
      phone: '',
      address: []
    });

    const tempUsername = ref("")
    const tempPhone = ref("")

    // 头像状态
    const hasAvatar = ref(false);

    // 编辑状态
    const editingUsername = ref(false);
    const editingPhone = ref(false);

    // 密码修改
    const showPasswordModal = ref(false);
    const passwordData = reactive({
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    });
    const passwordError = ref('');

    // 地址管理
    const showAddressModal = ref(false);
    const editingAddressId = ref(null);
    const addressData = reactive({
      address: '',
      is_default: false
    });

    // 客服聊天
    const chatMessages = ref([
      {
        sender: 'admin',
        text: '您好，欢迎来到花语客服中心，有什么可以帮助您的吗？',
        time: formatTime(new Date())
      }
    ]);
    const newMessage = ref('');
    const chatMessages_ref = ref(null);

    // 加载用户数据
    const loadUserData = async () => {
      try {
        const data = await getAuth();
        userData.username = data.username;
        userData.phone = data.phone;
        userData.address = data.address || [];
        tempUsername.value = userData.username
        tempPhone.value = userData.phone

        // 检查用户是否有头像
        await checkAvatar();
      } catch (error) {
        console.error('获取用户数据失败:', error);
      }
    };

    // 检查用户头像
    const checkAvatar = async () => {
      if (!userData.username) return;

      try {
        const response = await fetch(`/api/img/avator/${userData.username}`);
        hasAvatar.value = response.ok;
      } catch (error) {
        hasAvatar.value = false;
      }
    };


    // 处理头像上传
    const handleAvatarChange = async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      // 检查文件类型
      const allowedTypes = ['image/jpeg', 'image/png'];
      if (!allowedTypes.includes(file.type)) {
        alert('只支持 JPG 或 PNG 格式的图片');
        return;
      }

      // 检查文件大小（2MB = 2 * 1024 * 1024 bytes）
      const maxSize = 2 * 1024 * 1024;
      if (file.size > maxSize) {
        alert('文件大小不能超过 2MB');
        return;
      }

      // 创建 FormData 并添加文件
      const formData = new FormData();
      formData.append('avatar', file);

      try {
        // 调用上传接口
        await uploadAvatar(formData);
        window.location.reload();
        // 更新头像状态
      } catch (error) {
        console.log(error);
      }
    };

    // 切换编辑状态
    const toggleEdit = async (field) => {
      if (field === 'username') {
        if (editingUsername.value) {
          if(userData.username !== tempUsername.value) {
            await updateAuth({name: tempUsername.value})
          }
          editingUsername.value = false;
          await loadUserData();
        } else {
          editingUsername.value = true;
        }
      } else if (field === 'phone') {
        if (editingPhone.value) {
          // 保存手机号
          if(userData.phone !== tempPhone.value) {
            await updateAuth({phone: tempPhone.value})
          }
          editingPhone.value = false;
          await loadUserData();
        } else {
          editingPhone.value = true;
        }
      }
    };

    // 修改密码
    const changePassword = async () => {
      // 验证新密码
      if (!passwordData.oldPassword) {
        passwordError.value = '请输入原密码';
        return;
      }

      if (!passwordData.newPassword) {
        passwordError.value = '请输入新密码';
        return;
      }

      if (passwordData.newPassword !== passwordData.confirmPassword) {
        passwordError.value = '两次输入的密码不一致';
        return;
      }

      try {
        // 这里添加修改密码的接口调用
        await updateAuth({oldpwd:passwordData.oldPassword,newpwd:passwordData.newPassword})

        // 重置密码数据
        passwordData.oldPassword = '';
        passwordData.newPassword = '';
        passwordData.confirmPassword = '';
        passwordError.value = '';
        loadUserData();

        // 关闭弹窗
        showPasswordModal.value = false;
      } catch (error) {
        passwordError.value = '密码修改失败，请检查原密码是否正确';
      }
    };

    // 编辑地址
    const editAddress = (address) => {
      editingAddressId.value = address.id;
      addressData.address = address.address;
      addressData.is_default = address.is_default;
      showAddressModal.value = true;
    };

    // 删除地址
    const deleteAddress = async (id) => {
      try {
        await delAddress(id);
        // 更新本地数据
        userData.address = userData.address.filter(addr => addr.id !== id);
      } catch (error) {
        console.error('删除地址失败:', error);
      }
    };

    // 设为默认地址
    const setDefaultAddress = async (id,addr,d) => {
      try {
        // 这里添加设置默认地址的接口调用
        await updateAddress(id,addr,d);

        // 更新本地数据
        userData.address.forEach(addr => {
          addr.is_default = addr.id === id;
        });
      } catch (error) {
        console.error('设置默认地址失败:', error);
      }
    };

    // 取消地址编辑
    const cancelAddressEdit = () => {
      editingAddressId.value = null;
      addressData.address = '';
      addressData.is_default = false;
      showAddressModal.value = false;
    };

    // 保存地址
    const saveAddress = async () => {
      if (!addressData.address.trim()) {
        return;
      }

      try {
        if (editingAddressId.value) {
          // 编辑现有地址
          await updateAddress(editingAddressId.value, addressData.address,addressData.is_default);
          // 更新本地数据
          const index = userData.address.findIndex(addr => addr.id === editingAddressId.value);
          if (index !== -1) {
            userData.address[index].address = addressData.address;

            // 如果设为默认，更新其他地址状态
            if (addressData.is_default) {
              userData.address.forEach((addr, i) => {
                addr.is_default = i === index;
              });
            } else {
              userData.address[index].is_default = false;
            }
          }
        } else {
          // 添加新地址
          // 模拟后端生成ID
          const addr = (await addAddr(addressData.address)).addr;
          // 更新本地数据
          userData.address.push({
            id: addr.id,
            address: addr.addr,
            is_default: addr.is_default
          });

        }

        // 重置表单
        cancelAddressEdit();
      } catch (error) {
        console.error('保存地址失败:', error);
      }
    };

    // 发送消息
    const sendMessage = () => {
      if (!newMessage.value.trim()) return;

      const currentTime = new Date();

      // 添加用户消息
      chatMessages.value.push({
        sender: 'user',
        text: newMessage.value,
        time: formatTime(currentTime)
      });

      // 清空输入框
      const message = newMessage.value;
      newMessage.value = '';

      // 模拟客服回复
      setTimeout(() => {
        chatMessages.value.push({
          sender: 'admin',
          text: getAutoReply(message),
          time: formatTime(new Date())
        });

        // 滚动到底部
        scrollToBottom();
      }, 1000);
    };

    // 滚动到聊天底部
    const scrollToBottom = () => {
      if (chatMessages_ref.value) {
        setTimeout(() => {
          chatMessages_ref.value.scrollTop = chatMessages_ref.value.scrollHeight;
        }, 50);
      }
    };

    // 格式化时间
    function formatTime(date) {
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
    }

    // 获取自动回复
    function getAutoReply(message) {
      // 转换为小写，避免区分大小写
      const lowerMessage = message.toLowerCase();

      if (lowerMessage.includes('发货') || lowerMessage.includes('物流')) {
        return '您的订单正在处理中，一般会在1-3个工作日内发货，发货后您会收到物流信息。';
      } else if (lowerMessage.includes('价格') || lowerMessage.includes('多少钱')) {
        return '我们的花束价格在不同季节可能会有所变动，建议您查看商品详情页了解最新价格。';
      } else if (lowerMessage.includes('退款') || lowerMessage.includes('退货')) {
        return '如需退款或退货，请提供您的订单号，我们的客服会尽快为您处理。';
      } else if (lowerMessage.includes('营业时间') || lowerMessage.includes('几点关门')) {
        return '我们的营业时间是每天早上9点到晚上8点，节假日时间可能会有所调整。';
      } else if (lowerMessage.includes('地址') || lowerMessage.includes('怎么去')) {
        return '我们的花店地址是：北京市朝阳区幸福路123号，欢迎随时光临！';
      } else if (lowerMessage.includes('付款方式') || lowerMessage.includes('支付')) {
        return '我们支持微信支付、支付宝、信用卡等多种支付方式。';
      } else if (lowerMessage.includes('优惠') || lowerMessage.includes('折扣')) {
        return '我们不定期会有优惠活动，建议您关注我们的公众号或官网获取最新优惠信息。';
      } else if (lowerMessage.includes('鲜花种类') || lowerMessage.includes('有哪些花')) {
        return '我们提供玫瑰、百合、康乃馨、向日葵等多种鲜花，具体种类请查看商品详情页。';
      } else if (lowerMessage.includes('花语') || lowerMessage.includes('含义')) {
        return '不同的花朵有不同的花语，例如红玫瑰代表热恋，百合象征纯洁与祝福。';
      } else if (lowerMessage.includes('人工客服') || lowerMessage.includes('转人工')) {
        return '好的，如果您需要人工客服请拨打我们的服务电话！1999999999。';
      } else if (lowerMessage.includes('谢谢') || lowerMessage.includes('辛苦了')) {
        return '不客气，祝您生活愉快！如果还有其他问题，随时告诉我哦。';
      } else if (lowerMessage.includes('你好') || lowerMessage.includes('在吗')) {
        return '您好，我是小花助手，很高兴为您服务！请问有什么我可以帮忙的吗？';
      } else if (lowerMessage.includes('再见') || lowerMessage.includes('拜拜')) {
        return '再见，期待下次为您服务！';
      } else if (lowerMessage.includes('天气')) {
        return '我暂时还不会看天气哦，建议您使用天气预报工具查询最新天气信息。';
      } else if (lowerMessage.includes('生日') || lowerMessage.includes('纪念日')) {
        return '送花庆祝生日或纪念日是非常浪漫的选择，我们有许多花束适合这些场合！';
      } else if (lowerMessage.includes('快递') || lowerMessage.includes('物流')) {
        return '我们发送的是邮政！';
      } else {
        return '不好意思，小机器人暂时不太了解，请您电话联系客服呢！1999999999';
      }
    }


    // 监听聊天消息变化，自动滚动到底部
    watch(chatMessages, () => {
      scrollToBottom();
    });

    onMounted(() => {
      loadUserData();
    });

    return {
      tempPhone,
      tempUsername,
      tabs,
      activeTab,
      userData,
      hasAvatar,
      editingUsername,
      editingPhone,
      handleAvatarChange,
      toggleEdit,
      showPasswordModal,
      passwordData,
      passwordError,
      changePassword,
      showAddressModal,
      editingAddressId,
      addressData,
      editAddress,
      deleteAddress,
      setDefaultAddress,
      cancelAddressEdit,
      saveAddress,
      chatMessages,
      newMessage,
      sendMessage,
      chatMessages_ref
    };
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
}

.profile-header {
  text-align: center;
  margin-bottom: 30px;
}

.profile-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.profile-header p {
  color: #666;
  font-size: 16px;
}

.tabs-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.tab {
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
  color: #666;
  border-bottom: 2px solid transparent;
}

.tab.active {
  color: #ff6b81;
  border-bottom-color: #ff6b81;
  font-weight: 500;
}

.tab-content {
  padding: 30px;
}

/* 个人信息样式 */
.personal-info {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-container {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 15px;
  background: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #ccc;
}

.no-avatar i {
  font-size: 50px;
  margin-bottom: 5px;
}

.no-avatar p {
  font-size: 14px;
}

.upload-btn {
  margin-top: 10px;
}

.custom-file-upload {
  display: inline-block;
  padding: 8px 16px;
  cursor: pointer;
  background: #ff6b81;
  color: white;
  border-radius: 4px;
  font-size: 14px;
  transition: background 0.3s;
}

.custom-file-upload:hover {
  background: #ff5267;
}

input[type="file"] {
  display: none;
}

.info-form {
  flex: 1;
  min-width: 300px;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  color: #333;
  transition: border-color 0.3s;
}

.form-group input:focus, .form-group textarea:focus {
  border-color: #ff6b81;
  outline: none;
}

.form-group input:disabled {
  background-color: #f9f9f9;
  color: #666;
}

.edit-btn {
  position: absolute;
  right: 0;
  top: 32px;
  background: transparent;
  border: none;
  color: #ff6b81;
  cursor: pointer;
  font-size: 14px;
}

.change-password-btn {
  background: #f5f5f5;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.change-password-btn:hover {
  background: #eee;
}

/* 地址管理样式 */
.address-management h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 20px;
}

.address-list {
  margin-bottom: 20px;
}

.address-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.address-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.default-address {
  border-color: #ff6b81;
  background-color: rgba(255, 107, 129, 0.05);
}

.address-content {
  flex: 1;
}

.address-text {
  margin-bottom: 8px;
  font-size: 15px;
  color: #333;
}

.address-tags {
  display: flex;
  gap: 8px;
}

.default-tag {
  display: inline-block;
  padding: 2px 8px;
  background-color: #ff6b81;
  color: white;
  border-radius: 3px;
  font-size: 12px;
}

.address-actions {
  display: flex;
  gap: 10px;
}

.address-btn {
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 3px;
  transition: all 0.3s;
}

.address-btn.edit {
  color: #2196f3;
}

.address-btn.delete {
  color: #f44336;
}

.address-btn.set-default {
  color: #4caf50;
}

.address-btn:hover {
  background-color: #f5f5f5;
}

.no-address {
  text-align: center;
  padding: 30px 0;
  color: #999;
}

.add-address-btn {
  background: #ff6b81;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
}

.add-address-btn:hover {
  background: #ff5267;
}

/* 客服交流样式 */
.customer-service h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 20px;
}

.chat-container {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 500px;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.message {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: #eee;
  flex-shrink: 0;
}

.message-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-no-avatar {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ccc;
}

.message-content {
  max-width: 70%;
  background: white;
  padding: 12px 15px;
  border-radius: 8px;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.user-message .message-content {
  background-color: #ff6b81;
  color: white;
}

.message-sender {
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.user-message .message-sender {
  color: rgba(255, 255, 255, 0.8);
}

.message-text {
  font-size: 15px;
  line-height: 1.5;
  word-break: break-word;
}

.message-time {
  font-size: 11px;
  color: #999;
  text-align: right;
  margin-top: 5px;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.chat-input {
  padding: 15px;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.chat-input textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px 12px;
  resize: none;
  height: 60px;
  font-family: inherit;
  font-size: 15px;
}

.chat-input textarea:focus {
  outline: none;
  border-color: #ff6b81;
}

.chat-input button {
  align-self: flex-end;
  background: #ff6b81;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.3s;
}
.chat-input button:hover {
  background: #ff5267;
}

.chat-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 弹窗样式 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  padding: 25px;
  width: 90%;
  max-width: 480px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 20px;
}

.error-message {
  color: #f44336;
  font-size: 14px;
  margin: 10px 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.cancel-btn:hover {
  background: #eee;
}

.confirm-btn {
  background: #ff6b81;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.confirm-btn:hover {
  background: #ff5267;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.checkbox-group label {
  margin-bottom: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .personal-info {
    flex-direction: column;
    gap: 20px;
  }

  .avatar-section {
    align-items: center;
    margin-bottom: 20px;
  }

  .tabs {
    flex-wrap: wrap;
  }

  .tab {
    flex: 1;
    text-align: center;
    padding: 12px 10px;
    font-size: 14px;
  }

  .message-content {
    max-width: 85%;
  }

  .address-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .address-actions {
    margin-top: 10px;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>