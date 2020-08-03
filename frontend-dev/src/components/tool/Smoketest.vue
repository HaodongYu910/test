<template>
  <div>
    <div class="container">
      <aside>
        <a href="http://192.168.2.22:3000/" target="_blank" />
      </aside>
      <div class="form-box" style="width:100%">
        <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
          <el-row>
            <el-col :span="4">
              <el-form-item label="测试版本" prop="version">
                <el-input id="version" v-model="form.version" placeholder="测试版本" />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="测试服务器" prop="Loadserver">
                <el-select v-model="form.Loadserver" clearable placeholder="请选择">
                  <el-option key="192.168.1.208" label="192.168.1.208" value="192.168.1.208" />
                  <el-option key="192.168.1.122" label="192.168.1.122" value="192.168.1.122" />
                  <el-option key="192.168.4.85" label="192.168.4.85" value="192.168.4.85" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="3">
              <el-form-item>
                <el-button type="primary" @click="find('form')">执行</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="6">
              <el-form-item label="测试版本" prop="nowversion">
                <el-select v-model="form.nowversion" multiple placeholder="请选择" @click.native="getversion()">
                  <el-option
                    v-for="(item,index) in tags"
                    :key="item.key"
                    :label="item.value"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>
            </el-col>
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
      </div>

    </div>
  </div>
</template>

<script>
import { stressTool, getVersion } from '@/router/api'

export default {
  name: 'Baseform',
  data() {
    return {
      form: {
        Loadserver: '',
        version: '',
        testdata: 'test_data.csv',
        loop_time: 1,
        block: 'false'
      },
      rules: {
        Loadserver: [
          { required: true, message: '请输入测试服务器', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入测试版本', trigger: 'blur' }
        ]
      },
      tableData: [],
      tags: []
    }
  },
  methods: {
    find(formName) {
      this.tableData = null
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const params = {
            version: this.form.version,
            loadserver: this.form.Loadserver,
            loop_time: this.form.loop_time,
            block: this.form.block,
            testdata: this.form.testdata,
            smoke: 1
          }
          const headers = {
            'Content-Type': 'application/json'
          }
          stressTool(headers, params).then(_data => {
            console.log(_data)
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
    addTag(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          var tags = this.form.tags
          if (tags.length == 0) {
            alert('请选择要添加的tag标签')
            return
          }
          const params = {
            rid: this.form.Loadserver + '',
            service: this.form.app + '_' + this.form.environment,
            tag: tags,
            type: 'add'
          }
          const headers = {
            'Content-Type': 'application/json'
          }
          tagTool(headers, params).then(_data => {
            console.log(_data)
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
            this.$message.success('添加成功！')
          })
        } else {
          console.log('error submit')
          return false
        }
      })
    },
    deleteTag(index, row) {
      var Loadserver = this.form.Loadserver
      if (typeof Loadserver === 'undefined' || Loadserver == null || Loadserver == '') {
        alert('请输入要删除的ID号')
        return
      }
      const params = {
        rid: this.form.Loadserver + '',
        service: this.form.app + '_' + this.form.environment,
        tag: row.name,
        type: 'del'
      }
      const headers = {
        'Content-Type': 'application/json'
      }
      tagTool(headers, params).then(_data => {
        console.log(_data)
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
        this.$message.success('删除成功！')
      })
    }
  }
}
</script>
