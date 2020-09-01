<template>
  <div class="app-container">
    <div class="filter-container">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline="true" :model="filters" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.patientid" placeholder="patientid" @keyup.enter.native="getData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getProjectList">查询</el-button>
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
          <el-table-column prop="patientid" label="Patientid" min-width="15%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.patientid }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="accessionnumber" label="accessionnumber" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.accessionnumber }}</span>
            </template>
          </el-table-column>
          <el-table-column label="studyuid" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.studyinstanceuid }}</span>
            </template>
          </el-table-column>
          <el-table-column label="原studyuid" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 20px">{{ scope.row.studyolduid }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="发送影像张数" label="发送影像张数" min-width="12%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.imagecount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="接收影像张数" label="接收影像张数" min-width="12%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.imagecount_server }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="预测结果" label="预测结果" min-width="12%" sortable>
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.aistatus }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="诊断结果" label="诊断结果" min-width="20%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.diagnosis }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="发送服务器" label="发送服务器" min-width="10%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.sendserver }}</span>
            </template>
          </el-table-column>
          <el-table-column label="发送时间" min-width="10%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.create_time }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="10px">
            <template slot-scope="scope">
              <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">查询结果</el-button>
            </template>
          </el-table-column>
        </el-table>
    </div>
  </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getduration,getdurationData,getHost, getVersion,getbase
    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    durationlist: [],
                },
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列

            }
        },
        created(){
          this.getParams();
          this.getDurationlist();
          },
        activated() {
          this.getParams();
          this.getDurationlist();
          },
        methods: {
            //获取由路由传递过来的参数
            getParams(){
              this.routerParams=this.$route.query;
              },
            // 获取数据列表
            getDurationlist() {
                this.listLoading = true
                const self = this
                const params = {
                  id:this.routerParams.id
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getdurationData(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.durationdatalist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
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