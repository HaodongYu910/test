<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-calendar"></i>测试工具</el-breadcrumb-item>
                <el-breadcrumb-item>性能工具</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box" style='width:100%'>
                <el-form ref="form" :model="form" status-icon :rules="rules" label-width="100px">
                    <el-row>
                        <el-col :span='4'>
                            <el-form-item label="测试版本" prop="version">
                                <el-input v-model="form.version" placeholder="测试版本" id='version'></el-input>
                            </el-form-item>
                        </el-col>
                    <el-col :span='4'>
                        <el-form-item label="负载服务器" prop="Loadserver" >
                            <el-select v-model="form.Loadserver" clearable placeholder="请选择">
                                <el-option key="192.168.1.208" label="192.168.1.208" value="192.168.1.208"></el-option>
                                <el-option key="192.168.1.122" label="192.168.1.122" value="192.168.1.122"></el-option>
                                <el-option key="192.168.4.85" label="192.168.4.85" value="192.168.4.85"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                        <el-col :span='3'>
                            <el-form-item label="循环次数" prop="cycle">
                                <el-input v-model="form.loop_time" placeholder="循环测试次数" id='loop_time'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span='3'>
                            <el-form-item label="是否立即返回" prop="need_result">
                                <el-select v-model="form.need_result" clearable placeholder="请选择">
                                    <el-option key="true" label="true" value="true"></el-option>
                                    <el-option key="false" label="false" value="false"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span='3'>
                            <el-form-item label="测试数据" prop="testdata">
                                <el-select v-model="form.testdata" clearable placeholder="请选择">
                                    <el-option key="ctmra.csv" label="ctmra" value="ctmra.csv"></el-option>
                                    <el-option key="lung.csv" label="lung" value="lung.csv"></el-option>
                                    <el-option key="rc5.csv" label="rc5" value="rc5.csv"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span='3'>
                            <el-form-item>
                                <el-button type="primary" @click="find('form')">执行</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span='6'>
                            <el-form-item label="测试版本" prop="tags">
                                <el-select multiple v-model="form.tags" placeholder="请选择" @click.native="getTags()">
                                    <el-option
                                            v-for="(item,index) in tags"
                                            :key='item.key'
                                            :label='item.value'
                                            :value='item.key'
                                    ></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span='4'>
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
                                            @click="deleteTag(scope.$index, scope.row)">删除
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
    import {stressTool, getAllTags} from "../../router/api";

    export default {
        name: 'baseform',
        data() {
            return {
                form: {
                    Loadserver: '',
                    version:'',
                    testdata: [],
                    loop_time:1,
                    need_result:"false",
                },
                rules: {
                    Loadserver: [
                        {required: true, message: '请输入服务器IP', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入测试版本', trigger: 'blur'}
                    ],
                    loop_time: [
                        {required: true, message: '请输入循环次数', trigger: 'change'}
                    ],
                    testdata: [
                        {required: true, message: '请输入测试数据名称', trigger: 'change'}
                    ]
                },
                tableData: [],
                tags: [],
            }
        },
        methods: {
            find(formName) {
                this.tableData = null;
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let params = {
                            version: this.form.version,
                            Loadserver: this.form.Loadserver,
                            loop_time: this.form.loop_time,
                            need_result: this.form.need_result,
                            testdata: this.form.testdata
                        };
                        let headers = {
                            "Content-Type": "application/json"
                        };
                        stressTool(headers, params).then(_data => {
                            console.log(_data);
                            let {msg, code, data} = _data;
                            if (code != '0') {
                                this.$message.error(msg);
                                return;
                            }
                            var result = data[0];
                            if (data != null && result == false) {
                                this.$message.error(data[1]);
                                return;
                            }
                            //请求正确时执行的代码
                            var mydata = data[1];
                            var tableData = [];
                            for (var i = 0; i < mydata.length; i++) {
                                tableData.push({"name": mydata[i]});
                            }
                            var json = JSON.stringify(tableData);
                            this.tableData = JSON.parse(json);
                        })
                    } else {
                        console.log('error submit');
                        return false;
                    }
                });
            },
            getTags() {
                let params = {
                    type: '1'
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getAllTags(headers, params).then(_data => {
                    console.log(_data);
                    let {msg, code, data} = _data;
                    if (code != '0') {
                        this.$message.error(msg);
                        return;
                    }
                    //请求正确时执行的代码
                    var mydata = data.data;
                    console.log(mydata);
                    var json = JSON.stringify(mydata);
                    this.tags = JSON.parse(json);
                })

            },
            addTag(form) {
                this.$refs[form].validate((valid) => {
                    if (valid) {
                        var tags = this.form.tags;
                        if (tags.length == 0) {
                            alert("请选择要添加的tag标签");
                            return;
                        }
                        let params = {
                            rid: this.form.Loadserver + '',
                            service: this.form.app + '_' + this.form.environment,
                            tag: tags,
                            type: 'add'
                        };
                        let headers = {
                            "Content-Type": "application/json"
                        };
                        tagTool(headers, params).then(_data => {
                            console.log(_data);
                            let {msg, code, data} = _data;
                            if (code != '0') {
                                this.$message.error(msg);
                                return;
                            }
                            var result = data[0];
                            if (data != null && result == false) {
                                this.$message.error(data[1]);
                                return;
                            }
                            //请求正确时执行的代码
                            var mydata = data[1];
                            var tableData = [];
                            for (var i = 0; i < mydata.length; i++) {
                                tableData.push({"name": mydata[i]});
                            }
                            var json = JSON.stringify(tableData);
                            this.tableData = JSON.parse(json);
                            this.$message.success('添加成功！');
                        })
                    } else {
                        console.log('error submit');
                        return false;
                    }
                });
            },
            deleteTag(index, row) {
                var Loadserver = this.form.Loadserver;
                if (typeof Loadserver == "undefined" || Loadserver == null || Loadserver == "") {
                    alert("请输入要删除的ID号");
                    return;
                }
                let params = {
                    rid: this.form.Loadserver + '',
                    service: this.form.app + '_' + this.form.environment,
                    tag: row.name,
                    type: 'del'
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                tagTool(headers, params).then(_data => {
                    console.log(_data);
                    let {msg, code, data} = _data;
                    if (code != '0') {
                        this.$message.error(msg);
                        return;
                    }
                    var result = data[0];
                    if (data != null && result == false) {
                        this.$message.error(data[1]);
                        return;
                    }
                    //请求正确时执行的代码
                    var mydata = data[1];
                    var tableData = [];
                    for (var i = 0; i < mydata.length; i++) {
                        tableData.push({"name": mydata[i]});
                    }
                    var json = JSON.stringify(tableData);
                    this.tableData = JSON.parse(json);
                    this.$message.success('删除成功！');
                });
            }
        }
    }
</script>
