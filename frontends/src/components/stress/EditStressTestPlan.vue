<template>
    <div class="app-container">
<el-collapse v-model="activeNames" @change="handleChange">
  <el-collapse-item title="服务配置 Server Config" name="1">
    <div>
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
            </el-col></el-row></div>
    <div>在界面中一致：所有的元素和结构需保持一致，比如：设计样式、图标和文本、元素的位置等。</div>
  </el-collapse-item>
  <el-collapse-item title="反馈 Feedback" name="2">
    <div>控制反馈：通过界面样式和交互动效让用户可以清晰的感知自己的操作；</div>
    <div>页面反馈：操作后，通过页面元素的变化清晰地展现当前状态。</div>
  </el-collapse-item>
  <el-collapse-item title="效率 Efficiency" name="3">
    <div>简化流程：设计简洁直观的操作流程；</div>
    <div>清晰明确：语言表达清晰且表意明确，让用户快速理解进而作出决策；</div>
    <div>帮助用户识别：界面简单直白，让用户快速识别而非回忆，减少用户记忆负担。</div>
  </el-collapse-item>
  <el-collapse-item title="可控 Controllability" name="4">
    <div>用户决策：根据场景可给予用户操作建议或安全提示，但不能代替用户进行决策；</div>
    <div>结果可控：用户可以自由的进行操作，包括撤销、回退和终止当前操作等。</div>
  </el-collapse-item>
</el-collapse>
        <div class="filter-container">
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
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <aside>
                    <a href="http://192.168.2.38:3000/d/Ss3q6hSZk/docker-and-os-metrics-test?orgId=1&refresh=5s&from=now-5m&to=now&var-host_name=192.168.2.60&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080" target="_blank">Stress Monitor
                    </a>
                </aside>
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span="3">
                            <el-form-item label="服务器" prop="loadserver">
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
                        <el-col :span="3">
                        <el-form-item label="测试版本" prop="version">
                          <el-input id="version" v-model="form.version" placeholder="测试版本" />
                        </el-form-item>
                      </el-col>
                        <el-col :span="3">
                              <el-form-item label="压测时间" prop="loop_time">
                                <el-input id="loop_time" v-model="form.loop_time" placeholder="测试小时" />
                              </el-form-item>
                            </el-col>
                        <el-col :span="3">
                            <el-form-item label="线程数" prop="loop_time">
                                <el-input id="thread" v-model="form.thread" placeholder="个" />
                              </el-form-item>
                            </el-col>
                            <el-col :span="3">
                              <el-form-item label="循环次数" prop="loop">
                                <el-input id="loop" v-model="form.loop" placeholder="个" />
                              </el-form-item>
                            </el-col>
                        <el-col :span="3">
                              <el-form-item label="并发" prop="synchronizing">
                                <el-input id="synchronizing" v-model="form.synchronizing" placeholder="个" />
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
                    <el-row>
                            <el-checkbox-group v-model="form.testdata" size="small">
                              <el-checkbox-button v-for="(item,index) in dibase" :label="item.remarks" :key="item.remarks">{{item.remarks}}</el-checkbox-button>
                            </el-checkbox-group>
                    </el-row>

            </el-col>
        </div>
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
