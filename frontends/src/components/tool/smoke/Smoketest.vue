<template>
  <div class="app-container">
    <div class="filter-container">
        <!--工具条-->
        <el-col :span="20" class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline="true" :model="filters" @submit.native.prevent>
        <el-form-item label="服务器" prop="server">
                  <el-select v-model="filters.server"  placeholder="请选择服务" @click.native="gethost()">
                    <el-option v-for="(item,index) in tags"
                                :key="item.host"
                                :label="item.name"
                                :value="item.host"
                              />
                    </el-select>
                  </el-form-item>
        <el-form-item label="版本">
          <el-input v-model="filters.version" ></el-input>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.diseases" placeholder="请选择病种类型" @click.native="getBase()">
            <el-option v-for="(item,index) in tags"
                             :key="item.remarks"
                             :label="item.remarks"
                             :value="item.remarks"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="warning" @click="somketest">smoke测试</el-button>
        </el-form-item>
        <el-button type="danger" :disabled="this.sels.length===0" @click="batchdel">删除报告</el-button>
      </el-form>
    </el-col>
        <!--列表-->
        <el-table
          v-loading="listLoading"
          :data="stresslist"
          highlight-current-row
          style="width: 100%;"
          @selection-change="selsChange">
          <el-table-column prop="ID" label="ID" min-width="4%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.id }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="version" label="版本" min-width="8%" sortable>
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.version }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="patientid" label="Patientid" min-width="10%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.patientid }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="studyinstanceuid" label="Studyinstanceuid" min-width="25%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.studyinstanceuid }}</span>
            </template>
          </el-table-column>
          <el-table-column label="预测时间" min-width="8%" sortable>
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.time }}</span>
            </template>
          </el-table-column>
          <el-table-column label="slicenumber" min-width="8%" sortable>
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
            </template>
          </el-table-column>
          <el-table-column label="预测张数" min-width="5%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.imagecount }}</span>
            </template>
          </el-table-column>
          <el-table-column label="预测状态" min-width="8%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.aidiagnosis }}</span>
            </template>
          </el-table-column>
          <el-table-column label="标准诊断" min-width="10%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.diagnosis }}</span>
            </template>
          </el-table-column>
          <el-table-column label="实际结果" min-width="10%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.aidiagnosis }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="8px">
            <template slot-scope="scope">
    <!--          <el-button v-if=scope.row.edit  type="success"  size="small" icon="el-icon-circle-check-outline" @click="handleEdit(scope.$index, scope.row)">Ok</el-button>-->
    <!--          <el-button v-else type="primary" size="small" icon="el-icon-edit" @click=scope.row.edit=!scope.row.edit>Edit</el-button>-->
               <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">重测</el-button>
<!--              <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
            </template>
          </el-table-column>
        </el-table>
        <!--工具条-->
        <el-col :span="24" class="toolbar">
          <el-pagination
            layout="prev, pager, next"
            :page-size="20"
            :page-count="total"
            style="float:right;"
            @current-change="handleCurrentChange"
          />
        </el-col>
    </div>
  </div>
</template>

<script>
// import NProgress from 'nprogress'
import {
  getHost,getsomkerecord,getsomkestart, getbase,deldicomreport
} from '@/router/api'

// import ElRow from "element-ui/packages/row/src/row";
export default {
  // components: {ElRow},
  data() {
    return {
      filters: {
        diseases: null,
        slicenumber:null
      },
      total: 0,
      page: 1,
      listLoading: false,
      sels: [], // 列表选中列

      // 新增界面数据
      addForm: {
        diseases: '',
        server: '192.168.1.208',
        studyinstanceuid:''
      },
      addFormVisible: false, // 新增界面是否显示
      addLoading: false,
      addFormRules: {
        diseases: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ]
      }

    }
  },
  mounted() {
    this.getdata()
    this.gethost()
  },
  methods: {
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
          self.$message.error({message: msg,
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
        selecttype:"dicom",
        status:1
      }
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
    somketest() {
      this.listLoading = true
      const self = this
      const params = {
        server_ip: self.filters.server,
        diseases: self.filters.diseases,
        version: self.filters.version
      }
      const headers = { Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token')) }
      getsomkestart(headers, params).then((res) => {
        self.listLoading = false
        const { msg, code, data } = res
        if (code === '0') {
          self.stresslist = data.data
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
        diseases: self.filters.diseases,
        server: self.filters.server,
        slicenumber:self.filters.slicenumber,
        type:'Gold'
      }
      const headers = { Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token')) }
      getsomkerecord(headers, params).then((res) => {
        self.listLoading = false
        const { msg, code, data } = res
        if (code === '0') {
          self.total = data.total
          self.page = data.page
          self.stresslist = data.data
        } else {
          self.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 删除
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        const self = this
        const params = { ids: [row.id] }
        const header = {
          'Content-Type': 'application/json',
          Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
        }
        deldicomdata(header, params).then(_data => {
          const { msg, code, data } = _data
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
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 显示新增界面
    handleAdd: function() {
      this.addFormVisible = true
      this.addForm = {
        patientid: null,
        diseases: null,
        studyinstanceuid: null,
      }
    },
    // 编辑
    editSubmit: function() {
      const self = this
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            self.editLoading = true
            // NProgress.start();
            const params = {
              id: self.editForm.id,
              patientid: self.editForm.patientid,
              studyinstanceuid: self.editForm.studyinstanceuid,
              diseases: self.editForm.diseases,
              slicenumber: self.editForm.slicenumber,
              vote: self.editForm.vote
            }
            const header = {
              'Content-Type': 'application/json',
              Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
            }
            updatedicomdata(header, params).then(_data => {
              const { msg, code, data } = _data
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
    // 新增
    addSubmit: function() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          const self = this
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            self.addLoading = true
            // NProgress.start();
            const params = JSON.stringify({
              diseases: self.addForm.diseases,
              patientid: self.addForm.patientid,
              server: self.addForm.server,
              studyinstanceuid:self.addForm.studyinstanceuid
            })
            const header = {
              'Content-Type': 'application/json',
              Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
            }
            adddicomdata(header, params).then(_data => {
              const { msg, code, data } = _data
              self.addLoading = false
              if (code === '0') {
                self.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                self.$refs['addForm'].resetFields()
                self.addFormVisible = false
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
                self.$refs['addForm'].resetFields()
                self.addFormVisible = false
                self.getdata()
              }
            })
          })
        }
      })
    },
    selsChange: function(sels) {
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
    batchRemove: function() {
      const ids = this.sels.map(item => item.id)
      const self = this
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        const self = this
        const params = { ids: ids }
        const header = {
          'Content-Type': 'application/json',
          Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
        }
        deldicomdata(header, params).then(_data => {
          const { msg, code, data } = _data
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
    batchCsv: function() {
      const ids = this.sels.map(item => item.id)
      const self = this
      this.$confirm('确认生成选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        const self = this
        const params = { ids: ids }
        const header = {
          'Content-Type': 'application/json',
          Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
        }
        dicomcsv(header, params).then(_data => {
          const { msg, code, data } = _data
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
    // 批量删除报告
    batchDel: function() {
      const ids = this.sels.map(item => item.id)
      const self = this
      this.$confirm('确认删除选中记录的报告吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        const self = this
        const params = { ids: ids }
        const header = {
          'Content-Type': 'application/json',
          Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
        }
        deldicomreport(header, params).then(_data => {
          const { msg, code, data } = _data
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
