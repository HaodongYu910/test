<template>
    <section>

        <el-dialog title="修改所属分组" :visible.sync="updateGroupFormVisible" :close-on-click-modal="false"
                   style="width: 60%; left: 20%">
            <el-form :model="updateGroupForm" label-width="80px" :rules="updateGroupFormRules" ref="updateGroupForm">
                <el-form-item label="分组名称" prop="firstGroup">
                    <el-select v-model="updateGroupForm.firstGroup" placeholder="请选择">
                        <el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="updateGroupFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="updateGroupSubmit" :loading="updateGroupLoading">提交</el-button>
            </div>
        </el-dialog>
        <el-container style="height: auto; width:auto; border: 1px solid #eee">

            <el-aside style="height: auto; width:auto;">
                <el-radio-group v-model="isCollapse" style="margin-bottom: 20px;">
                    <el-radio-button :label="false">展开</el-radio-button>
                    <el-radio-button :label="true">收起</el-radio-button>
                </el-radio-group>
                <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen"
                         @close="handleClose"
                         :collapse="isCollapse">
                    <template v-for="(item,index) in groupData">
<!--                        <router-link :to="{ name: '分组接口列表', params: {project_id: project, firstGroup: item.id}}"-->
<!--                                     style="text-decoration:none;">-->
                            <el-menu-item :index="index+''" :key="item.id" class="group">
                                <template slot="title">
                                    <i class="el-icon-folder-opened"></i>
                                    {{item.name}}
                                    <el-dropdown trigger="hover" class="editGroup" style="margin-right:10%">
                                        <i class="el-icon-more"></i>
                                        <el-dropdown-menu slot="dropdown">
                                            <el-dropdown-item @click.native="handleDelFirst(item.id)">删除
                                            </el-dropdown-item>
                                            <el-dropdown-item @click.native="handleEditFirstGroup(item.id, item.name)">
                                                修改
                                            </el-dropdown-item>
                                        </el-dropdown-menu>
                                    </el-dropdown>
                                </template>
                            </el-menu-item>
<!--                        </router-link>-->
                    </template>
                </el-menu>
            </el-aside>

            <el-container>
                <el-header style="text-align: right; font-size: 12px">
                    <!--工具条-->
                    <el-col :span="24" style="height: 46px">
                        <el-form :inline="true" :model="filters" @submit.native.prevent>
                            <el-form-item>
                                <el-input v-model.trim="filters.name" placeholder="名称"
                                          @keyup.enter.native="getApiList"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click="getApiList">查询</el-button>
                            </el-form-item>
                            <el-form-item>
                                <router-link :to="{ name: '新增接口', params: {project_id: this.project_id}}"
                                             style='text-decoration: none;color: aliceblue;'>
                                    <el-button type="primary">新增</el-button>
                                </router-link>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" :disabled="update" @click="changeGroup">修改分组</el-button>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click.native="DownloadApi">下载用例</el-button>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" @click.native="loadSwaggerApi = true">导入场景</el-button>
                                <el-dialog title="导入swagger接口" :visible.sync="loadSwaggerApi"
                                           :close-on-click-modal="false">
                                    <el-input v-model.trim="swaggerUrl" placeholder="请输入swagger接口地址"
                                              style="width:90%"></el-input>
                                    <el-button type="primary" @click="addSubmit" :loading="addLoading">导入</el-button>
                                    <P v-if="!swaggerUrl" style="color: red; margin: 0px">不能为空</P>
                                </el-dialog>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-header>

                <el-main>
                    <!--列表-->
                    <el-table :data="apiCase" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                              style="width: auto;">
                        <el-table-column type="selection" min-width="5%">
                        </el-table-column>
                        <el-table-column prop="caseName" label="场景名称" min-width="15%" sortable show-overflow-tooltip>
                            <template slot-scope="scope">
                                <el-icon name="name"></el-icon>
                                <router-link :to="{ name: '场景用例', params: {case_id: scope.row.id}}"
                                             style='text-decoration: none;'>{{ scope.row.caseName }}
                                </router-link>
                            </template>
                        </el-table-column>
                        <el-table-column prop="level" label="用例级别" min-width="10%" sortable show-overflow-tooltip>
                            <template slot-scope="scope">
                                <el-tag :type="levelType(scope.row.level)" disable-transitions="ture">P{{ scope.row.level }}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column prop="steps" label="步骤数" min-width="10%" sortable show-overflow-tooltip>
                        </el-table-column>
                        <el-table-column prop="result" label="最后结果" min-width="10%" sortable show-overflow-tooltip>
                        </el-table-column>
                        <el-table-column prop="pass_rate" label="通过率" min-width="10%" sortable show-overflow-tooltip>
                        </el-table-column>
                        <el-table-column prop="updateUser" label="最近更新者" min-width="10%" sortable show-overflow-tooltip>
                        </el-table-column>
                        <el-table-column prop="updateTime" label="更新日期" min-width="15%" sortable
                                         show-overflow-tooltip>
                        </el-table-column>
                        <el-table-column label="操作" min-width="20%">
                            <template slot-scope="scope">
                                <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除
                                </el-button>
                                <router-link :to="{ name: '修改', params: {api_id: scope.row.id}}"
                                             style='text-decoration: none;color: aliceblue;'>
                                    <el-button type="info" size="small">修改</el-button>
                                </router-link>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-main>
            </el-container>
        </el-container>

    </section>

</template>

<script>
    import sceneMenu from './sceneMenu';
    import {getApiScene,getApiGroupList} from '../../../router/api'
    import $ from 'jquery'

    export default {
        data() {
            return {
                project_id:localStorage.getItem("project_id"),
                levelList: ['','danger','warning','','success','info'], // 用例级别
                isCollapse: true,
                filters: {
                    name: ''
                },
                apiCase: [],
                total: 0,
                page: 1,
                groupname: '',
                listLoading: false,
                sels: [],//列表选中列
                updateGroupFormVisible: false,
                updateGroupForm: {
                    firstGroup: "",
                },
                updateGroupFormRules: {
                    firstGroup: [{type: 'number', required: true, message: '请选择分组', trigger: 'blur'}],
                },
                group: [],
                updateGroupLoading: false,
                update: true,
                loadSwaggerApi: false,
                addLoading: false,
                //新增界面数据
                swaggerUrl: "",
            }
        },
        methods: {
            beforeCreate(){

            },
            // 用例级别
            levelType(level){
                console.log(this.levelList[level])
                return this.levelList[level]
            },
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            },
            // 获取api分组
            getApiGroup() {
                let self = this;
                let params = {
                    project_id: this.project_id,
                    name:this.groupname,
                    type:'scene'
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getApiGroupList(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '0') {
                        self.groupData = data;
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            // 获取接口列表
            getApiList() {
                this.listLoading = true;
                let self = this;
                let params = {project_id: this.project_id, page: self.page, name: self.filters.name};
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getApiScene(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total;
                        self.apiCase = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 修改接口所属分组
            updateGroupSubmit() {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认修改所属分组吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.updateGroupLoading = true;
                    //NProgress.start();
                    let params = JSON.stringify({
                        project_id: Number(this.project_id),
                        ApiGroup_id: Number(self.updateGroupForm.firstGroup),
                        ids: ids,
                    });
                    $.ajax({
                        type: "post",
                        url: test + "/Interface/Interface/update_group",
                        async: true,
                        data: params,
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function (data) {
                            self.updateGroupLoading = false;
                            if (data.code === '0') {
                                self.$message({
                                    message: '修改成功',
                                    center: true,
                                    type: 'success'
                                });
                                self.$router.push({
                                    name: '分组接口列表',
                                    params: {
                                        project_id: self.$route.params.project_id,
                                        firstGroup: self.updateGroupForm.firstGroup
                                    }
                                });
                            } else {
                                self.$message.error({
                                    message: data.msg,
                                    center: true,
                                })
                            }
                            self.updateGroupFormVisible = false;
                            self.getApiList();
                        },
                    })
                }).catch(() => {

                });
            },
            // 修改分组弹窗
            changeGroup() {
                this.getApiGroup();
                this.updateGroupFormVisible = true
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    $.ajax({
                        type: "post",
                        url: test + "/Interface/Interface/del_api",
                        async: true,
                        data: JSON.stringify({project_id: Number(this.project_id), ids: [row.id]}),
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function (data) {
                            if (data.code === '0') {
                                self.$message({
                                    message: '删除成功',
                                    center: true,
                                    type: 'success'
                                })
                            } else {
                                self.$message.error({
                                    message: data.msg,
                                    center: true,
                                })
                            }
                            self.getApiList();
                        },
                    })

                }).catch(() => {
                });
            },
            // 下载接口文档
            DownloadApi() {
                $.ajax({
                    type: "get",
                    url: test + "/Interface/Interface/Download",
                    async: true,
                    data: {project_id: this.project_id},
                    headers: {
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    },
                    timeout: 5000,
                    success: function (data) {
                        if (data.code === "0") {
                            window.open(test + "/Interface/Interface/download_doc?url=" + data.data)
                        }
                    },
                })
            },
            // 翻页
            handleCurrentChange(val) {
                this.page = val;
                this.getApiList()
            },
            selsChange: function (sels) {
                if (sels.length > 0) {
                    this.sels = sels;
                    this.update = false
                } else {
                    this.update = true
                }
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
                    $.ajax({
                        type: "post",
                        url: test + "/Interface/Interface/del_api",
                        async: true,
                        data: JSON.stringify({project_id: Number(this.project_id), ids: ids}),
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        },
                        timeout: 5000,
                        success: function (data) {
                            self.listLoading = false;
                            if (data.code === '0') {
                                self.$message({
                                    message: '删除成功',
                                    center: true,
                                    type: 'success'
                                })
                            } else {
                                self.$message.error({
                                    message: data.msg,
                                    center: true,
                                })
                            }
                            self.getApiList();
                        },
                    })
                }).catch(() => {
                });
            },
            addSubmit() {
                let self = this;
                this.addLoading = true;
                console.log(this.swaggerUrl);
                if (this.swaggerUrl) {
                    $.ajax({
                        type: "post",
                        url: test + "/Interface/Interface/lead_swagger",
                        async: true,
                        data: JSON.stringify({project_id: Number(this.project_id), url: this.swaggerUrl}),
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                        },
                        // timeout: 5000,
                        success: function (data) {
                            if (data.code === '0') {
                                self.$message({
                                    message: '添加成功',
                                    center: true,
                                    type: 'success'
                                });
                                self.listLoading = true;
                                self.addLoading = false;
                                self.loadSwaggerApi = false;
                                self.getApiList()
                            } else {
                                self.addLoading = false;
                                self.$message.error({
                                    message: "导入失败，请检查地址是否正确",
                                    center: true,
                                })
                            }
                            self.getApiList();
                        },
                    })
                } else {
                    this.addLoading = false
                }
            },
        },
        mounted() {
            this.getApiList();
            this.getApiGroup();

        }
    }
</script>

<style lang="scss" scoped>
    .api-title {
        padding: 15px;
        margin: 0px;
        text-align: center;
        border-radius: 5px;
        font-size: 15px;
        color: aliceblue;
        background-color: rgb(32, 160, 255);
        font-family: PingFang SC;
    }

    .group .editGroup {
        float: right;
    }

    .row-title {
        margin: 35px;
    }

    .addGroup {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }

    .api-view-a {
        margin-left: 15px;
        margin-right: 15px;
        display: block;
    }

    .api-view-b {
        margin-left: 15px;
        margin-right: 15px;
        display: none;
    }

    .el-menu-vertical-demo:not(.el-menu--collapse) {
        width: 200px;
        min-height: 400px;
    }
</style>