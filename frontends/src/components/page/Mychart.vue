<template>
    <div>
        <div class="container" style="overflow:hidden">
            <div id='myChart' class="myChart" style="margin-top:100px;width:500px;height:600px;float:left">
            </div>
            <div id='myChartTwo' class="myChart" style="width:600px;height:600px;margin-top:100px;margin-left:100px;float:left">
            </div>
        </div>
    </div>
</template>

<script>
    import echarts from "echarts";
    import { getstressversion,getstressresult, getHost,getreportfigure} from '@/router/api';
    export default {
        name: 'basecharts',
        data:function(){
            return{
                msg:'图表',
                oneData:[],
                reportLineData:[['Brain', 'CT_Hematoma', 'SVD', 'SWI', 'Tumor', 'CTA', 'CTP', 'Lung', 'Lung1', 'Lung2', 'Lung3', 'Lung4',
              'MRA', 'coronary', 'Heart', 'Neck', 'post_surgery'],['1', '2', '3', '4', '2', '1', '0', '1', '9', '7', '6', '1',
              '5', '6', '7', '2', '1'],['1', '2', '3', '4', '2', '1', '0', '1', '9', '7', '6', '1',
              '5', '6', '7', '2', '1']]

            }
        },
        created(){
            this.getData();
        },
        mounted() {
            this.drawLineOne();
            this.drawLineTwo();
        },
        methods:{
            getData(){
                let params = {
                    "checkversion": "BUG",
                    "version": "Boimind"
                };
                let headers = {
                    "Content-Type": "application/json"
                };
                getreportfigure(headers, params).then(_data => {
                    let {code, msg, data} = _data;
                    console.log(data.figure_list)
                    this.reportLineData = data.figure_list;

                    this.reportLineoption.series[0].data = this.reportLineData[1];
                    this.reportLineoption.series[1].data = this.reportLineData[2];

                    this.reportBarData = data.solution_state.sort(function (a, b) {
                        return a.value - b.value;
                    });
                    this.reportBaroption.series[0].data = this.reportBarData;
                    this.oneData=[
                    {value:335, name:'开放'},
                    {value:310, name:'PROGRESS'},
                    {value:274, name:'已解决'},
                    {value:400, name:'已关闭'},
                    {value:200, name:'重新打开'}
                ];

                });
            },
            drawLineOne(){
                let myChart = echarts.init(document.getElementById('myChart'));
                myChart.setOption({
                    backgroundColor: '#2c343c',
                    title:  {
                        text: 'Bug解决数量状态图',
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: '#ccc'
                        }
                    },
                    visualMap: {
                        show: false,
                        min: 80,
                        max: 600,
                        inRange: {
                            colorLightness: [0, 1]
                        }
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    series : [
                    {
                        name:'解决状态',
                        type:'pie',
                        radius : '55%',
                        center: ['50%', '50%'],
                        data:this.oneData.sort(function (a, b) { return a.value - b.value; }),
                        roseType: 'radius',
                        label: {
                            normal: {
                                textStyle: {
                                    color: 'rgba(255, 255, 255, 0.3)'
                                }
                            }
                        },
                        labelLine: {
                            normal: {
                                lineStyle: {
                                    color: 'rgba(255, 255, 255, 0.3)'
                                },
                                smooth: 0.2,
                                length: 10,
                                length2: 20
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: '#c23531',
                                shadowBlur: 200,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },

                        animationType: 'scale',
                        animationEasing: 'elasticOut',
                        animationDelay: function (idx) {
                            return Math.random() * 200;
                        }
                    }
                    ]
                });
            },
            drawLineTwo(){
                let myChartTwo = echarts.init(document.getElementById('myChartTwo'));
                myChartTwo.setOption({
                    title: {
                        text: '创建与解决问题对比图'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['创建问题','解决问题']
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
                    xAxis:  {
                        type: 'category',
                        boundaryGap: false,
                        data: this.reportLineData[0]
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value} 个'
                        }
                    },
                    series: [
                    {
                        name:'创建问题',
                        type:'line',
                        data:this.reportLineData[1],
                        markPoint: {
                            data: [
                            {type: 'max', name: '最大值'},
                            {type: 'min', name: '最小值'}
                            ]
                        },
                    },
                    {
                        name:'解决问题',
                        type:'line',
                        data:this.reportLineData[2],
                        markPoint: {
                            data: [
                            {type: 'max', name: '最大值'},
                            {type: 'min', name: '最小值'}
                            ]
                        },
                    }
                    ]
                })
            }
        }
    }
</script>
  .myChart{
    float:left;
  }
  .myChartTwo{
    margin-top:50px;
    float:left;
  }
<style scoped>
    
</style>