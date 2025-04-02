<template>
  <div v-if="show" class="payment-modal-overlay" @click.self="cancelPayment">
    <div class="payment-modal">
      <div class="payment-modal-header">
        <h2>订单支付</h2>
        <button class="close-btn" @click="cancelPayment">&times;</button>
      </div>

      <div class="payment-modal-body">
        <div class="order-amount">
          <span class="amount-label">支付金额</span>
          <span class="amount-value">{{ formatPrice(totalAmount) }}</span>
        </div>

        <div class="payment-methods">
          <h3>选择支付方式</h3>
          <div class="payment-method-options">
            <div
                v-for="method in paymentMethods"
                :key="method.id"
                :class="['payment-method-item', selectedMethod === method.id ? 'active' : '']"
                @click="selectPaymentMethod(method.id)"
            >
              <div class="payment-icon">
                <font-awesome-icon :icon="method.icon" />
              </div>
              <div class="payment-name">{{ method.name }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="payment-modal-footer">
        <button class="cancel-btn" @click="cancelPayment">取消支付</button>
        <button
            class="confirm-btn"
            :disabled="!selectedMethod"
            @click="confirmPayment"
        >
          确认支付
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faWeixin, faAlipay, faCcVisa } from '@fortawesome/free-brands-svg-icons';
import {buyFlowersNow} from "@/api/order.js";

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  totalAmount: {
    type: Number,
    required: true
  },
  orderId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['close', 'payment-success']);

const selectedMethod = ref('');

const paymentMethods = [
  { id: 'wechat', name: '微信支付', icon: faWeixin },
  { id: 'alipay', name: '支付宝', icon: faAlipay },
  { id: 'visa', name: 'Visa卡', icon: faCcVisa }
];

const selectPaymentMethod = (methodId) => {
  selectedMethod.value = methodId;
};

const formatPrice = (price) => {
  return `¥${parseFloat(price).toFixed(2)}`;
};

const confirmPayment = () => {
  if (!selectedMethod.value) return;

  // 在实际应用中，这里应该调用支付API
  // 模拟支付成功
  buyFlowersNow(props.orderId)

  setTimeout(() => {
    emit('payment-success', {
      orderId: props.orderId,
      method: selectedMethod.value,
      amount: props.totalAmount
    });
    // 重置并关闭
    selectedMethod.value = '';
    emit('close');
  }, 500);
};

const cancelPayment = () => {
  selectedMethod.value = '';
  emit('close');
};
</script>

<style scoped>
.payment-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.payment-modal {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: modal-in 0.3s ease-out;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.payment-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.payment-modal-header h2 {
  font-size: 20px;
  color: #333;
  margin: 0;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  transition: color 0.2s;
  line-height: 1;
}

.close-btn:hover {
  color: #f44336;
}

.payment-modal-body {
  padding: 20px;
}

.order-amount {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.amount-label {
  font-size: 16px;
  color: #666;
}

.amount-value {
  font-size: 24px;
  color: #f44336;
  font-weight: 700;
}

.payment-methods h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
  font-weight: 500;
}

.payment-method-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.payment-method-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.payment-method-item:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
}

.payment-method-item.active {
  background-color: #e8f5e9;
  border-color: #4caf50;
}

.payment-icon {
  font-size: 28px;
  margin-bottom: 10px;
  color: #555;
}

.payment-method-item.active .payment-icon {
  color: #4caf50;
}

.payment-method-item:nth-child(1) .payment-icon {
  color: #07c160;
}

.payment-method-item:nth-child(2) .payment-icon {
  color: #1677ff;
}

.payment-method-item:nth-child(3) .payment-icon {
  color: #172b85;
}

.payment-name {
  font-size: 14px;
  color: #666;
}

.payment-method-item.active .payment-name {
  color: #333;
  font-weight: 500;
}

.payment-modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn, .confirm-btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-weight: 500;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

.confirm-btn {
  background-color: #4caf50;
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #43a047;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.confirm-btn:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
  opacity: 0.7;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .payment-method-options {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .payment-method-item {
    flex-direction: row;
    justify-content: flex-start;
    padding: 12px 15px;
  }

  .payment-icon {
    margin-bottom: 0;
    margin-right: 15px;
  }
}
</style>