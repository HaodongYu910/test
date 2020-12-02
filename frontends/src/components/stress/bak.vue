<template>
    <div class="app-container">
<!--        <el-row>-->
<!--          <el-col :span="12" :offset="2">-->
<!--            <el-button :disabled="isReadOnly" type="primary" plain @click="save">保存</el-button>-->
<!--            <el-button :disabled="isReadOnly" type="primary" plain @click="saveAndRun">保存并测试-->
<!--            </el-button>-->
<!--            <el-button :disabled="isReadOnly" type="warning" plain @click="cancel">取消-->
<!--            </el-button>-->

<!--            <ms-schedule-config :schedule="testPlan.schedule" :save="saveCronExpression" @scheduleChange="saveSchedule"-->
<!--                                :check-open="checkScheduleEdit" :test-id="testId" :custom-validate="durationValidate"/>-->
<!--          </el-col>-->
<!--        </el-row>-->
            <!--工具条-->

              <el-collapse-item title="服务配置 Server Config" name="1">
                <el-form  :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span="5">
                            <el-form-item label="基本配置" prop="loadserver">
                            <el-select v-model="form.loadserver"  placeholder="请选择" @click.native="gethost()">
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
                        <el-form-item label="测试版本" prop="version">
                          <el-input id="version" v-model="form.version" placeholder="测试版本" />
                        </el-form-item>
                      </el-col>
                        <el-col :span="3">
                              <el-form-item label="压测时间" prop="loop_time">
                                <el-input id="loop_time" v-model="form.loop_time" placeholder="测试小时" />
                              </el-form-item>
                            </el-col>
                    </el-row>
                </el-form>
              </el-collapse-item>
              <el-collapse-item title="压力配置" name="2">
                <el-form  :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span="4">
                            <el-form-item label="线程数" prop="loop_time">
                                <el-input-number v-model="form.thread" @change="handleChange" :min="1" :max="10000" label="描述文字"></el-input-number>
                              </el-form-item>
                            </el-col>
                            <el-col :span="4">
                              <el-form-item label="循环次数" prop="loop">
                                  <el-input-number v-model="form.loop" @change="handleChange" :min="0" :max="10000" label="描述文字"></el-input-number>
                              </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                        <el-col :span="3">
                              <el-form-item label="并发用户数：" prop="synchronizing">
                                  <el-input-number v-model="form.synchronizing" @change="handleChange" :min="1" :max="10000" label="描述文字"></el-input-number>
                              </el-form-item>
                            </el-col>
                        <el-col :span="3">
                            <el-form-item label="dicom发送" prop="loadserver">
                                <el-switch v-model="form.switch" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                                </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item>
                                <el-button type="primary" @click="stressrun('form')">执行</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
              </el-collapse-item>
<!--              <el-collapse-item title="参数配置" name="3">-->
<!--                  <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>-->
<!--                      <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>-->
<!--                          <div style="margin: 15px 0;"></div>-->
<!--                          <el-checkbox-group v-model="form.testdata" @change="mounted">-->
<!--                            <el-checkbox v-for="(item,index) in dibase" :label="item.remarks" :key="item.remarks">{{item.remarks}}</el-checkbox>-->
<!--                          </el-checkbox-group>-->
<!--              </el-collapse-item>-->
<!--              <el-collapse-item title="jmeter 文件上传" name="4">-->
<!--                <el-upload accept=".jmx,.csv,.jar"  drag action=""-->
<!--                         :limit="fileNumLimit"-->
<!--                         multiple-->
<!--                         :show-file-list="false"-->
<!--                         :before-upload="beforeUpload"-->
<!--                         :http-request="handleUpload"-->
<!--                         :on-exceed="handleExceed"-->
<!--                         :disabled="isReadOnly"-->
<!--                         :file-list="fileList">-->
<!--                  <i class="el-icon-upload"/>-->
<!--                  <div class="el-upload__text" v-html="将文件拖到此处,或点击上传"></div>-->
<!--                  <template v-slot:tip>-->
<!--                    <div class="el-upload__tip">只能上传JMX/CSV文件</div>-->
<!--                  </template>-->
<!--                </el-upload>-->

<!--              <el-table class="basic-config" :data="tableData">-->
<!--                <el-table-column-->
<!--                  prop="name"-->
<!--                  :label="文件名">-->
<!--                </el-table-column>-->
<!--                <el-table-column-->
<!--                  prop="size"-->
<!--                  :label="文件大小">-->
<!--                </el-table-column>-->
<!--                <el-table-column-->
<!--                  prop="type"-->
<!--                  :label="文件类型">-->
<!--                </el-table-column>-->
<!--                <el-table-column-->
<!--                  :label="修改时间">-->
<!--                  <template v-slot:default="scope">-->
<!--                    <i class="el-icon-time"/>-->
<!--                    <span class="last-modified">{{ scope.row.updateTime | timestampFormatDate }}</span>-->
<!--                  </template>-->
<!--                </el-table-column>-->
<!--                <el-table-column-->
<!--                  :label="操作">-->
<!--                  <template v-slot:default="scope">-->
<!--                    <el-button @click="handleDownload(scope.row)" :disabled="!scope.row.id || isReadOnly" type="primary"-->
<!--                               icon="el-icon-download"-->
<!--                               size="mini" circle/>-->
<!--                    <el-button :disabled="isReadOnly" @click="handleDelete(scope.row, scope.$index)" type="danger"-->
<!--                               icon="el-icon-delete" size="mini"-->
<!--                               circle/>-->
<!--                  </template>-->
<!--                </el-table-column>-->
<!--              </el-table>-->
<!--                </el-collapse-item>-->

<!--                &lt;!&ndash;工具条&ndash;&gt;-->
<!--                <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">-->
<!--&lt;!&ndash;                    <el-form :inline="true" :model="filters" @submit.native.prevent>&ndash;&gt;-->
<!--&lt;!&ndash;                        <el-select v-model="filters.server"  placeholder="请选择服务器" @click.native="gethost()">&ndash;&gt;-->
<!--&lt;!&ndash;                              <el-option&ndash;&gt;-->
<!--&lt;!&ndash;                                v-for="(item,index) in tags"&ndash;&gt;-->
<!--&lt;!&ndash;                                :key="item.host"&ndash;&gt;-->
<!--&lt;!&ndash;                                :label="item.name"&ndash;&gt;-->
<!--&lt;!&ndash;                                :value="item.host"&ndash;&gt;-->
<!--&lt;!&ndash;                              />&ndash;&gt;-->
<!--&lt;!&ndash;                            </el-select>&ndash;&gt;-->
<!--&lt;!&ndash;                        <el-select v-model="filters.version"  placeholder="当前版本" @click.native="getversion()">&ndash;&gt;-->
<!--&lt;!&ndash;                              <el-option&ndash;&gt;-->
<!--&lt;!&ndash;                                v-for="(item,index) in versions"&ndash;&gt;-->
<!--&lt;!&ndash;                                :key="item.version"&ndash;&gt;-->
<!--&lt;!&ndash;                                :label="item.version"&ndash;&gt;-->
<!--&lt;!&ndash;                                :value="item.version"&ndash;&gt;-->
<!--&lt;!&ndash;                              />&ndash;&gt;-->
<!--&lt;!&ndash;                            </el-select>&ndash;&gt;-->
<!--&lt;!&ndash;                        <el-select v-model="filters.checkversion"  placeholder="以前版本" @click.native="getversion()">&ndash;&gt;-->
<!--&lt;!&ndash;                              <el-option&ndash;&gt;-->
<!--&lt;!&ndash;                                v-for="(item,index) in versions"&ndash;&gt;-->
<!--&lt;!&ndash;                                :key="item.version"&ndash;&gt;-->
<!--&lt;!&ndash;                                :label="item.version"&ndash;&gt;-->
<!--&lt;!&ndash;                                :value="item.version"&ndash;&gt;-->
<!--&lt;!&ndash;                              />&ndash;&gt;-->
<!--&lt;!&ndash;                            </el-select>&ndash;&gt;-->
<!--                        <el-form-item>-->
<!--                            <el-button type="primary" @click="getDurationlist">查询</el-button>-->
<!--                        </el-form-item>-->
<!--                        <el-form-item>-->
<!--                            <el-button type="primary" @click="handleAdd">生成报告</el-button>-->
<!--                        </el-form-item>-->
<!--                </el-col>-->
        </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        StressDetail,getstressversion,getstressresult, getHost,getbase,stressTool
    } from '@/router/api'
    import {addbaseData, loadRisk} from "../../router/api";
    import stressDetail from "./stressDetail";
  export default {
    // import ElRow from "element-ui/packages/row/src/row";
        // components: {ElRow},
        data() {
            return {
                cities: ['lung','swi','svd'],
                form: {
                    version: '',
                    loadserver: '192.168.1.208',
                    loop_time: '1',
                    thread:4,
                    synchronizing:0,
                    testdata:['Lung','Brain','SWI','SVD','Tumor','Heart','Hematoma','CTA','CTP'],
                    switch:false
                },
                rules: {
                    server: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入测试版本', trigger: 'blur'}
                    ]
                },
                filters: {
                    diseases: ''
                },
                durationlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列
                elForm:'',
                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                options: [{label: 'Web', value: 'Web'}, {label: 'App', value: 'App'}],
                editFormRules: {
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
                    ],
                    description: [
                        {required: false, message: '请输入描述', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                filters: {
                    checkversion: '2.11.0',
                    version: '2.10.0RC9',
                    server: '192.168.1.208'
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
            this.getBase()
        },
        created(){
            this.getParams();
            this.getData();
        },
        activated() {
            this.getParams();
            this.getData();
        },
        methods: {
          getData(){
            let params={
                id:this.routerParams.id
            };
            let headers= {
                'Content-Type': 'application/x-www-form-urlencoded'
            };
          StressDetail(headers,params).then(_data=>{
              if(_data.length==0) {
                this.from=null;
                return;
              }
              this.from=_data;
            });
            },
          //获取由路由传递过来的参数
          getParams(){
            this.routerParams=this.$route.query;
            },
            // 执行压测
          stressrun(formName) {
            let self = this;
            this.tableData = null
            this.$refs[formName].validate((valid) => {
              if (valid) {
                let params = JSON.stringify({
                  version: this.form.version,
                  loadserver: this.form.loadserver,
                  loop_time: this.form.loop_time,
                  thread:this.form.thread,
                  testdata: this.form.testdata,
                  switch: this.form.switch,
                  loop: this.form.loop,
                  synchronizing:this.form.synchronizing
                });
                let header = {
                  "Content-Type": "application/json",
                  Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                stressTool(header, params).then(_data => {
                  let {msg, code,data } = _data;
                  if (code === '0') {
                    self.$message({
                      message: '执行成功',
                      center: true,
                      type: 'Success'
                    });
                  } else {
                    self.$message.error({
                      message: msg,
                      center: true,
                    });
                  }
                })
              }
            })
            },
            getversion() {
                let self = this;
                this.listLoading = true
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressversion(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
                        this.versions = JSON.parse(json)
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
                let self = this;
                this.listLoading = true
                const params = {selecttype:"dicom",status:1}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getbase(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
                        this.dibase = JSON.parse(json)
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
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.total = data.total
                        this.list = data.data
                        var json = JSON.stringify(this.list)
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
                let self = this;
                const params = {
                    version: this.filters.version,
                    checkversion: this.filters.checkversion,
                    server: this.filters.server
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressresult(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.prediction = data.predictionresult
                        this.job =data.jobresult
                        this.lung =data.lungresult
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
