<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <aside>
                    <a href="http://192.168.2.38:9000/" target="_blank">删除dicom数据
                    </a>
                </aside>
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span="5">
                            <el-form-item label="测试服务器" prop="server_ip">
                            <el-select v-model="form.server_ip"  placeholder="请选择" @click.native="gethost()">
                              <el-option
                                v-for="(item,index) in tags"
                                :key="item.host"
                                :label="item.name"
                                :value="item.host"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :span="5">
                            <el-form-item label="删除数据" prop="deldata">
                                <el-input id="deldata" v-model="form.deldata" placeholder="删除数据"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="5">
                            <el-form-item label="数据类型" prop="testtype">
                                <el-select v-model="form.testtype" placeholder="请选择">
                                    <el-option key="" label="患者姓名" value="CTA"/>
                                    <el-option key="CTP" label="患者编号" value="CTP"/>
                                    <el-option key="Lung" label="预测结果" value="Lung"/>
                                    <el-option key="MRA" label="检查类型" value="MRA"/>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item label="模糊搜索" prop="fuzzy">
                                <el-select v-model="form.fuzzy" clearable placeholder="请选择">
                                    <el-option key="True" label="是" value="True"/>
                                    <el-option key="False" label="否" value="False"/>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item>
                                <el-button type="primary" @click="deldicom('form')">删除</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <div>
                    <el-table :data="tableData" style="width: 50%">
                        <el-table-column label="结果显示" width="180">
                            <template slot-scope="scope">
                                <el-popover trigger="hover" placement="top">
                                    <p>tag标签: {{ scope.row.name }}</p>
                                    <div slot="reference" class="name-wrapper">
                                        <el-tag size="medium">{{ scope.row.name }}</el-tag>
                                    </div>
                                </el-popover>
                            </template>
                        </el-table-column>
                        <el-table-column fixed="right" label="">
                            <template slot-scope="scope">
                                <el-button
                                        size="mini"
                                        type="danger"
                                        @click="deleteTag(scope.$index, scope.row)"
                                >开始/关闭
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <aside>
                    <a href="http://192.168.2.38:9000/" target="_blank">匿名发送dicom数据
                    </a>
                </aside>
                <!--工具条-->
                <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-form-item>
                            <el-input v-model="filters.name" placeholder="名称"
                                      @keyup.enter.native="getDurationlist"></el-input>
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
                          style="width: 100%;">
                    <el-table-column type="selection" min-width="5%">
                    </el-table-column>
                    <el-table-column prop="version" label="ID" min-width="5%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.id }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="服务器IP" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.server }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="匿名名称" min-width="9%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.keyword }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="结束时间" min-width="15%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.end_time  | dateformat('YYYY-MM-DD HH:mm:ss')}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="发送类型" min-width="20%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.dicom }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="共计发送" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.time }} 个</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="接收成功" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.time }} 个</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="AI预测成功" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.time }} 个</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="AI预测失败" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.time }} 个</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="运行状态" min-width="8%">
                        <template slot-scope="scope">
                            <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px" src="../../../assets/img/qidong.png"/>
                            <img v-show="!scope.row.status" style="width:15px;height:15px;margin-right:5px;margin-bottom:5px" src="../../../assets/img/ting-zhi.png"/>
                        </template>
                    </el-table-column>
                    <el-table-column label="修改时间" min-width="15%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.update_time  | dateformat('YYYY-MM-DD HH:mm:ss')}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" min-width="20px">
                        <template slot-scope="scope">
                            <el-button type="danger" size="small" @click="showDetail(scope.$index, scope.row)">数据</el-button>
                            <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">修改
                            </el-button>
                            <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">
                                {{scope.row.status===false?'启用':'停用'}}
                            </el-button>

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
                           style="width: 75%; left: 12.5%">
                    <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                        <el-row>
                            <el-col :span="6">
                                <el-form-item label="持续时间" prop="loop_time">
                                    <el-input id="looptime" v-model="editForm.loop_time" placeholder="小时"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="8">
                                <el-form-item label="数据类型" prop="senddata">
                                    <el-select v-model="editForm.senddata" multiple placeholder="请选择" @click.native="getBase()">
                                      <el-option
                                        v-for="(item,index) in tags"
                                        :key="item.remarks"
                                        :label="item.remarks"
                                        :value="item.remarks"
                                      />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item label="匿名名称" prop="keyword">
                                    <el-input id="keyword" v-model="editForm.keyword" placeholder="数据名称"/>
                                </el-form-item>
                            </el-col>
                            <el-col :span="4">
                                <el-form-item label="" prop="keyword">
                                    <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </el-dialog>
                <!--新增界面-->
                <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false"
                           style="width: 75%; left: 12.5%">
                    <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                        <el-form :inline="true" :model="filters" @submit.native.prevent>
                            <el-row>
                                <el-col :span="5">
                                    <el-form-item label="发送服务器" prop="sendserver">
                                        <el-select v-model="addForm.sendserver"  placeholder="请选择" @click.native="gethost()">
                                          <el-option
                                            v-for="(item,index) in tags"
                                            :key="item.host"
                                            :label="item.name"
                                            :value="item.host"
                                          />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="4">
                                    <el-form-item label="持续时间" prop="loop_time">
                                        <el-input id="loop_time" v-model="addForm.loop_time" placeholder="小时"/>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="6">
                                    <el-form-item label="数据类型" prop="senddata">
                                        <el-select v-model="addForm.senddata" multiple placeholder="请选择" @click.native="getBase()">
                                          <el-option
                                            v-for="(item,index) in tags"
                                            :key="item.remarks"
                                            :label="item.remarks"
                                            :value="item.remarks"
                                          />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="4">
                                    <el-form-item label="匿名名称" prop="keyword">
                                        <el-input id="keyword" v-model="addForm.keyword" placeholder="数据名称"/>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="4">
                                    <el-form-item label="保存操作" prop="save">
                                        <el-button type="primary" @click="addSubmit('form')">保存</el-button>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-form>
                </el-dialog>
            </el-col>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getduration,addduration,delduration, updateduration, delete_patients, getHost, getVersion,disable_duration,enable_duration,getbase
    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                form: {
                    server_ip: '',
                    fuzzy: '是',
                    testtype: '患者编号',
                    deldata: ''
                },
                rules: {
                    server_ip: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                filters: {
                    diseases: ''
                },
                durationlist: {
                    end_date:'2099-12-31 23:59:59'
                },
                total: 0,
                page: 1,
                listLoading: false,
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
                    ],
                    description: [
                        {required: false, message: '请输入描述', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                editForm: {
                    diseases: '',
                    version: '',
                    type: '',
                    description: ''
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
                        {pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）'}
                    ]
                },
                // 新增界面数据
                addForm: {
                    diseases: '',
                    version: '',
                    type: '',
                    description: ''
                }

            }
        },
        mounted() {
            this.getDurationlist()
            this.gethost()
        },
        methods: {
            showDetail(index,row){
             this.$router.push({
                    path:'/durationData',
                    query:{
                        id:row.id,
                        name:row.server_ip
                    }
                });
            },
            deldicom(formName) {
                this.tableData = null
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        const params = {
                            server_ip: this.form.server_ip,
                            deldata: this.form.deldata,
                            testtype: this.form.testtype,
                            fuzzy: this.form.fuzzy
                        }
                        const headers = {
                            'Content-Type': 'application/json'
                        }
                        delete_patients(headers, params).then(_data => {
                            console.log(this.form.testtype)
                            const {msg, code, data} = _data
                            if (code != '0') {
                                this.$message.error(msg)
                                return
                            }
                            var result = data[0]
                            if (data != null && result == false) {
                                this.$message.error(data[1])
                                return
                            }
                            // 请求正确时执行的代码
                            var mydata = data[1]
                            var tableData = []
                            for (var i = 0; i < mydata.length; i++) {
                                tableData.push({'name': mydata[i]})
                            }
                            var json = JSON.stringify(tableData)
                            this.tableData = JSON.parse(json)
                        })
                    } else {
                        console.log('error submit')
                        return false
                    }
                })
            },
            getversion() {
                const params = {
                    type: '1'
                }
                const headers = {
                    'Content-Type': 'application/json'
                }
                getVersion(headers, params).then(_data => {
                    console.log(_data)
                    const {msg, code, data} = _data
                    if (code != '0') {
                        this.$message.error(msg)
                        return
                    }
                    // 请求正确时执行的代码
                    var mydata = data.data
                    console.log(mydata)
                    var json = JSON.stringify(mydata)
                    this.tags = JSON.parse(json)
                })
            },
            // 获取getBase列表
            getBase() {
                this.listLoading = true
                const self = this
                const params = {selecttype:"dicom"}
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
            // 获取host数据列表
            gethost() {
                this.listLoading = true
                const self = this
                const params = {}
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
            // 获取数据列表
            getDurationlist() {
                this.listLoading = true
                const self = this
                const params = {}
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
            },
            handleCurrentChange(val) {
                this.page = val
                this.handleDel()
            },
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)
            },
            // 改变状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    disable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '停止成功',
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
                    enable_duration(headers, params).then(_data => {
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
            // 显示新增界面
            handleAdd: function () {
                this.addFormVisible = true
                this.addForm = {
                    server: null,
                    port:null,
                    loop_time: null,
                    aet:null,
                    keyword: null,
                    dicom: null,
                    sendstatus: false,
                    status: false
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
                                server: self.editForm.sendserver,
                                port:'4242',
                                loop_time: self.editForm.loop_time,
                                aet:'qatest',
                                keyword: this.editForm.keyword,
                                dicom: this.editForm.senddata
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
                                server: self.addForm.sendserver,
                                port:'4242',
                                loop_time: self.addForm.loop_time,
                                aet:'qatest',
                                keyword: this.addForm.keyword,
                                dicom: this.addForm.senddata,
                                sendstatus: false,
                                status: false
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
        width:15px;
        height:15px;
        margin-right:3px;
        margin-bottom:5px
    }
</style>
