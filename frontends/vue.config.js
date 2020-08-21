module.exports = {
    publicPath: '/',
    outputDir: 'dist',
    assetsDir: 'static',
    productionSourceMap: false,
    devServer: {
        proxy: {
            /*'/api':{
                target:'http://jsonplaceholder.typicode.com',
                changeOrigin:true,
                pathRewrite:{
                    '/api':''
                }
            },*/
            '/api':{
                //http://127.0.0.1:8000
                target:'http://39.105.135.38:8000',
                ws:true,
                changeOrigin:true,
                pathRewrite:{
                    '/api':''
                }
            },
            '/bishijie': {
                target: "http://39.105.135.38:8000/api",
                ws:true,
                changOrigin:true,
                pathRewrite:{
                    '^/bishijie':'/'
                }
            },
            '/ms':{
                target: 'https://www.easy-mock.com/mock/592501a391470c0ac1fab128',
                changeOrigin: true
            }
        }
    }
}