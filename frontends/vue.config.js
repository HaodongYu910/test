module.exports = {
    publicPath: '/',
    outputDir: 'dist',
    assetsDir: 'static',
    productionSourceMap: false,
    devServer: {
        proxy: {
            /*'/Interface':{
                target:'http://jsonplaceholder.typicode.com',
                changeOrigin:true,
                pathRewrite:{
                    '/Interface':''
                }
            },*/
            // '/Interface':{
            //     // 测试环境
            //     target:'http://127.0.0.1:8000',
            //     ws:true,
            //     changeOrigin:true,
            //     pathRewrite:{
            //         '/Interface':''
            //     }
            // },
            // '/prod': {
            //     target: "http://192.168.1.121:9000",
            //     ws:true,
            //     changOrigin:true,
            //     pathRewrite:{
            //         '^/Interface':'/'
            //     }
            // },
            '/ms':{
                target: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
                changeOrigin: true
            }
        }
    }
}