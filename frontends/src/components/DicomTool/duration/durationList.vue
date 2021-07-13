<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="30" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>
                    <el-form-item label="服务器" prop="server">
                        <el-select v-model="filters.server" placeholder="请选择服务" @click.native="gethost()">
                            <el-option key="" label="" value=""></el-option>
                            <el-option v-for="(item,index) in Hosts"
                                       :key="item.id"
                                       :label="item.name"
                                       :value="item.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="getDurationlist">查询</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleAdd">新增</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <!--列表-->
            <el-table :data="durationlist" highlight-current-row v-loading="listLoading"
                      @selection-change="selsChange"
                      width="100%">
                <el-table-column type="selection" min-width="5%"></el-table-column>
                <el-table-column prop="version" label="版本" min-width="12%"  sortable>
                    <template slot-scope="scope">
                        <router-link v-if="scope.row.version" :to="{ name: 'durationData', query: {id: scope.row.id}}"
                                     style='text-decoration: none;color: #0000ff;'>
                            <span style="margin-left: 10px">{{ scope.row.version }}</span>
                        </router-link>
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="服务" min-width="20%">
                    <template slot-scope="scope">
                        <router-link v-if="scope.row.server" :to="{ name: 'durationData', query: {id: scope.row.id}}"
                                     style='text-decoration: none;color: #0000ff;'>
                            <span style="margin-left: 10px">{{ scope.row.server }}：{{ scope.row.port }}</span>
                        </router-link>
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="数据类型" min-width="20%" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.dicomLabel }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="每日发送" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.sendcount }} 个</span>
                    </template>
                </el-table-column>
                <el-table-column label="共计数量" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #FF0000;">{{ scope.row.totalsend }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="今日数量" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #FF0000;">{{ scope.row.todaysend }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="开始日期" min-width="15%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #00A600;;">{{ scope.row.update_time | dateformat('YYYY-MM-DD')}}</span>
                    </template>
                </el-table-column>
                <el-table-column label="结束日期" min-width="15%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #00A600;;">{{ scope.row.end_time | dateformat('YYYY-MM-DD')}}</span>
                    </template>
                </el-table-column>
                <el-table-column label="发送类型" min-width="12%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px;color: #02C874;">{{ sendtype(scope.row.type) }}</span>
                    </template>
                </el-table-column>

                <el-table-column prop="sendstatus" label="状态" min-width="10%" sortable>
                    <template slot-scope="scope">
                        <img v-show="scope.row.sendstatus"
                             style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/qidong.png"/>
                        <img v-show="!scope.row.sendstatus"
                             style="width:15px;height:15px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/ting-zhi.png"/>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="20%">
                    <template slot-scope="scope">
                        <el-row>
                            <el-button :type="typestatus(scope.row.sendstatus)" size="small"
                                       @click="handleChangeStatus(scope.$index, scope.row)">
                                {{scope.row.sendstatus===false?'启用':'停用'}}
                            </el-button>
                            <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">修改
                            </el-button>
                        </el-row>
                        <el-row>
                            <el-button type="primary" size="small" :style="{ display: displaystatus(scope.row.type) }" @click="showReport(scope.$index, scope.row)">报告
                            </el-button>
                        </el-row>


                    </template>
                </el-table-column>
            </el-table>

            <!--工具条-->
            <el-col :span="24" class="toolbar">
                <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">删除</el-button>
                <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20"
                               :page-count="total" style="float:right;">
                </el-pagination>
            </el-col>

            <!--编辑界面-->
            <el-dialog title="修改" :visible.sync="editFormVisible" :close-on-click-modal="false"
                       style="width: 100%; left: 7.5%">
                <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                    <el-divider>基本配置</el-divider>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="数据类型" prop="senddata">
                                <el-cascader :options="groupOptions" v-model="editForm.senddata" clearable :props="props"
                                             @click.native="getgroupbase()"></el-cascader>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="每日发送" prop='sendcount'>
                                <el-input-number v-model="editForm.sendcount" :min="0"
                                                 :max="100000"
                                                 label="每日发送"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="结束时间">
                            <el-date-picker v-model="editForm.end_time" type="datetime"
                                            placeholder="选择日期" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
                        </el-form-item>
                        </el-col>
                    </el-row>
                    </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="editFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
                </div>
            </el-dialog>

            <!--新增界面-->
            <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false"
                       style="width: 100%; left: 10%">
                <el-form :model="addForm" label-width="120" :rules="addFormRules" ref="addForm">
                    <el-divider>基本配置</el-divider>
                    <el-row>
                        <el-form :inline="true" :model="filters" @submit.native.prevent>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="服务器:" prop="Host">
                                        <el-select v-model="addForm.Host" placeholder="请选择"
                                                   @click.native="gethost()">
                                            <el-option
                                                    v-for="(item,index) in Hosts"
                                                    :key="item.id"
                                                    :label="item.name"
                                                    :value="item.id"
                                            />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="端口号:" prop="port">
                                        <el-input id="port" v-model="addForm.port" placeholder=""/>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="数据类型" prop="senddata">
                                <el-cascader :options="groupOptions" v-model="addForm.senddata" clearable :props="props"
                                             @click.native="getgroupbase()"></el-cascader>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="已有版本" prop='version'>
                                 <el-select v-model="addForm.version" placeholder="请选择"
                                                   @click.native="getversion()">
                                            <el-option
                                                    v-for="(item,index) in VersionInfo"
                                                    :key="item.id"
                                                    :label="item.version"
                                                    :value="item.id"
                                            />
                                        </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>

                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="每日发送" prop='sendcount'>
                                <el-input-number v-model="addForm.sendcount" :min="0"
                                                 :max="100000"
                                                 label="每日发送"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="结束时间">
                            <el-date-picker v-model="addForm.end_time" type="datetime"
                                            placeholder="选择日期" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
                        </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="addFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="addSubmit" :loading="addLoading">保存</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>

    import {
        getduration,
        getGroupBase,
        addduration,
        delduration,
        updateduration,
        getHost,
        getVersionInfo,
        disable_duration,
        enable_duration
    } from '@/router/api'
    
    export default {
        // components: {ElRow},
        data() {
            return {
                project_id:localStorage.getItem("project_id"),
                Hosts:[],
                versionlist:[],
                typeoptions: [{
                    value: 1,
                    label: '匿名'
                }, {
                    value: 0,
                    label: '正常'
                }, {
                    value: 2,
                    label: '持续化'
                }],
                props: {multiple: true},
                VersionInfo: {},
                form: {
                    server_ip: '',
                    fuzzy: '是',
                    testtype: 'PatientID',
                    deldata: ''
                },
                rules: {
                    server_ip: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'}
                    ]
                },
                filters: {
                    diseases: '',
                    server: ''
                },
                durationlist: {},
                total: 0,
                page: 1,
                page_size: 10,
                listLoading: true,
                sels: [], // 列表选中列

                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                editForm: {
                    loop_time: '',
                    port: '4242',
                    end_time:null
                },

                addForm: {
                    port: '4242',
                    type: '匿名',
                    sendcount: 0,
                    end_time:null

                },
                addFormVisible: false, // 新增界面是否显示
                addLoading: false,
                addFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                    ]
                }
            }
        },
        created() {
            // 实现轮询
            this.clearTimeSet = window.setInterval(() => {
                setTimeout(this.getDurationlist(), 0);
            }, 30000);
        },
        beforeDestroy() {    //页面关闭时清除定时器
            clearInterval(this.clearTimeSet);
        },
        mounted() {
            this.getDurationlist()
            this.gethost()
            this.getgroupbase()
        },
        beforeDestroy() {    //页面关闭时清除定时器
            clearInterval(this.clearTimeSet);
        },
        methods: {
            //发送类型翻译
            sendtype: function (i) {
                if (i === 0) {
                    return '正常'
                }
                else if (i === 1) {
                    return '匿名'
                }
                else if (i === 2) {
                    return '持续化'
                }else {
                    return 'Nightly'
                }

            },
            // 获取版本列表
            getversion() {
                this.listLoading = true
                let self = this;
                const params = {
                    page_size: 999,
                    project_id:this.project_id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getVersionInfo(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.VersionInfo = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            displaystatus: function (i) {
                if (i ===2) {
                    return ''
                } else {
                    return 'none'
                }
            },
            typestatus: function (i) {
                if (i === true) {
                    return 'danger'
                } else {
                    return 'primary'
                }

            },
            showReport(index, row) {
                this.$router.push({
                    path: '/DurationReport/reportid=' + row.id,
                });
            },
            showDetail(index, row) {
                this.$router.push({
                    path: '/durationData',
                    query: {
                        id: row.id,
                        name: row.server_ip
                    }
                });
            },
            // 获取级联 查询 组信息列表
            getgroupbase() {
                this.listLoading = true
                const self = this
                const params = {
                    "project_id":this.project_id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getGroupBase(headers, params).then((res) => {
                        self.listLoading = false
                        const {msg, code, data} = res
                        if (code === '0') {
                            this.groupOptions = data.groupOptions

                        } else {
                            self.$message.error({
                                message: msg,
                                center: true
                            })
                        }
                    }
                )
            },
            // 获取host数据列表
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
                        this.Hosts = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
            // 获取数据列表
            getDurationlist() {
                this.listLoading = true
                const self = this
                const params = {
                    page: self.page,
                    page_size: self.page_size,
                    server: this.filters.server,
                    type: 2,
                    project_id:this.project_id

                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getduration(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.durationlist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            }
            ,
            // 删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {ids: [row.id]}
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }

                    delduration(header, params).then(_data => {
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
                        self.getDurationlist()
                    })
                })
            }
            ,
            handleCurrentChange(val) {
                this.page = val
                this.getDurationlist()
            }
            ,

            // 改变状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.sendstatus) {
                    disable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '停止成功',
                                center: true,
                                type: 'success'
                            });
                            row.sendstatus = !row.sendstatus;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '启用成功',
                                center: true,
                                type: 'success'
                            });
                            row.sendstatus = !row.sendstatus;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            }
            ,
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)

            }
            ,
            // 显示新增界面
            handleAdd: function () {
                this.addFormVisible = true
                this.addForm = {
                    server: null,
                    port: 4242,
                    dicom: null,
                    durationType: null,
                    sendstatus: false,
                    status: false,
                    sendcount: 0,
                    type: 2,
                    end_time:null
                }
            }
            ,
            // 编辑
            editSubmit: function () {
                const self = this
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true
                            // NProgress.start();
                            const params = {
                                id: self.editForm.id,
                                dicom: this.editForm.senddata,
                                sendcount: this.editForm.sendcount,
                                end_time:this.editForm.end_time
                            }
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            updateduration(header, params).then(_data => {
                                const {msg, code, data} = _data
                                self.editLoading = false
                                if (code === '0') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.$refs['editForm'].resetFields()
                                    self.editFormVisible = false
                                    self.getDurationlist()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                }
                            })
                        })
                    }
                })
            }
            ,
            // 新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        const self = this
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true
                            // NProgress.start();
                            const params = JSON.stringify({
                                port: self.addForm.port,
                                version: self.addForm.version,
                                loop_time: self.addForm.loop_time,
                                patientname: 'DR',
                                patientid: 'dr',
                                dicom: this.addForm.senddata,
                                sendcount: this.addForm.sendcount,
                                end_time:this.addForm.end_time,
                                type: 'duration',
                                sendstatus: false,
                                status: false,
                                Host: this.addForm.Host,
                                project:this.project_id
                            })
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            addduration(header, params).then(_data => {
                                const {msg, code, data} = _data
                                self.addLoading = false
                                if (code === '0') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.$refs['addForm'].resetFields()
                                    self.addFormVisible = false
                                    self.getDurationlist()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true
                                    })
                                    self.$refs['addForm'].resetFields()
                                    self.addFormVisible = false
                                    self.getDurationlist()
                                }
                            })
                        })
                    }
                })
            }
            ,
            selsChange: function (sels) {
                this.sels = sels
            }
            ,
            cancelEdit(row) {
                row.title = row.originalTitle
                row.edit = false
                this.$message({
                    message: 'The title has been restored to the original value',
                    type: 'warning'
                })
            }
            ,
            confirmEdit(row) {
                row.edit = false
                row.originalTitle = row.title
                this.$message({
                    message: 'The title has been edited',
                    type: 'success'
                })
            }
            ,
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
                    delduration(header, params).then(_data => {
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
                        self.getDurationlist()
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

    .view-png {
        width: 15px;
        height: 15px;
        margin-right: 3px;
        margin-bottom: 5px
    }
</style>
