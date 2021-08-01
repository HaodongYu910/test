import Vue from 'vue';
import Router from 'vue-router';

const ProjectInfo = () => import('../components/project/Projectdetail.vue');
const Server = () => import('../components/project/global/ServerList.vue');
const API = () => import('../components/Interface/api/API.vue');
const ApiList = () => import('../components/Interface/api/ApiList.vue');
const ApiListGroup = () => import('../components/Interface/api/ApiListGroup.vue');
const FestTest = () => import('../components/Interface/api/FestTest.vue');
const addApi = () => import('../components/Interface/api/Addapi.vue');
const detail = () => import('../components/Interface/api/updateApi/ApiForm.vue');
const ApiInfo = () => import('../components/Interface/api/updateApi/ApiInfo.vue');
const testApi = () => import('../components/Interface/api/updateApi/TestApi.vue');
const UpdateApi = () => import('../components/Interface/api/updateApi/UpdateApi.vue');
const ApiDynamic = () => import('../components/Interface/api/updateApi/ApiDynamic.vue');
const AutomationTest = () => import('../components/Interface/automation/AutomationTest.vue');
const CaseList = () => import('../components/Interface/automation/CaseList.vue');
const CaseListGroup = () => import('../components/Interface/automation/CaseListGroup.vue');
const CaseApiList = () => import('../components/Interface/automation/CaseApiList.vue');
const AddCaseApi = () => import('../components/Interface/automation/AddCaseApi.vue');
const UpdateCaseApi = () => import('../components/Interface/automation/UpdateCaseApi.vue');
const TestReport = () => import('../components/Interface/automation/TestReport.vue');
const ProjectMember = () => import('../components/project/ProjectMember.vue');
const ProjectDynamic = () => import('../components/project/ProjectDynamic.vue');
const ProjectTitle = () => import('../components/project/projectTitle/ProjectTitle.vue');
const ProjectReport = () => import('../components/project/ProjectReport.vue');
const ReportInfo = () => import('../components/report/Testreportdetail.vue');
const ReportTitle = () => import('../components/home/Dashboard.vue');


Vue.use(Router);

export default new Router({

    routes: [
        //  登录页面
        {
            path: '/login',
            component: resolve => require(['../components/login/Login.vue'], resolve)
        },

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
                /* *******    项目 页面    *******   */
                {
                    path: '/project',
                    component: resolve => require(['../components/project/Projectlist.vue'], resolve),
                    meta: {title: '项目列表'}
                },
                {
                    path: '/projectVersion',
                    component: resolve => require(['../components/project/ProjectVersion.vue'], resolve),
                    meta: {title: '项目版本'}
                },
                {
                    //安装部署
                    path: '/deploy',
                    component: resolve => require(['../components/deploy/deployList.vue'], resolve),
                    meta: {title: '安装部署'}
                },
                {
                    //publish
                    path: '/Publish',
                    component: resolve => require(['../components/publish/Publish.vue'], resolve),
                    meta: {title: '持续集成'}
                },
                {
                    //Publish Detail
                    path: '/PublishDetail',
                    component: resolve => require(['../components/publish/PublishDetail.vue'], resolve),
                    meta: {title: '集成详情'}
                },
                {
                    path: '/host',
                    component: resolve => require(['../components/project/global/ServerList.vue'], resolve),
                    meta: {title: 'Host配置'}
                },
                {
                    path: '/projectDynamic',
                    component: ProjectDynamic,
                    meta: {title: '项目动态'},
                    name: '项目动态',
                    leaf: true
                },
                /* *******    UI 页面    *******   */
                {
                    // UICase 用例
                    path: '/UICase',
                    component: resolve => require(['../components/autoui/UICase.vue'], resolve),
                    meta: {title: 'UI用例'}

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
                /* *******    UI列表 页面    *******   */
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
                /* *******    性能页面     *******   */
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
                    path: '/stressDetail',
                    component: resolve => require(['../components/stress/stressDetail.vue'], resolve),
                    meta: {title: '性能详情'},
                    name: "stressDetail"
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
                    path: '/monitor',
                    component: resolve => require(['../components/stress/stressMonitor.vue'], resolve),
                    meta: {title: '性能监控'}
                },
                /* *******    Dicom 工具页面     *******   */
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
                    meta: {title: 'Dicom数据'},
                    name: 'Dicom数据'

                },
                {
                    path: '/dicomGroup',
                    component: resolve => require(['../components/DicomTool/DicomGroup/dicomGroup.vue'], resolve),
                    meta: {title: 'Dicom组管理'}

                },
                {
                    path: '/durationData',
                    name: 'durationData',
                    component: resolve => require(['../components/DicomTool/duration/durationDetail.vue'], resolve),
                    meta: {title: '持续化详情'}

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
                /* *******      接口自动化 页面     *******   */
                //  接口自动化 页面
                // {
                //     //duration 删除
                //     path: '/apiHome',
                //     component: resolve => require(['../components/Interface/home/ApiTestHome.vue'], resolve),
                //     meta: {title: 'API接口'}
                // },
                {
                    path: '/Interface',
                    component: API,
                    meta: {title: 'API列表'},
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
                            path: '/detail/project=:project_id/Interface=:api_id',
                            component: detail,
                            name: '接口',
                            children: [
                                {
                                    path: '/apiInfo/project=:project_id/Interface=:api_id',
                                    component: ApiInfo,
                                    meta: {title: '基础信息'},
                                    name: '基础信息'
                                },
                                {
                                    path: '/testApi/project=:project_id/Interface=:api_id',
                                    component: testApi,
                                    meta: {title: '测试'},
                                    name: '测试'
                                },
                                {
                                    path: '/apiDynamic/project=:project_id/Interface=:api_id',
                                    component: ApiDynamic,
                                    meta: {title: '历史'},
                                    name: '历史'
                                },
                            ]
                        },
                        {path: '/updateApi/project=:project_id/Interface=:api_id', component: UpdateApi, name: '修改'},
                    ]
                },
                {
                    path: '/automationTest',
                    component: AutomationTest,
                    name: '自动化测试',
                    meta: {title: '自动化测试'},
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
                            path: '/updateCaseApi/project=:project_id/case=:case_id/Interface=:api_id',
                            component: UpdateCaseApi,
                            name: '修改接口'
                        },
                        {path: '/testReport/project=:project_id', component: TestReport, name: '测试报告'},
                    ]
                },
                {
                    path: '/projectReport',
                    component: ProjectReport,
                    meta: {title: '自动化测试报告'},
                    name: '自动化测试报告',
                    leaf: true
                },
                //
                {

                    path: '/scene',
                    component: resolve => require(['../components/Interface/scene/sceneList.vue'], resolve),
                    meta: {title: '接口场景'},
                    child: true,
                    children: []
                },
                {
                    path: '/SceneCase',
                    component: resolve => require(['../components/Interface/scene/sceneCase.vue'], resolve),
                    meta: {title: '场景用例'},
                    name: '场景用例'
                },
                {
                    path: '/SmokeList',
                    component: resolve => require(['../components/Interface/gold/goldList.vue'], resolve),
                    meta: {title: '金标准列表'}

                },
                {
                    path: '/goldDetail',
                    component: resolve => require(['../components/Interface/gold/goldDetails.vue'], resolve),
                    meta: {title: '金标准详情'},
                    name: '金标准详情'

                },
                {
                    path: '/report/goldid=:goldid',
                    component: resolve => require(['../components/Interface/gold/goldReport.vue'], resolve),
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
                    component: resolve => require(['../components/Interface/gold/goldtest.vue'], resolve),
                    meta: {title: '金标准结果'}

                },
                /* *******       系统消息     *******   */
                {
                    path: '/message',
                    component: resolve => require(['../components/page/Tabs.vue'], resolve),
                    meta: {title: '消息中心'}
                },
                /* *******       系统设置页面     *******   */
                // 成员管理
                {
                    path: '/projectMember',
                    component: ProjectMember, meta: {title: '成员管理'},
                    name: '成员管理',
                    leaf: true
                },
                {
                    // dds监控界面
                    path: '/dds',
                    component: resolve => require(['../components/DicomTool/DDS/dds.vue'], resolve),
                    meta: {title: 'DDS监控'}

                },

                {
                    //邮件配置
                    path: '/mailconfig',
                    component: resolve => require(['../components/report/Mailset.vue'], resolve),
                    meta: {title: '邮件配置'}
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
                    // 个人中心
                    path: '/Personal',
                    component: resolve => require(['../components/settings/personal/PersonSetting.vue'], resolve),
                    meta: {title: '个人中心'}
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
                    ]
                }
            ]
        },
        // 错误页面
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
