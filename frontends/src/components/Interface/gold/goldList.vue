<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form-item label="服务器" prop="server">
                  <el-select v-model="filters.server"  placeholder="请选择服务" @click.native="gethost()">
                    <el-option v-for="(item,index) in hosts"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                              />
                    </el-select>
                  </el-form-item>
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="版本" @keyup.enter.native="getsmokeList"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getsmokeList">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">创建测试</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="showData">查看数据</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <!--列表-->
        <el-table :data="Smokelist" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                  style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="version" label="版本" min-width="12%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link v-if=true :to="{ name: '金标准详情', params: {goldid: scope.row.id}}"
                                 style='text-decoration: none;color: #0000ff;'>
                        {{ scope.row.version }}
                    </router-link>
                </template>
            </el-table-column>
            <el-table-column prop="Host" label="服务" min-width="15%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.Host }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="diseases" label="规则" min-width="30%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.diseases }}</span>
                </template>
            </el-table-column>
            <el-table-column label="开始时间" min-width="18%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.starttime  | dateformat('YYYY-MM-DD HH:mm:SS')}}</span>
                </template>
            </el-table-column>
            <el-table-column label="结束时间" min-width="18%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.completiontime  | dateformat('YYYY-MM-DD HH:mm:SS')}}</span>
                </template>
            </el-table-column>
            <el-table-column label="测试进度" min-width="25%" sortable>
                <template slot-scope="scope">
                    <el-progress :text-inside="true" :stroke-width="26" :percentage=scope.row.progress></el-progress>
                </template>
            </el-table-column>
            <el-table-column prop="success" label="匹配成功" min-width="15%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.success }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="fail" label="匹配失败" min-width="15%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.fail }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="aifail" label="执行失败" min-width="15%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.aifail }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="9%">
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="30%">
                <template slot-scope="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope.$index, scope.row)">修改</el-button>
<!--                    <el-button type="primary" size="small" @click="smoketest(scope.$index, scope.row)">测试</el-button>-->
                    <el-button type="warning" size="small" @click="showReport(scope.$index, scope.row)">报告</el-button>
                    <el-button :type="typestatus(scope.row.status)" size="small" @click="handleChangeStatus(scope.$index, scope.row)">
                        {{scope.row.status===false?'启用':'停止'}}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20"
                           :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>

        <!--详细界面-->
        <el-dialog :visible.sync="editFormVisible" :close-on-click-modal="false"
                   style="width: 100%; left: 5.5%">
            <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                <el-divider>基本配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="版本" prop='version'>
                            <el-input v-model.trim="editForm.version" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="线程数" prop='thread'>
                            <el-input-number v-model="editForm.thread" @change="handleChange" :min="1" :max="5"
                                             label="线程数"></el-input-number>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-divider>数据配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="类型" prop='diseases'>
                            <el-select v-model="editForm.diseases" multiple placeholder="请选择" @click.native="getsetUp()">
                                <el-option v-for="(item,index) in model"
                                           :key="item.id"
                                           :label="item.remarks"
                                           :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">关闭</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">修改</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增测试" :visible.sync="addFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-divider>基本配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="版本" prop='version'>
                            <el-input v-model.trim="addForm.version" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="服务器" prop='server'>
                            <el-select v-model="addForm.Host" placeholder="请选择服务器" @click.native="gethost()">
                                <el-option
                                        v-for="(item,index) in hosts"
                                        :key="item.id"
                                        :label="item.name"
                                        :value="item.id"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="线程数" prop='thread'>
                            <el-input-number v-model="addForm.thread" @change="handleChange" :min="1" :max="5"
                                             label="线程数"></el-input-number>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-divider>数据配置</el-divider>
                <el-row :gutter="24">
                    <el-checkbox-group v-model="addForm.diseases" size="small">
                        <el-checkbox-button v-for="(item,index) in model" :label="item.id" :key="item.id">
                            {{item.remarks}}
                        </el-checkbox-button>
                    </el-checkbox-group>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">保存</el-button>
            </div>
        </el-dialog>
    </section>
</template>

<script>
    //import NProgress from 'nprogress'
    import {
        getsmoke, DelSmoke, DisableSmoke, EnableSmoke,
        UpdateSmoke, addSmoke, stresssave, getHost, getsmokestart, getupload
    } from '../../../router/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    name: ''
                },
                model:'',
                Smokelist: [],
                total: 0,
                page: 1,
                page_size:10,
                listLoading: false,
                sels: [],//列表选中列
                hosts:{},
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    diseases: [
                        {required: true, message: '请选择病种', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                    ]
                },
                //编辑界面数据
                editForm: {
                    version: '',
                    thread: 1
                },
                percentage:'',
                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    diseases: [
                        {required: true, message: '请选择模型类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                    ]
                },
                //新增界面数据
                addForm: {
                    Host: '',
                    version: '',
                    diseases: [],
                    status: false
                }
            }
        },
        created() {
            // 实现轮询
             this.clearTimeSet=window.setInterval(() => {
              setTimeout(this.getsmokeList(), 0);
            }, 30000);
          },
        beforeDestroy() {    //页面关闭时清除定时器
            clearInterval(this.clearTimeSet);
        },
        mounted() {
            this.gethost()
        },
        methods: {
            typestatus: function (i) {
                if (i ===true) {
                    return 'danger'
                } else {
                    return 'primary'
                }

            },
            showReport(index, row) {
                this.$router.push({
                    path: '/report/goldid=' + row.id,
                });
            },
            showdetail(index, row) {
                this.$router.push({
                    path: '/stressdetail',
                    query: {
                        id: row.id,
                        name: row.name
                    }
                });
            },
            // 获取host数据列表
            gethost() {
                this.listLoading = true
                let self = this;
                const params = {
                    page_size:100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
                        this.hosts = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取项目列表
            getsmokeList() {
                this.listLoading = true;
                let self = this;
                let params = {
                    page: self.page,
                    page_size:self.page_size,
                    version: self.filters.version
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getsmoke(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '0') {
                        self.total = data.total;
                        self.Smokelist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            //保存
            handleSave: function (index, row) {
                this.$confirm('确认测试完成了吗?', '提示', {
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
                        self.getsmokeList()
                    });
                })
            },
            handleChange(value) {
                console.log(value);
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
                    DisableSmoke(headers, params).then(_data => {
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
                    EnableSmoke(headers, params).then(_data => {
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
            handleCurrentChange(val) {
                this.page = val;
                this.getsmokeList()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //展示风险项
            showData(index,row){
             this.$router.push({
                    path:'/dicom',
                    query:{
                        type:"gold"
                    }
                });
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    version: null,
                    Host: '',
                    thread: 1,
                    diseases: [],
                };
            },
            //smoke测试
            smoketest: function (index, row) {
                this.$confirm('执行测试?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: row.id,
                        type: true
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    getsmokestart(header, params).then(_data => {
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
                        self.getsmokeList()
                    });
                })
            },
            //编辑修改
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认保存吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                id: self.editForm.id,
                                version: self.editForm.version,
                                diseases: self.editForm.diseases,
                                thread: this.editForm.thread,
                                progress: 0,
                                status: true
                            };
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            UpdateSmoke(header, params).then(_data => {
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
                                    self.getsmokeList()
                                } else if (code === '999997') {
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
                            });
                        });
                    }
                });
            },
            //新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认保存吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = JSON.stringify({
                                Host: self.addForm.Host,
                                version: self.addForm.version,
                                diseases: self.addForm.diseases,
                                thread: this.addForm.thread,
                                progress: 0,
                                status: false,
                            });
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            addSmoke(header, params).then(_data => {
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
                                    self.getsmokeList()
                                } else if (code === '999997') {
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
                                    self.getsmokeList()
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
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: ids};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    DelSmoke(header, params).then(_data => {
                        let {msg, code, data} = _data;
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
                        self.getsmokeList()
                    });
                })
            }
        },
        mounted() {
            this.getsmokeList();
        }
    }

</script>

<style>

</style>