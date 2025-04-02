import { createApp } from 'vue'
import './assets/styles/global.css'
import App from './App.vue'
import router from './routes'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'
import { library } from '@fortawesome/fontawesome-svg-core'; // 导入核心库
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'; // 导入 Vue 组件
// 在导入图标的地方添加新的图标
import {
    faSearch, faShoppingCart, faArrowLeft, faChevronDown,faTruck,faFileExport,
    faUser, faListAlt, faSignOutAlt, faChevronLeft, faChevronRight,faEye,faTrash,
    faClock, faCircleCheck, faTruckFast, faFlagCheckered,faRedo,faTimesCircle,
    faBars, faBell, faTachometerAlt, faShoppingBag, faReceipt, faUsers, faPercent,
    faCog, faHeadset, faMotorcycle, faDollarSign,faTree,faYenSign,faEllipsisV,
    faExclamationTriangle, faArrowUp, faArrowDown,faShop,faUpload,faTimes,faFileAlt,
} from '@fortawesome/free-solid-svg-icons';

// 在 library.add 中添加新图标
library.add(
    faSearch, faShoppingCart, faArrowLeft, faChevronDown,faTruck,faFileExport,
    faUser, faListAlt, faSignOutAlt, faChevronLeft, faChevronRight,faEye,faTrash,
    faClock, faCircleCheck, faTruckFast, faFlagCheckered,faRedo,faTimesCircle,
    faBars, faBell, faTachometerAlt, faShoppingBag, faReceipt, faUsers, faPercent,
    faCog, faHeadset, faMotorcycle, faDollarSign,faTree,faYenSign,faEllipsisV,
    faExclamationTriangle, faArrowUp, faArrowDown,faShop,faUpload,faTimes,faFileAlt,
);

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
app.component('FontAwesomeIcon', FontAwesomeIcon);
