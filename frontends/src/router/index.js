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
        //  ????????????
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
            meta: {title: '??????'},
            children: [
                {
                    path: '/home',
                    component: resolve => require(['../components/home/Dashboard.vue'], resolve),
                    meta: {title: '????????????'}
                },
                /* *******    ?????? ??????    *******   */
                {
                    path: '/project',
                    component: resolve => require(['../components/project/Projectlist.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    path: '/projectVersion',
                    component: resolve => require(['../components/project/ProjectVersion.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    //????????????
                    path: '/deploy',
                    component: resolve => require(['../components/deploy/deployList.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    //publish
                    path: '/Publish',
                    component: resolve => require(['../components/publish/Publish.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    //Publish Detail
                    path: '/PublishDetail',
                    component: resolve => require(['../components/publish/PublishDetail.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    path: '/host',
                    component: resolve => require(['../components/project/global/ServerList.vue'], resolve),
                    meta: {title: 'Host??????'}
                },
                {
                    path: '/projectDynamic',
                    component: ProjectDynamic,
                    meta: {title: '????????????'},
                    name: '????????????',
                    leaf: true
                },
                /* *******    UI ??????    *******   */
                {
                    // UICase ??????
                    path: '/UICase',
                    component: resolve => require(['../components/autoui/UICase.vue'], resolve),
                    meta: {title: 'UI??????'}

                },
                {
                    path: '/UICase/caseid=:caseid',
                    component: resolve => require(['../components/autoui/UIMarkdown.vue'], resolve),
                    meta: {title: 'UI????????????'},
                    hidden: true,
                    children: [
                        {
                            path: '/UICase/caseid=:caseid',
                            component: resolve => require(['../components/autoui/UIMarkdown.vue'], resolve),
                            meta: {title: 'UI????????????'}, name: 'UI????????????', leaf: true
                        }
                    ]
                },
                /* *******    UI?????? ??????    *******   */
                {
                    path: '/UIList',
                    component: resolve => require(['../components/autoui/UIList.vue'], resolve),
                    meta: {title: 'UI???????????????'}

                },
                {
                    path: '/UI/UIid=:UIid',
                    component: resolve => require(['../components/autoui/UIDetails.vue'], resolve),
                    meta: {title: 'UI???????????????'},
                    hidden: true,
                    children: [
                        {
                            path: '/UI/UIid=:UIid',
                            component: resolve => require(['../components/autoui/UIDetails.vue'], resolve),
                            meta: {title: 'UI???????????????'}, name: 'UI???????????????', leaf: true
                        }
                    ]
                },
                /* *******    ????????????     *******   */
                {
                    path: '/stressdata',
                    component: resolve => require(['../components/stress/stressData.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    path: '/stressHome',
                    component: resolve => require(['../components/stress/stressList.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    path: '/stressDetail',
                    component: resolve => require(['../components/stress/stressDetail.vue'], resolve),
                    meta: {title: '????????????'},
                    name: "stressDetail"
                },
                {
                    path: '/data',
                    component: resolve => require(['../components/stress/stressData.vue'], resolve),
                    meta: {title: '????????????'}
                },
                {
                    path: '/stressReport',
                    component: resolve => require(['../components/stress/stressReport.vue'], resolve),
                    meta: {title: '????????????'},
                    name: '????????????', leaf: true
                },
                {
                    path: '/monitor',
                    component: resolve => require(['../components/stress/stressMonitor.vue'], resolve),
                    meta: {title: '????????????'}
                },
                /* *******    Dicom ????????????     *******   */
                {
                    path: '/DicomSend',
                    component: resolve => require(['../components/DicomTool/duration/DicomSend.vue'], resolve),
                    meta: {title: 'Dicom??????'}

                },
                {
                    path: '/duration',
                    component: resolve => require(['../components/DicomTool/duration/durationList.vue'], resolve),
                    meta: {title: '???????????????'}

                },
                {
                    path: '/DurationReport/reportid=:reportid',
                    component: resolve => require(['../components/DicomTool/duration/durationReport.vue'], resolve),
                    meta: {title: '???????????????'}

                },
                {
                    path: '/dicom',
                    component: resolve => require(['../components/DicomTool/dicomdata/dicomData.vue'], resolve),
                    meta: {title: 'Dicom??????'},
                    name: 'Dicom??????'

                },
                {
                    path: '/dicomGroup',
                    component: resolve => require(['../components/DicomTool/DicomGroup/dicomGroup.vue'], resolve),
                    meta: {title: 'Dicom?????????'}

                },
                {
                    path: '/durationData',
                    name: 'durationData',
                    component: resolve => require(['../components/DicomTool/duration/durationDetail.vue'], resolve),
                    meta: {title: '???????????????'}

                },
                {
                    //????????????
                    path: '/base',
                    component: resolve => require(['../components/DicomTool/DicomFile/dicomFile.vue'], resolve),
                    meta: {title: 'dicom??????'}
                },
                {
                    //duration ??????
                    path: '/deldicom',
                    component: resolve => require(['../components/DicomTool/orthanc/deldicom.vue'], resolve),
                    meta: {title: 'dicom??????'}
                },
                /* *******      ??????????????? ??????     *******   */
                //  ??????????????? ??????
                // {
                //     //duration ??????
                //     path: '/apiHome',
                //     component: resolve => require(['../components/Interface/home/ApiTestHome.vue'], resolve),
                //     meta: {title: 'API??????'}
                // },
                {
                    path: '/Interface',
                    component: API,
                    meta: {title: 'API??????'},
                    children: [
                        {
                            path: '/apiList/project=:project_id',
                            component: ApiList,
                            meta: {title: '????????????'},
                            name: '????????????'
                        },
                        {
                            path: '/apiList/project=:project_id/first=:firstGroup',
                            meta: {title: '??????????????????'},
                            component: ApiListGroup,
                            name: '??????????????????'
                        },
                        {
                            path: '/fastTest/project=:project_id',
                            component: FestTest,
                            meta: {title: '????????????'},
                            name: '????????????'
                        },
                        {
                            path: '/addApi/project=:project_id',
                            component: addApi,
                            meta: {title: '????????????'},
                            name: '????????????'
                        },
                        {
                            path: '/detail/project=:project_id/Interface=:api_id',
                            component: detail,
                            name: '??????',
                            children: [
                                {
                                    path: '/apiInfo/project=:project_id/Interface=:api_id',
                                    component: ApiInfo,
                                    meta: {title: '????????????'},
                                    name: '????????????'
                                },
                                {
                                    path: '/testApi/project=:project_id/Interface=:api_id',
                                    component: testApi,
                                    meta: {title: '??????'},
                                    name: '??????'
                                },
                                {
                                    path: '/apiDynamic/project=:project_id/Interface=:api_id',
                                    component: ApiDynamic,
                                    meta: {title: '??????'},
                                    name: '??????'
                                },
                            ]
                        },
                        {path: '/updateApi/project=:project_id/Interface=:api_id', component: UpdateApi, name: '??????'},
                    ]
                },
                {
                    path: '/automationTest',
                    component: AutomationTest,
                    name: '???????????????',
                    meta: {title: '???????????????'},
                    child: true,
                    children: [
                        {
                            path: '/caseList/project=:project_id',
                            component: CaseList,
                            meta: {title: '????????????'},
                            name: '????????????'
                        },
                        {
                            path: '/caseList/project=:project_id/first=:firstGroup',
                            component: CaseListGroup,
                            meta: {title: '??????????????????'},
                            name: '??????????????????'
                        },
                        {
                            path: '/caseApiList/project=:project_id/case=:case_id',
                            component: CaseApiList,
                            meta: {title: '??????????????????'},
                            name: '??????????????????'
                        },
                        {
                            path: '/addCaseApi/project=:project_id/case=:case_id',
                            component: AddCaseApi,
                            meta: {title: '???????????????'},
                            name: '???????????????'
                        },
                        {
                            path: '/updateCaseApi/project=:project_id/case=:case_id/Interface=:api_id',
                            component: UpdateCaseApi,
                            name: '????????????'
                        },
                        {path: '/testReport/project=:project_id', component: TestReport, name: '????????????'},
                    ]
                },
                {
                    path: '/projectReport',
                    component: ProjectReport,
                    meta: {title: '?????????????????????'},
                    name: '?????????????????????',
                    leaf: true
                },
                //
                {

                    path: '/scene',
                    component: resolve => require(['../components/Interface/scene/sceneList.vue'], resolve),
                    meta: {title: '????????????'},
                    child: true,
                    children: []
                },
                {
                    path: '/SceneCase',
                    component: resolve => require(['../components/Interface/scene/sceneCase.vue'], resolve),
                    meta: {title: '????????????'},
                    name: '????????????'
                },
                {
                    path: '/SmokeList',
                    component: resolve => require(['../components/Interface/gold/goldList.vue'], resolve),
                    meta: {title: '???????????????'}

                },
                {
                    path: '/goldDetail',
                    component: resolve => require(['../components/Interface/gold/goldDetails.vue'], resolve),
                    meta: {title: '???????????????'},
                    name: '???????????????'

                },
                {
                    path: '/report/goldid=:goldid',
                    component: resolve => require(['../components/Interface/gold/goldReport.vue'], resolve),
                    meta: {title: '???????????????'},
                    name: '???????????????', leaf: true
                },
                {
                    path: '/SmokeReport/reportid=:reportid',
                    component: resolve => require(['../components/deploy/deployReport.vue'], resolve),
                    meta: {title: '????????????'}

                },
                {
                    path: '/SmokeResult',
                    component: resolve => require(['../components/Interface/gold/goldtest.vue'], resolve),
                    meta: {title: '???????????????'}

                },
                /* *******       ????????????     *******   */
                {
                    path: '/message',
                    component: resolve => require(['../components/page/Tabs.vue'], resolve),
                    meta: {title: '????????????'}
                },
                /* *******       ??????????????????     *******   */
                // ????????????
                {
                    path: '/projectMember',
                    component: ProjectMember, meta: {title: '????????????'},
                    name: '????????????',
                    leaf: true
                },
                {
                    // dds????????????
                    path: '/dds',
                    component: resolve => require(['../components/DicomTool/DDS/dds.vue'], resolve),
                    meta: {title: 'DDS??????'}

                },

                {
                    //????????????
                    path: '/mailconfig',
                    component: resolve => require(['../components/report/Mailset.vue'], resolve),
                    meta: {title: '????????????'}
                },

                //??????????????????
                {
                    path: '/',
                    component: ReportInfo,
                    meta: {title: '????????????'},
                    hidden: true,
                    children: [
                        {path: 'ReportTitle/report=:report_id', component: ReportTitle, name: '????????????', leaf: true},
                        {path: '/ReportTitle/report=:report_id', component: Server, name: '????????????', leaf: true},
                    ]
                },
                {
                    //????????????
                    path: '/testreport',
                    component: resolve => require(['../components/report/Testreport.vue'], resolve),
                    meta: {title: '??????????????????'}

                },

                {
                    //??????????????????
                    path: '/analysisReport',
                    component: resolve => require(['../components/report/AnalysisReport.vue'], resolve),
                    meta: {title: '??????????????????'}

                },

                {
                    // ????????????
                    path: '/Personal',
                    component: resolve => require(['../components/settings/personal/PersonSetting.vue'], resolve),
                    meta: {title: '????????????'}
                },

                {
                    //dictionary ??????
                    path: '/dictionary',
                    component: resolve => require(['../components/settings/dictionary/dictionaryData.vue'], resolve),
                    meta: {title: '??????'}
                },

                {
                    // ????????????
                    path: '/permission',
                    component: resolve => require(['../components/page/Permission.vue'], resolve),
                    meta: {title: '????????????', permission: true}
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
                    meta: {title: '??????'},
                    hidden: true,
                    children: [
                        {
                            path: '/ProjectTitle/project=:project_id',
                            component: ProjectTitle,
                            meta: {title: '????????????'},
                            name: '????????????',
                            leaf: true
                        },
                    ]
                }
            ]
        },
        // ????????????
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
