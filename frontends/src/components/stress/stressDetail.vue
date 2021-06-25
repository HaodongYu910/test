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
                                    <el-select v-model="detailForm.version" placeholder="请选择"
                                               @click.native="getversion()">
                                        <el-option
                                                v-for="(item,index) in VersionInfo"
                                                :key="item.id"
                                                :label="item.version"
                                                :value="item.id"
                                        />
                                    </el-select>
                                </el-form-item>
                            </el-row>
                            <el-row :gutter="24">
                                <el-col :span="16">
                                    <el-card>
                                        <el-table
                                                :data="tableData"
                                                style="width: 100%"
                                                :row-class-name="tableRowClassName">
                                            <el-table-column
                                                    prop="name"
                                                    label="场景名称"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="CSVData"
                                                    label="CSVData"
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
                                                         :percentage="10"></el-progress>
                                        </el-form-item>
                                        <el-form-item label="单一测试" prop='thread'>
                                            <el-progress :color="customColors" :text-inside="true" :stroke-width="26"
                                                         :percentage="70"></el-progress>
                                        </el-form-item>
                                        <el-form-item label="混合测试" prop='thread'>
                                            <el-progress :color="customColors" :text-inside="true" :stroke-width="26"
                                                         :percentage="100" status="success"></el-progress>
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
                    <el-tab-pane label="基准测试" name="benchmark">
                        <el-form :model="detailForm" label-width="80px" :rules="addFormRules" ref="addForm">
                            <el-row :gutter="24">
                                <el-col :span="6">
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
                                <el-col :span="14">
                                    <el-card>
                                        <el-table
                                                :data="tableData"
                                                style="width: 100%"
                                                :row-class-name="tableRowClassName">
                                            <el-table-column
                                                    prop="date"
                                                    label="模型"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="name"
                                                    label="开始时间"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="name"
                                                    label="结束时间"
                                                    width="180">
                                            </el-table-column>
                                            <el-table-column
                                                    prop="address"
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
                                                <el-button type="primary" @click="stressTest('dy')"
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
                                                <el-button type="primary" @click="stressTest('dy')"
                                                >测试报告
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                    </el-card>
                                </el-col>
                            </el-row>
                        </el-form>
                    </el-tab-pane>
                    <el-tab-pane label="单一测试" name="third">
                        <el-form :model="detailForm" label-width="80px" :rules="addFormRules" ref="addForm">
                            <el-row :gutter="24">
                                <el-col :span="8">
                                    <el-card>
                                        <el-divider>单一-配置</el-divider>

                                        <el-form-item label="测试时间" prop='single'>
                                            <el-input-number v-model="detailForm.single" @change="handleChange" :min="0"
                                                             :max="12"
                                                             label="单一循环"></el-input-number>
                                            时
                                        </el-form-item>
                                    </el-card>
                                </el-col>
                                <el-col :span="8">
                                    <el-card>
                                        <el-divider>混合-配置</el-divider>
                                        <!--                            <el-form-item label="发送数量" prop='loop_count'>-->
                                        <!--                                <el-input-number v-model="addForm.loop_count" @change="handleChange" :min="1"-->
                                        <!--                                                 :max="5000"-->
                                        <!--                                                 label="发送数量"></el-input-number>-->
                                        <!--                            </el-form-item>-->
                                        <el-form-item label="持续时间" prop='thread'>
                                            <el-input-number v-model="detailForm.duration" @change="handleChange"
                                                             :min="1"
                                                             :max="200"
                                                             label="持续时间"></el-input-number>
                                            时
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
                                                    <el-input-number v-model="addForm.ramp" @change="handleChange"
                                                                     :min="0"
                                                                     :max="5000"
                                                                     label="Ramp-Up"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="12">
                                                <el-form-item label="并发数" prop='synchroniz'>
                                                    <el-input-number v-model="addForm.synchroniz" @change="handleChange"
                                                                     :min="0"
                                                                     :max="100"
                                                                     label="并发数"></el-input-number>
                                                </el-form-item>
                                            </el-col>

                                            <el-col :span="12">
                                                <el-form-item label="持续时间" prop='single'>
                                                    <el-input-number v-model="addForm.loop_time" @change="handleChange"
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
                    <el-tab-pane label="混合测试" name="fourth">
                        <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                            <el-row :gutter="24">
                                <el-col :span="8">
                                    <el-card>
                                        <el-divider>混合-配置</el-divider>
                                        <!--                            <el-form-item label="发送数量" prop='loop_count'>-->
                                        <!--                                <el-input-number v-model="addForm.loop_count" @change="handleChange" :min="1"-->
                                        <!--                                                 :max="5000"-->
                                        <!--                                                 label="发送数量"></el-input-number>-->
                                        <!--                            </el-form-item>-->
                                        <el-form-item label="持续时间" prop='thread'>
                                            <el-input-number v-model="addForm.duration" @change="handleChange" :min="1"
                                                             :max="200"
                                                             label="持续时间"></el-input-number>
                                            时
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
                                                    <el-input-number v-model="addForm.thread" @change="handleChange"
                                                                     :min="1"
                                                                     :max="100"
                                                                     label="线程数"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-form-item label="Ramp-Up" prop='ramp'>
                                                    <el-input-number v-model="addForm.ramp" @change="handleChange"
                                                                     :min="0"
                                                                     :max="5000"
                                                                     label="Ramp-Up"></el-input-number>
                                                </el-form-item>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="12">
                                                <el-form-item label="并发数" prop='synchroniz'>
                                                    <el-input-number v-model="addForm.synchroniz" @change="handleChange"
                                                                     :min="0"
                                                                     :max="100"
                                                                     label="并发数"></el-input-number>
                                                </el-form-item>
                                            </el-col>

                                            <el-col :span="12">
                                                <el-form-item label="持续时间" prop='single'>
                                                    <el-input-number v-model="addForm.loop_time" @change="handleChange"
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
                            <el-row>
                                <el-form-item>
                                    <el-button type="primary" @click="stressTest('dy')"
                                               :disabled="this.sels.length===0">测试
                                    </el-button>
                                </el-form-item>
                            </el-row>
                        </el-form>

                    </el-tab-pane>
                </el-tabs>

            </el-row>

            <!--工具条-->
            <el-col :span="24" class="toolbar">
            </el-col>

            <!--编辑界面-->
            <el-dialog title="修改" :visible.sync="editFormVisible" :close-on-click-modal="false"
                       style="width: 100%; left: 7.5%">
                <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                    <el-divider>场景配置</el-divider>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="数据类型" prop="senddata">
                                <el-cascader :options="options" v-model="editForm.senddata" clearable :props="props"
                                             @click.native="getBase()"></el-cascader>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="发送类型" prop="type">
                                <el-select v-model="editForm.type" placeholder="请选择类型">
                                    <el-option
                                            v-for="item in typeoptions"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-divider>匿名配置</el-divider>

                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="每日发送" prop='sendcount'>
                                <el-input-number v-model="editForm.sendcount" @change="handleChange" :min="0"
                                                 :max="100000"
                                                 label="每日发送"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="结束时间">
                                <el-date-picker v-model="editForm.end_time" type="datetime"
                                                placeholder="选择日期" value-format="yyyy-MM-dd HH:mm:ss"></el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="延时数量" prop='sleepcount'>
                                <el-input-number v-model="editForm.sleepcount" @change="handleChange" :min="0"
                                                 :max="99999"
                                                 label="延时数量"></el-input-number>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="延时时间（秒）" prop='sleeptime'>
                                <el-input-number v-model="editForm.sleeptime" @change="handleChange" :min="0"
                                                 :max="5000"
                                                 label="延时时间（秒）"></el-input-number>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-row>
                            <el-col :span="15">
                                <el-form-item label="DDS服务" prop="dds">
                                    <el-select v-model="editForm.dds" placeholder="请选择DDS服务"
                                               @click.native="gethost()">
                                        <el-option
                                                v-for="(item,index) in Host"
                                                :key="item.host"
                                                :label="item.name"
                                                :value="item.host"
                                        />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item label="series延时" prop="series">
                                    <el-switch v-model="editForm.series" active-color="#13ce66"
                                               inactive-color="#ff4949"></el-switch>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="editFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="editSubmit" :loading="editLoading">保存</el-button>
                </div>
            </el-dialog>

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
        getVersionInfo, StressDetail,
        updateStress, stresssave, getHost, getDictionary, stressTool, addupload, delupload

    } from '@/router/api'

    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                activeName: 'SceneConfiguration',
                customColors: [
                    {color: '#f5ce6c', percentage: 20},
                    {color: '#3ccde6', percentage: 40},
                    {color: '#1989fa', percentage: 60},
                    {color: '#6f7ad3', percentage: 80},
                    {color: '#03fa54', percentage: 100},
                ],
                typeoptions: [{
                    value: '匿名',
                    label: '匿名'
                }, {
                    value: '正常',
                    label: '正常'
                }, {
                    value: '持续化',
                    label: '持续化'
                }],
                props: {multiple: true},
                options: [{
                    value: 'test',
                    label: 'test',
                    children: [{
                        value: 1,
                        label: 'Lung'
                    }, {
                        value: 1,
                        label: 'Brain'
                    }, {
                        value: 13,
                        label: 'SWI'
                    }]
                }, {
                    value: 'Gold',
                    label: 'Gold',
                    children: [{
                        value: 1,
                        label: 'Lung'
                    }, {
                        value: 1,
                        label: 'Brain'
                    }, {
                        value: 13,
                        label: 'SWI'
                    }]
                }],
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
            handleClick(tab, event) {
                console.log(tab, event);
            },
            //获取由路由传递过来的参数
            getParams() {
                console.log(this.$route)
                this.stressid = this.$route.query.stressid;
                this.StressDetaillist();
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
            displaystatus: function (i) {
                if (i === '持续化') {
                    return ''
                } else {
                    return 'none'
                }
            },
            typestatus: function (i) {
                if (i === true) {
                    return 'danger'
                } else {
                    return 'primary'
                }

            },
            showReport(index, row) {
                this.$router.push({
                    path: '/DurationReport/reportid=' + row.id,
                });
            },
            showDetail(index, row) {
                this.$router.push({
                    path: '/durationData',
                    query: {
                        id: row.id,
                        name: row.server_ip
                    }
                });
            },
            deldicom(formName) {
                this.tableData = null
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        const params = {
                            server_ip: this.form.server_ip,
                            deldata: this.form.deldata,
                            testtype: this.form.testtype,
                            fuzzy: this.form.fuzzy
                        }
                        const headers = {
                            'Content-Type': 'application/json'
                        }
                        delete_patients(headers, params).then(_data => {

                            const {msg, code, data} = _data
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
                                tableData.push({'name': mydata[i]})
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
            durationVerifyData() {
                const params = {}
                const headers = {
                    'Content-Type': 'application/json'
                }
                durationverifydata(headers, params).then(_data => {
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
            }
            ,
            // 获取数据列表
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
            }
            ,
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
</style>
