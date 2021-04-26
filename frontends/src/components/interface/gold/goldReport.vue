<template>
    <div class="wid-2000 " for="pc">
        <el-container style=" border: 1px solid #eee">
                <el-header style="text-align: center; color: rgb(71,62,62); font-size: 24px">
                    <el-dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item>查看</el-dropdown-item>
                            <el-dropdown-item>新增</el-dropdown-item>
                            <el-dropdown-item>删除</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <span>BioMind Gold Standard Test Report</span>
                </el-header>
                <el-main>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../../assets/img/bug-10.png">
                            <span class="bug-ex-item">概述Summary</span>
                            <img class="img-revers" src="../../../assets/img/bug-10.png"></p>
                    </div>
                    <el-row>
                        <el-col style="width: 50%">
                            <el-form ref="form" :model="basedata" label-width="60%">
                                <el-row>
                                    <el-divider></el-divider>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left">

                                        <el-form-item label="测试版本：" label-position="left">
                                            <el-input v-model="basedata.version"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="测试服务：" class="labelcss">
                                            <el-select v-model="basedata.server" placeholder="请选择活动区域">
                                            </el-select>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left" class="labelcss">
                                        <el-form-item label="共计预测：" label-position="left" class="label-content">
                                            <el-tag effect="dark" type="warning" size="150%">{{basedata.total}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%" label-position="left" class="labelcss">
                                        <el-form-item label="" label-position="left" class="label-content">
                                            <p></p>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left" class="labelcss">
                                        <el-form-item label="预测成功：" label-position="left" class="label-content">
                                            <el-tag effect="dark" type="success" size="150%">{{basedata.aisuccess}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="预测失败：">
                                            <el-tag effect="dark" type="danger" size="150%">{{basedata.error}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left" class="labelcss">
                                        <el-form-item label="匹配成功：" label-position="left" class="label-content">
                                            <el-tag effect="dark" type="success" size="150%">{{basedata.success}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="匹配失败：">
                                            <el-tag effect="dark" type="danger" size="150%">{{basedata.fail}} 笔
                                            </el-tag>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 50%" label-position="left">
                                        <el-form-item label="开始时间：" label-position="left">
                                            <el-input v-model="basedata.start_date"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col style="width: 50%">
                                        <el-form-item label="结束时间：">
                                            <el-input v-model="basedata.end_date"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col style="width: 40%">

                                    </el-col>
                                </el-row>
                            </el-form>

                        </el-col>
                        <el-col style="width: 25%">
                            <p>金标准</p>
                            <ve-ring :data="goldchartData" :settings="chartSettings"></ve-ring>
                        </el-col>
                        <el-col style="width: 25%">
                            <p>Error</p>

                            <ve-ring :data="FailData" :settings="SummarySettings"></ve-ring>

                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col style="width: 100%">
                            <p class="bug-exp-step p-t-20 p-b-10"><img src="../../../assets/img/bug-10.png">
                                <span class="bug-ex-item">金标准结果</span><img src="../../../assets/img/bug-10.png"></p>
                            <el-table
                                    :data="goldData"
                                    style="width: 100%">
                                <el-table-column
                                        label="类型"
                                >
                                    <template slot-scope="scope">
                                        <span style="margin-left: 10px">{{ scope.row.diseases }}</span>
                                    </template>
                                </el-table-column>
                                 <el-table-column
                                        label="共计预测"
                                >
                                    <template slot-scope="scope">
                                        <div slot="reference" class="name-wrapper">
                                            <el-tag size="medium" type="warning">{{ scope.row.total }}</el-tag>
                                        </div>

                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="预测成功"
                                >
                                    <template slot-scope="scope">
                                            <div slot="reference" class="name-wrapper">
                                                <el-tag size="medium" type="success">{{ scope.row.aisuccess }}</el-tag>
                                            </div>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="预测失败"
                                >
                                    <template slot-scope="scope">
                                        <el-popover trigger="hover" placement="top">
                                            <p>预测失败: {{ scope.row.errorInfo }}</p>
                                            <div slot="reference" class="name-wrapper">
                                                <el-tag size="medium" type="danger">{{ scope.row.error }}</el-tag>
                                            </div>
                                        </el-popover>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="匹配成功"
                                >
                                    <template slot-scope="scope">
                                            <div slot="reference" class="name-wrapper">
                                                <el-tag size="medium" type="success">{{ scope.row.success }}</el-tag>
                                            </div>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="匹配失败"
                                >
                                    <template slot-scope="scope">
                                        <el-popover trigger="hover" placement="top">
                                            <p v-html="scope.row.failInfo"></p>
                                            <div slot="reference" class="name-wrapper">
                                                <el-tag size="medium" type="danger" >{{ scope.row.fail }}</el-tag>
                                            </div>
                                        </el-popover>
                                    </template>
                                </el-table-column>
                                <el-table-column label="操作">
                                    <template slot-scope="scope">
                                        <el-button
                                                size="mini"
                                                type="danger"
                                                @click="showDetail(scope.$index, scope.row)">详情
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-col>
                    </el-row>
                </el-main>
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
    import {
        getHost, getGoldreport, getbase
    } from '@/router/api'

    export default {
        data() {
            this.chartSettings = {
                roseType: 'radius'
            }
            this.SummarySettings = {
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
                this.goldid = this.$route.params.goldid
            },
            valuestatus: function (a) {
                if (a === "匹配成功") {
                    return 'statuscssb';
                } else {
                    return 'statuscssa';
                }
            },
            showDetail(index, row) {
                this.$router.push({
                    path: '/goldDetail',
                    query: {
                        gold_id: this.goldid,
                        diseases: row.diseases
                    }
                });
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
                    id: this.goldid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getGoldreport(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.reportdata = data
                        self.goldchartData.rows = data.goldrows
                        this.basedata = data.basedata
                        this.goldData = data.goldData
                        this.FailData = {
                            columns: ['状态', '数量'],
                            rows: data.errorData
                        }
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