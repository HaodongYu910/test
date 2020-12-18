import Axios from 'axios'
import { Loading, Message, MessageBox } from 'element-ui'
import router from '../router'

// 超时时间
Axios.defaults.timeout = 5000
// http请求拦截器
var loadinginstace
Axios.interceptors.request.use(config => {
   // element ui Loading方法
       loadinginstace = Loading.service({ fullscreen: true })
   return config
}, error => {
   loadinginstace.close();
   Message.error({
         message: '网络不给力,请稍后再试'
     })
   return Promise.reject(error)
})
//   http响应拦截器
Axios.interceptors.response.use(data => {
    // 响应成功关闭loading
    loadinginstace.close();
    const code = data.data.code;
    if(code == 401) { //未登录
        MessageBox.alert('请先登录', '提示', {
            confirmButtonText: '确定',
            callback: action => {
                router.replace({
                    name: 'login',
                    query: {redirect: router.currentRoute.fullPath} //登录后再跳回此页面时要做的配置
                })
            }
        });
    }
    return data
}, error => {
    loadinginstace.close();
    // Message.error({
    //      message: '请稍后再试'
    //  })
    return Promise.reject(error)
})