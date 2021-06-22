<template>
  <div class="app-container">
    <div class="filter-container">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.patientname" placeholder="patientname" @keyup.enter.native="getDurationlist" />
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker v-model="filters.startdate" type="datetime"
                                           value-format="yyyy-MM-dd HH:mm:ss" placeholder="选择日期"></el-date-picker>
          </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker v-model="filters.enddate" type="datetime"
                                           value-format="yyyy-MM-dd HH:mm:ss" placeholder="选择日期"></el-date-picker>
          </el-form-item>
        <el-form-item>
          <el-select v-model="filters.type" placeholder="请选择类型">
            <el-option key="AiTrue" label="预测成功chenggongle!" value="AiTrue"></el-option>
            <el-option key="AiFalse" label="预测失败" value="AiFalse"></el-option>
            <el-option key="Not_sent" label="未发送" value="Not_sent"></el-option>
            <el-option key="sent" label="已发送数据" value="sent"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getDurationlist">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getdurationVerify">同步结果</el-button>
        </el-form-item>
      </el-form>

    </el-col>
        <!--列表-->
        <el-table
          v-loading="listLoading"
          :data="durationdatalist"
          highlight-current-row
          style="width: 100%;"
          @selection-change="selsChange">
          <el-table-column prop="patientname" label="PatientName" min-width="15%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.patientname }}</span>

            </template>
          </el-table-column>
          <el-table-column prop="studyolduid" label="studyolduid" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.studyolduid }}</span>
            </template>
          </el-table-column>
          <el-table-column label="studyuid" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.studyinstanceuid }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="发送张数" label="发送张数" min-width="12%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.imagecount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="接收张数" label="接收张数" min-width="12%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.imagecount_server }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="预测结果" label="预测结果" min-width="9%" sortable>
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.aistatus }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="诊断结果" label="诊断结果" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.diagnosis }}</span>
            </template>
          </el-table-column>
             <el-table-column prop="耗时/张" label="耗时/张" min-width="12%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.time }}</span>
            </template>
          </el-table-column>
          <el-table-column label="发送日期" min-width="10%">
            <template slot-scope="scope">
              <span style="margin-left: 12px">{{ scope.row.create_time  | dateformat('YYYY-MM-DD HH:MM:SS') }}</span>
            </template>
          </el-table-column>
            <el-table-column label="操作" min-width="20%">
                    <template slot-scope="scope">
                       <el-button type="primary" size="small" @click="handleU(scope.$index, scope.row)">跳转</el-button>
                        <el-button type="primary" size="small" @click="handlesource(scope.row)">源</el-button>
                    </template>
                </el-table-column>
        </el-table>
      <el-footer style="margin-top:20px;">
          <el-pagination
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                  :current-page="page"
                  :page-sizes="[20,50,100]"
                  :page-size="page-size"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="count"
                   style="float:right;"
                ></el-pagination>
      </el-footer>
      <!--工具条-->
        <!--源数据界面-->
        <el-dialog title="源数据" :visible.sync="sourceFormVisible" :close-on-click-modal="false"
                       style="width: 100%; left: 10%">
                <el-form :model="sourceForm" label-width="120"  ref="sourceForm">
                    <el-divider>源数据信息</el-divider>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="patientname：" prop='patientname'>
                            </el-form-item>
                            <el-input id="patientname" v-model="sourceForm.patientname"
                                      placeholder="patientname"></el-input>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="patientid：" prop='patientid'>
                            </el-form-item>
                            <el-input id="patientid" v-model="sourceForm.patientid"
                                      placeholder="patientid"></el-input>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="studyinstanceuid：" prop='studyinstanceuid'>
                            </el-form-item>
                            <el-input id="studyinstanceuid" v-model="sourceForm.studyinstanceuid"
                                      placeholder="studyinstanceuid"></el-input>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="diseases：" prop='diseases'>
                            </el-form-item>
                            <el-input id="diseases" v-model="sourceForm.diseases"
                                      placeholder="diseases"></el-input>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="route：" prop='route'>
                            </el-form-item>
                            <el-input id="route" v-model="sourceForm.route"
                                      placeholder="route"></el-input>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="status：" prop='status'>
                            </el-form-item>
                            <el-input id="status" v-model="sourceForm.status"
                                      placeholder="status"></el-input>
                        </el-col>
                    </el-row>
                    <el-divider>匿名数据</el-divider>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="sourceFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="handleDisable" :loading="sourceLoading">禁用</el-button>
                </div>
            </el-dialog>
    </div>
  </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getdurationData,getdurationverify,
        getdicomurl,detailDisable,getdurationsource
    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    durationlist: [],
                    selectdate:'',
                },
                sourceForm:{

                },
                total:0,
                page: 1,
                count:0,
                page_size:20,
                size:"",
                durationdatalist:[],
                patientname:'',
                listLoading: false,
                sels: [], // 列表选中列
                sourceFormVisible:false,
                sourceLoading:false

            }
        },
        created(){
          this.getParams();
          },
        activated() {
          this.getParams();
          },
        methods: {

            //获取由路由传递过来的参数
            getParams(){
                console.log(this.$route)
              this.id=this.$route.query.id;
              this.getDurationlist();
              },
            handlesource: function(row) {
                this.getsource(row)
                this.sourceFormVisible = true
            },
            handleSizeChange: function(size) {
              this.page_size = size;
              this.getDurationlist()
            },
            getsource(row) {
                this.sourceLoading = true
                const self = this
                const params = {
                  id:row.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdurationsource(headers, params).then((res) => {
                    self.sourceLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.sourceForm = data
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
                const params = {
                  page: self.page,
                  page_size: self.page_size,
                  patientname: self.filters.patientname,
                  type:self.filters.type,
                  startdate:self.filters.startdate,
                  enddate:self.filters.enddate,
                  id:this.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdurationData(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.count = data.count
                        self.durationdatalist = data.data
                        self.durationresult = data.durationresult
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            getdurationVerify() {
                this.listLoading = true
                const self = this
                const params = {
                  id: this.routerParams.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdurationverify(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.datalist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            handleDisable: function (index, row) {
                this.$confirm('确认禁用原数据?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        studyuid: row.studyolduid
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    detailDisable(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            self.$message.info({
                                message: msg,
                                center: true,
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getdata()
                    });
                })
            },
            handleU: function (index, row) {
                this.$confirm('打开imageview页面?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: row.id,
                        type: "duration"
                    };
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    getdicomurl(header, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '0') {
                            const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : screen.left
                            const dualScreenTop = window.screenTop !== undefined ? window.screenTop : screen.top

                            const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width
                            const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height

                            const left = ((width / 2) - (800 / 2)) + dualScreenLeft
                            const top = ((height / 2) - (800 / 2)) + dualScreenTop
                            const newWindow = window.open(data.url, 'title', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=yes, copyhistory=no, width=' + '800' + ', height=' + '800' + ', top=' + top + ', left=' + left)

                              // Puts focus on the newWindow
                            if (window.focus) {
                                newWindow.focus()
                            }
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getdata()
                    });
                })
            },
            handleCurrentChange(val) {
                this.page = val
                this.getDurationlist()
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