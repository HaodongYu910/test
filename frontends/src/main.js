import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import ElementUI from 'element-ui';

import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import './assets/css/theme-green/index.css';       // 浅绿色主题
import './assets/icons/iconfont.css'
import './assets/css/icon.css';
import './utils/directives';
// import 'normalize.css/normalize.css' // a modern alternative to CSS resets
import './styles/element-variables.scss'
import './styles/index.scss' // global css
import './assets/icons' // icon
import VCharts from 'v-charts'

import "babel-polyfill";
import qs from 'qs';
import moment from 'moment'

Vue.config.productionTip = false
Vue.use(ElementUI, {
    size: 'small'
});
// Vue.use(ECharts);
Vue.prototype.$ajax = axios;
Vue.prototype.$qs = qs;

 // 全局设置网络超时
axios.defaults.timeout = 30000;

Vue.use(VCharts)

// new Vue({
//   el: '#app',
//   render: h => h(App)
// })

//   http响应拦截器
//返回状态判断(添加响应拦截器)

axios.interceptors.response.use(res => {
    //对响应数据做些事
        if (res.data && !res.data.success) {
            console.log("成功")
        }
        return res;
        }, error => {
        if (error.response.status === 401) {
                // Message({
                //     showClose: true,
                //     message: "登录状态信息过期,请重新登录",
                //     type: "error"
                // });
                router.push({
                    path: "/login"
                });
            } else {
                // 下面是接口回调的satus ,因为我做了一些错误页面,所以都会指向对应的报错页面
                if (error.response.status === 403) {
                    router.push({
                        path: "/error/403"
                    });
                }
                else if (error.response.status === 500) {
                    // if (confirm("提示：接口请求失败 500 ！ 是否联系管理员？")) {
                    //     alert("请喊他！~");
                    // }
                    // else {
                    //     alert("这就对了");
                    // }

                    alert("提示：接口请求失败 500");

                }
                else if (error.response.status === 502) {
                    router.push({
                        path: "/error/502"
                    });
                }
                else if (error.response.status === 404) {
                    router.push({
                        path: "/error/404"
                    });
                }
            }
        // // 返回 response 里的错误信息
        // let errorInfo = error.data.error ? error.data.error.message : error.data;
        // return Promise.reject(errorInfo);
});

//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {
    const role = localStorage.getItem('ms_username');
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (to.meta.permission) {
        // 如果是管理员权限则可进入，这里只是简单的模拟管理员权限而已
        role === 'admin' ? next() : next('/403');
    } else if (to.matched.length === 0) {  //如果未匹配到路由
        from.name ? next({name: from.name}) : next('/');   //如果上级也未匹配到路由则跳转登录页面，如果上级能匹配到则转上级路由
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
Vue.filter('dateformat', function (dataStr, pattern = 'YYYY-MM-DD HH:mm:ss') {
    return moment(dataStr).format(pattern)
})

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')

