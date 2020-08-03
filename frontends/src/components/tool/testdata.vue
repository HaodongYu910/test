<template>
  <div class="app-container">
    <div class="filter-container">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
      <el-form :inline="true" :model="filters" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.name" placeholder="名称" @keyup.enter.native="getProjectList" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getProjectList">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>
        <!--列表-->
        <el-table
          v-loading="listLoading"
          :data="stresslist"
          highlight-current-row
          style="width: 100%;"
          @selection-change="selsChange">
          <el-table-column type="selection" min-width="3%" />
          <el-table-column prop="ID" label="ID" min-width="5%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.id }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="patientid" label="Patientid" min-width="20%" sortable>
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
                <el-table-column label="手动/自动" min-width="10%" sortable>
                  <template slot-scope="scope">
                    <span style="margin-left: 20px">{{ scope.row.automatic }}</span>
                  </template>
                </el-table-column>
    <!--      <el-table-column min-width="10%" label="类型">-->
    <!--        <template slot-scope="scope">-->
    <!--          <template v-if="row.edit">-->
    <!--            <el-input v-model="row.diseases" class="edit-input" size="small" />-->
    <!--            <el-button-->
    <!--              class="cancel-btn"-->
    <!--              size="small"-->
    <!--              icon="el-icon-refresh"-->
    <!--              type="warning"-->
    <!--              @click="cancelEdit(row)"-->
    <!--            >-->
    <!--              cancel-->
    <!--            </el-button>-->
    <!--          </template>-->
    <!--          <span v-else>{{ scope.row.diseases }}</span>-->
    <!--        </template>-->
    <!--      </el-table-column>-->
          <el-table-column label="挂载序列" min-width="35%">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.vote }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="30px">
            <template slot-scope="scope">
    <!--          <el-button v-if=scope.row.edit  type="success"  size="small" icon="el-icon-circle-check-outline" @click="handleEdit(scope.$index, scope.row)">Ok</el-button>-->
    <!--          <el-button v-else type="primary" size="small" icon="el-icon-edit" @click=scope.row.edit=!scope.row.edit>Edit</el-button>-->
              <el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
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
        <!--新增界面-->
        <el-dialog
          title="新增"
          :visible.sync="addFormVisible"
          :close-on-click-modal="false"
          style="width: 75%; left: 12.5%"
        >
          <el-form ref="addForm" :model="addForm" label-width="80px" :rules="addFormRules">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="类型" prop="type">
                  <el-select v-model="addForm.type" placeholder="请选择">
                    <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="patientid" prop="patientid">
                  <el-input v-model.trim="addForm.patientid" auto-complete="off" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="项目开始时间">
                  <el-date-picker
                    v-model="addForm.start_date"
                    type="datetime"
                    placeholder="选择日期"
                    value-format="yyyy-MM-dd HH:mm:ss"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="接口提测时间" prop="api_date">
                  <el-date-picker
                    v-model="addForm.api_date"
                    type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss"
                    placeholder="选择日期"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="APP提测时间" prop="app_date">
                  <el-date-picker
                    v-model="addForm.app_date"
                    type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss"
                    placeholder="选择日期"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="接口上线时间" prop="api_online_date">
                  <el-date-picker
                    v-model="addForm.api_online_date"
                    type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss"
                    placeholder="选择日期"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="发布日期" prop="end_date">
                  <el-date-picker
                    v-model="addForm.end_date"
                    type="datetime"
                    value-format="yyyy-MM-dd HH:mm:ss"
                    placeholder="选择日期"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="项目状态" prop="projectstatus">
                  <el-select v-model="addForm.projectstatus" placeholder="请选择">
                    <el-option key="未开发" label="未开发" value="未开发" />
                    <el-option key="开发中" label="开发中" value="开发中" />
                    <el-option key="接口测试" label="接口测试" value="接口测试" />
                    <el-option key="功能测试" label="功能测试" value="功能测试" />
                    <el-option key="灰度测试" label="灰度测试" value="灰度测试" />
                    <el-option key="已上线" label="已上线" value="已上线" />
                  </el-select>
                </el-form-item>
              </el-col>

            </el-row>
            <el-form-item label="描述" prop="description">
              <el-input v-model="addForm.description" type="textarea" :rows="6" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="addFormVisible = false">取消</el-button>
            <el-button type="primary" :loading="addLoading" @click.native="addSubmit">提交</el-button>
          </div>
        </el-dialog>
    </div>
  </div>
</template>

<script>
// import NProgress from 'nprogress'
import {
  getstressdata, delstressdata, updatestressdata, addstressdata, stressTool, getVersion
} from '@/router/api'

// import ElRow from "element-ui/packages/row/src/row";
export default {
  // components: {ElRow},
  data() {
    return {
      form: {
        Loadserver: '192.168.1.208',
        version: '',
        testdata: [],
        loop_time: 1
      },
      rules: {
        Loadserver: [
          { required: true, message: '请输入测试服务器', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入测试版本', trigger: 'blur' }
        ]
      },
      filters: {
        diseases: ''
      },
      project: [],
      total: 0,
      page: 1,
      listLoading: false,
      sels: [], // 列表选中列

      editFormVisible: false, // 编辑界面是否显示
      editLoading: false,
      options: [{ label: 'Web', value: 'Web' }, { label: 'App', value: 'App' }],
      editFormRules: {
        diseases: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择类型', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入版本号', trigger: 'change' },
          { pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
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
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择类型', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入版本号', trigger: 'change' },
          { pattern: /^\d+\.\d+\.\d+$/, message: '请输入合法的版本号（x.x.x）' }
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
    this.getstressdata()
  },
  methods: {
    run(formName) {
      this.tableData = null
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const params = {
            version: this.form.version,
            loadserver: this.form.Loadserver,
            loop_time: this.form.loop_time,
            testdata: this.form.testdata,
            duration: this.form.duration,
            keyword: this.form.keyword
          }
          const headers = {
            'Content-Type': 'application/json'
          }
          stressTool(headers, params).then(_data => {
            console.log(this.form.testdata)
            const { msg, code, data } = _data
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
              tableData.push({ 'name': mydata[i] })
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
    // 获取数据列表
    getstressdata() {
      this.listLoading = true
      const self = this
      const params = { page: self.page, diseases: self.filters.diseases }
      const headers = { Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token')) }
      getstressdata(headers, params).then((res) => {
        self.listLoading = false
        const { msg, code, data } = res
        if (code === '0') {
          self.total = data.total
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
        delstressdata(header, params).then(_data => {
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
          self.getstressdata()
        })
      })
    },
    handleCurrentChange(val) {
      this.page = val
      this.getstressdata()
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
        version: null,
        diseases: null,
        status: null,
        start_date: null,
        api_date: null,
        app_date: null,
        api_online_date: null,
        end_date: null,
        type: null,
        projectstatus: null,
        description: null
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
              automatic: self.editForm.automatic,
              vote: self.editForm.vote
            }
            const header = {
              'Content-Type': 'application/json',
              Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
            }
            updatestressdata(header, params).then(_data => {
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
                self.getstressdata()
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
              type: self.addForm.type,
              version: self.addForm.version,
              description: self.addForm.description,
              start_date: this.addForm.start_date,
              api_date: this.addForm.api_date,
              app_date: this.addForm.app_date,
              api_online_date: this.addForm.api_online_date,
              end_date: this.addForm.end_date,
              projectstatus: this.addForm.projectstatus
            })
            const header = {
              'Content-Type': 'application/json',
              Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
            }
            addstressdata(header, params).then(_data => {
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
                self.getstressdata()
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
                self.getstressdata()
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
        delstressdata(header, params).then(_data => {
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
          self.getstressdata()
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
