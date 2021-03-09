<<template>
    <div>
        <mu-circular-progress :size="40" v-if="loading"/>
        <div v-html="html"></div>
    </div>
</template>
<style>

</style>
<script>
    import {
        gethtmlurl
    } from '@/router/api'
    export default {
        // 使用时请使用 :url.sync=""传值
        props: {
            url: {
                required: true
            }
        },
        data() {
            return {
                loading: true,
                html: ''
            }
        },
        watch: {
            url() {
                this.getloadurl()
            }
        },
        mounted() {
            this.getloadurl();
        },
        created() {
            this.getParams();
            this.getloadurl();
        },
        activated() {
            this.getParams();
            this.getloadurl();
        },
        methods: {
            //获取由路由传递过来的参数
            getParams() {
                this.routerParams = this.$route.query;
            },
            getloadurl() {
                this.listLoading = true
                const self = this
                const params = {
                  type:this.routerParams.type,
                  id:this.routerParams.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                gethtmlurl(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.loading = false
                        // 处理HTML显示
                        this.html = 'http://192.168.1.121/static/test.html'
                    } else {
                        self.$message.error({
                            message: "加载失败",
                            center: true
                        })
                    }
                })
            }
            // load(url) {
            //     if (url && url.length > 0) {
            //         // 加载中
            //         this.loading = true
            //         let param = {
            //             accept: 'text/html, text/plain'
            //         }
            //         this.$http.get(url, param).then((response) => {
            //             this.loading = false
            //             // 处理HTML显示
            //             this.html = response.data
            //         }).catch(() => {
            //             this.loading = false
            //             this.html = '加载失败'
            //         })
            //     }
            // }
        }
    }
</script>

<style scoped>

</style>
