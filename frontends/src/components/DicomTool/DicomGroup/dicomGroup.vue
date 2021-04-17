<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="30" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>
                    <el-form-item label="组名：" prop="server">
                        <el-select v-model="filters.server" placeholder="请输入组" @click.native="gethost()">
                            <el-option key="" label="" value=""></el-option>
                            <el-option v-for="(item,index) in tags"
                                       :key="item.id"
                                       :label="item.name"
                                       :value="item.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="getdicomgrouplist">查询</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleAdd">新增</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
            <!--列表-->
            <el-table :data="dicomgrouplist" highlight-current-row v-loading="listLoading"
                      @selection-change="selsChange"
                      width="100%">
                <el-table-column type="selection" min-width="10%"></el-table-column>
                <el-table-column prop="name" label="名称" min-width="20%" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.name }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="备注" min-width="20%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.remark }}</span>
                    </template>
                </el-table-column>

                <el-table-column prop="status" label="状态" min-width="20%" sortable>
                    <template slot-scope="scope">
                        <img v-show="scope.row.status"
                             style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/qidong.png"/>
                        <img v-show="!scope.row.status"
                             style="width:15px;height:15px;margin-right:5px;margin-bottom:5px"
                             src="../../../assets/img/ting-zhi.png"/>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="20%">
                    <template slot-scope="scope">
                        <el-row>
                            <el-button :type="typestatus(scope.row.sendstatus)" size="small"
                                       @click="handleChangeStatus(scope.$index, scope.row)">
                                {{scope.row.sendstatus===false?'启用':'禁用'}}
                            </el-button>
                            <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">修改
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
                    <el-divider>基本信息</el-divider>
                    <el-row>
                        <el-form :inline="true" :model="filters" @submit.native.prevent>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="名称:" prop="name">
                                        <el-input  v-model="editForm.name" placeholder=""/>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="备注:" prop="remark">
                                        <el-input  v-model="editForm.remark" placeholder=""/>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-row>
                    <el-divider>详细数据</el-divider>
                    <el-row>
                        <div style="text-align: center">
                            <el-transfer
                                    style="text-align: left; display: inline-block"
                                    v-model="groupData"
                                    filterable
                                    :left-default-checked="[2, 3]"
                                    :right-default-checked="[1]"
                                    :titles="['全部数据', '虚拟组数据']"
                                    :button-texts="['到左边', '到右边']"
                                    :format="{
                                noChecked: '${total}',
                                hasChecked: '${checked}/${total}'
                              }"
                                    @change="ChangeHandle"
                                    :data="infoData">
                                <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>
                                <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>
                                <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button>
                            </el-transfer>
                        </div>
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
                    <el-divider>基本信息</el-divider>
                    <el-row>
                        <el-form :inline="true" :model="filters" @submit.native.prevent>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="名称:" prop="name">
                                        <el-input id="name" v-model="addForm.name" placeholder=""/>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="备注:" prop="remark">
                                        <el-input id="remark" v-model="addForm.remark" placeholder=""/>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-row>
                    <el-divider>详细数据</el-divider>
                    <el-row>
                        <div style="text-align: center">
                            <el-transfer
                                    style="text-align: left; display: inline-block"
                                    v-model="groupData"
                                    filterable
                                    :left-default-checked="[2, 3]"
                                    :right-default-checked="[1]"
                                    :titles="['全部数据', '虚拟组数据']"
                                    :button-texts="['到左边', '到右边']"
                                    :format="{
                                noChecked: '${total}',
                                hasChecked: '${checked}/${total}'
                              }"
                                    @change="ChangeHandle"
                                    :data="infoData">
                                <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>
                                <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>
                                <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button>
                            </el-transfer>
                        </div>
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
    // import NProgress from 'nprogress'
    import draggable from 'vuedraggable'
    import {getbase,getGroup,AddGroup,Updategroup,EnableGroup,DelGroup,DisableGroup,getGroupInfo } from "../../../router/api";

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        data() {
            return {
                filters: {
                    name: '',
                    remark: ''
                },
                groupId:'',
                infoData:[],
                groupData:[],
                dicomgrouplist: {},
                total: 0,
                page: 1,
                page_size: 10,
                listLoading: true,
                sels: [], // 列表选中列

                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                editForm: {
                    name: '',
                    remask: ''
                },

                addForm: {
                    name: '',
                    remask: ''


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
        mounted() {
            this.getdicomgrouplist()
        },

        components: {
            draggable
        },
        methods: {
            // 修改组内数据
            ChangeHandle(groupData, direction, movedKeys) {
                console.log(groupData, direction, movedKeys);
            },
            // 组内dicom 信息
            GroupInfo(row) {
                this.listLoading = true
                let self = this;
                const params = {
                    groupId: row.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getGroupInfo(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.groupData = data.groupData
                        this.infoData = data.info
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            displaystatus: function (i) {
                if (i === '持续化') {
                    return ''
                } else {
                    return 'none'
                }
            },
            typestatus: function (i) {
                if (i === true) {
                    return 'primary'
                } else {
                    return 'danger'
                }

            },
            // 获取数据列表
            getdicomgrouplist() {
                this.listLoading = true
                const self = this
                const params = {
                    page: self.page,
                    page_size: self.page_size,
                    name: this.filters.name,
                    remark: this.filters.remark
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getGroup(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.dicomgrouplist = data.data
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

                    DelGroup(header, params).then(_data => {
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
                        self.getdicomgrouplist()
                    })
                })
            }
            ,
            handleCurrentChange(val) {
                this.page = val
                this.getdicomgrouplist()
            }
            ,
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)
                this.groupId = row.id
                this.GroupInfo(row)
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
                    DisableGroup(headers, params).then(_data => {
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
                    EnableGroup(headers, params).then(_data => {
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
            // 显示新增界面
            handleAdd: function () {
                this.addFormVisible = true
                this.addForm = {
                    name: '',
                    remask: '',
                    status: true,
                    type: 'dicom',
                    groupData:[]
                }
                this.GroupInfo({id:""})
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
                                id: this.editForm.id,
                                name: this.editForm.name,
                                remask: this.editForm.remask,
                                groupData: this.groupData
                            }
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            Updategroup(header, params).then(_data => {
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
                                    self.getdicomgrouplist()
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
            // 新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        const self = this
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true
                            // NProgress.start();
                            const params = JSON.stringify({
                                name: this.addForm.name,
                                remask: this.addForm.remask,
                                groupData: this.groupData,
                                type: 'dicom',
                                status: true
                            })
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            AddGroup(header, params).then(_data => {
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
                                    self.getdicomgrouplist()
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
                                    self.getdicomgrouplist()
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
                    DelGroup(header, params).then(_data => {
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
                        self.getdicomgrouplist()
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

    .transfer-footer {
        margin-left: 20px;
        padding: 6px 5px;
    }
</style>
