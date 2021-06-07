<template>
    <div style="margin:35px">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model.trim="filters.name" placeholder="版本" @keyup.enter.native="getProVersionlist"></el-input>
                </el-form-item>
                <el-form-item label="项目" prop="type" >
                        <el-select v-model="filters.type"  placeholder="请选择" >
                            <el-option key="model" label="model" value="model"></el-option>
                            <el-option key="sql" label="sql" value="sql"></el-option>
                            <el-option key="graphql" label="graphql" value="graphql"></el-option>
                            <el-option key="file" label="文件类型" value="file"></el-option>
                            <el-option key="diseases" label="diseases" value="diseases"></el-option>
                        </el-select>
                    </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getProVersionlist">查询</el-button>
                </el-form-item>
<!--                <el-form-item>-->
<!--                    <el-button type="primary" @click="handleAdd">新增</el-button>-->
<!--                </el-form-item>-->
            </el-form>
        </el-col>
        <!--列表-->
        <el-table :data="project" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="project_name" label="项目" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="version" label="版本" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="branch" label="分支" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="package_name" label="安装包" min-width="15%"  show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="path" label="地址" min-width="20%"  show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="type" label="类型" min-width="8%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column label="创建时间" min-width="20%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.create_time  | dateformat('YYYY-MM-DD HH:mm')}}</span>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="10%" sortable>
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="30%">
                <template slot-scope="scope">
                    <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
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
                <el-form-item label="Key" prop="key">
                    <el-input v-model.trim="editForm.key" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Value" prop='value'>
                    <el-input v-model.trim="editForm.value" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="类型" prop="type" >
                        <el-select v-model="editForm.type"  placeholder="请选择" >
                            <el-option key="model" label="model" value="model"></el-option>
                            <el-option key="sql" label="sql" value="sql"></el-option>
                            <el-option key="graphql" label="graphql" value="graphql"></el-option>
                            <el-option key="file" label="文件类型" value="file"></el-option>
                            <el-option key="diseases" label="diseases" value="diseases"></el-option>
                        </el-select>
                    </el-form-item>
                <el-form-item label="说明" prop='remarks'>
                    <el-input type="textarea" :rows="3" v-model.trim="editForm.remarks"></el-input>
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
                <el-form-item label="Key" prop="key">
                    <el-input v-model.trim="addForm.key" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Value" prop='value'>
                    <el-input v-model.trim="addForm.value" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="类型" prop="type" >
                        <el-select v-model="addForm.type"  placeholder="请选择" >
                            <el-option key="model" label="model" value="model"></el-option>
                            <el-option key="sql" label="sql" value="sql"></el-option>
                            <el-option key="graphql" label="graphql" value="graphql"></el-option>
                            <el-option key="file" label="文件类型" value="file"></el-option>
                            <el-option key="diseases" label="diseases" value="diseases"></el-option>
                        </el-select>
                    </el-form-item>
                <el-form-item label="说明" prop='remarks'>
                    <el-input type="textarea" :rows="3" v-model.trim="addForm.remarks"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">添加</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    //import NProgress from 'nprogress'
    import { getProVersion, DelDictionary, DisableDictionary, EnableDictionary,
    UpdateDictionary, addDictionary} from '../../router/api'
    export default {
        data() {
            return {
                filters: {
                    name: ''
                },
                project: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列

                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    key: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                    value: [
                        { required: true, message: '请输入value', trigger: 'blur' },
                    ],
                    remarks: [
                        { required: false, message: '请输入描述', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editForm: {
                    key: '',
                    value: '',
                    remarks: ''
                },
                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    key: [
                        { required: true, message: '请输入key', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                    value: [
                        { required: true, message: 'value', trigger: 'blur' },
                        // { validator: checkIp, trigger: 'blur' }
                    ],
                    remarks: [
                        { required: false, message: '请输入描述', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //新增界面数据
                addForm: {
                    key: '',
                    value: '',
                    type:'',
                    remarks: '',
                    status:true
                }

            }
        },
        methods: {
            // 获取字典列表
            getProVersionlist() {
                this.listLoading = true;
                let self = this;
                let params = {
                    type: self.filters.type,
                    page: self.page,
                    name: self.filters.name
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getProVersion(headers, params).then(_data => {
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
                        ids: [row.id, ]
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    };
                    delDictionary(headers, params).then(_data => {
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
                        self.getProVersionlist()
                    });
                });
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
                    DisableDictionary(headers, params).then(_data => {
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
                    EnableDictionary(headers, params).then(_data => {
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
                this.getProVersionlist()
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
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                id: Number(self.editForm.id),
                                key: self.editForm.key,
                                value: self.editForm.value,
                                type: self.editForm.type,
                                remarks: self.editForm.remarks
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            UpdateDictionary(headers, params).then(_data => {
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
                                    self.getProVersionlist()
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
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认添加吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = {
                                key: self.addForm.key,
                                value: self.addForm.value,
                                type: self.addForm.type,
                                remarks: self.addForm.remarks,
                                status:true
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            addDictionary(headers, params).then(_data => {
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
                                    self.getProVersionlist()
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
                                    self.getProVersionlist()
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
                        ids: ids
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    DelDictionary(headers, params).then(_data => {
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
                        self.getProVersionlist()
                    })
                })
            }
        },
        mounted() {
            this.getProVersionlist();

        }
    }

</script>
<style>
</style>
