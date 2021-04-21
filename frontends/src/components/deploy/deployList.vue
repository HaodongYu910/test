<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form-item label="服务器" prop="server">
                <el-select v-model="filters.server" placeholder="请选择服务" @click.native="gethost()">
                    <el-option v-for="(item,index) in tags"
                               :key="item.id"
                               :label="item.name"
                               :value="item.id"
                    />
                </el-select>
            </el-form-item>
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="名称" @keyup.enter.native="getInstalllist"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getInstalllist">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">创建任务</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <!--列表-->
        <el-table :data="UIlist" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                  style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <!--            <el-table-column prop="ID" label="ID" min-width="12%" sortable>-->
            <!--                <template slot-scope="scope">-->
            <!--                    <span style="margin-left: 10px">{{ scope.row.id }}</span>-->
            <!--                </template>-->
            <!--            </el-table-column>-->
            <el-table-column prop="version" label="部署版本" min-width="12%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link :to="{ name: '冒烟报告', params: {reportid: scope.row.id}}"
                                 style='text-decoration: none;color: #0000ff;'>
                        {{ scope.row.version }}
                    </router-link>
                </template>
            </el-table-column>
            <el-table-column prop="server" label="部署服务" min-width="12%" sortable>
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.server }}</span>
                </template>
            </el-table-column>
            <el-table-column label="部署时间" min-width="16%">
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row.starttime  | dateformat('YYYY-MM-DD HH:mm:SS')}}</span>
                </template>
            </el-table-column>
            <el-table-column label="进度" min-width="45%">
                <el-steps slot-scope="scope" :active="scope.row.type" align-center finish-status="success">
                    <el-step title="准备中"></el-step>
                    <el-step title="备份上传"></el-step>
                    <el-step title="安装部署"></el-step>
                    <el-step title="重启服务"></el-step>
                    <el-step title="完成"></el-step>
                    <el-step title="金标准"></el-step>
                    <el-step title="UI测试"></el-step>
                </el-steps>
            </el-table-column>
            <el-table-column prop="installstatus" label="全新部署" min-width="8%">
                <template slot-scope="scope">
                    <img v-show="scope.row.installstatus"
                         style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.installstatus"
                         style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="6%">
                <template slot-scope="scope">
                    <img v-show="scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/qiyong.png"/>
                    <img v-show="!scope.row.status" style="width:18px;height:18px;margin-right:5px;margin-bottom:5px"
                         src="../../assets/img/fou.png"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="25%">
                <template slot-scope="scope">

                    <el-row>
                       <el-button :type="typestatus(scope.row.status)" size="small"
                                   @click="handleChangeStatus(scope.$index, scope.row)">
                            {{scope.row.status===false?'部 署':'停 止'}}
                        </el-button>
                        <el-button type="warning" size="small" @click="showJournal(scope.$index, scope.row)">日 志
                        </el-button>
                        <el-button type="primary" size="small" @click="handleCreate(scope.$index, scope.row)">创建用户
                        </el-button>
                         <el-button type="danger" size="small" @click="Restart(scope.$index, scope.row)">重启
                        </el-button>
                    </el-row>
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
                <el-row :gutter="36">
                    <el-col :span="12">
                        <el-form-item label="setUp" prop='setUp'>
                            <el-select v-model="editForm.setup" multiple placeholder="请选择" @click.native="getsetUp()">
                                <el-option v-for="(item,index) in setUp"
                                           :key="item.caseid"
                                           :label="item.name"
                                           :value="item.caseid"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="case" prop='case'>
                            <el-select v-model="editForm.testdata" multiple placeholder="请选择" @click.native="getCase()">
                                <el-option v-for="(item,index) in testcase"
                                           :key="item.caseid"
                                           :label="item.name"
                                           :value="item.caseid"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="tearDown" prop='tearDown'>
                            <el-select v-model="editForm.tearDown" multiple placeholder="请选择"
                                       @click.native="gettearDown()">
                                <el-option v-for="(item,index) in tearDown"
                                           :key="item.caseid"
                                           :label="item.name"
                                           :value="item.caseid"
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

        <!--新增界面-->
        <el-dialog title="新增部署" :visible.sync="addFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-divider>基本配置</el-divider>
                <el-row :gutter="24">
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
                    <el-col :span="12">
                        <el-form-item label="选择版本" prop='version'>
                            <el-select v-model="addForm.version" placeholder="请选择安装版本"
                                       @click.native="Installversion()">
                                <el-option
                                        v-for="item in versionlist"
                                        :key="item"
                                        :label="item"
                                        :value="item"
                                />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="24">
                    <el-col :span="8">
                        <el-switch
                                style="display: block"
                                v-model="addForm.installstatus"
                                active-color="#13ce66"
                                inactive-color="#ff4949"
                                active-text="全新安装"
                                inactive-text="升级安装">
                        </el-switch>
                    </el-col>

                    <el-col :span="8">
                        <el-switch
                                style="display: block"
                                v-model="addForm.testcase"
                                active-color="#13ce66"
                                inactive-color="#ff4949"
                                active-text=""
                                inactive-text="更新备份">
                        </el-switch>
                    </el-col>
                    <el-col :span="8">
                        <el-switch
                                style="display: block"
                                v-model="addForm.cache"
                                active-color="#13ce66"
                                inactive-color="#ff4949"
                                active-text=""
                                inactive-text="更新cache">
                        </el-switch>
                    </el-col>
                </el-row>
                <el-divider>冒烟配置</el-divider>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-switch
                                style="display: block"
                                v-model="addForm.smokeid"
                                active-color="#13ce66"
                                inactive-color="#ff4949"
                                active-text=""
                                inactive-text="金标准测试">
                        </el-switch>
                    </el-col>
                    <el-col :span="12">
                        <el-switch
                                style="display: block"
                                v-model="addForm.uid"
                                active-color="#13ce66"
                                inactive-color="#ff4949"
                                active-text=""
                                inactive-text="UI测试">
                        </el-switch>
                    </el-col>
                </el-row>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">保存</el-button>
            </div>
        </el-dialog>

        <!--错误图片页面-->
        <el-dialog title="错误截图" :visible.sync="imageVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <div class="block" v-for="(value, key, index) in fits" :key="fit">
                <span class="demonstration">{{ key }}</span>
                <el-image
                        style="width: 100px; height: 100px"
                        :src="value"
                        :fit="key"
                        :preview-src-list="srcList">
                </el-image>
            </div>

            <div slot="footer" class="dialog-footer">
                <el-button @click.native="imageVisible = false">关闭</el-button>
            </div>
        </el-dialog>

        <!--安装日志页面-->
        <el-dialog :visible.sync="journalVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-tabs v-model="activeName" type="border-card" stretch ="ture" @tab-click="handleClick">
                <el-tab-pane label="部署日志" name="deploy">
                    <el-card id="deploycard" class="box-card"
                             style="background:black;color:white;max-height:27.2em;overflow:auto">
                        <div id="deploytext" style="background:black;color:white;" @click="autoFocus()">
                            <ul id="deployid">
                                <li style="color:#44ff00;">【部署日志】<br/></li>
                                <li>========================================================================<br/></li>
                                <div style="color:yellow;" :key="journal" class="text item">
                                    <p v-html="deploystr" style="white-space: pre-line;"></p>
                                </div>
                            </ul>
                            <el-input
                                    v-loading="loading"
                                    type="text"
                                    id="deploy"
                                    class="input_text"
                                    v-model="command"
                                    resize="none"
                                    @keyup.enter.native="enter()"
                                    autofocus="autofocus">
                                <span slot="prepend" style="font-size:18px">></span>
                            </el-input>
                        </div>
                    </el-card>
                    <div slot="footer" class="dialog-footer">
                        <el-button @click.native="journalVisible = false">关闭</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="安装日志" name="second">
                    <el-card id="installcard" class="box-card"
                             style="background:black;color:white;max-height:27.2em;overflow:auto">
                        <div id="installid" style="background:black;color:white;" @click="autoFocus()">
                            <ul id="installul">
                                <li style="color:#44ff00;">【安装日志】<br/></li>
                                <li>========================================================================<br/></li>
                                <div style="color:yellow;" :key="journal" class="text item">
                                    <p v-html="installstr" style="white-space: pre-line;"></p>
                                </div>
                            </ul>
                            <el-input
                                    v-loading="loading"
                                    type="text"
                                    id="install"
                                    class="input_text"
                                    v-model="command"
                                    resize="none"
                                    @keyup.enter.native="enter()"
                                    autofocus="autofocus">
                                <span slot="prepend" style="font-size:18px">></span>
                            </el-input>
                        </div>
                    </el-card>
                    <div slot="footer" class="dialog-footer">
                        <el-button @click.native="journalVisible = false">关闭</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="重启日志" name="third">
                    <el-card id="card" class="box-card"
                             style="background:black;color:white;max-height:27.2em;overflow:auto">
                        <div id="restartid" style="background:black;color:white;" @click="autoFocus()">
                            <ul id="ulrestart">
                                <li style="color:#44ff00;">【重启日志】<br/></li>
                                <li>========================================================================<br/></li>
                                <div style="color:yellow;" :key="journal" class="text item">
                                    <p v-html="restartstr" style="white-space: pre-line;"></p>
                                </div>
                            </ul>
                            <el-input
                                    v-loading="loading"
                                    type="text"
                                    id="restar"
                                    class="input_text"
                                    v-model="command"
                                    resize="none"
                                    @keyup.enter.native="enter()"
                                    autofocus="autofocus">
                                <span slot="prepend" style="font-size:18px">></span>
                            </el-input>
                        </div>
                    </el-card>
                    <div slot="footer" class="dialog-footer">
                        <el-button @click.native="journalVisible = false">关闭</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="金标准日志" name="fourth">
                    <el-card id="goldcard" class="box-card"
                             style="background:black;color:white;max-height:27.2em;overflow:auto">
                        <div id="goldid" style="background:black;color:white;" @click="autoFocus()">
                            <ul id="ulgold">
                                <li style="color:#44ff00;">【金标准日志】<br/></li>
                                <li>========================================================================<br/></li>
                                <div style="color:yellow;" :key="journal" class="text item">
                                    <p v-html="goldstr" style="white-space: pre-line;"></p>
                                </div>
                            </ul>
                            <el-input
                                    v-loading="loading"
                                    type="text"
                                    id="gold"
                                    class="input_text"
                                    v-model="command"
                                    resize="none"
                                    @keyup.enter.native="enter()"
                                    autofocus="autofocus">
                                <span slot="prepend" style="font-size:18px">></span>
                            </el-input>
                        </div>
                    </el-card>
                    <div slot="footer" class="dialog-footer">
                        <el-button @click.native="journalVisible = false">关闭</el-button>
                    </div>
                </el-tab-pane>
            </el-tabs>

        </el-dialog>
    </section>

</template>

<script>
    //import NProgress from 'nprogress'
    import {
        getInstall, delInstall, DisableInstall, EnableInstall, getInstallersion,
        updateInstall, addInstall, getJournal, getImage, getHost, getbase, getCreateRestart
    } from '../../router/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                log: 0,
                timerId: 1, // 模拟计时器id，唯一性
                timerObj: {}, // 计时器存储器
                command: '',
                loading: false,
                activeName:"deploy",
                filters: {
                    name: ''
                },
                id: '',
                UIlist: [],
                versionlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列
                deploystr: '',
                installstr: '',
                restartstr: '',
                golgstr: '',
                journalVisible: false, //日志页面是否显示
                imageVisible: false, //错误图像页面是否显示
                reportVisible: false, //报告页面是否显示
                fits: ["暂无图片"],
                reports: ["未生成报告内容"],
                url: 'http://192.168.1.121/static/UI/demo.jpg',
                srcList: [
                    'http://192.168.1.121/static/UI/demo.jpg'
                ],
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                options: [{label: "Web", value: "Web"}, {label: "App", value: "App"}],
                editFormRules: {
                    Host: [
                        {required: true, message: '请选择服务', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                    ]
                },
                //编辑界面数据
                editForm: {
                    Host: '',
                    version: '',
                    thread: 1,
                    testdata: []
                },

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
                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    Host: [
                        {required: true, message: '请选择服务', trigger: 'blur'}
                    ]
                },
                //新增界面数据
                addForm: {
                    server: '',
                    version: '',
                    status: false,
                    installstatus: false,
                    smokeid: true,
                    uid: false,
                    testcase: false,
                    cache: true
                }
            }
        },
        created() {
            // 实现轮询
            this.InstalllTimeSet = window.setInterval(() => {
                setTimeout(this.getInstalllist(), 0);
            }, 10000);
        },
        beforeDestroy() {    //页面关闭时清除定时器
            clearInterval(this.InstalllTimeSet);
            clearInterval(this.journalTimeSet);
        },
        mounted() {
            this.gethost()
            this.getBase()
        },
        directives: {
            focus: {
                inserted: function (el, {value}) {
                    console.log(el, {value})
                    if (value) {
                        el.focus()
                    }
                }
            }
        },
        watch: {
            loading: {
                handler(newVal, oldVal) {
                    if (newVal == false) {
                        this.scoll()
                    }
                },
                deep: true
            }
        },
        methods: {
            /*
           * 开始轮训
           * */
            startTraining() {
                let this_ = this;
                const id = this.timerId++
                this.timerObj[id] = true

                async function timerFn() {
                    if (!this_.timerObj[id]) return
                    await this_.showJournal(this.id);
                    setTimeout(timerFn, 1 * 1000)
                }

                timerFn();
            },
            /*
                * 停止轮训
                * */
            stopTime() {
                this.timerObj = {}
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
                    path: '/SmokeReport/reportid=' + row.id,
                });
            },
            handleClick(tab, event) {
                this.showJournal()
            },
            showJournal(index, row) {
                this.journalVisible = true;
                this.listLoading = true
                let self = this;
                const params = {
                    id: row.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getJournal(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.deploy = data.deploy
                        this.install = data.install
                        this.restart = data.restart
                        this.gold = data.gold

                        this.deploystr = this.deploy.replace(/↵/g, "\n");
                        this.installstr = this.install.replace(/↵/g, "\n");
                        this.restartstr = this.restart.replace(/↵/g, "\n");
                        this.goldstr = this.gold.replace(/↵/g, "\n");

                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            //显示错误截图
            showImage(index, row) {
                this.imageVisible = true;
                let self = this;
                const params = {
                    autoid: row.autoid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getImage(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.srcList = data.srcList
                        this.fits = data.fits
                        // var json = JSON.stringify(this.list)
                        // this.tearDown = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            //  重启服务
            Restart(index, row) {
                this.listLoading = true
                let self = this;
                const params = {
                    id: row.id,
                    type: 1
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getCreateRestart(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
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
            // 获取host数据列表
            Installversion() {
                this.listLoading = true
                let self = this;
                const params = {
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getInstallersion(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.versionlist = data.data
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
                let self = this;
                const params = {
                    page_size: 100
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
            // 获取getBase列表
            getBase() {
                this.listLoading = true
                const self = this
                const params = {
                    status: 1,
                    type: 'gold'
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getbase(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.model = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取列表
            getInstalllist() {
                this.listLoading = true;
                let self = this;
                let params = {
                    page: self.page,
                    version: self.filters.version
                };
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getInstall(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '0') {
                        self.total = data.total;
                        self.UIlist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
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
                    DisableInstall(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '已停止',
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
                    EnableInstall(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '启动成功',
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
                this.getInstalllist()
                this.getBase()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示新增界面
            handleCreate: function (index, row) {
                this.createFormVisible = true;
                this.createForm = Object.assign({}, row);
                this.createForm[pwd] = 1
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    version: null,
                    server: '',
                    smokeid: true,
                    uid: false,
                    testcase: false,
                    cache: true
                };
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
                                autoid: self.editForm.autoid,
                                version: self.editForm.version,
                                setup: self.editForm.setup,
                                cases: self.editForm.cases,
                                tearDown: self.editForm.tearDown,
                                thread: this.editForm.thread
                            };
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            updateInstall(header, params).then(_data => {
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
                                    self.getInstalllist()
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
                                installstatus: self.addForm.installstatus,
                                smokeid: self.addForm.smokeid,
                                uid: self.addForm.uid,
                                testcase: self.addForm.testcase,
                                cache: self.addForm.cache,
                                status: false
                            });
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            addInstall(header, params).then(_data => {
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
                                    self.getInstalllist()
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
                                    self.getInstalllist()
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
                    delInstall(header, params).then(_data => {
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
                        self.getInstalllist()
                    });
                })
            }
        },
        mounted() {
            this.getInstalllist();
            this.getBase();
        }
    }

</script>

<style>
    ul {
        margin: 0px;
        padding: 0px;
        list-style: none;
    }

    .input_text .el-input__inner:focus {
        border: 1px solid black;
    }

    .input_text .el-input__inner:hover {
        border: 1px solid black;
    }

    .input_text .el-input__inner {
        color: green;
        border: 1px solid black;
        background-color: black;
    }

    .input_text .el-input-group__prepend {
        padding: 0px;
        color: white;
        border: 1px solid black;
        background-color: black;
    }

</style>