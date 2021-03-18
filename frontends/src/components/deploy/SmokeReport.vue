<template>
    <div class="wid-2000 " for="pc">
        <el-container style="height: 2000px; border: 1px solid #eee">
            <el-container>
                <el-header style="text-align: center; color: rgb(71,62,62); font-size: 24px">
                    <el-dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item>查看</el-dropdown-item>
                            <el-dropdown-item>新增</el-dropdown-item>
                            <el-dropdown-item>删除</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <span>BioMind Smoke Test Report</span>
                </el-header>
                <el-main>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">概述Summary</span>
                            <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    </div>
                    <el-row>
                        <el-col style="width: 50%">
                            <el-table :data="basedata" border>
                                <el-table-column
                                        prop="version"
                                        label="版本">
                                </el-table-column>
                                <el-table-column
                                        prop="product"
                                        label="策略">
                                </el-table-column>
                                <el-table-column
                                        prop="success"
                                        label="成功"
                                        class=statuscssa>
                                </el-table-column>
                                <el-table-column
                                        prop="fail"
                                        label="失败">
                                </el-table-column>
                                <el-table-column
                                        prop="error"
                                        label="报错">
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col style="width: 25%">
                            <p>金标准</p>
                            <ve-ring :data="goldchartData" :settings="chartSettings"></ve-ring>
                        </el-col>
                        <el-col style="width: 25%">
                            <p>UI自动化</p>
                            <ve-ring :data="uichartData" :settings="chartSettings"></ve-ring>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col style="width: 50%">
                            <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                                <span class="bug-ex-item">金标准结果</span><img src="../../assets/img/bug-10.png"></p>
                            <el-table :data="goldData" border style="width: 100%" row-key="id" border
                                      default-expand-all
                                      :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
                                <el-table-column
                                        prop="diseases"
                                        label="类型">
                                </el-table-column>
                                <el-table-column
                                        prop="success"
                                        label="成功数量">
                                </el-table-column>
                                <el-table-column
                                        prop="fail"
                                        label="失败数量"
                                >
                                </el-table-column>
                                <el-table-column
                                        prop="error"
                                        label="报错数量">
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col style="width: 50%">
                            <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                                <span class="bug-ex-item">UI自动化结果</span>
                                <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                            <el-table :data="UIData" border style="width: 100%">
                                <el-table-column
                                        prop="diseases"
                                        label="类型">
                                </el-table-column>
                                <el-table-column
                                        prop="success"
                                        label="成功数量">
                                </el-table-column>
                                <el-table-column
                                        prop="fail"
                                        label="失败数量"
                                >
                                </el-table-column>
                                <el-table-column
                                        prop="error"
                                        label="报错数量">
                                </el-table-column>
                                <el-table-column
                                        prop="online"
                                        label="详情"
                                >
                                </el-table-column>
                            </el-table>
                        </el-col>
                    </el-row>
                </el-main>

            </el-container>
        </el-container>

    </div>
</template>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }

    .el-aside {
        color: #333;
    }

    .statuscssa {
        color: #E61717
    }

    .statuscssb {
        color: #67c23a;
    }

    .statuscssc {
        color: #666666;
    }
</style>

<script>
    import {stresssave} from "../../router/api";
    import {
        getHost, getInstallReport, getbase
    } from '@/router/api'

    export default {
        data() {
            this.chartSettings = {
                roseType: 'radius'
            }
            return {
                goldchartData: {
                    columns: ['状态', '数量'],
                    rows: [
                        {'状态': '成功', '数量': 0},
                        {'状态': '失败', '数量': 0},
                        {'状态': '报错', '数量': 0}
                    ]
                },
                uichartData: {
                    columns: ['状态', '数量'],
                    rows: [
                        {'状态': '成功', '数量': 0},
                        {'状态': '失败', '数量': 0},
                        {'状态': '报错', '数量': 0}
                    ]
                },
                basedata: [],
                goldData: [{
                    diseases: 'CTA',
                    success: '50',
                    fail: '10',
                    error: '5'
                }, {
                    diseases: 'brain',
                    success: '23',
                    fail: '11',
                    error: '1'
                },],
                UIData: []

            }
        },
        created() {
            this.getParams();
        },
        mounted() {
            this.getParams()
            this.getReport()
        },
        activated() {
            this.getParams();
        },
        methods: {
            getParams() {
                this.routerParams = this.$route.query;
                this.reportid = this.$route.params.reportid
            },
            valuestatus: function (a) {
                if (a === "匹配成功") {
                    return 'statuscssb';
                } else {
                    return 'statuscssa';
                }
            },
            gethost() {
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
                        this.tags = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取getBase列表
            getBase() {
                this.listLoading = true
                const self = this
                const params = {
                    selecttype: "dicom", type: "gold",
                    status: 1
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getbase(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.bases = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取数据列表
            getReport() {
                this.listLoading = true
                const self = this
                const params = {
                    id: this.reportid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getInstallReport(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.reportdata = data
                        self.goldchartData.rows = data.goldrows
                        self.uichartData.rows = data.uirows
                        this.basedata = data.basedata
                        this.goldData = data.goldData
                        this.uiData = uiData
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            handleCurrentChange(val) {
                this.page = val
                this.getdata()
            },
            selsChange: function (sels) {
                this.sels = sels
            },
            // 批量删除
            batchRemove: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {ids: ids}
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }
                    deldicomdata(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true
                            })
                        }
                        self.getdata()
                    })
                })
            },
            handleR: function (index, row) {
                this.$confirm('确认重新测试吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {id: row.id};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    stresssave(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message({
                                message: '成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getdata()
                    });
                })
            },
            handleU: function (index, row) {
                this.$confirm('跳转到imageview页面?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: row.id,
                        type: "gold"
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    getdicomurl(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            console.log(JSON.stringify(data.url))
                            window.location.href = JSON.stringify(data.url),
                                //刷新当前页面
                                // window.location.reload();
                                self.$message({
                                    message: '成功',
                                    center: true,
                                    type: 'success'
                                })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getdata()
                    });
                })
            }
        }
    }
</script>