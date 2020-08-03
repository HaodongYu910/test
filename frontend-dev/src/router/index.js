import Vue from 'vue';
import Router from 'vue-router';

const ProjectInfo = () => import('../components/project/Projectdetail.vue');
const globalHost = () => import('../components/project/global/Globalhost.vue');
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
const AutomationTest = () => import('../components/project/automation/AutomationTest.vue');
const CaseList = () => import('../components/project/automation/CaseList.vue');
const CaseListGroup = () => import('../components/project/automation/CaseListGroup.vue');
const CaseApiList = () => import('../components/project/automation/CaseApiList.vue');
const AddCaseApi = () => import('../components/project/automation/AddCaseApi.vue');
const UpdateCaseApi = () => import('../components/project/automation/UpdateCaseApi.vue');
const TestReport = () => import('../components/project/automation/TestReport.vue');
const ProjectMember = () => import('../components/project/ProjectMember.vue');
const ProjectDynamic = () => import('../components/project/ProjectDynamic.vue');
const ProjectTitle = () => import('../components/project/projectTitle/ProjectTitle.vue');
const ProjectReport = () => import('../components/project/ProjectReport.vue');
const ReportInfo = () => import('../components/report/Testreportdetail.vue');
const ReportTitle = () => import('../components/page/Dashboard.vue');


Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/home'
        },
        {
            path: '/',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            meta: { title: '自述文件' },
            children:[
                {
                    path: '/home',
                    component: resolve => require(['../components/page/Dashboard.vue'], resolve),
                    meta: { title: '系统首页' }
                },
                {
                    path: '/icon',
                    component: resolve => require(['../components/page/Icon.vue'], resolve),
                    meta: { title: '自定义图标' }
                },
                {
                    path: '/project',
                    component: resolve => require(['../components/project/Projectlist.vue'], resolve),
                    meta: { title: '项目列表' }
                },
                {
                    path: '/table',
                    component: resolve => require(['../components/page/BaseTable.vue'], resolve),
                    meta: { title: '环境地址' }
                },
                {
                    path: '/cd',
                    component: resolve => require(['../components/page/Tabs.vue'], resolve),
                    meta: { title: '消息中心' }
                },
                {
                    path: '/dicom',
                    component: resolve => require(['../components/tool/dicom.vue'], resolve),
                    meta: { title: 'Dicom工具' }
                },
                {
                    path: '/stress',
                    component: resolve => require(['../components/tool/stress/stress.vue'], resolve),
                    meta: { title: '性能工具' }
                },
                {
                    path: '/data',
                    component: resolve => require(['../components/tool/testdata.vue'], resolve),
                    meta: { title: '测试数据' }
                },
                {
                    //邮件配置
                    path: '/mailconfig',
                    component: resolve => require(['../components/report/Mailset.vue'], resolve),
                    meta: { title: '邮件配置' }
                },
                //邮件詳情頁面
                {
                    path: '/',
                    component: ReportInfo,
                    meta: { title: '邮件' },
                    hidden: true,
                    children: [
                        {   path: 'ReportTitle/report=:report_id', component: ReportTitle, name: '邮件详情', leaf: true},
                        {   path: '/ReportTitle/report=:report_id', component: globalHost, name: '邮件详情', leaf: true},
                    ]
                },
                {
                    //测试报告
                    path: '/testreport',
                    component: resolve => require(['../components/report/Testreport.vue'], resolve),
                    meta: { title: '版本测试报告' }

                },

                {
                    //质量分析报告
                    path: '/analysisReport',
                    component: resolve => require(['../components/report/AnalysisReport.vue'], resolve),
                    meta: { title: '质量分析报告' }

                },
                {
                    //风险点列表
                    path: '/danger',
                    component: resolve => require(['../components/project/danger.vue'], resolve),
                    meta: { title: '风险点列表' }

                },
                {
                    // 富文本编辑器组件
                    path: '/editor',
                    component: resolve => require(['../components/page/VueEditor.vue'], resolve),
                    meta: { title: '富文本编辑器' }
                },
                {
                    // markdown组件
                    path: '/markdown',
                    component: resolve => require(['../components/page/Markdown.vue'], resolve),
                    meta: { title: 'markdown编辑器' }
                },
                {
                    // 图片上传组件
                    path: '/upload',
                    component: resolve => require(['../components/page/Upload.vue'], resolve),
                    meta: { title: '文件上传' }
                },
                {
                    // vue-schart组件
                    path: '/charts',
                    component: resolve => require(['../components/page/BaseCharts.vue'], resolve),
                    meta: { title: 'schart图表' }
                },
                {
                    // 拖拽列表组件
                    path: '/bind',
                    component: resolve => require(['../components/tool/BindList.vue'], resolve),
                    meta: { title: '风控绑定' }
                },
                {
                    // 拖拽Dialog组件
                    path: '/dialog',
                    component: resolve => require(['../components/page/DragDialog.vue'], resolve),
                    meta: { title: '拖拽弹框' }
                },
                {
                    // QR code
                    path: '/qrcode',
                    component: resolve => require(['../components/page/qrcode.vue'], resolve),
                    meta: { title: '版本下载' }
                },
                {
                    // sonar
                    path: '/sonar',
                    component: resolve => require(['../components/page/qrcode.vue'], resolve),
                    meta: { title: '版本下载' }
                },
                {
                    // 权限页面
                    path: '/permission',
                    component: resolve => require(['../components/page/Permission.vue'], resolve),
                    meta: { title: '权限测试', permission: true }
                },
                {
                    path: '/404',
                    component: resolve => require(['../components/page/404.vue'], resolve),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: resolve => require(['../components/page/403.vue'], resolve),
                    meta: { title: '403' }
                },
                //項目詳情頁面
                {
                    path: '/project/project=:project_id',
                    component: ProjectInfo,
                    meta: { title: '項目' },
                    hidden: true,
                    children: [
                        {   path: '/ProjectTitle/project=:project_id', component: ProjectTitle, name: '项目概况', leaf: true},
                        {   path: '/GlobalHost/project=:project_id', component: globalHost, name: 'Host配置', leaf: true},
                        {   path: '/api/project=:project_id',
                            component: API,
                            name: 'API接口',
                            leaf: true,
                            child: true,
                            children: [
                                {   path: '/apiList/project=:project_id', component: ApiList, name: '接口列表'},
                                {   path: '/apiList/project=:project_id/first=:firstGroup', component: ApiListGroup, name: '分组接口列表'},
                                {   path: '/fastTest/project=:project_id', component: FestTest, name: '快速测试'},
                                {   path: '/addApi/project=:project_id', component: addApi, name: '新增接口'},
                                {   path: '/detail/project=:project_id/api=:api_id',
                                    component: detail,
                                    name: '接口',
                                    children: [
                                        { path: '/apiInfo/project=:project_id/api=:api_id', component: ApiInfo, name: '基础信息'},
                                        { path: '/testApi/project=:project_id/api=:api_id', component: testApi, name: '测试'},
                                        { path: '/apiDynamic/project=:project_id/api=:api_id', component: ApiDynamic, name: '历史'},
                                    ]
                                },
                                { path: '/updateApi/project=:project_id/api=:api_id', component: UpdateApi, name: '修改'},
                            ]},
                        {   path: '/automationTest/project=:project_id',
                            component: AutomationTest,
                            name: '自动化测试',
                            leaf: true,
                            child: true,
                            children: [
                                {   path: '/caseList/project=:project_id', component: CaseList, name: '用例列表'},
                                {   path: '/caseList/project=:project_id/first=:firstGroup', component: CaseListGroup, name: '分组用例列表'},
                                {   path: '/caseApiList/project=:project_id/case=:case_id', component: CaseApiList, name: '用例接口列表'},
                                {   path: '/addCaseApi/project=:project_id/case=:case_id', component: AddCaseApi, name: '添加新接口'},
                                {   path: '/updateCaseApi/project=:project_id/case=:case_id/api=:api_id', component: UpdateCaseApi, name: '修改接口'},
                                {   path: '/testReport/project=:project_id', component: TestReport, name: '测试报告'},
                            ]
                        },
                        {   path: '/projectMember/project=:project_id', component: ProjectMember, name: '成员管理', leaf: true},
                        {   path: '/projectDynamic/project=:project_id', component: ProjectDynamic, name: '项目动态', leaf: true},
                        {   path: '/projectReport/project=:project_id', component: ProjectReport, name: '自动化测试报告', leaf: true},
                    ]
                }
            ]
        },
        {
            path: '/login',
            component: resolve => require(['../components/page/Login.vue'], resolve)
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
  //       path: '/GlobalHost/project=:project_id',
  //       component: '@/views//project/global/Globalhost.vue',
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