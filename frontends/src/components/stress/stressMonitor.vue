<template>
    <div style="width: auto">
        <el-col :span="30" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item label="服务器" prop="server">
                    <el-select v-model="filters.host" placeholder="请选择服务" @click.native="getHosts">
                        <el-option key="" label="" value=""></el-option>
                        <el-option v-for="(item,index) in hosts"
                                   :key="item.id"
                                   :label="item.name"
                                   :value="item.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleMonitor('add')">新增</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="danger" @click="handleMonitor('restart')">全部重启</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <iframe style="width:auto;height:800%;" frameborder="0" scrolling="no" id="bdIframe"
                :src="bdTokenUrl"></iframe>
        <!--工具条-->
    </div>
</template>
<script>
    // import NProgress from 'nprogress'

    import {getMonitor, getHost} from "../../router/api";

    // import ElRow from "element-ui/packages/row/src/row";
    export default {

        name: 'turnoverfamily',
        // components: {ElRow},
        data() {
            return {
                filters: {
                    host: ''
                },
                hosts: "",
                operation: "",
                bdTokenUrl : "http://10.10.10.2:8083/targets"
            }
        },
        created() {
            this.getUrl();
            this.$nextTick(() => {
                this.getCode();
            });
        },
        mounted() {
            /**
             * iframe-宽高自适应显示
             */
            const oIframe = document.getElementById('bdIframe');
            const deviceWidth = document.documentElement.clientWidth;
            const deviceHeight = document.documentElement.clientHeight;
            oIframe.style.width = (Number(deviceWidth) - 220) + 'px'; //数字是页面布局宽度差值
            oIframe.style.height = (Number(deviceHeight) +4200) + 'px'; //数字是页面布局高度差
            this.getHosts()
        },
        methods: {
            /**
             * 获取-外部接口信息
             */
            getUrl() {
                let that = this
                let bdUrl = {queryurl: this.$paths.bdpath + '/locate'};
                this.$api.getBdToken(bdUrl, function (res) {
                    that.bdTokenUrl = res.data.data;
                })
            },
            // 获取host数据列表
            getHosts() {
                this.listLoading = true
                const self = this
                const params = {
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.hosts = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
            // 重启&新增
            handleMonitor: function (operation) {
                this.$confirm('确认新增&重启服务监控吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    if (this.filters.host === '') {
                        this.$message({
                            message: "请选择服务器",
                            center: true,
                            type: 'warning'
                        })
                    } else {
                        this.listLoading = true
                        // NProgress.start();
                        const self = this
                        const params = {
                            host_id: this.filters.host,
                            operation: operation
                        }
                        const header = {
                            'Content-Type': 'application/json',
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        }
                        getMonitor(header, params).then(_data => {
                            const {msg, code, data} = _data
                            if (code === '0') {
                                this.$message({
                                    message: msg,
                                    center: true,
                                    type: 'success'
                                })
                            } else {
                                this.$message.error({
                                    message: msg,
                                    center: true
                                })
                            }
                        })
                    }
                })
            }
        }
    }

</script>

<style scoped>
    .edit-input {
        padding-right: 100px;
    }

    .cancel-btn {
        position: absolute;
        right: 15px;
        top: 10px;
    }

    .iframe {
        width: 100%;
        height: 800%;
    }
</style>
