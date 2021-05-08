<template>
    <div style="margin:35px">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model.trim="filters.name" placeholder="名称" @keyup.enter.native="getServer"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getServer">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">新增</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <!--列表-->
        <el-table :data="project" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="name" label="名称" min-width="12%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="host" label="HOST" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="port" label="Port" min-width="8%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="user" label="用户" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="pwd" label="密码" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="remarks" label="orthanc" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="27%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="10%" sortable>
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="30%">
                <template slot-scope="scope">
                    <el-button type="warning" size="small" @click="handleChangeProtocol(scope.$index, scope.row)">{{scope.row.protocol===false?'Https':'Http'}}</el-button>
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
<!--                    <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
                    <el-button type="primary" size="small" @click="handleCreate(scope.$index, scope.row)">创建用户
                        </el-button>
<!--                         <el-button type="danger" size="small" @click="Restart(scope.$index, scope.row)">重启-->
<!--                        </el-button>-->
                    <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启用':'禁用'}}</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>

        <!--编辑界面-->
        <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 60%; left: 20%">
            <el-form :model="editForm"  :rules="editFormRules" ref="editForm" label-width="80px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model.trim="editForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Host" prop='host'>
                    <el-input v-model.trim="editForm.host" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Port" prop='Port'>
                    <el-input v-model.trim="editForm.port" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="用户" prop='User'>
                    <el-input v-model.trim="editForm.user" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop='pwd'>
                    <el-input v-model.trim="editForm.pwd" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Orthanc" prop='Orthanc'>
                    <el-input v-model.trim="editForm.remarks" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="配置信息" prop='description'>
                    <el-input type="textarea" :rows="5" v-model.trim="editForm.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false" style="width: 60%; left: 20%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-form-item label="名称" prop="name">
                    <el-input v-model.trim="addForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Host" prop='host'>
                    <el-input v-model.trim="addForm.host" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Port" prop='Port'>
                    <el-input v-model.trim="addForm.port" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="用户" prop='User'>
                    <el-input v-model.trim="addForm.user" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop='pwd'>
                    <el-input v-model.trim="addForm.pwd" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Orthanc" prop='Orthanc'>
                    <el-input v-model.trim="addForm.remarks" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="配置信息" prop='description'>
                    <el-input type="textarea" :rows="5" v-model.trim="addForm.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增用户界面-->
        <el-dialog title="添加用户" :visible.sync="createFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="createForm" label-width="80px" :rules="createFormRules" ref="addForm">
                <el-divider>基本配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="12">
                       <el-form-item label="账号" prop='version'>
                            <el-input v-model.trim="createForm.user" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="密码" prop='version'>
                            <el-input v-model.trim="createForm.pwd" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="createFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="CreateUser" :loading="addLoading">保存</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    //import NProgress from 'nprogress'
    import {
        getHost, delHost, disableHost, enableHost,
        updateHost, addHost, disableHostProtocol, enableHostProtocol, getCreateRestart
    } from '../../../router/api'
    export default {
        data() {
            var checkIp = (rule, value, callback) => {
                if (!this.isValidIP(value)) {
                    return callback(new Error('IP地址格式错误'));
                } else {
                    return callback()
                }
            };
            return {
                filters: {
                    name: ''
                },
                project: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列
                project_id:1,
                createFormVisible: false,//新增用户界面是否显示
                createLoading: false,
                createFormRules: {
                    user: [
                        {required: true, message: '请输入用户', trigger: 'blur'}
                    ]
                },
                //新增用户界面数据
                createForm: {
                    user: '',
                    pwd: '',
                },
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    name: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                    host: [
                        { required: true, message: '请输入host', trigger: 'blur' },
                    ],
                    description: [
                        { required: false, message: '请输入描述', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editForm: {
                    name: '',
                    host: '',
                    user:'',
                    pwd:'',
                    remarks:'',
                    description: ''
                },
                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    name: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                    host: [
                        { required: true, message: '请输入host', trigger: 'blur' },
                        // { validator: checkIp, trigger: 'blur' }
                    ],
                    description: [
                        { required: false, message: '请输入描述', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //新增界面数据
                addForm: {
                    name: '',
                    host: '',
                    port:'',
                    user:'',
                    pwd:'',
                    remarks:'',
                    description: '',
                    protocol:'https'
                }

            }
        },
        created(){
          this.getParams();
          this.getServer();
          },
        activated() {
          this.getParams();
          this.getServer();

          },
        methods: {
            getParams(){
              this.routerParams=this.$route.query;
              this.project_id =this.routerParams.project_id;
              },
            // IP格式验证
            isValidIP(ip) {
                var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
                var regPort = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5]):([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$$/;

                return regPort.test(ip) || reg.test(ip);
            },
             //显示新增界面
            handleCreate: function (index, row) {
                this.createFormVisible = true;
                this.createForm = Object.assign({}, row);
                this.createForm[pwd] = 1
            },
            //  创建用户或重启
            CreateUser() {
                this.listLoading = true
                let self = this;
                const params = {
                    id: this.createForm.id,
                    type: 2,
                    user: this.createForm.user,
                    pwd: this.createForm.pwd,
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getCreateRestart(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.createFormVisible = false,
                         self.$message.success({
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
            },
            // 获取HOST列表
            getServer() {
                this.listLoading = true;
                let self = this;
                let params = {
                    project_id:this.project_id,
                    page: self.page,
                    name: self.filters.name
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getHost(headers, params).then(_data => {
                    let { msg, code, data } = _data;
                    self.listLoading = false;
                    if (code === '0') {
                        self.total = data.total;
                        self.project = data.data
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        project_id: Number(this.$route.params.project_id),
                        ids: [row.id, ]
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    };
                    delHost(headers, params).then(_data => {
                        let { msg, code, data } = _data;
                        if (code === '0') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getServer()
                    });
                });
            },
            handleChangeProtocol: function(index, row) {
                let self = this;
                this.listLoading = true;
                let params = {
                    project_id: Number(this.$route.params.project_id),
                    host_id: Number(row.id)
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.protocol) {
                    disableHostProtocol(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '切换成Https 成功',
                                center: true,
                                type: 'success'
                            });
                            row.protocol = !row.protocol;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enableHostProtocol(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '切换成Http 成功',
                                center: true,
                                type: 'success'
                            });
                            row.protocol = !row.protocol;
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
                    project_id: Number(this.$route.params.project_id),
                    host_id: Number(row.id)
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    disableHost(headers, params).then(_data => {
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
                    enableHost(headers, params).then(_data => {
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
            handleCurrentChange(val) {
                this.page = val;
                this.getServer()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
            },
            //编辑
            editSubmit: function () {
                let self = this;
                let host = this.editForm.host.toLowerCase();
                if (host.indexOf("http://") ===0){
                    host = host.slice(7)
                }
                if (host.indexOf("https://") ===0){
                    host = host.slice(8)
                }
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                project_id: Number(this.project_id),
                                id: Number(self.editForm.id),
                                name: self.editForm.name,
                                host: host,
                                port: self.editForm.port,
                                user:self.editForm.user,
                                pwd:self.editForm.pwd,
                                remarks:self.editForm.remarks,
                                description: self.editForm.description,
                                protocol:'https'
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            updateHost(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.editLoading = false;
                                if (code === '0') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    self.getServer()
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                }
                            })
                        });
                    }
                });
            },
            //新增
            addSubmit: function () {
                let host = this.addForm.host.toLowerCase();
                if (host.indexOf("http://") ===0){
                    host = host.slice(7)
                }
                if (host.indexOf("https://") ===0){
                    host = host.slice(8)
                }
                this.$refs.addForm.validate((valid) => {
                    console.log(valid);
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = {
                                project_id: Number(this.project_id),
                                name: self.addForm.name,
                                host: host,
                                port:self.addForm.port ,
                                user:self.addForm.user,
                                pwd:self.addForm.pwd,
                                remarks:self.addForm.remarks,
                                description: self.addForm.description,
                                protocol:'https'
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            addHost(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.addLoading = false;
                                if (code === '0') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getServer()
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getServer()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    let params = {
                        project_id: Number(this.$route.params.project_id),
                        ids: ids
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delHost(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getServer()
                    })
                })
            }
        },
        mounted() {
            this.getServer();

        }
    }

</script>
<style>
</style>
