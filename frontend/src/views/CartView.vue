<template>
  <Header/>
  <div class="cart-container">
    <div class="cart-header">
      <h1>欢迎下单🌺</h1>
      <p>城内下单，三小时必达！快递默认发顺风加急，请您放心下单！</p>
      <div v-if="cartItems.length === 0" class="empty-cart">
        <p>您的购物车是空的</p>
        <router-link to="/" class="btn-primary">去选购鲜花</router-link>
      </div>
    </div>

    <div v-if="cartItems.length > 0" class="cart-content">
      <!-- 商品列表 -->
      <div class="cart-items-container">
        <div class="select-all">
          <div class="select-all-left">
            <label class="checkbox-container">
              <input type="checkbox" v-model="allSelected" @change="toggleSelectAll">
              <span class="checkmark"></span>
              全选
            </label>
            <p>已选择 {{ selectedItems.length }} 件商品</p>
          </div>
          <div class="cart-actions">
            <button class="clear-cart-btn"  @click="showConfirmModal = true">
              <i class="trash-icon">🗑️</i> 清空购物车
            </button>
          </div>
        </div>

        <div v-if="showConfirmModal" class="modal-overlay">
          <div class="modal">
            <p>确定要清空吗？</p>
            <div class="modal-buttons">
              <button @click="clearCart">确定</button>
              <button @click="showConfirmModal = false">取消</button>
            </div>
          </div>
        </div>

        <div class="cart-items-scroll">
          <div class="cart-items">
            <div v-for="item in cartItems" :key="item.cart_id" class="cart-item">
              <label class="checkbox-container">
                <input type="checkbox" v-model="selectedItemIds" :value="item.cart_id">
                <span class="checkmark"></span>
              </label>

              <div class="item-image">
                <img :src="`api/img/${item.flower_name}`" :alt="item.flower_name" />
              </div>

              <div class="item-details">
                <h3>{{ item.flower_name }}</h3>
                <div class="price-container">
                  <p v-if="item.discount" class="original-price">¥{{ item.price.toFixed(2) }}</p>
                  <p class="item-price" :class="{ 'discounted': item.discount }">
                    ¥{{ (item.discount ? item.price * (1 - item.discount/100) : item.price).toFixed(2) }}
                  </p>
                  <span v-if="item.discount" class="discount-tag">{{ ((1-item.discount)*100).toFixed(2) }}% OFF</span>
                </div>
              </div>

              <div class="quantity-control">
                <button @click="decreaseQuantity(item)" :disabled="item.quantity <= 1">-</button>
                <input type="number" v-model.number="item.quantity" min="1" @change="updateQuantity(item)">
                <button @click="increaseQuantity(item)">+</button>
              </div>

              <div class="item-subtotal">
                <p>¥{{ getItemSubtotal(item).toFixed(2) }}</p>
              </div>

              <button class="delete-btn" @click="removeFromCart(item.cart_id)">
                <i class="remove-icon">×</i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 结算区域 -->
      <div class="checkout-container">
        <!-- 收货地址选择 -->
        <div class="address-selection">
          <h3>收货地址</h3>
          <div v-if="addresses.length === 0" class="no-address">
            <p>您还没有添加收货地址</p>
            <router-link to="/AuthInfo" class="btn-primary">添加地址</router-link>
          </div>

          <div v-else class="address-list">
            <div v-for="addr in addresses" :key="addr.id"
                 class="address-item"
                 :class="{ 'selected': selectedAddress.id === addr.id }"
                 @click="selectAddress(addr)">
              <div class="address-info">
                <p>{{ addr.address }}</p>
                <span v-if="addr.is_default" class="default-tag">默认</span>
              </div>
            </div>
            <router-link to="/AuthInfo" class="add-address-btn">
              <i class="plus-icon">+</i>
              添加新地址
            </router-link>
          </div>
        </div>

        <!-- 订单摘要 -->
        <div class="order-summary">
          <h3>订单摘要</h3>
          <div class="summary-row">
            <span>商品总价</span>
            <span>¥{{ totalPrice.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>运费</span>
            <span>¥{{ shipping.toFixed(2) }}</span>
          </div>
          <div class="summary-row discount" v-if="discount > 0">
            <span>折扣</span>
            <span>-¥{{ discount.toFixed(2) }}</span>
          </div>
          <div class="summary-row total">
            <span>总计</span>
            <span>¥{{ finalTotal.toFixed(2) }}</span>
          </div>

          <div class="coupon-input">
            <input type="text" v-model="couponCode" placeholder="输入优惠码">
            <button @click="applyCoupon" :disabled="!couponCode">应用</button>
          </div>

          <button class="checkout-btn"
                  @click="proceedToCheckout"
                  :disabled="selectedItems.length === 0">
            结算 ({{ selectedItems.length }})
          </button>
        </div>
      </div>
    </div>

    <!-- 支付弹窗 -->
    <div class="payment-modal" v-if="showPaymentModal">
      <div class="modal-content">
        <h2>确认支付</h2>
        <div class="order-details">
          <p>共 {{ selectedItems.length }} 件商品</p>
          <p>收货地址: {{ selectedAddress.address || '未选择地址' }}</p>
          <p class="modal-total">总计: ¥{{ finalTotal.toFixed(2) }}</p>
        </div>
        <div class="payment-methods">
          <div class="payment-method"
               v-for="method in paymentMethods"
               :key="method.id"
               :class="{ 'selected': selectedPaymentMethod === method.id }"
               @click="selectedPaymentMethod = method.id">
            <img :src="method.icon" :alt="method.name" style="width: 100px; height: 90px;">
            <span>{{ method.name }}</span>
          </div>
        </div>
        <div class="modal-buttons">
          <button class="btn-cancel" @click="cancelPayment">取消</button>
          <button class="btn-later" @click="payLater">稍后支付</button>
          <button class="btn-confirm" @click="confirmPayment">确认支付</button>
        </div>
      </div>
    </div>

    <!-- 支付结果提示 -->
    <div class="payment-result" v-if="showPaymentResult">
      <div class="result-content">
        <div class="result-icon" :class="{ 'success': paymentSuccess }">
          <i v-if="paymentSuccess" class="success-icon">✓</i>
          <i v-else class="pending-icon">⏱</i>
        </div>
        <h2>{{ paymentSuccess ? '支付成功' : '订单已保存' }}</h2>
        <p>{{ paymentSuccess ? '您的订单已提交，我们将尽快为您发货' : '您可以稍后在订单中心完成支付' }}</p>
        <div class="result-buttons">
          <button @click="shutDownPay()" class="btn-continue">继续购物</button>
          <router-link to="/orders" class="btn-orders">查看订单</router-link>
        </div>
      </div>
    </div>
  </div>
  <Footer/>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {getAuth} from "@/api/auth.js";
import {updateCart, delCart, getCarts, clearUserCart} from "@/api/cart.js";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import {addOrder} from "@/api/order.js";
import {ElMessage} from "element-plus";

export default {
  name: 'ShoppingCart',
  components: {Header, Footer},
  setup() {
    const router = useRouter()
    const cartItems = ref([])
    const addresses = ref([])
    const selectedItemIds = ref([])
    const selectedAddress = ref({})
    const couponCode = ref('')
    const discount = ref(0)
    const shipping = ref(10) // 默认运费
    const showPaymentModal = ref(false)
    const showPaymentResult = ref(false)
    const paymentSuccess = ref(false)
    const selectedPaymentMethod = ref(1)
    const showConfirmModal = ref(false)

    const paymentMethods = ref([
      { id: 1, name: '微信支付', icon: 'src/assets/images/微信.png' },
      { id: 2, name: '支付宝', icon: 'src/assets/images/支付宝.png' },
      { id: 3, name: '银行卡', icon: 'src/assets/images/visa.png' }
    ])

    // 获取购物车数据
    const fetchCartItems = async () => {
      cartItems.value = await getCarts();
    }

    const shutDownPay = () => {
      showPaymentResult.value = false
    }

    // 获取地址数据
    const fetchAddresses = async () => {
      try {
        const response = await getAuth();
        addresses.value = response.address || []

        // 设置默认地址
        if (addresses.value.length > 0) {
          const defaultAddress = addresses.value.find(addr => addr.is_default === 1)
          selectedAddress.value = defaultAddress || addresses.value[0]
        }
      } catch (error) {
        console.error('获取地址数据失败:', error)
      }
    }

    // 计算属性
    const selectedItems = computed(() => {
      return cartItems.value.filter(item => selectedItemIds.value.includes(item.cart_id))
    })

    const getItemSubtotal = (item) => {
      const actualPrice = item.discount ? item.price * (1 - item.discount/100) : item.price
      return actualPrice * item.quantity
    }

    const totalPrice = computed(() => {
      return selectedItems.value.reduce((sum, item) => sum + getItemSubtotal(item), 0)
    })

    const finalTotal = computed(() => {
      return totalPrice.value + shipping.value - discount.value
    })

    const allSelected = computed({
      get: () => {
        return cartItems.value.length > 0 && selectedItemIds.value.length === cartItems.value.length
      },
      set: (value) => {
        if (value) {
          selectedItemIds.value = cartItems.value.map(item => item.cart_id)
        } else {
          selectedItemIds.value = []
        }
      }
    })

    // 方法
    const toggleSelectAll = () => {
      if (allSelected.value) {
        selectedItemIds.value = cartItems.value.map(item => item.cart_id)
      } else {
        selectedItemIds.value = []
      }
    }

    const selectAddress = (address) => {
      selectedAddress.value = address
    }

    const increaseQuantity = (item) => {
      item.quantity++
      updateQuantity(item)
    }

    const decreaseQuantity = (item) => {
      if (item.quantity > 1) {
        item.quantity--
        updateQuantity(item)
      }
    }

    const updateQuantity = (item) => {
      // 这里可以添加更新购物车数量的API调用
      updateCart(item.flower_id,item.quantity)
    }

    const removeFromCart = async (cartId) => {
      try {
        await delCart(cartId)
        // 更新本地数据
        cartItems.value = cartItems.value.filter(item => item.cart_id !== cartId)
        selectedItemIds.value = selectedItemIds.value.filter(id => id !== cartId)
      } catch (error) {
        console.error('删除商品失败:', error)
      }
    }

    const applyCoupon = () => {
      // 模拟优惠码检查和应用
      if (couponCode.value === 'FLOWER10') {
        discount.value = totalPrice.value * 0.1
        alert('优惠码已应用！享受10%折扣')
      } else {
        alert('无效的优惠码')
        discount.value = 0
      }
      couponCode.value = ''
    }

    const proceedToCheckout = () => {
      if (selectedItems.value.length === 0) {
        ElMessage.error('请至少选择一件商品')
        return
      }

      if(!selectedAddress.value.address){
        ElMessage.error("请选择地址")
        return;
      }

      showPaymentModal.value = true
    }

    const cancelPayment = () => {
      showPaymentModal.value = false
    }

    const payLater = async () => {
      try {
        // 提交稍后支付的订单
        const orderData = {
          cart_ids: selectedItemIds.value,
          status: 'pending',
          address: selectedAddress.value.address || '',
          fTotal: finalTotal.value,
        }
        await addOrder(orderData)

        showPaymentModal.value = false
        paymentSuccess.value = false
        showPaymentResult.value = true

        // 成功后清除已选商品
        setTimeout(() => {
          removeSelectedItemsFromCart()
        }, 2000)
      } catch (error) {
        console.error('创建订单失败:', error)
      }
    }

    const confirmPayment = async () => {
      try {
        // 提交并支付订单
        const orderData = {
          cart_ids: selectedItemIds.value,
          status: 'paid',
          address: selectedAddress.value.address || '',
          fTotal: finalTotal.value,
        }
        await addOrder(orderData)
        showPaymentModal.value = false
        paymentSuccess.value = true
        showPaymentResult.value = true

        // 成功后清除已选商品
        setTimeout(() => {
          removeSelectedItemsFromCart()
        }, 2000)
      } catch (error) {
        console.error('支付失败:', error)
        alert('支付失败，请重试')
      }
    }

    const removeSelectedItemsFromCart = () => {
      cartItems.value = cartItems.value.filter(item => !selectedItemIds.value.includes(item.cart_id))
      selectedItemIds.value = []
    }

    const clearCart = async () => {
      await clearUserCart()
      showConfirmModal.value = false
      cartItems.value = []
      selectedItemIds.value = []
    }

    // 生命周期钩子
    onMounted(() => {
      fetchCartItems()
      fetchAddresses()
    })

    return {
      cartItems,
      addresses,
      selectedItemIds,
      selectedAddress,
      couponCode,
      discount,
      shipping,
      showPaymentModal,
      showPaymentResult,
      paymentSuccess,
      paymentMethods,
      selectedPaymentMethod,
      selectedItems,
      totalPrice,
      finalTotal,
      allSelected,
      toggleSelectAll,
      selectAddress,
      increaseQuantity,
      decreaseQuantity,
      updateQuantity,
      removeFromCart,
      clearCart,
      applyCoupon,
      proceedToCheckout,
      cancelPayment,
      payLater,
      confirmPayment,
      getItemSubtotal,
      shutDownPay,
      showConfirmModal,
    }
  }
}
</script>

<style scoped>
.cart-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #f8f9fa;
  min-height: 80vh;
}

.cart-header {
  margin-bottom: 30px;
  text-align: center;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.cart-header h1 {
  font-size: 32px;
  color: #ff6b6b;
  margin-bottom: 10px;
  font-weight: 600;
}

.cart-header p {
  color: #666;
  font-size: 16px;
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 40px;
  background-color: white;
  border-radius: 8px;
  margin-top: 30px;
}

.empty-cart p {
  margin: 20px 0;
  font-size: 18px;
  color: #666;
}

.btn-primary {
  background-color: #ff6b6b;
  color: white;
  padding: 12px 30px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
  box-shadow: 0 4px 6px rgba(255, 107, 107, 0.2);
}

.btn-primary:hover {
  background-color: #ff5252;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(255, 107, 107, 0.3);
}

.cart-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.cart-items-container {
  flex: 1 1 65%;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.select-all {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.select-all-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.cart-actions {
  display: flex;
  align-items: center;
}

.clear-cart-btn {
  display: flex;
  align-items: center;
  background-color: transparent;
  color: #ff6b6b;
  border: 1px solid #ff6b6b;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.clear-cart-btn:hover {
  background-color: #ff6b6b;
  color: white;
}

.trash-icon {
  margin-right: 6px;
  font-size: 16px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 16px;
  color: #333;
}

.checkbox-container input {
  margin-right: 10px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* 添加滚动区域 */
.cart-items-scroll {
  max-height: 600px;
  overflow-y: auto;
  padding-right: 5px;
  /* 滚动条样式 */
  scrollbar-width: thin;
  scrollbar-color: #ff6b6b #f1f1f1;
}

.cart-items-scroll::-webkit-scrollbar {
  width: 6px;
}

.cart-items-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.cart-items-scroll::-webkit-scrollbar-thumb {
  background: #ff6b6b;
  border-radius: 10px;
}

.cart-items-scroll::-webkit-scrollbar-thumb:hover {
  background: #ff5252;
}

.cart-items {
  padding: 10px 0;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.cart-item:hover {
  background-color: #f9f9f9;
}

.item-image {
  width: 100px;
  height: 100px;
  margin: 0 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.item-image img:hover {
  transform: scale(1.05);
}

.item-details {
  flex: 1;
}

.item-details h3 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.price-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.item-price {
  font-size: 18px;
  color: #ff6b6b;
  font-weight: 600;
}

.item-price.discounted {
  color: #ff4040;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.discount-tag {
  background-color: #ff4040;
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 500;
}

.quantity-control {
  display: flex;
  align-items: center;
  margin: 0 20px;
  background-color: #f9f9f9;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.quantity-control button {
  width: 36px;
  height: 36px;
  background-color: #f5f5f5;
  border: none;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.quantity-control button:hover:not(:disabled) {
  background-color: #eaeaea;
}

.quantity-control button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-control input {
  width: 45px;
  height: 36px;
  text-align: center;
  border: none;
  background-color: white;
  font-size: 16px;
}

.item-subtotal {
  width: 100px;
  text-align: right;
  font-weight: 600;
  color: #ff6b6b;
  font-size: 18px;
}

.delete-btn {
  margin-left: 20px;
  width: 36px;
  height: 36px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.delete-btn:hover {
  background-color: #ffeeee;
}

.remove-icon {
  font-size: 26px;
  color: #999;
  transition: color 0.2s;
}

.delete-btn:hover .remove-icon {
  color: #ff6b6b;
}

.checkout-container {
  flex: 1 1 30%;
  min-width: 300px;
}

.address-selection, .order-summary {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 25px;
  margin-bottom: 20px;
}

.address-selection h3, .order-summary h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #333;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.no-address {
  text-align: center;
  padding: 30px 0;
}

.address-list {
  max-height: 200px;
  overflow-y: auto;
  padding-right: 5px;
  /* 滚动条样式 */
  scrollbar-width: thin;
  scrollbar-color: #ff6b6b #f1f1f1;
}

.address-list::-webkit-scrollbar {
  width: 6px;
}

.address-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.address-list::-webkit-scrollbar-thumb {
  background: #ff6b6b;
  border-radius: 10px;
}

.address-list::-webkit-scrollbar-thumb:hover {
  background: #ff5252;
}

.address-item {
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 6px;
  margin-bottom: 10px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.address-item:hover {
  border-color: #ff6b6b;
  background-color: #fff9f9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.address-item.selected {
  border-color: #ff6b6b;
  background-color: #fff9f9;
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.1);
}

.address-info {
  word-break: break-all;
}

.default-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff6b6b;
  color: white;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.add-address-btn {
  display: flex;
  align-items: center;
  color: #666;
  text-decoration: none;
  padding: 15px;
  border: 1px dashed #ddd;
  border-radius: 6px;
  margin-top: 15px;
  transition: all 0.2s;
}

.add-address-btn:hover {
  color: #ff6b6b;
  border-color: #ff6b6b;
  background-color: #fff9f9;
}

.plus-icon {
  margin-right: 8px;
  font-size: 18px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  font-size: 16px;
}

.summary-row.total {
  margin-top: 15px;
  padding-top: 20px;
  border-top: 2px solid #eee;
  font-weight: bold;
  font-size: 20px;
  color: #ff6b6b;
}

.summary-row.discount {
  color: #ff6b6b;
}

.coupon-input {
  display: flex;
  margin: 25px 0;
}

.coupon-input input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px 0 0 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.coupon-input input:focus {
  outline: none;
  border-color: #ff6b6b;
}

.coupon-input button {
  padding: 12px 20px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.coupon-input button:hover:not(:disabled) {
  background-color: #ff5252;
}

.coupon-input button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.checkout-btn {
  width: 100%;
  padding: 15px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.checkout-btn:hover {
  background-color: #ff5252;
}

.checkout-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 弹窗样式 */
.payment-modal, .payment-result {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content, .result-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-content h2, .result-content h2 {
  text-align: center;
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.order-details {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.modal-total {
  font-weight: bold;
  color: #ff6b6b;
  font-size: 18px;
}

.payment-methods {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
}

.payment-method {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 4px;
  cursor: pointer;
}

.payment-method.selected {
  border-color: #ff6b6b;
  background-color: #fff9f9;
}

.payment-method img {
  margin-bottom: 8px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
}

.btn-cancel, .btn-later, .btn-confirm {
  padding: 12px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-cancel {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.btn-later {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.btn-confirm {
  background-color: #ff6b6b;
  color: white;
  border: none;
}

.btn-confirm:hover {
  background-color: #ff5252;
}

/* 支付结果样式 */
.result-content {
  text-align: center;
}

.result-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  background-color: #f5f5f5;
}

.result-icon.success {
  background-color: #e6f7ef;
}

.success-icon {
  color: #28a745;
  font-size: 40px;
}

.pending-icon {
  color: #ffc107;
  font-size: 40px;
}

.result-buttons {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  gap: 20px;
}

.btn-continue, .btn-orders {
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.3s;
}

.btn-continue {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.btn-orders {
  background-color: #ff6b6b;
  color: white;
  border: none;
}

.btn-orders:hover {
  background-color: #ff5252;
}

@media (max-width: 768px) {
  .cart-item {
    flex-wrap: wrap;
  }

  .item-image {
    margin: 0 10px 10px 0;
  }

  .item-details {
    width: calc(100% - 130px);
  }

  .quantity-control, .item-subtotal {
    margin-top: 10px;
  }

  .quantity-control {
    margin-right: auto;
  }

  .modal-buttons {
    flex-direction: column;
    gap: 10px;
  }

  .btn-cancel, .btn-later, .btn-confirm {
    width: 100%;
  }
}

/* 模态框遮罩层样式 */
.modal-overlay {
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

/* 模态框样式 */
.modal {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

.modal-buttons button {
  margin: 0 10px;
}
</style>