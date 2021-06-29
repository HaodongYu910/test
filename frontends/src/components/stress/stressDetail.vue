<template>
    <div class="app-container">
        <div class="filter-container">
            <el-row>
                <!--工具条-->
                <el-col :span="30" class="toolbar" style="padding-bottom: 0px;">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-form-item label="版本/名称" prop="version">
                            <el-input placeholder="请输入内容" v-model="detailForm.name">
                                <template slot="prepend">{{detailForm.version}}</template>
                            </el-input>

                        </el-form-item>
                        <el-form-item label="服务器" prop="server">
                            <el-select v-model="detailForm.loadserver" placeholder="请选择服务" @click.native="gethost()">
                                <el-option key="" label="" value=""></el-option>
                                <el-option v-for="(item,index) in Host"
                                           :key="item.id"
                                           :label="item.name"
                                           :value="item.id"
                                />
                            </el-select>
                        </el-form-item>

                        <el-form-item>
                            <el-button type="primary" @click="handleAdd">修改</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="danger" @click="handleAdd">停止</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
            <!--列表-->
            <el-row>
                <!--                <el-tabs v-model="activeName" @tab-click="handleClick">-->
                <el-tabs v-model="activeName" tab-position="top" @tab-click="handleClick">
                    <el-tab-pane label="场景配置" name="SceneConfiguration">
                        <el-form :model="detailForm" label-width="25%" :rules="addFormRules" ref="addForm">
                            <el-row>
                                <el-form-item label="Jmeter文件" prop="name">
                                    <el-select v-model="detailForm.filename" placeholder="请选择"
                                               @click.native="getuploadList()">
                                        <el-option
                                                v-for="(item,index) in jmeterList"
                                                :key="item.filename"
                                                :label="item.filename"
                                                :value="item.filename"
                                        />
                                    </el-select>
                                </el-form-item>
                            </el-row>
                            <el-row :gutter="24">
                                <el-col :span="16">
                                    <el-card>
                                        <el-table
                                                :data="jmeterData"
                                                style="width: 100%"
                                                :row-class-name="jmeterData">
                                            <el-table-column
                                                    prop="filename"
                                                    label="场景名称"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="CSVData"
                                                    label="CSVData"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="变量"
                                                    label="变量"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="address"
                                                    label="操作">
                                            </el-table-column>
                                        </el-table>
                                    </el-card>
                                </el-col>
                                <el-col :span="8">
                                    <el-card>
                                        <el-divider>测试进度</el-divider>
                                        <el-form-item label="基准测试" prop='thread'>
                                            <el-progress :color="customColors" :text-inside="true" :stroke-width="26"
                                                         :percentage="progress.manual"></el-progress>
                                        </el-form-item>
                                        <el-form-item label="单一测试" prop='thread'>
                                            <el-progress :color="customColors" :text-inside="true" :stroke-width="26"
                                                         :percentage="progress.single"></el-progress>
                                        </el-form-item>
                                        <el-form-item label="混合测试" prop='thread'>
                                            <el-progress :color="customColors" :text-inside="true" :stroke-width="26"
                                                         :percentage="progress.hybrid" status="success"></el-progress>
                                        </el-form-item>
                                    </el-card>
                                </el-col>
                            </el-row>
                            <el-row :gutter="24">
                                <el-col :span="16">
                                    <el-card>
                                        <el-divider>Jmeter-配置</el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-form-item label="线程数" prop='thread'>
                                                    <el-input-number v-model="detailForm.thread" @change="handleChange"
                                                                     :min="1"
                                                                     :max="100"
                                                                     label="线程数"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-form-item label="Ramp-Up" prop='ramp'>
                                                    <el-input-number v-model="detailForm.ramp" @change="handleChange"
                                                                     :min="0"
                                                                     :max="5000"
                                                                     label="Ramp-Up"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="12">
                                                <el-form-item label="并发数" prop='synchroniz'>
                                                    <el-input-number v-model="detailForm.synchroniz"
                                                                     @change="handleChange"
                                                                     :min="0"
                                                                     :max="100"
                                                                     label="并发数"></el-input-number>
                                                </el-form-item>
                                            </el-col>

                                            <el-col :span="12">
                                                <el-form-item label="持续时间" prop='single'>
                                                    <el-input-number v-model="detailForm.loop_time"
                                                                     @change="handleChange"
                                                                     :min="0"
                                                                     :max="1000000"
                                                                     label="持续时间"></el-input-number>
                                                    秒
                                                </el-form-item>

                                            </el-col>
                                        </el-row>
                                    </el-card>
                                </el-col>
                                <el-col :span="8">
                                    <el-divider>Jmeter-文件上传</el-divider>
                                    <el-upload
                                            class="upload-demo"
                                            action="#"
                                            :file-list="fileList"
                                            :on-change="changeData"
                                            multiple
                                            :http-request="handleRequest"
                                            :before-upload="beforeUpload"
                                            :on-remove="handleRemove"
                                            :before-remove="beforeRemove">

                                        <el-button class="btn upload-btn">上传附件</el-button>
                                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                        <div slot="tip" class="el-upload__tip">只能上传jmx/.py文件</div>
                                    </el-upload>
                                    <el-progress :stroke-width="16" :percentage="100"></el-progress>
                                </el-col>
                            </el-row>
                        </el-form>

                    </el-tab-pane>
                    <el-tab-pane label="基准测试" name="JZ">
                        <el-form :model="detailForm" label-width="80px" :rules="addFormRules" ref="addForm">
                            <el-row :gutter="24">
                                <el-col :span="4">
                                    <el-card>
                                        <el-divider>基准-配置</el-divider>
                                        <el-row>
                                            <el-col>
                                                <el-form-item label="循环次数" prop='benchmark'>
                                                    <el-input-number v-model="detailForm.benchmark"
                                                                     @change="handleChange"
                                                                     :min="1"
                                                                     :max="5000"
                                                                     label="基准循环次数"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                            <el-col>
                                                <el-form-item label="开始时间" prop='benchmarkstart'>
                                                    <el-input
                                                            placeholder="请选择日期"
                                                            suffix-icon="el-icon-date"
                                                            v-model="detailForm.benchmarkstart">
                                                    </el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col>
                                                <el-form-item label="结束时间" prop='benchmarkend'>
                                                    <el-input
                                                            placeholder="请选择日期"
                                                            suffix-icon="el-icon-date"
                                                            v-model="detailForm.benchmarkend">
                                                    </el-input>
                                                </el-form-item>
                                            </el-col>

                                        </el-row>

                                    </el-card>
                                </el-col>
                                <el-col :span="16">
                                    <el-card>
                                        <el-table :data="modelDetail" v-loading="listLoading"
                                                  @selection-change="selsChange"
                                                  style="width: 100%;">
                                            <el-table-column prop="modelname" label="模型" min-width="10%">
                                                <template slot-scope="scope">
                                                    <span  style="margin-left: 11px;color: #07c4a8; font-family:微软雅黑">{{ scope.row.modelname }}</span>
                                                </template>
                                            </el-table-column>
                                            <el-table-column prop="slicenumber" label="层厚" min-width="6%">
                                                <template slot-scope="scope">
                                                    <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                                                </template>
                                            </el-table-column>
                                            <el-table-column prop="type" label="Avg Time /s" min-width="15%">
                                                <template slot-scope="scope">
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.jobavg)">{{ scope.row.jobavg }}</span>
                                                    </el-row>
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                                                    </el-row>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="Median Time /s" min-width="15%">
                                                <template slot-scope="scope">
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.jobmedian)">{{ scope.row.jobmedian }}</span>
                                                    </el-row>
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                                                    </el-row>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="Min Time /s" min-width="15%">
                                                <template slot-scope="scope">
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.jobmin)">{{ scope.row.jobmin }}</span>
                                                    </el-row>
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.min)">{{ scope.row.min }}</span>
                                                    </el-row>
                                                </template>
                                            </el-table-column>
                                            <el-table-column prop="type" label="Max Time /s" min-width="15%">
                                                <template slot-scope="scope">
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Job:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.jobmax)">{{ scope.row.jobmax }}</span>
                                                    </el-row>
                                                    <el-row>
                                                        <span style="margin-left: 10px;color: #0e9aef; font-family:微软雅黑">Prediction:</span>
                                                        <span style="margin-left: 10px"
                                                              :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                                                    </el-row>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="预测张数" min-width="6%">
                                                <template slot-scope="scope">
                                                    <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                                                </template>
                                            </el-table-column>
                                        </el-table>

                                    </el-card>
                                </el-col>
                                <el-col :span="4">
                                    <el-card>
                                        <el-divider>操作</el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >执行测试
                                                </el-button>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-button type="primary" @click="checkExpress(jzstart,jzend)"
                                                >服务监控
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-divider></el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >同步结果
                                                </el-button>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-button type="primary" @click="showReport"
                                                >测试报告
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-tab-pane>
                    <el-tab-pane label="单一测试" name="DY">
                        <el-form :model="detailForm" label-width="80px" :rules="addFormRules" ref="addForm">
                            <el-row :gutter="24">
                                <el-col :span="6">
                                    <el-card>
                                        <el-divider>单一配置</el-divider>
                                        <el-row>
                                            <el-col>
                                                <el-form-item label="测试时间" prop='benchmark'>
                                                    <el-input-number v-model="detailForm.single"
                                                                     @change="handleChange"
                                                                     :min="1"
                                                                     :max="100"
                                                                     label="测试时间"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                            <el-col>
                                                <el-form-item label="开始时间" prop='benchmarkstart'>
                                                    <el-input
                                                            placeholder="请选择日期"
                                                            suffix-icon="el-icon-date"
                                                            v-model="detailForm.start_date">
                                                    </el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col>
                                                <el-form-item label="结束时间" prop='benchmarkend'>
                                                    <el-input
                                                            placeholder="请选择日期"
                                                            suffix-icon="el-icon-date"
                                                            v-model="detailForm.end_date">
                                                    </el-input>
                                                </el-form-item>
                                            </el-col>

                                        </el-row>

                                    </el-card>
                                </el-col>
                                <el-col :span="14">
                                    <el-card>
                                        <el-table
                                                :data="modelDetail"
                                                style="width: 100%"
                                                :row-class-name="modelDetail">
                                            <el-table-column
                                                    prop="modelname"
                                                    label="模型"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="start_date"
                                                    label="开始时间"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="end_date"
                                                    label="结束时间"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="operation"
                                                    label="操作">
                                            </el-table-column>
                                        </el-table>
                                    </el-card>
                                </el-col>
                                <el-col :span="4">
                                    <el-card>
                                        <el-divider>操作</el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >执行测试
                                                </el-button>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-button type="primary" @click="checkExpress(dystart,dyend)"
                                                >服务监控
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-divider></el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >同步结果
                                                </el-button>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-button type="primary" @click="showReport"
                                                >测试报告
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-tab-pane>
                    <el-tab-pane label="混合测试" name="HH">
                        <el-form :model="detailForm" label-width="80px" :rules="addFormRules" ref="addForm">
                            <el-row :gutter="24">
                                <el-col :span="6">
                                    <el-card>
                                        <el-divider>混合-配置</el-divider>
                                        <el-row>
                                            <el-col>
                                                <el-form-item label="负载时间" prop='duration'>
                                                    <el-input-number v-model="detailForm.duration"
                                                                     @change="handleChange"
                                                                     :min="1"
                                                                     :max="100"
                                                                     label="负载时间"></el-input-number>
                                                    小时
                                                </el-form-item>
                                            </el-col>
                                            <el-col>
                                                <el-form-item label="开始时间" prop='benchmarkstart'>
                                                    <el-input
                                                            placeholder="请选择日期"
                                                            suffix-icon="el-icon-date"
                                                            v-model="detailForm.start_date">
                                                    </el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col>
                                                <el-form-item label="结束时间" prop='benchmarkend'>
                                                    <el-input
                                                            placeholder="请选择日期"
                                                            suffix-icon="el-icon-date"
                                                            v-model="detailForm.end_date">
                                                    </el-input>
                                                </el-form-item>
                                            </el-col>

                                        </el-row>

                                    </el-card>
                                </el-col>
                                <el-col :span="14">
                                    <el-card>
                                        <el-table
                                                :data="modelDetail"
                                                style="width: 100%"
                                                :row-class-name="modelDetail">
                                            <el-table-column
                                                    prop="modelname"
                                                    label="模型"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="start_date"
                                                    label="开始时间"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="end_date"
                                                    label="结束时间"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="operation"
                                                    label="操作">
                                            </el-table-column>
                                        </el-table>
                                    </el-card>
                                </el-col>
                                <el-col :span="4">
                                    <el-card>
                                        <el-divider>操作</el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >执行测试
                                                </el-button>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-button type="primary"
                                                           @click="checkExpress(detailForm.start_date,detailForm.end_date)"
                                                >服务监控
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-divider></el-divider>
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >同步结果
                                                </el-button>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-button type="primary" @click="showReport"
                                                >测试报告
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-tab-pane>
                </el-tabs>

            </el-row>

            <!--工具条-->
            <el-col :span="24" class="toolbar">
            </el-col>

            <!--新增界面-->
            <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false"
                       style="width: 100%; left: 10%">
                <el-form :model="addForm" label-width="120" :rules="addFormRules" ref="addForm">
                    <el-divider>基本配置</el-divider>
                    <el-row>
                        <el-form :inline="true" :model="filters" @submit.native.prevent>
                            <el-row :gutter="24">
                                <el-col :span="12">
                                    <el-form-item label="服务器:" prop="Host">
                                        <el-select v-model="addForm.Host" placeholder="请选择"
                                                   @click.native="gethost()">
                                            <el-option
                                                    v-for="(item,index) in Host"
                                                    :key="item.id"
                                                    :label="item.name"
                                                    :value="item.id"
                                            />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="12">
                                    <el-form-item label="端口号:" prop="port">
                                        <el-input id="port" v-model="addForm.port" placeholder=""/>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-row>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="addFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="addSubmit" :loading="addLoading">保存</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>
<script>
    // import NProgress from 'nprogress'

    import {
        getupload,
        getVersionInfo, StressDetail, StrategyDetail,
        updateStress, stresssave, getHost, getDictionary, stressTool, addupload, delupload

    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                fileList: [],
                filedict: {},
                progress: {}, // 策略进度
                modelDetail: [], //策略模型详情
                activeName: 'SceneConfiguration',
                jzstart: '',
                jzend: '',
                dystart: '',
                dyend: '',
                customColors: [
                    {color: '#f5ce6c', percentage: 20},
                    {color: '#3ccde6', percentage: 40},
                    {color: '#1989fa', percentage: 60},
                    {color: '#6f7ad3', percentage: 80},
                    {color: '#03fa54', percentage: 100},
                ],
                Host: {},
                jmeterList: {},
                jmeterData: {},
                props: {multiple: true},
                form: {
                    server_ip: '',
                    fuzzy: '是',
                    testtype: 'PatientID',
                    deldata: ''
                },
                rules: {
                    server_ip: [
                        {required: true, message: '请输入测试服务器', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'}
                    ]
                },
                filters: {
                    diseases: '',
                    server: ''
                },
                detailForm: {},
                total: 0,
                page: 1,
                page_size: 10,
                listLoading: true,
                sels: [], // 列表选中列

                editFormVisible: false, // 编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ]
                },
                // 编辑界面数据
                editForm: {
                    loop_time: '',
                    port: '4242',
                    end_time: null
                },

                addForm: {
                    port: '4242',
                    type: '匿名',
                    sendcount: 0,
                    end_time: null

                },
                addFormVisible: false, // 新增界面是否显示
                addLoading: false,
                addFormRules: {
                    diseases: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    version: [
                        {required: true, message: '请输入版本号', trigger: 'change'},
                    ]
                }
            }
        },
        mounted() {
            this.getParams()
        },
        methods: {
            // 样式 显示
            valuestatus: function (i) {
                if (!/-/g.test(i)) {
                    console.log("2")
                    i = 0
                } else if (!/\+/g.test(i)) {
                    i = 1
                } else {
                    console.log("1")
                    i = 2
                }
                switch (i) {
                    case 0:
                        return 'statuscssa';
                    case 1:
                        return 'statuscssb';
                    case 2:
                        return 'statuscssc';
                }

            },
            //展示监控
            checkExpress: function (start_date, end_date) {
                console.log(start_date, end_date)
                if (start_date === null) {
                    var startstamp = new Date().getTime();
                } else {
                    var startdate = start_date.replace(/-/g, '/');
                    var startstamp = new Date(startdate).getTime();
                }
                if (end_date === null) {
                    var endstamp = new Date().getTime();
                } else {
                    var enddate = end_date.replace(/-/g, '/');
                    var endstamp = new Date(enddate).getTime();
                }
                const url = "http://192.168.1.121:3000/d/Ss3q6hSZk/server-monitor-test?orgId=1&from=" +
                    startstamp + "&to=" + endstamp + "&var-host_name=" +
                    this.detailForm.loadserver + "&var-gpu_exporter_port=9445&var-node_exporter_port=9100&var-cadvisor_port=8080"
                const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : screen.left
                const dualScreenTop = window.screenTop !== undefined ? window.screenTop : screen.top

                const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width
                const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height

                const left = ((width / 2) - (1500 / 2)) + dualScreenLeft
                const top = ((height / 2) - (800 / 2)) + dualScreenTop
                const newWindow = window.open(url, '服务监控', 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=yes, copyhistory=no, width=' + '1500' + ', height=' + '800' + ', top=' + top + ', left=' + left)

                // Puts focus on the newWindow
                if (window.focus) {
                    newWindow.focus()
                }
            },
            changeData(file, fileList) {
                // 数据小于0.1M的时候按KB显示
                const size = file.size / 1024 / 1024 > 0.1 ? `(${(file.size / 1024 / 1024).toFixed(1)}M)` : `(${(file.size / 1024).toFixed(1)}KB)`
                file.name.indexOf('M') > -1 || file.name.indexOf('KB') > -1 ? file.name : file.name += size
            },
            beforeRemove(file) {
                const isLt2M = file.size / 1024 / 1024 < 100;
                if (!isLt2M) {
                    this.$message.info('文件删除中 ！!');
                    return isLt2M;
                }
            },
            handleRequest(data) {
                let params = new FormData()
                params.append('file', data.file)
                params.append('type', "stress")
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                addupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        var filename = data.filename
                        this.filedict[filename] = data.fileid;
                        this.$set(this.filedict, data.filename, data.fileid)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            //上传前对文件大小进行校验
            beforeUpload(file) {
                const isLt2M = file.size / 1024 / 1024 < 100;
                if (!isLt2M) {
                    this.$message.error('上传文件大小大小不能超过 100MB!');
                    return isLt2M;
                }
            },
            handleRemove(file, fileList) {
                console.log(file)
                var id = this.filedict[file.raw.name]
                let params = {"id": id, "filename": file.raw.name}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                delupload(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code} = res
                    if (code === '0') {
                        self.$message.info({
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
            },
            handleClick(tab, event) {
                this.StressStrategyDetail();
            },
            handleChange(value) {
                console.log(value);
            },
            //获取由路由传递过来的参数
            getParams() {
                this.stressid = this.$route.query.stressid;
                this.StressDetaillist();
                this.StressStrategyDetail();
            },
            // 获取host数据列表
            Installversion() {
                this.listLoading = true
                let self = this;
                const params = {
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getInstallersion(headers, params).then((res) => {
                    this.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        this.versionlist = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            typestatus: function (i) {
                if (i === true) {
                    return 'danger'
                } else {
                    return 'primary'
                }

            },
            showReport() {
                this.$router.push({
                    path: '/stressReport',
                    query: {
                        stress_id: this.stressid,
                        strategy: self.activeName
                    }
                });
            },
            getuploadList() {
                const params = {
                    page_size: "999999",
                    type: "stress"
                }
                const headers = {
                    'Content-Type': 'application/json'
                }
                getupload(headers, params).then(_data => {
                    const {msg, code, data} = _data
                    if (code != '0') {
                        this.$message.error(msg)
                        return
                    }
                    // 请求正确时执行的代码
                    this.jmeterList = data.data
                    for (var i in this.jmeterList) {
                        if (i["filename"] === this.detailForm.filename) {
                            this.jmeterData = i
                        }
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
                    const {msg, code, data} = _data
                    if (code != '0') {
                        this.$message.error(msg)
                        return
                    }
                    // 请求正确时执行的代码
                    var mydata = data.data
                    var json = JSON.stringify(mydata)
                    this.Host = JSON.parse(json)
                })
            },

            // 获取getBase列表
            getBase() {
                this.listLoading = true
                const self = this
                const params = {
                    selecttype: "dicom",
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getbase(headers, params).then((res) => {
                        self.listLoading = false
                        const {msg, code, data} = res
                        if (code === '0') {
                            self.total = data.total
                            self.list = data.data
                            self.type = data.type
                            this.options = []
                            var json = JSON.stringify(self.list)
                            this.dis = JSON.parse(json)
                            for (var k in self.type) {
                                var testchildren = []
                                for (var i in this.dis) {
                                    var disjson = this.dis[i]
                                    if (self.type[k] === disjson['type']) {
                                        testchildren.push({
                                                value: disjson['id'],
                                                label: disjson['remarks']
                                            }
                                        )
                                    }
                                }
                                this.options.push({
                                    value: self.type[k],
                                    label: self.type[k],
                                    children: testchildren
                                })
                            }
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true
                            })
                        }
                    }
                )
            },
            // 获取host数据列表
            gethost() {
                this.listLoading = true
                const self = this
                const params = {
                    page_size: 100
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getHost(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.Host = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取性能数据列表
            StressDetaillist() {
                this.listLoading = true
                const self = this
                const params = {
                    stressid: self.stressid
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                StressDetail(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.detailForm = data.data[0]
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取性能数据列表
            StressStrategyDetail() {
                this.listLoading = true
                const self = this
                const params = {
                    stressid: self.stressid,
                    strategy: self.activeName
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                StrategyDetail(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.progress = data.progress
                        self.modelDetail = data.modelDetail
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {ids: [row.id]}
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }

                    delduration(header, params).then(_data => {
                        const {msg, code, data} = _data
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
                        self.StressDetaillist()
                    })
                })
            }
            ,
            handleCurrentChange(val) {
                this.page = val
                this.StressDetaillist()
            }
            ,
            // 显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true
                this.editForm = Object.assign({}, row)
            }
            ,
            // 改变状态
            handleChangeStatus: function (index, row) {
                let self = this;
                this.listLoading = true;
                let params = {id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.sendstatus) {
                    disable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '停止成功',
                                center: true,
                                type: 'success'
                            });
                            row.sendstatus = !row.sendstatus;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enable_duration(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '0') {
                            self.$message({
                                message: '启用成功',
                                center: true,
                                type: 'success'
                            });
                            row.sendstatus = !row.sendstatus;
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            }
            ,
            // 显示新增界面
            handleAdd: function () {
                this.addFormVisible = true
                this.addForm = {
                    server: null,
                    port: 4242,
                    loop_time: '',
                    keyword: null,
                    dicom: null,
                    dds: null,
                    sendstatus: false,
                    status: false,
                    sleepcount: null,
                    sleeptime: 0,
                    sendcount: 0,
                    type: '匿名',
                    series: false,
                    end_time: null
                }
            }
            ,
            // 编辑
            editSubmit: function () {
                const self = this
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true
                            // NProgress.start();
                            const params = {
                                id: self.editForm.id,
                                loop_time: self.editForm.loop_time,
                                patientname: this.editForm.patientname,
                                patientid: this.editForm.patientid,
                                dicom: this.editForm.senddata,
                                sendcount: this.editForm.sendcount,
                                dds: this.editForm.dds,
                                sleepcount: this.editForm.sleepcount,
                                sleeptime: this.editForm.sleeptime,
                                series: this.editForm.series,
                                type: this.editForm.type,
                                end_time: this.editForm.end_time
                            }
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            updateduration(header, params).then(_data => {
                                const {msg, code, data} = _data
                                self.editLoading = false
                                if (code === '0') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.$refs['editForm'].resetFields()
                                    self.editFormVisible = false
                                    self.StressDetaillist()
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
            }
            ,
            // 新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        const self = this
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true
                            // NProgress.start();
                            const params = JSON.stringify({
                                port: self.addForm.port,
                                version: self.addForm.version,
                                loop_time: self.addForm.loop_time,
                                patientname: 'duration',
                                patientid: '',
                                dicom: this.addForm.senddata,
                                sendcount: this.addForm.sendcount,
                                dds: this.addForm.dds,
                                sleepcount: this.addForm.sleepcount,
                                sleeptime: this.addForm.sleeptime,
                                series: this.addForm.series,
                                end_time: this.addForm.end_time,
                                type: '持续化',
                                sendstatus: false,
                                status: false,
                                Host: this.addForm.Host
                            })
                            const header = {
                                'Content-Type': 'application/json',
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            }
                            addduration(header, params).then(_data => {
                                const {msg, code, data} = _data
                                self.addLoading = false
                                if (code === '0') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.$refs['addForm'].resetFields()
                                    self.addFormVisible = false
                                    self.StressDetaillist()
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
                                    self.StressDetaillist()
                                }
                            })
                        })
                    }
                })
            }
            ,
            selsChange: function (sels) {
                this.sels = sels
            }
            ,
            cancelEdit(row) {
                row.title = row.originalTitle
                row.edit = false
                this.$message({
                    message: 'The title has been restored to the original value',
                    type: 'warning'
                })
            }
            ,
            confirmEdit(row) {
                row.edit = false
                row.originalTitle = row.title
                this.$message({
                    message: 'The title has been edited',
                    type: 'success'
                })
            }
            ,
            // 批量删除
            batchRemove: function () {
                const ids = this.sels.map(item => item.id)
                console.log(ids)
                const self = this
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true
                    // NProgress.start();
                    const self = this
                    const params = {ids: ids}
                    const header = {
                        'Content-Type': 'application/json',
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    }
                    delduration(header, params).then(_data => {
                        const {msg, code, data} = _data
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
                        self.StressDetaillist()
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

    .view-png {
        width: 15px;
        height: 15px;
        margin-right: 3px;
        margin-bottom: 5px
    }

    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }

    .el-aside {
        color: #333;
    }

    .word {
        color: #898888;
    }

    .statuscssa {
        color: #E61717
    }

    .statuscssb {
        color: #67c23a;
    }

    .statuscssc {
        color: #1dc5a3;
    }
</style>
