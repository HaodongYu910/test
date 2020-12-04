<template>
    <div class="app-container">

        <div class="filter-container">
            <!--工具条-->
            <el-col :span="100" class="toolbar" style="padding-bottom: 0px;">
                <el-card shadow="hover" style="width:100%;height:800px;">
                        <el-row :gutter="50">
                            <el-col :span="30">
                                <el-card shadow="hover">
                                    <div id='predictionLine' class="myLine" style="width:1500px;height:600px;margin:0 auto">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>
                <el-card shadow="hover" style="width:100%;height:800px;">
                        <el-row :gutter="50">
                            <el-col :span="30">
                                <el-card shadow="hover">
                                    <div id='jobLine' class="myLine" style="width:1500px;height:600px;margin:0 auto">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>
                <el-card shadow="hover" style="width:100%;height:800px;">
                        <el-row :gutter="50">
                            <el-col :span="30">
                                <el-card shadow="hover">
                                    <div id='lungLine' class="myLine" style="width:750px;height:600px;margin:0 auto">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>
                <el-card shadow="hover" style="width:100%;height:800px;">
                        <el-row :gutter="50">
                            <el-col :span="30">
                                <el-card shadow="hover">
                                    <div id='lungjobLine' class="myLine" style="width:750px;height:600px;margin:0 auto">
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                    </el-card>
                <!--工具条-->
                <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
                    <el-form :inline="true" :model="filters" @submit.native.prevent>
                        <el-select v-model="filters.server"  placeholder="请选择服务器" @click.native="gethost()">
                              <el-option
                                v-for="(item,index) in tags"
                                :key="item.host"
                                :label="item.name"
                                :value="item.host"
                              />
                            </el-select>
                        <el-select v-model="filters.version"  placeholder="当前版本" @click.native="getversion()">
                              <el-option
                                v-for="(item,index) in versions"
                                :key="item.version"
                                :label="item.version"
                                :value="item.version"
                              />
                            </el-select>
                        <el-select v-model="filters.checkversion"  placeholder="以前版本" @click.native="getversion()">
                              <el-option
                                v-for="(item,index) in versions"
                                :key="item.version"
                                :label="item.version"
                                :value="item.version"
                              />
                            </el-select>
                        <el-form-item>
                            <el-button type="primary" @click="getDurationlist">查询</el-button>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleAdd">生成报告</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
                <!--列表-->
                <span style="margin-left: 10px">prediction time</span>
                <el-table :data="prediction" v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="modelname" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="prediction_count" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.min)">{{ scope.row.min}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="rate of success" min-width="8%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.rate }}</span>
                        </template>
                    </el-table-column>
                </el-table>

                <span style="margin-left: 10px">job time</span>
                <el-table :data="job" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="version" label="modelname" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.modelname }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="job_count" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg single job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.single)">{{ scope.row.single }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median job time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }} 秒</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min job time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.min)">{{ scope.row.min }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max job time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" >{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <span style="margin-left: 10px">Lung prediction time</span>
                <el-table :data="lung" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="version" label="slicenumber" min-width="6%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.min)">{{ scope.row.min }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.minimages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="max images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.maximages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="avg images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                        </template>
                    </el-table-column>
                </el-table>
                <span style="margin-left: 10px">Lung Job time</span>
                <el-table :data="lungjob" highlight-current-row v-loading="listLoading"
                          @selection-change="selsChange"
                          style="width: 100%;">
                    <el-table-column prop="version" label="slicenumber" min-width="6%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.slicenumber }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="avg pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.avg)">{{ scope.row.avg }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="median pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.median)">{{ scope.row.median }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min pred time /s" min-width="10%" sortable>
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.min)">{{ scope.row.min }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="max pred time /s" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px" :class="valuestatus(scope.row.max)">{{ scope.row.max }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="type" label="coef. of variation" min-width="10%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.coef }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="min images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.minimages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="max images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.maximages }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="avg images" min-width="8%">
                        <template slot-scope="scope">
                            <span style="margin-left: 10px">{{ scope.row.avgimages }}</span>
                        </template>
                    </el-table-column>
                </el-table>
            </el-col>
        </div>
    </div>
</template>

<script>
    // import NProgress from 'nprogress'

    import {
        getstressversion,getstressresult, getHost,getreportfigure
    } from '@/router/api';
    import echarts from "echarts";
  export default {
    // import ElRow from "element-ui/packages/row/src/row";
        // components: {ElRow},
        data() {
            return {
                filters: {
                    diseases: ''
                },
                durationlist: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [], // 列表选中列

                //定义表
                predictionLine: {},
                jobLine: {},
                lungLine: {},
                //定义表数据
                predictionLineData: [],
                jobLineData: [],
                lungData: [],
                twoData: [],
                //定义表数据对应的option数据
                predictionLineoption: {
                    title: {
                        text: '模型预测时间对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: ['aibrainct','aibrainmri','aicardiomodel','archcta',
                          'bodypart','brainct','braincta','brainctp','brainmra',
                          'headcta','postsurgery'],
                        padding: 25
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: true},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 秒'
                        }
                    },
                    series: [
                        {
                            name: 'aibrainct',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'aibrainmri',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'aicardiomodel',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'archcta',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'bodypart',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'brainct',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'braincta',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'brainctp',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'brainmra',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'headcta',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'lungct',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'postsurgery',
                            type: 'line',
                            data: [],
                            markPoint: {
                            },
                        },
                    ]
                },
                jobLineoption: {
                    title: {
                        text: 'Job时间对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: ['aibrainct','aibrainmri','aicardiomodel','archcta',
                          'bodypart','brainct','braincta','brainctp','brainmra',
                          'headcta','postsurgery'],
                        padding: 25
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: true},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 秒'
                        }
                    },
                    series: [
                        {
                            name: 'aibrainct',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'aibrainmri',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'aicardiomodel',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'archcta',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'bodypart',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'brainct',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'braincta',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'brainctp',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'brainmra',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'headcta',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'lungct',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: 'postsurgery',
                            type: 'line',
                            data: [],
                            markPoint: {
                            },
                        },
                    ]
                },
                lungLineoption: {
                    title: {
                        text: 'Lung层厚预测时间对比图'
                    },
                    tooltip: {
                        trigger: 'axis',
                        padding: 25
                    },
                    legend: {
                        data: ['1.0','1.25','1.5','5.0',
                          '10.0'],
                        padding: 25
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: true},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 秒'
                        }
                    },
                    series: [
                        {
                            name: '1.0',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: '1.25',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: '1.5',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: '5.0',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        },
                        {
                            name: '10.0',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                        }
                    ]
                }
            }
        },
        components: {},
        mounted() {
            this.drawpredictionLine();
            this.drawjobLine();
            this.drawlungLine();
            this.gethost();
            this.getBase();
        },
        created() {
            this.getreportData();
            this.getData();
        },
        watch: {
            //观察option的变化
            predictionLineoption: {
                handler(newVal, oldVal) {
                    if (this.reportBar) {
                        if (newVal) {
                            this.predictionLine.setOption(newVal);
                        } else {
                            this.predictionLine.setOption(oldVal);
                        }
                    } else {
                        this.drawpredictionLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            jobLineoption: {
                handler(newVal, oldVal) {
                    if (this.coinnessBar) {
                        if (newVal) {
                            this.jobLine.setOption(newVal);
                        } else {
                            this.jobLine.setOption(oldVal);
                        }
                    } else {
                        this.drawjobLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            },
            lungLineoption: {
                handler(newVal, oldVal) {
                    if (this.lungBar) {
                        if (newVal) {
                            this.lungLine.setOption(newVal);
                        } else {
                            this.lungLine.setOption(oldVal);
                        }
                    } else {
                        this.drawlungLine();
                    }
                },
                deep: true //对象内部属性的监听，关键。
            }
        },
        methods: {
            valuestatus: function (i) {
                if (!/-/g.test(i)) {
                    i = 0
                }
                else if (!/\+/g.test(i)) {
                    i = 1
                }
                else {
                    i = 2
                }
                console.log(i)
                switch (i) {
                    case 0:
                        return 'statuscssa';
                    case 1:
                        return 'statuscssb';
                    case 2:
                        return 'statuscssc';
                }

            },
            // 压测版本
            getversion() {
                this.listLoading = true
                const self = this
                const params = {}
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressversion(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.total = data.total
                        self.list = data.data
                        var json = JSON.stringify(self.list)
                        this.versions = JSON.parse(json)
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
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
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true
                        })
                    }
                })
            },
            // 获取数据列表
            getDurationlist() {
                this.listLoading = true
                const self = this
                const params = {
                    version: this.filters.version,
                    checkversion: this.filters.checkversion,
                    server: this.filters.server
                }
                const headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))}
                getstressresult(headers, params).then((res) => {
                    self.listLoading = false
                    const {msg, code, data} = res
                    if (code === '0') {
                        self.prediction = data.predictionresult
                        self.job =data.jobresult
                        self.lung =data.lungresult
                        self.lungjob =data.lungjob
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
        //     //获取由路由传递过来的参数
        //     getParams(){
        //         this.routerParams=this.$route.query;
        //     },
            getreportData() {
                let params = {
                    "version": "Boimind",
                    "type":"prediction"
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getreportfigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    this.predictionLineData = data.predictionFigure;
                    this.jobLineData = data.jobFigure;
                    this.lungLineData = data.lungFigure;
                    this.predictionLineoption.xAxis.data = this.predictionLineData[0];
                    this.jobLineoption.xAxis.data = this.jobLineData[0];
                    this.lungLineoption.xAxis.data = this.lungLineData[0];

                    for (var i = 0;i<this.predictionLineData.length;i++)
                        {
                             this.predictionLineoption.series[i].data = this.predictionLineData[(i+1)];
                             this.jobLineoption.series[i].data =this.jobLineData[i+1];

                        };
                    this.lungLineoption.series[0].data =this.lungLineData[1];
                    this.lungLineoption.series[1].data =this.lungLineData[2];
                    this.lungLineoption.series[2].data =this.lungLineData[3];
                    this.lungLineoption.series[3].data =this.lungLineData[4];
                    this.lungLineoption.series[4].data =this.lungLineData[5];
                    this.reportBarData = data.solution_state.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    this.reportBaroption.series[0].data = this.reportBarData;
                });
            },
            drawreportBar() {
                this.reportBar = echarts.init(document.getElementById('reportBar'));
                this.reportBar.setOption(this.reportBaroption, true);
                setTimeout(() => {
                    window.onresize = reportBar.resize;
                }, 200);
            },
            drawCoinNessBar() {
                this.coinnessBar = echarts.init(document.getElementById('coinnessBar'));
                this.coinnessBar.setOption(this.coinnessBaroption, true);
                setTimeout(() => {
                    window.onresize = coinnessBar.resize;
                }, 200);
            },
            drawpredictionLine() {
                this.predictionLine = echarts.init(document.getElementById('predictionLine'));
                this.predictionLine.setOption(this.predictionLineoption);
                setTimeout(() => {
                    window.onresize = predictionLine.resize;
                }, 200);
            },
            drawjobLine() {
                this.jobLine = echarts.init(document.getElementById('jobLine'));
                this.jobLine.setOption(this.jobLineoption);
                setTimeout(() => {
                    window.onresize = jobLine.resize;
                }, 200);
            },
            drawlungLine() {
                this.lungLine = echarts.init(document.getElementById('lungLine'));
                this.lungLine.setOption(this.lungLineoption);
                setTimeout(() => {
                    window.onresize = lungLine.resize;
                }, 200);
            },
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
    .el-row {
        margin-bottom: 20px;
    }

    .grid-content {
        display: flex;
        align-items: center;
        height: 100px;
    }

    .grid-cont-right {
        flex: 1;
        text-align: center;
        font-size: 14px;
        color: #999;
    }

    .grid-num {
        font-size: 30px;
        font-weight: bold;
    }

    .grid-con-icon {
        font-size: 50px;
        width: 100px;
        height: 100px;
        text-align: center;
        line-height: 100px;
        color: #fff;
    }

    .grid-con-1 .grid-con-icon {
        background: rgb(45, 140, 240);
    }

    .grid-con-1 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-2 .grid-con-icon {
        background: rgb(100, 213, 114);
    }

    .grid-con-2 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-3 .grid-con-icon {
        background: rgb(242, 94, 67);
    }

    .grid-con-3 .grid-num {
        color: rgb(242, 94, 67);
    }

    .user-info {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #ccc;
        margin-bottom: 20px;
    }

    .user-avator {
        width: 120px;
        height: 120px;
        border-radius: 50%;
    }

    .user-info-cont {
        padding-left: 50px;
        flex: 1;
        font-size: 14px;
        color: #999;
    }

    .user-info-cont div:first-child {
        font-size: 30px;
        color: #222;
    }

    .user-info-list {
        font-size: 14px;
        color: #999;
        line-height: 25px;
    }

    .user-info-list span {
        margin-left: 70px;
    }

    .mgb20 {
        margin-bottom: 20px;
    }
    .statuscssa{
        color:#E61717
    }
    .statuscssb{
        color:#67c23a;
    }
    .statuscssc{
        color:#666666;
    }
</style>
