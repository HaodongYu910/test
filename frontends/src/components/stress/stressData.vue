<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="20" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>
                    <el-form-item>
                        <el-select v-model="filters.diseases" placeholder="请选择病种" @click.native="getBase()">
                            <el-option v-for="(item,index) in tags"
                                       :key="item.remarks"
                                       :label="item.remarks"
                                       :value="item.remarks"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-select v-model="filters.slicenumber" placeholder="肺炎层厚">
                            <el-option key="1.0" label="1.0" value="1.0"/>
                            <el-option key="1.25" label="1.25" value="1.25"/>
                            <el-option key="1.5" label="1.5" value="1.5"/>
                            <el-option key="5.0" label="5.0" value="5.0"/>
                            <el-option key="10.0" label="10.0" value="10.0"/>
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="getdata">查询</el-button>
                    </el-form-item>
<!--                    <el-button type="primary" @click="getdetail">同步</el-button>-->
                    <el-button type="danger" :disabled="this.sels.length===0" @click="handleSynchro">同步</el-button>
                </el-form>
            </el-col>
            <!--列表-->
            <el-table
                    v-loading="listLoading"
                    :data="stresslist"
                    highlight-current-row
                    style="width: 100%;"
                    @selection-change="selsChange">
                <el-table-column type="selection" min-width="4%"/>
                <el-table-column prop="ID" label="ID" min-width="4%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.id }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="patientid" label="patientid" min-width="12%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.patientid }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="patientname" label="patientname" min-width="12%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.patientname }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="studyinstanceuid" label="Studyinstanceuid" min-width="25%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.studyinstanceuid }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="类型" min-width="10%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.diseases }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="slicenumber" min-width="10%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="预测张数" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.imagecount }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="graphql" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.graphql }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="25%">
                    <template slot-scope="scope">
                      <el-button type="primary" size="small" @click="handleChange(scope.$index, scope.row)">{{scope.row.benchmarkstatus===false?'正常':'基准'}}</el-button>
                    <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="handleTB(scope.$index, scope.row)">同步</el-button>
                    <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启用':'禁用'}}</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--工具条-->
            <el-col :span="24" class="toolbar">
                <el-button type="danger" :disabled="this.sels.length===0" @click="batchRemove">批量删除</el-button>
                <el-pagination
                        layout="prev, pager, next"
                        :page-size="20"
                        :page-count="total"
                        style="float:right;"
                        @current-change="handleCurrentChange"
                />
            </el-col>
            <!--编辑界面-->
            <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false"
                       style="width: 75%; left: 12.5%">
                <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="标注诊断">
                                <el-input v-model="editForm.diagnosis"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="病种">
                                <el-input v-model="editForm.diseases"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="层厚">
                                <el-input v-model="editForm.slicenumber"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="影像张数">
                                <el-input v-model="editForm.imagecount" auto-complete="off"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item label="挂载">
                        <el-input type="textarea" :rows="10" v-model="editForm.vote"  auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="Graphql">
                        <el-input type="textarea" :rows="10" v-model="editForm.graphql"  auto-complete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="editFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
                </div>
            </el-dialog>

            <!--新增界面-->
            <el-dialog
                    title="新增"
                    :visible.sync="addFormVisible"
                    :close-on-click-modal="false"
                    style="width: 75%; left: 12.5%"
            >
                <el-form ref="addForm" :model="addForm" label-width="80px" :rules="addFormRules">
                    <el-row :gutter="24">
                        <el-col :span="10">
                            <el-form-item label="服务器" prop="server">
                                <el-select v-model="addForm.server" placeholder="请选择" @click.native="gethost()">
                                    <el-option v-for="(item,index) in tags"
                                               :key="item.host"
                                               :label="item.name"
                                               :value="item.host"
                                    />
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="patientid" prop="patientid">
                                <el-input v-model.trim="addForm.patientid" auto-complete="off"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="studyinstanceuid" prop="studyinstanceuid">
                                <el-input v-model.trim="addForm.studyinstanceuid" auto-complete="off"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="类型" prop="diseases">
                                <el-select v-model="addForm.diseases" placeholder="请选择" @click.native="getBase()">
                                    <el-option
                                            v-for="(item,index) in tags"
                                            :key="item.remarks"
                                            :label="item.remarks"
                                            :value="item.remarks"
                                    />
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="addFormVisible = false">取消</el-button>
                    <el-button type="primary" :loading="addLoading" @click.native="addSubmit">提交</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'
    import {
        dicomdetail,
        getHost,
        getdicomdata,
        updatedicomdata,
        StressData,
        getbase,
        addStressData,
        DelStressData,
      DisableDicom,
      disableBenchmarkstatus,
      EnableDicom,
        StressSynchro,
      enableBenchmarkstatus
    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    diseases: null,
                    slicenumber: null
                },
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列
                editFormRules: {
                    diagnosis: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 500, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    slicenumber: [
                        {required: false, message: '请输入', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                //编辑界面数据
                editForm: {
                    diseases: '',
                    slicenumber: '',
                    type: '',
                    diagnosis: ''
                },
                editFormVisible: false, // 新增界面是否显示
                editLoading: false,
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
            this.getdata()
            this.gethost()
        },
        methods: {
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
            // 获取getBase列表
            getBase() {
                this.listLoading = true
                const self = this
                const params = {
                    selecttype: "dicom",
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
                        this.tags = JSON.parse(json)
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
                    diseases: self.filters.diseases,
                    slicenumber: self.filters.slicenumber
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                StressData(headers, params).then((res) => {
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
            handleChange: function(index, row) {
                let self = this;
                this.listLoading = true;
                let params = {
                    id: Number(row.id)
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.benchmarkstatus) {
                    disableBenchmarkstatus(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '成功',
                                center: true,
                                type: 'success'
                            });
                            row.benchmarkstatus = !row.benchmarkstatus;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enableBenchmarkstatus(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '成功',
                                center: true,
                                type: 'success'
                            });
                            row.benchmarkstatus = !row.benchmarkstatus;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            },
            handleChangeStatus: function(index, row) {
                let self = this;
                this.listLoading = true;
                let params = {
                    id: Number(row.id)
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    DisableDicom(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '禁用成功',
                                center: true,
                                type: 'success'
                            });
                            row.status = !row.status;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    EnableDicom(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '启用成功',
                                center: true,
                                type: 'success'
                            });
                            row.status = !row.status;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            },
            // 同步
            handleTB: function (index, row) {
                this.$confirm('208环境同步该记录吗?', '提示', {
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
                    StressSynchro(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            self.$message({
                                message: '成功',
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
            handleCurrentChange(val) {
                this.page = val
                this.getdata()
            },
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)
            },
            // 显示新增界面
            handleAdd: function () {
                this.addFormVisible = true
                this.addForm = {
                    patientid: null,
                    diseases: null,
                    studyinstanceuid: null,
                }
            },
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
                                diseases: self.editForm.diseases,
                                slicenumber: self.editForm.slicenumber,
                                vote: self.editForm.vote,
                                diagnosis: self.editForm.diagnosis,
                                imagecount: self.editForm.imagecount,
                                graphql:self.editForm.graphql
                            }
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            updatedicomdata(header, params).then(_data => {
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
                                    self.getdata()
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
            },
            getdetail() {
                this.listLoading = true
                // const ids = this.sels.map(item => item.id)
                const self = this
                const params = {
                    diseases: self.filters.diseases,
                    server: self.filters.server,
                    type: self.filters.type,
                    ids: ''
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                dicomdetail(headers, params).then((res) => {
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
            // 新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        const self = this
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true
                            // NProgress.start();
                            const params = JSON.stringify({
                                diseases: self.addForm.diseases,
                                patientid: self.addForm.patientid,
                                server: self.addForm.server,
                                studyinstanceuid: self.addForm.studyinstanceuid
                            })
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            adddicomdata(header, params).then(_data => {
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
                                    self.getdata()
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
                                    self.getdata()
                                }
                            })
                        })
                    }
                })
            },
            selsChange: function (sels) {
                this.sels = sels
            },
            cancelEdit(row) {
                row.title = row.originalTitle
                row.edit = false
                this.$message({
                    message: 'The title has been restored to the original value',
                    type: 'warning'
                })
            },
            confirmEdit(row) {
                row.edit = false
                row.originalTitle = row.title
                this.$message({
                    message: 'The title has been edited',
                    type: 'success'
                })
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
                    DelStressData(header, params).then(_data => {
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
            // 批量同步
            handleSynchro: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认生成选中记录详细信息吗？', '提示', {
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
                    StressSynchro(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            self.$message({
                                message: '生成成功',
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
            // 批量生成压测数据
            stressD: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认生成选中记录为压测数据吗？', '提示', {
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
                    addStressData(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            self.$message({
                                message: '生成成功',
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
                    deldicomreport(header, params).then(_data => {
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
</style>
