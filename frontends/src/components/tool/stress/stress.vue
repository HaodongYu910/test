<template>
  <div class="app-container">
    <div class="filter-container">
        <!--工具条-->
        <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
          <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
          <el-row>
            <el-col :span="4">
              <el-form-item label="测试版本" prop="version">
                <el-input id="version" v-model="form.version" placeholder="测试版本" />
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="测试服务器" prop="Loadserver">
                <el-select v-model="form.Loadserver"  placeholder="请选择" @click.native="gethost()">
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
              <el-form-item label="压测时间" prop="loop_time">
                <el-input id="loop_time" v-model="form.loop_time" placeholder="循环次数" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="测试数据" prop="testdata">
<!--                <el-select v-model="form.testdata" multiple placeholder="请选择" @click.native="getBase()">-->
<!--                <el-option-->
<!--                        v-for="(item,index) in tags"-->
<!--                        :key="item.key"-->
<!--                        :label="item.key"-->
<!--                        :value="item.key"-->
<!--                />-->
<!--                </el-select>-->
<!--              </el-form-item>-->
                <el-select v-model="form.testdata" multiple placeholder="请选择">
                  <el-option key="CTA" label="CTA" value="CTA" />
                  <el-option key="CTP" label="CTP" value="CTP" />
                  <el-option key="Lung" label="Lung" value="Lung" />
                  <el-option key="MRA" label="MRA" value="MRA" />
                  <el-option key="SVD" label="SVD" value="SVD" />
                  <el-option key="SWI" label="SWI" value="SWI" />
                  <el-option key="Tumor" label="Tumor" value="Tumor" />
                  <el-option key="Brain" label="Brain" value="Brain" />
                  <el-option key="Hematoma" label="Hematoma" value="Hematoma" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="是否匿名数据" prop="duration">
                <el-select v-model="form.duration" clearable placeholder="请选择">
                  <el-option key=True label="是" value=True />
                  <el-option key=False label="否" value=False />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="数据名称" prop="keyword">
                <el-input id="keyword" v-model="form.keyword" placeholder="数据名称" />
              </el-form-item>
            </el-col>
            <el-col :span="3">
              <el-form-item>
                <el-button type="primary" @click="run('form')">执行</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          </el-form>
          <el-form :inline="true" :model="filters" @submit.native.prevent>
            <el-row>
            <el-col :span="6">
              <el-form-item label="比较版本" prop="checkversion">
                <el-select v-model="form.checkversion" multiple placeholder="请选择" @click.native="getversion()">
                  <el-option
                    v-for="(item,index) in tags"
                    :key="item.key"
                    :label="item.value"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-button type="primary" @click="addTag('form')"> 生成测试报告</el-button>
              </el-form-item>
            </el-col>
          </el-row>
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
              <el-table-column fixed="right" label="操作">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="danger"
                    @click="deleteTag(scope.$index, scope.row)"
                  >删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          </el-form>
        </el-col>
    </div>
  </div>
</template>

<script>
// import NProgress from 'nprogress'
import {
  getstressdata, delstressdata, updatestressdata, addstressdata, stressTool, getVersion,getHost
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
    this.getHost()
    this.getBase()
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
    getversion() {
      const params = {
        type: '1'
      }
      const headers = {
        'Content-Type': 'application/json'
      }
      getVersion(headers, params).then(_data => {
        console.log(_data)
        const { msg, code, data } = _data
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
      this.gethost()
      this.getBase()
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
            }else {
                self.$message.error({
                    message: msg,
                    center: true
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
