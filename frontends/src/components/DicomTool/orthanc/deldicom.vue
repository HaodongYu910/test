<template>
    <div class="app-container">
        <div class="filter-container">
            <!--工具条-->
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <aside>
                    <a href="http://192.168.2.38:9000/" target="_blank">删除dicom数据
                    </a>
                </aside>
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span="5">
                            <el-form-item label="测试服务器" prop="serverID">
                            <el-select v-model="form.serverID"  placeholder="请选择" @click.native="gethost()">
                              <el-option
                                v-for="(item,index) in tags"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                              />
                            </el-select>
                          </el-form-item>
                        </el-col>
                        <el-col :span="5">
                            <el-form-item label="删除数据" prop="deldata">
                                <el-input id="deldata" v-model="form.deldata" placeholder="删除数据"/>
                            </el-form-item>
                        </el-col>
                        <el-col :span="5">
                            <el-form-item label="数据类型" prop="testtype">
                                <el-select v-model="form.testtype" placeholder="请选择">
                                    <el-option key="fail" label="预测失败" value="fail"/>
                                    <el-option key="repeat" label="重复" value="repeat"/>
                                    <el-option key="gold" label="金标准" value="gold"/>
                                    <el-option key="error" label="错误数据" value="error"/>
                                    <el-option key="patientname" label="患者姓名" value="patientname"/>
                                    <el-option key="patientid" label="患者编号" value="patientid"/>
                                    <el-option key="studyinstanceuid" label="studyinstanceuid" value="studyinstanceuid"/>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="3">
                            <el-form-item label="模糊搜索" prop="fuzzy">
                                <el-switch v-model="form.fuzzy" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item>
                                <el-button type="primary" @click="deldicom('form')">删除</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <div>
                     <!--工具条-->
                    <template v-for="(item,index) of delresult">
                                <li>StudyUID : {{ item }}       PatientName: {{index}} </li>
                            </template>
                    <!--列表-->
                    <el-table :data="delresult" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 200%">

                </el-table>
                </div>
            </el-col>
        </div>
    </div>
</template>

<script>
    import {
        delete_patients, getHost
    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                form: {
                    serverID: '',
                    fuzzy: '是',
                    testtype: 'gold',
                    deldata: ''
                },
                rules: {
                    serverID: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                },
                delresult: {},
                listLoading: true,
                sels: [], // 列表选中列

            }
        },
        mounted() {
            this.gethost()
        },
        methods: {
            deldicom(formName) {
                this.listLoading =true
                this.tableData = null
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        const params = {
                            serverID: this.form.serverID,
                            deldata: this.form.deldata,
                            testtype: this.form.testtype,
                            fuzzy: this.form.fuzzy
                        }
                        const headers = {
                            'Content-Type': 'application/json'
                        }
                        delete_patients(headers, params).then(_data => {
                            console.log(this.form.testtype)
                            const {msg, code, data} = _data
                            if (code != '0') {
                                this.$message.error(msg)
                                return
                            }
                            var result = data[0]
                            if (data != null && result == false) {
                                this.$message.error("删除失败")
                                return
                            }
                            // // 请求正确时执行的代码
                            // var mydata = data
                            // var tableData = []
                            // for (var i = 0; i < mydata.length; i++) {
                            //     tableData.push({'name': mydata[i]})
                            // }
                            this.listLoading = false
                            var del = JSON.stringify(data)
                            this.delresult = JSON.parse(del)
                            console.log(this.delresult)
                            this.$message.error("删除成功")
                        })
                    } else {
                        console.log('error submit')
                        return false
                    }
                })
            },
            // 获取host数据列表
            gethost() {
                this.listLoading = true
                const self = this
                const params = {
                    page_size:100
                }
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
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            selsChange: function (sels) {
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
