import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import ElementUI from 'element-ui';
import ECharts from 'echarts';
import VCharts from 'v-charts';

import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import './assets/css/theme-green/index.css';       // 浅绿色主题
import './assets/icons/iconfont.css'
import './assets/css/icon.css';
import './components/common/directives';
// import 'normalize.css/normalize.css' // a modern alternative to CSS resets
import './styles/element-variables.scss'
import './styles/index.scss' // global css
import './assets/icons' // icon


import "babel-polyfill";
import qs from 'qs';
import moment from 'moment'

Vue.config.productionTip = false
Vue.use(ElementUI, {
    size: 'small'
});
Vue.use(ECharts);
Vue.prototype.$ajax = axios;
Vue.prototype.$qs = qs;



//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {
    const role = localStorage.getItem('ms_username');
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (to.meta.permission) {
        // 如果是管理员权限则可进入，这里只是简单的模拟管理员权限而已
        role === 'admin' ? next() : next('/403');
    } else {
        // 简单的判断IE10及以下不进入富文本编辑器，该组件不兼容
        if (navigator.userAgent.indexOf('MSIE') > -1 && to.path === '/editor') {
            Vue.prototype.$alert('vue-quill-editor组件不兼容IE10及以下浏览器，请使用更高版本的浏览器查看', '浏览器不兼容通知', {
                confirmButtonText: '确定'
            });
        } else {
            next();
        }
    }
})
//格式化时间
Vue.filter('dateformat', function(dataStr, pattern = 'YYYY-MM-DD HH:mm:ss') {
    return moment(dataStr).format(pattern)
})

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')