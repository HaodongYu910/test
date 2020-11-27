<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><i class="el-icon-lx-calendar" />测试工具</el-breadcrumb-item>
        <el-breadcrumb-item>测试数据</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="form-box" style="width:80%">
        <el-form ref="form" :model="form" status-icon :rules="rules" label-width="80px">
          <el-row>
            <el-col :span="6">
              <el-form-item label="环境选择" prop="environment">
                <el-select v-model="form.environment" clearable placeholder="请选择环境">
                  <el-option key="test" label="测试环境" value="test" />
                  <el-option key="online" label="灰度环境" value="staging" />
                </el-select>
              </el-form-item>
            </el-col>
            <!--<el-col :span='6'>-->
            <!--<el-form-item label="修改类型"  prop="update_type">-->
            <!--<el-select multiple v-model="form.update_type" placeholder="请选择" @click.native="getTags()">-->
            <!--<el-option-->
            <!--v-for="(item,index) in update_type"-->
            <!--:key='item.key'-->
            <!--:label='item.value'-->
            <!--:value='item.key'-->
            <!--&gt;</el-option>-->
            <!--</el-select>-->
            <!--</el-form-item>-->
            <!--</el-col>-->

            <el-col :span="6">
              <el-form-item label="修改类型" prop="update_type">
                <el-select v-model="form.update_type" clearable placeholder="请选择修改类型">
                  <el-option key="1" label="修改积分" value="1" />
                  <el-option key="2" label="修改CNNS" value="2" />
                  <el-option key="3" label="新增红包" value="3" />
                </el-select>
              </el-form-item>
            </el-col>
            <!--<el-col :span='4'>-->
            <!--<el-form-item>-->
            <!--<el-button type="primary" @click="find('form')">修改</el-button>-->
            <!--</el-form-item>-->
            <!--</el-col>-->
          </el-row>
          <el-row>
            <el-col :span="6">
              <el-form-item label="用户" prop="showID">
                <el-input id="showID" v-model="form.showID" placeholder="手机号，邮箱" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="数值" prop="value">
                <el-input id="value" v-model="form.value" placeholder="增加数值" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="6">
              <el-form-item label="币种" prop="coin">
                <el-select v-model="form.coin" clearable placeholder="请选择币种">
                  <el-option key="test" label="test" value="test" />
                  <el-option key="cnns" label="cnns" value="cnns" />
                  <el-option key="tether" label="USDT" value="tether" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-button type="primary" @click="updatatool('form')">添加/修改</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="6">
              <el-form-item label="选择红包" prop="candy">
                <el-select v-model="form.candy" clearable placeholder="请选择红包">
                  <el-option key="test" label="普通红包" value="test" />
                  <el-option key="cnns" label="手气红包" value="cnns" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="选择红包类型" prop="candy_type">
                <el-select v-model="form.candy_type" clearable placeholder="请选择红包类型">
                  <el-option key="test" label="粉丝红包" value="test" />
                  <el-option key="cnns" label="分享红包" value="cnns" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-button type="primary" @click="updatatool('form')">添加红包</el-button>
              </el-form-item>
            </el-col>
          </el-row>
          <div>
            <el-table :data="tableData" style="width: 50%">
              <el-table-column label="数据" width="180">
                <template slot-scope="scope">
                  <el-popover trigger="hover" placement="top">
                    <p>type标签: {{ scope.row.name }}</p>
                    <div slot="reference" class="name-wrapper">
                      <el-tag size="medium">{{ scope.row.name }}</el-tag>
                    </div>
                  </el-popover>
                </template>
              </el-table-column>
              <el-table-column fixed="right" label="结果">
                <template slot-scope="scope">
                  <el-button
                    size="mini"
                    type="danger"
                    @click="deleteTag(scope.$index, scope.row)"
                  >删除</el-button>
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
import { updatedata } from '@/router/api'
export default {
  name: 'Baseform',
  data() {
    return {
      form: {
        showID: '',
        types: []
      },
      rules: {
        showID: [
          { required: true, message: '请输入用户ID', trigger: 'blur' }
        ],
        environment: [
          { required: true, message: '请选择环境', trigger: 'change' }
        ],
        update_type: [
          { required: true, message: '请选择修改类型', trigger: 'change' }
        ],
        value: [
          { required: true, message: '请输入值', trigger: 'change' }
        ]
      },
      tableData: [],
      update_type: []
    }
  },
  methods: {
    find(formName) {
      this.tableData = null
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const params = {
            service: this.form.app + '_' + this.form.environment,
            showid: this.form.showID + '',
            type: '1',
            value: ''
          }
          const headers = {
            'Content-Type': 'application/json'
          }
          updatedata(headers, params).then(_data => {
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
            this.$message.success('修改成功！')
            var mydata = data[1]
            var tableData = []
            for (var i = 0; i < mydata.length; i++) {
              tableData.push({ 'name': mydata[i] })
            }
            var json = JSON.stringify(tableData)
            this.tableData = JSON.parse(json)
            this.$message.success('成功！')
          })
        } else {
          console.log('error submit')
          return false
        }
      })
    },
    updatatool(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          var update_type = this.form.update_type
          if (update_type.length == 0) {
            alert('请选择修改类型')
            return
          }
          const params = {
            service: this.form.environment,
            showid: this.form.showID + '',
            type: this.form.update_type,
            value: this.form.value,
            coin: this.form.coin
          }
          const headers = {
            'Content-Type': 'application/json'
          }
          updatedata(headers, params).then(_data => {
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
            this.$message.success('修改成功！')
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
    deleteTag(index, row) {
      var showID = this.form.showID
      if (typeof showID === 'undefined' || showID == null || showID == '') {
        alert('请输入要删除的ID号')
        return
      }
      const params = {
        showid: this.form.showID + '',
        service: this.form.app + '_' + this.form.environment,
        type: row.name,
        type: 'del'
      }
      const headers = {
        'Content-Type': 'application/json'
      }
      updatedata(headers, params).then(_data => {
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
