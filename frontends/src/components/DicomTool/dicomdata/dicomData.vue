<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="22" class="toolbar" style="padding-bottom: 0px;">
                <el-form :inline="true" :model="filters" @submit.native.prevent>

                    <el-form-item>
                        <el-cascader :options="groupOptions" :props="{ checkStrictly: true }" v-model="filters.type"
                                     clearable
                                     @click.native="getgroupbase()"></el-cascader>
                    </el-form-item>

                    <el-form-item>
                        <el-input v-model="filters.patientid" placeholder="patientid"
                                  @keyup.enter.native="getdata"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-select v-model="filters.slicenumber" placeholder="肺炎层厚">
                            <el-option key="" label="" value=""></el-option>
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
                    <el-button type="primary" :disabled="this.sels.length===0" @click="handleAnonymization">重新匿名</el-button>
                    <el-button type="primary" :disabled="this.sels.length===0" @click="handleCollection">收藏</el-button>
                    <el-button type="warning" :disabled="this.sels.length===0" @click.native="Unbind">解除绑定</el-button>
                </el-form>
            </el-col>
            <!--列表-->
            <el-table
                    v-loading="listLoading"
                    :data="datalist"
                    highlight-current-row
                    style="width: 100%;"
                    @selection-change="selsChange">
                <el-table-column type="selection" min-width="4%"/>
                <el-table-column prop="别名" label="别名" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.remark }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="patientid" label="Patientid" min-width="10%" sortable>
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.patientid }}</span>
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
                <el-table-column label="类型" min-width="10%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.type }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="标准诊断" min-width="15%">
                    <template slot-scope="scope">
                        <span style="margin-left: 10px">{{ scope.row.diagnosis }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" min-width="12px">
                    <template slot-scope="scope">
                        <!--          <el-button v-if=scope.row.edit  type="success"  size="small" icon="el-icon-circle-check-outline" @click="handleEdit(scope.$index, scope.row)">Ok</el-button>-->
                        <!--          <el-button v-else type="primary" size="small" icon="el-icon-edit" @click=scope.row.edit=!scope.row.edit>Edit</el-button>-->
                        <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">
                            {{scope.row.status===false?'启用':'禁用'}}
                        </el-button>
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
                            <el-form-item label="患者ID:">
                                <el-input v-model="editForm.patientid"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="患者姓名:">
                                <el-input v-model="editForm.patientname"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="8">
                            <el-form-item label="别名">
                                <el-input v-model="editForm.remark"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="8">
                            <el-form-item label="标注诊断">
                                <el-input v-model="editForm.diagnosis"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="8">
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
                        <el-input type="textarea" :rows="10" v-model="editForm.vote" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="Graphql">
                        <el-input type="textarea" :rows="10" v-model="editForm.graphql" auto-complete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="editFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
                </div>
            </el-dialog>

            <!--收藏界面-->
            <el-dialog
                    :visible.sync="CollectionFormVisible"
                    :close-on-click-modal="false"
                    style="width: 30%; left: 62%"
            >
                <el-row :gutter="24">
                    <el-col :span="15">
                        <el-select v-model="groupId" placeholder="请选择组">
                            <el-option v-for="(item,index) in dicomgrouplist"
                                       :key="item.id"
                                       :label="item.name"
                                       :value="item.id"
                            />
                        </el-select>
                    </el-col>
                    <el-col :span="9">
                        <el-button type="primary" :loading="collectionLoading" @click.native="Collection">保存</el-button>
                    </el-col>
                </el-row>

            </el-dialog>

            <!--重新匿名界面-->
            <el-dialog
                    title="重新匿名"
                    :visible.sync="AnonymizationFormVisible"
                    :close-on-click-modal="false"
                    style="width: 75%; left: 12.5%"
            >
                <el-form ref="AnonymizationForm" :model="AnonymizationForm" label-width="80px" :rules="AnonymizationRules">
                    <el-row :gutter="24">
                        <el-col span="8">
                            <span>患者ID(PatientID):</span>
                        </el-col>
                        <el-col :span="12">
                            <el-input v-model.trim="AnonymizationForm.PatientID" auto-complete="off"/>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col span="8">
                            <span>患者姓名(PatientName):</span>
                        </el-col>
                        <el-col :span="12">

                            <el-input v-model.trim="AnonymizationForm.PatientName" auto-complete="off"/>

                        </el-col>
                    </el-row>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="AnonymizationFormVisible = false">取消</el-button>
                    <el-button type="primary" :loading="addLoading" @click.native="addSubmit">修改</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'
    import {
        dicomdetail,
        getdicomdata,
        deldicomdata,
        updatedicomdata,
        DicomUnbind,
        getGroup,
        deldicomreport,
        dicomcsv,
        DicomAdd,
        DisableDicom,
        EnableDicom,
        getDictionary
    } from '@/router/api'
    import {getGroupBase} from "../../../router/api";


    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                project_id:localStorage.getItem("project_id"),
                filters: {
                    diseases: '',
                    slicenumber: '',
                    type: ''
                },
                total: 0,
                page: 1,
                tags: {},
                filetype: {},
                datalist: [],
                options:{},
                listLoading: false,
                CollectionFormVisible: false,
                collectionLoading: false,
                dicomgrouplist: {},
                groupId: "",
                groupOptions: null,
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
                    diagnosis: '',
                    remark: ''
                },
                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                // 新增界面数据
                AnonymizationForm: {
                    PatientID: '',
                    PatientName: ''
                },
                AnonymizationFormVisible: false, // 重新页面显示状态
                addLoading: false,
                AnonymizationRules: {
                    PatientID: [
                        {required: true, message: '请输入PatientID', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    PatientName: [
                        {required: true, message: '请输入PatientName', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ]
                }

            }
        },
        mounted() {
            this.getParams();
        },
		activated() {
			  this.getParams();
			  },
        methods: {
            // 获取传参
            getParams() {
                if (this.$route.params.type === true){
                    this.filters.type =  this.$route.params.type;
                    this.getdata();
                }
                else {
                    this.getdata();
                }
            },
            // 获取数据列表
            getdicomgrouplist() {
                this.listLoading = true
                const self = this
                const params = {
                    page: 1,
                    page_size: 9999,
                    type: "Virtual"
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
            },
            getfile() {
                this.listLoading = true;
                let self = this;
                let params = {
                    type: 'file',
                    status: 1,
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getDictionary(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.filetype = JSON.parse(json)
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
                    slicenumber: self.filters.slicenumber,
                    type: this.filters.type[0],
                    diseases: this.filters.type[1],
                    patientid: self.filters.patientid,
                    project_id: this.project_id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdicomdata(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.page = data.page
                        self.datalist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取级联 查询 组信息列表
            getgroupbase() {
                this.listLoading = true
                const self = this
                const params = {}
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
            handleCurrentChange(val) {
                this.page = val
                this.getdata()
            },
            // 显示关联组页面
            handleCollection: function (index, row) {
                this.CollectionFormVisible = true,
                    this.getdicomgrouplist()
            },
            // 显示重新匿名页面
            handleAnonymization: function (index, row) {
                this.AnonymizationFormVisible = true,
                    this.Anonymization()
            },
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)
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
                                patientid: self.editForm.patientid,
                                patientname: self.editForm.patientname,
                                diseases: self.editForm.diseases,
                                slicenumber: self.editForm.slicenumber,
                                vote: self.editForm.vote,
                                remark: self.editForm.remark,
                                diagnosis: self.editForm.diagnosis,
                                imagecount: self.editForm.imagecount,
                                graphql: self.editForm.graphql
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
                        self.datalist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
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
            // 批量生成CSV
            batchCsv: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认生成选中记录吗？', '提示', {
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
                    dicomcsv(header, params).then(_data => {
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
            // 改变项目状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
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
                        } else {
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
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            },
            // 数据解除绑定
            Unbind: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('注意：是否确认解除该数据的绑定组信息？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {
                        ids: ids
                    }
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }
                    DicomUnbind(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            this.CollectionFormVisible = false,
                                self.$message({
                                    message: msg,
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
            // 收藏组数据
            Collection: function () {
                const ids = this.sels.map(item => item.id)
                const self = this
                this.$confirm('确认保存？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {
                        ids: ids,
                        groupId: this.groupId
                    }
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }
                    DicomAdd(header, params).then(_data => {
                        const {msg, code, data} = _data
                        if (code === '0') {
                            this.CollectionFormVisible = false,
                                self.$message({
                                    message: msg,
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
