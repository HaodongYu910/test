<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="20" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>
                    <el-select v-model="filters.status" placeholder="预测状态">
                        <el-option key="true" label="成功" value="true"/>
                        <el-option key="false" label="失败" value="false"/>
                    </el-select>
                    <el-form-item>
                        <el-button type="primary" @click="getdata">查询</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <!--列表-->
            <el-table
                    v-loading="listLoading"
                    :data="stresslist"
                    highlight-current-row
                    style="width: 100%;"
                    @selection-change="selsChange">
                <el-table-column prop="ID" label="ID" min-width="4%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.id }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="patientid" label="patientid" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.patientid }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="patientname" label="patientname" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.patientname }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="diseases" label="病种" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.diseases }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="studyinstanceuid" label="Studyinstanceuid" min-width="25%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.studyinstanceuid }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="sendstatus" label="预测状态" min-width="8%">
                    <template slot-scope="scope">
                        <img v-show="scope.row.status"
                             style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/qiyong.png"/>
                        <img v-show="!scope.row.status"
                             style="width:15px;height:15px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/shibai.png"/>
                    </template>
                </el-table-column>
                <el-table-column label="预测时间" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.time }} 秒</span>
                    </template>
                </el-table-column>
                <el-table-column label="slice" min-width="8%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="预测张数" min-width="5%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.imagecount }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="标准" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.result)">{{ scope.row.diagnosis }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="实际" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px" :class="valuestatus(scope.row.result)">{{ scope.row.aidiagnosis }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="结果" min-width="8%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px"
                              :class="valuestatus(scope.row.result)">{{ scope.row.result }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="8px">
                    <template slot-scope="scope">
                        <!--          <el-button v-if=scope.row.edit  type="success"  size="small" icon="el-icon-circle-check-outline" @click="handleEdit(scope.$index, scope.row)">Ok</el-button>-->
                        <!--          <el-button v-else type="primary" size="small" icon="el-icon-edit" @click=scope.row.edit=!scope.row.edit>Edit</el-button>-->
                        <el-button type="warning" size="small" @click="handleR(scope.$index, scope.row)">重测</el-button>
                        <el-button type="primary" size="small" @click="handleU(scope.$index, scope.row)">跳转</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--工具条-->
            <el-col :span="24" class="toolbar">
                <el-pagination
                        layout="prev, pager, next"
                        :page-size="20"
                        :page-count="total"
                        style="float:right;"
                        @current-change="handleCurrentChange"
                />
            </el-col>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'
    import {
        getHost, getsmokerecord, getsmokestart, deldicomresult, getdicomurl
    } from '@/router/api'
    import {stresssave} from "../../../router/Interface";

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    diseases: null,
                    slicenumber: null,
                    diseases: '',
                    server: '',
                    version: '',
                    status: ''
                },
                total: 0,
                page: 1,
                page_size: 50,
                listLoading: false,
                sels: [], // 列表选中列

                // 新增界面数据
                addForm: {
                    diseases: '',
                    server: '192.168.1.208',
                    studyinstanceuid: ''
                },
                addFormVisible: false, // 新增界面是否显示
                addLoading: false,
                addFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ]
                }

            }
        },
        mounted() {
            this.gethost();
            this.getParams();
            this.getdata();
        },
        created(){
			  this.getParams();
			  this.getdata();
			  },
		activated() {
			  this.getParams();
			  this.getdata();
			  },
        methods: {
            getParams() {
                this.routerParams = this.$route.query;
                this.smokeid = this.$route.params.smokeid
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
                    page_size:100
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
            smoketest() {
                this.listLoading = true
                const self = this
                const params = {
                    server_ip: self.filters.server,
                    diseases: self.filters.diseases,
                    version: self.filters.version
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getsmokestart(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.$message.success({
                            message: "运行中！~~~~~",
                            center: true
                        })
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取数据列表
            getdata() {
                this.listLoading = true
                const self = this
                const params = {
                    page: self.page,
                    smokeid: this.smokeid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getsmokerecord(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.page = data.page
                        self.stresslist = data.data
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
            },
            // 批量删除报告
            batchDel: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认删除选中记录的报告吗？', '提示', {
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
                    deldicomresult(header, params).then(_data => {
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
