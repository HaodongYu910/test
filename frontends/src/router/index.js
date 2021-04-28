import Vue from 'vue';
import Router from 'vue-router';

const ProjectInfo = () => import('../components/project/Projectdetail.vue');
const Server = () => import('../components/project/global/ServerList.vue');
const API = () => import('../components/project/api/API.vue');
const ApiList = () => import('../components/project/api/ApiList.vue');
const ApiListGroup = () => import('../components/project/api/ApiListGroup.vue');
const FestTest = () => import('../components/project/api/FestTest.vue');
const addApi = () => import('../components/project/api/Addapi.vue');
const detail = () => import('../components/project/api/updateApi/ApiForm.vue');
const ApiInfo = () => import('../components/project/api/updateApi/ApiInfo.vue');
const testApi = () => import('../components/project/api/updateApi/TestApi.vue');
const UpdateApi = () => import('../components/project/api/updateApi/UpdateApi.vue');
const ApiDynamic = () => import('../components/project/api/updateApi/ApiDynamic.vue');
const AutomationTest = () => import('../components/interface/automation/AutomationTest.vue');
const CaseList = () => import('../components/interface/automation/CaseList.vue');
const CaseListGroup = () => import('../components/interface/automation/CaseListGroup.vue');
const CaseApiList = () => import('../components/interface/automation/CaseApiList.vue');
const AddCaseApi = () => import('../components/interface/automation/AddCaseApi.vue');
const UpdateCaseApi = () => import('../components/interface/automation/UpdateCaseApi.vue');
const TestReport = () => import('../components/interface/automation/TestReport.vue');
const ProjectMember = () => import('../components/project/ProjectMember.vue');
const ProjectDynamic = () => import('../components/project/ProjectDynamic.vue');
const ProjectTitle = () => import('../components/project/projectTitle/ProjectTitle.vue');
const ProjectReport = () => import('../components/project/ProjectReport.vue');
const ReportInfo = () => import('../components/report/Testreportdetail.vue');
const ReportTitle = () => import('../components/home/Dashboard.vue');


Vue.use(Router);

export default new Router({
    mode:'history',
    base:'/',
    routes: [

        {
            path: '/',
            redirect: '/home'
        },
        {
            path: '/',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            meta: {title: '主页'},
            children: [
                {
                    path: '/home',
                    component: resolve => require(['../components/home/Dashboard.vue'], resolve),
                    meta: {title: '系统首页'}
                },
                {
                    path: '/project',
                    component: resolve => require(['../components/project/Projectlist.vue'], resolve),
                    meta: {title: '项目列表'}
                },
                {
                    path: '/message',
                    component: resolve => require(['../components/page/Tabs.vue'], resolve),
                    meta: {title: '消息中心'}
                },
                {
                    path: '/DicomSend',
                    component: resolve => require(['../components/DicomTool/duration/DicomSend.vue'], resolve),
                    meta: {title: 'Dicom发送'}

                },
                {
                    path: '/duration',
                    component: resolve => require(['../components/DicomTool/duration/durationList.vue'], resolve),
                    meta: {title: '持续化工具'}

                },
                {
                    path: '/DurationReport/reportid=:reportid',
                    component: resolve => require(['../components/DicomTool/duration/durationReport.vue'], resolve),
                    meta: {title: '持续化报告'}

                },
                {
                    path: '/dicom',
                    component: resolve => require(['../components/DicomTool/dicomdata/dicomData.vue'], resolve),
                    meta: {title: 'Dicom数据'}

                },
                {
                    path: '/dicomGroup',
                    component: resolve => require(['../components/DicomTool/DicomGroup/dicomGroup.vue'], resolve),
                    meta: {title: 'Dicom组管理'}

                },
                {
                    path: '/durationData',
                    component: resolve => require(['../components/DicomTool/duration/durationDetail.vue'], resolve),
                    meta: {title: '持续化详情'}

                },
                {
                    // dds监控界面
                    path: '/dds',
                    component: resolve => require(['../components/DicomTool/DDS/dds.vue'], resolve),
                    meta: { title: 'DDS监控' }

                },
                {
                    // UICase 用例
                    path: '/UICase',
                    component: resolve => require(['../components/autoui/UICase.vue'], resolve),
                    meta: { title: 'UI用例' }

                },
                {
                    path: '/UICase/caseid=:caseid',
                    component: resolve => require(['../components/autoui/UIMarkdown.vue'], resolve),
                    meta: {title: 'UI用例详情'},
                    hidden: true,
                    children: [
                        {
                            path: '/UICase/caseid=:caseid',
                            component: resolve => require(['../components/autoui/UIMarkdown.vue'], resolve),
                            meta: {title: 'UI用例详情'}, name: 'UI用例详情', leaf: true
                        }
                    ]
                },
                // UI列表
                {
                    path: '/UIList',
                    component: resolve => require(['../components/autoui/UIList.vue'], resolve),
                    meta: {title: 'UI自动化列表'}

                },
                {
                    path: '/UI/UIid=:UIid',
                    component: resolve => require(['../components/autoui/UIDetails.vue'], resolve),
                    meta: {title: 'UI自动化详情'},
                    hidden: true,
                    children: [
                        {
                            path: '/UI/UIid=:UIid',
                            component: resolve => require(['../components/autoui/UIDetails.vue'], resolve),
                            meta: {title: 'UI自动化详情'}, name: 'UI自动化详情', leaf: true
                        }
                    ]
                },
                {
                    path: '/SmokeList',
                    component: resolve => require(['../components/interface/gold/goldList.vue'], resolve),
                    meta: {title: '金标准列表'}

                },
                {
                    path: '/goldDetail',
                    component: resolve => require(['../components/interface/gold/goldDetails.vue'], resolve),
                    meta: {title: '金标准详情'}
                },
                {
                    path: '/report/goldid=:goldid',
                    component: resolve => require(['../components/interface/gold/goldReport.vue'], resolve),
                    meta: {title: '金标准报告'},
                    name: '金标准报告', leaf: true
                },
                {
                    path: '/SmokeReport/reportid=:reportid',
                    component: resolve => require(['../components/deploy/deployReport.vue'], resolve),
                    meta: {title: '冒烟报告'}

                },
                {
                    path: '/SmokeResult',
                    component: resolve => require(['../components/interface/gold/goldtest.vue'], resolve),
                    meta: {title: '金标准结果'}

                },
                {
                    path: '/monitor',
                    component: resolve => require(['../components/stress/stressMonitor.vue'], resolve),
                    meta: {title: '性能监控'}
                },
                {
                    path: '/stressdata',
                    component: resolve => require(['../components/stress/stressData.vue'], resolve),
                    meta: {title: '性能数据'}
                },
                {
                    path: '/stressHome',
                    component: resolve => require(['../components/stress/stressList.vue'], resolve),
                    meta: {title: '性能测试'}
                },
                {
                    path: '/data',
                    component: resolve => require(['../components/stress/stressData.vue'], resolve),
                    meta: {title: '性能数据'}
                },
                {
                    path: '/stressReport',
                    component: resolve => require(['../components/stress/stressReport.vue'], resolve),
                    meta: {title: '性能报告'},
                    name: '性能报告', leaf: true
                },
                {
                    //邮件配置
                    path: '/mailconfig',
                    component: resolve => require(['../components/report/Mailset.vue'], resolve),
                    meta: {title: '邮件配置'}
                },
                {
                    //安装部署
                    path: '/deploy',
                    component: resolve => require(['../components/deploy/deployList.vue'], resolve),
                    meta: {title: '安装部署'}
                },
                //邮件詳情頁面
                {
                    path: '/',
                    component: ReportInfo,
                    meta: {title: '邮件详情'},
                    hidden: true,
                    children: [
                        {path: 'ReportTitle/report=:report_id', component: ReportTitle, name: '邮件详情', leaf: true},
                        {path: '/ReportTitle/report=:report_id', component: Server, name: '邮件详情', leaf: true},
                    ]
                },
                {
                    //测试报告
                    path: '/testreport',
                    component: resolve => require(['../components/report/Testreport.vue'], resolve),
                    meta: {title: '版本测试报告'}

                },

                {
                    //质量分析报告
                    path: '/analysisReport',
                    component: resolve => require(['../components/report/AnalysisReport.vue'], resolve),
                    meta: {title: '质量分析报告'}

                },
                {
                    // 图片上传组件
                    path: '/upload',
                    component: resolve => require(['../components/page/Upload.vue'], resolve),
                    meta: {title: '文件上传'}
                },
                {
                    // vue-schart组件
                    path: '/charts',
                    component: resolve => require(['../components/page/BaseCharts.vue'], resolve),
                    meta: {title: 'schart图表'}
                },
                {
                    // 拖拽Dialog组件
                    path: '/dialog',
                    component: resolve => require(['../components/page/DragList.vue'], resolve),
                    meta: {title: '拖拽弹框'}
                },
                {
                    // QR code
                    path: '/reportdemo',
                    component: resolve => require(['../components/page/Mychart.vue'], resolve),
                    meta: {title: '版本下载'}
                },
                {
                    // sonar
                    path: '/sonar',
                    component: resolve => require(['../components/page/qrcode.vue'], resolve),
                    meta: {title: '版本下载'}
                },
                {
                    //基础配置
                    path: '/base',
                    component: resolve => require(['../components/DicomTool/DicomFile/dicomFile.vue'], resolve),
                    meta: {title: 'dicom文件'}
                },
                {
                    //duration 删除
                    path: '/deldicom',
                    component: resolve => require(['../components/DicomTool/orthanc/deldicom.vue'], resolve),
                    meta: {title: 'dicom删除'}
                },
                {
                    //dictionary 字典
                    path: '/dictionary',
                    component: resolve => require(['../components/settings/dictionary/dictionaryData.vue'], resolve),
                    meta: {title: '字典'}
                },
                {
                    // 权限页面
                    path: '/permission',
                    component: resolve => require(['../components/page/Permission.vue'], resolve),
                    meta: {title: '权限测试', permission: true}
                },
                {
                    path: '/502',
                    component: resolve => require(['../components/errorpage/502.vue'], resolve),
                    meta: {title: '502'}
                },
                {
                    path: '/500',
                    component: resolve => require(['../components/errorpage/500.vue'], resolve),
                    meta: {title: '500'}
                },
                {
                    path: '/404',
                    component: resolve => require(['../components/errorpage/404.vue'], resolve),
                    meta: {title: '404'}
                },
                {
                    path: '/403',
                    component: resolve => require(['../components/errorpage/403.vue'], resolve),
                    meta: {title: '403'}
                },
                {
                    path: '/host',
                    component: resolve => require(['../components/project/global/ServerList.vue'], resolve),
                    meta: {title: 'Host配置'}
                },
                // {
                //     path: '/Service',
                //     component: resolve => require(['../components/settings/organization/ServiceIntegration.vue'], resolve),
                //     meta: { title: '服务集成' }
                // },
                //項目詳情頁面
                {
                    path: '/project/project=:project_id',
                    component: ProjectInfo,
                    meta: {title: '項目'},
                    hidden: true,
                    children: [
                        {
                            path: '/ProjectTitle/project=:project_id',
                            component: ProjectTitle,
                            meta: {title: '项目概况'},
                            name: '项目概况',
                            leaf: true
                        },
                        {
                            path: '/Server/project=:project_id',
                            component: Server,
                            meta: {title: 'Host配置'},
                            name: 'Host配置',
                            leaf: true
                        },
                        {
                            path: '/api/project=:project_id',
                            component: API,
                            name: 'API接口',
                            leaf: true,
                            child: true,
                            children: [
                                {
                                    path: '/apiList/project=:project_id',
                                    component: ApiList,
                                    meta: {title: '接口列表'},
                                    name: '接口列表'
                                },
                                {
                                    path: '/apiList/project=:project_id/first=:firstGroup',
                                    meta: {title: '分组接口列表'},
                                    component: ApiListGroup,
                                    name: '分组接口列表'
                                },
                                {
                                    path: '/fastTest/project=:project_id',
                                    component: FestTest,
                                    meta: {title: '快速测试'},
                                    name: '快速测试'
                                },
                                {
                                    path: '/addApi/project=:project_id',
                                    component: addApi,
                                    meta: {title: '新增接口'},
                                    name: '新增接口'
                                },
                                {
                                    path: '/detail/project=:project_id/api=:api_id',
                                    component: detail,
                                    name: '接口',
                                    children: [
                                        {
                                            path: '/apiInfo/project=:project_id/api=:api_id',
                                            component: ApiInfo,
                                            meta: {title: '基础信息'},
                                            name: '基础信息'
                                        },
                                        {
                                            path: '/testApi/project=:project_id/api=:api_id',
                                            component: testApi,
                                            meta: {title: '测试'},
                                            name: '测试'
                                        },
                                        {
                                            path: '/apiDynamic/project=:project_id/api=:api_id',
                                            component: ApiDynamic,
                                            meta: {title: '历史'},
                                            name: '历史'
                                        },
                                    ]
                                },
                                {path: '/updateApi/project=:project_id/api=:api_id', component: UpdateApi, name: '修改'},
                            ]
                        },
                        {
                            path: '/automationTest/project=:project_id',
                            component: AutomationTest,
                            name: '自动化测试',
                            meta: {title: '自动化测试'},
                            leaf: true,
                            child: true,
                            children: [
                                {
                                    path: '/caseList/project=:project_id',
                                    component: CaseList,
                                    meta: {title: '用例列表'},
                                    name: '用例列表'
                                },
                                {
                                    path: '/caseList/project=:project_id/first=:firstGroup',
                                    component: CaseListGroup,
                                    meta: {title: '分组用例列表'},
                                    name: '分组用例列表'
                                },
                                {
                                    path: '/caseApiList/project=:project_id/case=:case_id',
                                    component: CaseApiList,
                                    meta: {title: '用例接口列表'},
                                    name: '用例接口列表'
                                },
                                {
                                    path: '/addCaseApi/project=:project_id/case=:case_id',
                                    component: AddCaseApi,
                                    meta: {title: '添加新接口'},
                                    name: '添加新接口'
                                },
                                {
                                    path: '/updateCaseApi/project=:project_id/case=:case_id/api=:api_id',
                                    component: UpdateCaseApi,
                                    name: '修改接口'
                                },
                                {path: '/testReport/project=:project_id', component: TestReport, name: '测试报告'},
                            ]
                        },
                        {
                            path: '/projectMember/project=:project_id',
                            component: ProjectMember,
                            meta: {title: '成员管理'},
                            name: '成员管理',
                            leaf: true
                        },
                        {
                            path: '/projectDynamic/project=:project_id',
                            component: ProjectDynamic,
                            meta: {title: '项目动态'},
                            name: '项目动态',
                            leaf: true
                        },
                        {
                            path: '/projectReport/project=:project_id',
                            component: ProjectReport,
                            meta: {title: '自动化测试报告'},
                            name: '自动化测试报告',
                            leaf: true
                        },
                    ]
                }
            ]
        },
        {
            path: '/login',
            component: resolve => require(['../components/login/Login.vue'], resolve)
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})


// //項目詳情頁面
// {
//   path: '/project/project=:project_id',
//   component: ProjectInfo,
//   meta: {title: '項目'},
//   hidden: true,
//   children: [
//     {
//       path: '/ProjectTitle/project=:project_id',
//       component: '@/views//project/projectTitle/ProjectTitle.vue',
//       name: '项目概况',
//       leaf: true
//     },
//     {
//       path: '/Server/project=:project_id',
//       component: '@/views//project/global/ServerList.vue',
//       name: 'Host配置',
//       leaf: true
//     },
//     {
//       path: '/api/project=:project_id',
//       component: API,
//       name: 'API接口',
//       leaf: true,
//       child: true,
//       children: [
//         {
//           path: '/apiList/project=:project_id/first=:firstGroup',
//           component: '@/views//project/api/ApiListGroup.vue',
//           name: '分组接口列表'
//         },
//         {path: '/fastTest/project=:project_id', component: '@/views//project/api/FestTest.vue', name: '快速测试'},
//         {path: '/addApi/project=:project_id', component: '@/views//project/api/Addapi.vue', name: '新增接口'},
//         {
//           path: '/detail/project=:project_id/api=:api_id',
//           component: detail,
//           name: '接口',
//           children: [
//             {
//               path: '/apiInfo/project=:project_id/api=:api_id',
//               component: '@/views//project/api/updateApi/ApiInfo.vue',
//               name: '基础信息'
//             },
//             {
//               path: '/testApi/project=:project_id/api=:api_id',
//               component: '@/views//project/api/updateApi/TestApi',
//               name: '测试'
//             },
//             {
//               path: '/apiDynamic/project=:project_id/api=:api_id',
//               component: '@/views//project/api/updateApi/ApiDynamic',
//               name: '历史'
//             },
//           ]
//         },
//         {
//           path: '/updateApi/project=:project_id/api=:api_id',
//           component: '@/views//project/updateApi/UpdateApi.vue',
//           name: '修改'
//         },
//       ]
//     },
//     {
//       path: '/automationTest/project=:project_id',
//       component: '@/views//project/automation/AutomationTest.vue',
//       name: '自动化测试',
//       leaf: true,
//       child: true,
//       children: [
//         {path: '/caseList/project=:project_id', component: '@/views//project/automation/CaseList.vue', name: '用例列表'},
//         {
//           path: '/caseList/project=:project_id/first=:firstGroup',
//           component: '@/views//project/automation/CaseListGroup',
//           name: '分组用例列表'
//         },
//         {
//           path: '/caseApiList/project=:project_id/case=:case_id',
//           component: '@/views//project/automation/CaseApiList.vue',
//           name: '用例接口列表'
//         },
//         {
//           path: '/addCaseApi/project=:project_id/case=:case_id',
//           component: '@/views//project/automation/AddCaseApi.vue',
//           name: '添加新接口'
//         },
//         {
//           path: '/updateCaseApi/project=:project_id/case=:case_id/api=:api_id',
//           component: '@/views//project/automation/UpdateCaseApi.vue',
//           name: '修改接口'
//         },
//         {
//           path: '/testReport/project=:project_id',
//           component: '@/views//project/automation/TestReport.vue',
//           name: '测试报告'
//         },
//       ]
//     },
//     {
//       path: '/projectMember/project=:project_id',
//       component: '@/views//project/ProjectMember.vue',
//       name: '成员管理',
//       leaf: true
//     },
//     {
//       path: '/projectDynamic/project=:project_id',
//       component: '@/views//project/ProjectDynamic.vue',
//       name: '项目动态',
//       leaf: true
//     },
//     {
//       path: '/projectReport/project=:project_id',
//       component: '@/views//project/ProjectReport.vue',
//       name: '自动化测试报告',
//       leaf: true
//     },
//   ]
// },