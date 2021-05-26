import axios from 'axios';
export const test = process.env.VUE_APP_MODE


// 登录验证
export const requestLogin = (headers, params) => {
  return axios.post(`${test}/project/user/login`, params, headers).then(res => res.data)
}
// 获取项目
export const getProject = (headers, params) => {
  return axios.get(`${test}/project/project_list`, { params: params, headers: headers }).then(res => res.data)
}
// 删除项目
export const delProject = (headers, params) => {
  return axios.post(`${test}/project/del_project`, params, { headers }).then(res => res.data)
}
// 禁用项目
export const disableProject = (headers, params) => {
  return axios.post(`${test}/project/disable_project`, params, { headers }).then(res => res.data)
}
// 启用项目
export const enableProject = (headers, params) => {
  return axios.post(`${test}/project/enable_project`, params, { headers }).then(res => res.data)
}
// 修改项目
export const updateProject = (headers, params) => {
  return axios.post(`${test}/project/update_project`, params, { headers }).then(res => res.data)
}
// 添加项目
export const addProject = (headers, params) => {
  return axios.post(`${test}/project/add_project`, params, { headers }).then(res => res.data)
}
// 获取项目详情
export const getProjectDetail = (headers, params) => {
  return axios.get(`${test}/project/title/project_info`, { params: params, headers: headers }).then(res => res.data)
}
// 获取测试地址列表
export const getHost = (headers, params) => {
  return axios.get(`${test}/project/global/host_total`, { params: params, headers: headers }).then(res => res.data)
}
// 修改测试地址列表
export const updateHost = (headers, params) => {
  return axios.post(`${test}/project/global/update_host`, params, { headers }).then(res => res.data)
}
// 添加测试地址列表
export const addHost = (headers, params) => {
  return axios.post(`${test}/project/global/add_host`, params, { headers }).then(res => res.data)
}
// 删除测试地址列表
export const delHost = (headers, params) => {
  return axios.post(`${test}/project/global/del_host`, params, { headers }).then(res => res.data)
}
// 禁用测试地址列表
export const disableHost = (headers, params) => {
  return axios.post(`${test}/project/global/disable_host`, params, { headers }).then(res => res.data)
}
// 启用测试地址列表
export const enableHost = (headers, params) => {
  return axios.post(`${test}/project/global/enable_host`, params, { headers }).then(res => res.data)
}
// 禁用http
export const disableHostProtocol = (headers, params) => {
  return axios.post(`${test}/project/global/disable_protocol`, params, { headers }).then(res => res.data)
}
// 启用http
export const enableHostProtocol = (headers, params) => {
  return axios.post(`${test}/project/global/enable_protocol`, params, { headers }).then(res => res.data)
}
// 获取项目动态
export const getProjectDynamicList = (headers, params) => {
  return axios.get(`${test}/project/dynamic/dynamic`, { params: params, headers: headers }).then(res => res.data)
}
// 获取项目成员
export const getProjectMemberList = (headers, params) => {
  return axios.get(`${test}/project/member/project_member`, { params: params, headers: headers }).then(res => res.data)
}
// 获取发送邮件配置
export const getEmailConfigDetail = (headers, params) => {
  return axios.get(`${test}/project/member/get_email`, { params: params, headers: headers }).then(res => res.data)
}
// 删除邮件配置
export const delEmailConfig = (headers, params) => {
  return axios.post(`${test}/project/member/del_email`, params, { headers }).then(res => res.data)
}
// 添加邮件配置
export const addEmailConfig = (headers, params) => {
  return axios.post(`${test}/project/member/email_config`, params, { headers }).then(res => res.data)
}
// 获取字典
export const getDictionary = (headers, params) => {
    return axios.get(`${test}/project/dictionary/list`, { params: params }, { headers }).then(res => res.data)
}
// 添加字典
export const addDictionary = (headers, params) => {
  return axios.post(`${test}/project/dictionary/add`, params, headers).then(res => res.data)
}
// 修改字典
export const UpdateDictionary = (headers, params) => {
  return axios.post(`${test}/project/dictionary/update`, params, headers).then(res => res.data)
}
// 启用字典
export const EnableDictionary = (headers, params) => {
  return axios.post(`${test}/project/dictionary/enable`, params, headers).then(res => res.data)
}
// 禁用字典
export const DisableDictionary = (headers, params) => {
  return axios.post(`${test}/project/dictionary/disable`, params, headers).then(res => res.data)
}
// 删除字典
export const DelDictionary = (headers, params) => {
  return axios.post(`${test}/project/dictionary/del`, params, headers).then(res => res.data)
}
// 加载版本列表
export const loadTestProject = (headers, params) => {
  return axios.get(`${test}/api/test_project `, { params: params }, headers).then(res => res.data)
}
// 删除版本
export const deleteTestProject = (headers, params) => {
  return axios.post(`${test}/project/deltest_project`, params, headers).then(res => res.data)
}
// 添加版本
export const addTestProject = (headers, params) => {
  return axios.post(`${test}/project/addtest_project`, params, { headers }).then(res => res.data)
}
// 修改版本
export const updateTestProject = (headers, params) => {
  return axios.post(`${test}/project/updatetest_project`, params, { headers }).then(res => res.data)
}
// 加载状态图
export const loadCharts = (headers, params) => {
  return axios.post(`${test}/project/jira/figure `, params, { headers }).then(res => res.data)
}

// 获取jira图表数据
export const loadFigure = (headers, params) => {
  return axios.post(`${test}/project/jira/figure `, params, headers).then(res => res.data)
}

// 重启 创建用户
export const getCreateRestart = (headers, params) => {
  return axios.post(`${test}/project/createRestart `, params, headers).then(res => res.data)
}
// 获取工作任务
export const loadtodo = (headers, params) => {
  return axios.get(`${test}/project/todo `, { params: params }, headers).then(res => res.data)
}

// 获取邮件配置
export const loadreport = (headers, params) => {
  return axios.get(`${test}/project/report `, { params: params }, headers).then(res => res.data)
}

// 增加邮件配置
export const addreport = (headers, params) => {
  return axios.post(`${test}/project/addreport`, params, headers).then(res => res.data)
}

// 修改邮件配置
export const updatereport = (headers, params) => {
  return axios.post(`${test}/project/updatereport`, params, headers).then(res => res.data)
}

// 修改邮件配置
export const delreport = (headers, params) => {
  return axios.post(`${test}/project/delreport`, params, headers).then(res => res.data)
}
// 上传文件
export const addupload = (headers, params) => {
  return axios.post(`${test}/project/addupload`, params, headers).then(res => res.data)
}
// 上传文件
export const delupload = (headers, params) => {
  return axios.post(`${test}/project/delupload`, params, headers).then(res => res.data)
}
// 自动测试记录
export const getupload = (headers, params) => {
  return axios.get(`${test}/project/upload`, { params: params }, { headers }).then(res => res.data)
}
// get install 列表
export const getInstall = (headers, params) => {
  return axios.get(`${test}/project/install/list`, params, headers).then(res => res.data)
}
// get install 版本
export const getInstallersion = (headers, params) => {
  return axios.get(`${test}/project/install/version`, params, headers).then(res => res.data)
}
// 安装日志
export const getJournal = (headers, params) => {
  return axios.post(`${test}/project/install/journal`, params, headers).then(res => res.data)
}
// 添加 安装部署任务
export const addInstall = (headers, params) => {
  return axios.post(`${test}/project/install/add`, params, headers).then(res => res.data)
}
// 修改 安装部署任务
export const updateInstall = (headers, params) => {
  return axios.post(`${test}/project/install/update`, params, headers).then(res => res.data)
}
// 删除 安装部署任务
export const delInstall = (headers, params) => {
  return axios.post(`${test}/project/install/del`, params, headers).then(res => res.data)
}
// 启用 安装部署任务
export const EnableInstall = (headers, params) => {
  return axios.post(`${test}/project/install/enable`, params, headers).then(res => res.data)
}
// 停止 安装部署任务
export const DisableInstall = (headers, params) => {
  return axios.post(`${test}/project/install/disable`, params, headers).then(res => res.data)
}
// 冒烟报告
export const getInstallReport = (headers, params) => {
  return axios.post(`${test}/project/install/getReport`, params, headers).then(res => res.data)
}

// 获取自动化测试结果
export const getTestResultList = (headers, params) => {
  return axios.get(`${test}/api/report/auto_test_report`, { params: params, headers: headers }).then(res => res.data)
}
// 获取最近10次测试时间
export const getTestTenTime = (headers, params) => {
  return axios.get(`${test}/api/report/test_time`, { params: params, headers: headers }).then(res => res.data)
}
// 获取最近10次测试比例结果
export const getTestTenResult = (headers, params) => {
  return axios.get(`${test}/api/report/lately_ten`, { params: params, headers: headers }).then(res => res.data)
}
// 添加接口
export const addApiDetail = (headers, params) => {
  return axios.post(`${test}/api/api/add_api`, params, { headers }).then(res => res.data)
}
// 获取接口分组列表
export const getApiGroupList = (headers, params) => {
  return axios.get(`${test}/api/api/group`, { params: params, headers: headers }).then(res => res.data)
}
// 添加接口分组
export const addApiGroup = (headers, params) => { return axios.post(`${test}/api/api/add_group`, params, { headers }).then(res => res.data) }
// 修改接口分组
export const updateApiGroup = (headers, params) => {
  return axios.post(`${test}/api/api/update_name_group`, params, { headers }).then(res => res.data)
}
// 删除接口分组
export const delApiGroup = (headers, params) => {
  return axios.post(`${test}/api/api/del_group`, params, { headers }).then(res => res.data)
}
// 金标准冒烟测试报告
export const getGoldreport = (headers, params) => {
  return axios.get(`${test}/api/gold/GoldReport`, { params: params }, { headers }).then(res => res.data)
}
// 金标准冒烟测试列表
export const getsmoke = (headers, params) => {
  return axios.get(`${test}/api/gold/smokelist`, { params: params }, { headers }).then(res => res.data)
}
// 添加金标准冒烟测试
export const addSmoke = (headers, params) => {
  return axios.post(`${test}/api/gold/addsmoke`, params, headers).then(res => res.data)
}
// 修改金标准冒烟测试
export const UpdateSmoke = (headers, params) => {
  return axios.post(`${test}/api/gold/updatesmoke`, params, headers).then(res => res.data)
}
// 启用金标准冒烟测试
export const EnableSmoke = (headers, params) => {
  return axios.post(`${test}/api/gold/enablesmoke`, params, headers).then(res => res.data)
}
// 禁用金标准冒烟测试
export const DisableSmoke = (headers, params) => {
  return axios.post(`${test}/api/gold/disablesmoke`, params, headers).then(res => res.data)
}
// 删除冒烟测试记录
export const DelSmoke = (headers, params) => {
  return axios.post(`${test}/api/gold/delsmoke`, params, headers).then(res => res.data)
}
// 冒烟测试记录
export const getsmokerecord = (headers, params) => {
  return axios.get(`${test}/api/gold/record`, { params: params }, { headers }).then(res => res.data)
}
// 金标准冒烟测试
export const getsmokestart = (headers, params) => {
  return axios.post(`${test}/api/gold/test`, params, headers).then(res => res.data)
}
// 金标准图表
export const getsmokefigure = (headers, params) => {
  return axios.post(`${test}/api/gold/figure`, params, headers).then(res => res.data)
}


// 压测报告模型列表
export const getstressmodel = (headers, params) => {
  return axios.get(`${test}/stress/stressmodel`, { params: params }, { headers }).then(res => res.data)
}
// 压测列表
export const stresslist = (headers, params) => {
  return axios.get(`${test}/stress/list`, { params: params }, { headers }).then(res => res.data)
}
// 新增压测
export const addStress = (headers, params) => {
  return axios.post(`${test}/stress/list/add`, params, headers).then(res => res.data)
}
// 修改压测
export const updateStress = (headers, params) => {
  return axios.post(`${test}/stress/list/update`, params, headers).then(res => res.data)
}
// 修改压测
export const delStress = (headers, params) => {
   return axios.post(`${test}/stress/list/del`, params, headers).then(res => res.data)
}
// 启用Stress数据状态
export const enableStress = (headers, params) => {
  return axios.post(`${test}/stress/list/enable`, params, headers).then(res => res.data)
}
// 禁用Stress数据状态
export const disableStress = (headers, params) => {
  return axios.post(`${test}/stress/list/disable`, params, headers).then(res => res.data)
}
//压测详情
export const StressDetail = (headers, params) => {
  return axios.get(`${test}/stress/Detail `, { params: params }, headers).then(res => res.data)
}
// 运行压力测试
export const stressTool = (headers, params) => {
  return axios.post(`${test}/stress/run`, params, headers).then(res => res.data)
}
// 停止压力测试
export const stressStop = (headers, params) => {
  return axios.post(`${test}/stress/stop`, params, headers).then(res => res.data)
}
// 压测数据
export const getVersion = (headers, params) => {
  return axios.get(`${test}/stress/version`, { params: params }, { headers }).then(res => res.data)
}
// 压测结果
export const getreportfigure = (headers, params) => {
  return axios.post(`${test}/stress/figure`,params, headers ).then(res => res.data)
}
// 压测report
export const getStressReport = (headers, params) => {
  return axios.get(`${test}/stress/Report`, { params: params }, { headers }).then(res => res.data)
}
// 压测结果
export const saveAnalysis = (headers, params) => {
  return axios.post(`${test}/stress/Analysis`,params, headers ).then(res => res.data)
}
// 压测版本
export const getstressversion = (headers, params) => {
  return axios.get(`${test}/stress/version`, { params: params }, { headers }).then(res => res.data)
}
// 压测结果
export const getstressresult = (headers, params) => {
  return axios.post(`${test}/stress/result`,params, headers ).then(res => res.data)
}
// 生成压测结果
export const stresssave = (headers, params) => {
  return axios.post(`${test}/stress/save`, params, headers).then(res => res.data)
}
// 压测数据列表
export const StressData = (headers, params) => {
  return axios.get(`${test}/stress/data/Data`, { params: params }, { headers }).then(res => res.data)
}
// 添加压测数据
export const addStressData = (headers, params) => {
  return axios.post(`${test}/stress/data/StressDataAdd`, params, headers).then(res => res.data)
}
// 删除压测数据
export const DelStressData = (headers, params) => {
  return axios.post(`${test}/stress/data/StressDataDel`, params, headers).then(res => res.data)
}
// 同步压测数据挂载信息
export const StressSynchro = (headers, params) => {
  return axios.post(`${test}/stress/data/SynchroStressData`, params, headers).then(res => res.data)
}
// disable基准数据
export const disableBenchmarkstatus = (headers, params) => {
  return axios.post(`${test}/stress/data/disablebenchmarkstatus`, params, { headers }).then(res => res.data)
}
// enable基准数据
export const enableBenchmarkstatus = (headers, params) => {
  return axios.post(`${test}/stress/data/enablebenchmarkstatus`, params, { headers }).then(res => res.data)
}


//------------------- Dicom  -------------------
// 删除数据
export const deldicomdata = (headers, params) => {
  return axios.post(`${test}/dicom/delDDD`, params, headers).then(res => res.data)
}
// 修改dicom数据
export const updatedicomdata = (headers, params) => {
  return axios.post(`${test}/dicom/update`, params, headers).then(res => res.data)
}
// 新增dicom数据
export const adddicomdata = (headers, params) => {
  return axios.post(`${test}/dicom/add_dicomData`, params, headers).then(res => res.data)
}
// DisableDicom数据
export const DisableDicom = (headers, params) => {
  return axios.post(`${test}/dicom/disabledicom`, params, headers).then(res => res.data)
}
// EnableDicom数据
export const EnableDicom = (headers, params) => {
  return axios.post(`${test}/dicom/enabledicom`, params, headers).then(res => res.data)
}
// 新增dicom数据
export const dicomdetail = (headers, params) => {
  return axios.post(`${test}/dicom/dicomdetail`, params, headers).then(res => res.data)
}
//dicom数据
export const getdicomdata = (headers, params) => {
  return axios.get(`${test}/dicom/dicomData`, { params: params }, { headers }).then(res => res.data)
}
//生成CSV
export const dicomcsv = (headers, params) => {
  return axios.post(`${test}/dicom/dicomcsv`, params, headers).then(res => res.data)
}
// 删除报告
export const deldicomreport = (headers, params) => {
  return axios.post(`${test}/dicom/delreport`, params, headers).then(res => res.data)
}

// 删除patient数据
export const delete_patients = (headers, params) => {
  return axios.post(`${test}/dicom/delete_patients`, params, headers).then(res => res.data)
}
// 获取dicom数据
export const getdicomSend = (headers, params) => {
  return axios.post(`${test}/dicom/dicomSend`, params, headers).then(res => res.data)
}
// 跳转imageview页面
export const getdicomurl = (headers, params) => {
  return axios.post(`${test}/dicom/dicomurl`, params, headers).then(res => res.data)
}
// 获取duration数据报告
export const getdurationReport = (headers, params) => {
    return axios.get(`${test}/dicom/report/durationreport`, { params: params }, { headers }).then(res => res.data)
}

// 获取duration数据
export const getduration = (headers, params) => {
    return axios.get(`${test}/dicom/duration/getduration`, { params: params }, { headers }).then(res => res.data)
}

// 获取duration发送数据
export const getdurationData = (headers, params) => {
    return axios.get(`${test}/dicom/duration/durationData`, { params: params }, { headers }).then(res => res.data)
}
//添加duration
export const addduration = (headers, params) => {
  return axios.post(`${test}/dicom/duration/add`, params, headers).then(res => res.data)
}
// 修改duration
export const updateduration = (headers, params) => {
  return axios.post(`${test}/dicom/duration/up`, params, headers).then(res => res.data)
}
// 删除duration
export const delduration = (headers, params) => {
  return axios.post(`${test}/dicom/duration/del`, params, headers).then(res => res.data)
}
// 启动匿名化
export const anonStart = (headers, params) => {
  return axios.post(`${test}/dicom/tool/anonymization`, params, headers).then(res => res.data)
}

// 启动提取dicom文件
export const get_dicom_start = (headers, params) => {
  return axios.post(`${test}/dicom/tool/get_dicom`, params, headers).then(res => res.data)
}

// 修改duration发送状态
export const enable_duration = (headers, params) => {
  return axios.post(`${test}/dicom/duration/enable_duration`, params, headers).then(res => res.data)
}
// 修改duration发送状态
export const disable_duration = (headers, params) => {
  return axios.post(`${test}/dicom/duration/disable_duration`, params, headers).then(res => res.data)
}

// 持续化数据验证
export const getdurationverify = (headers, params) => {
      return axios.get(`${test}/dicom/duration/verify`, { params: params }, { headers }).then(res => res.data)
}
// 持续化数据验证统计
export const durationverifydata = (headers, params) => {
      return axios.get(`${test}/dicom/duration/durationverifydata`, { params: params }, { headers }).then(res => res.data)
}
// 获取基础数据
export const getbase = (headers, params) => {
    return axios.get(`${test}/dicom/base/getdata`, { params: params }, { headers }).then(res => res.data)
}
// 添加基础数据
export const addbaseData = (headers, params) => {
  return axios.post(`${test}/dicom/base/addData`, params, headers).then(res => res.data)
}
// 修改基础数据
export const UpdatebaseData = (headers, params) => {
  return axios.post(`${test}/dicom/base/upData`, params, headers).then(res => res.data)
}
// 启用基础数据
export const Enablebase = (headers, params) => {
  return axios.post(`${test}/dicom/base/enablebase`, params, headers).then(res => res.data)
}
// 禁用基础数据
export const Disablebase = (headers, params) => {
  return axios.post(`${test}/dicom/base/disablebase`, params, headers).then(res => res.data)
}
// 删除基础数据
export const Delbasedata = (headers, params) => {
  return axios.post(`${test}/dicom/base/delbasedata`, params, headers).then(res => res.data)
}
// 获取组数据
export const getGroup = (headers, params) => {
    return axios.get(`${test}/dicom/group/getgroup`, { params: params }, { headers }).then(res => res.data)
}
// 获取组信息
export const getGroupInfo = (headers, params) => {
    return axios.get(`${test}/dicom/group/getinfo`, { params: params }, { headers }).then(res => res.data)
}
// 获取级联组信息
export const getGroupBase = (headers, params) => {
    return axios.get(`${test}/dicom/group/groupbase`, { params: params }, { headers }).then(res => res.data)
}
// 添加组
export const AddGroup = (headers, params) => {
  return axios.post(`${test}/dicom/group/groupadd`, params, headers).then(res => res.data)
}
// 修改组
export const Updategroup = (headers, params) => {
  return axios.post(`${test}/dicom/group/groupup`, params, headers).then(res => res.data)
}
// 启用组
export const EnableGroup = (headers, params) => {
  return axios.post(`${test}/dicom/group/enablegroup`, params, headers).then(res => res.data)
}
// 禁用组
export const DisableGroup = (headers, params) => {
  return axios.post(`${test}/dicom/group/disablegroup`, params, headers).then(res => res.data)
}
// 删除组
export const DelGroup = (headers, params) => {
  return axios.post(`${test}/dicom/group/delgroup`, params, headers).then(res => res.data)
}
// 同步数据数量
export const dicomcount = (headers, params) => {
    return axios.get(`${test}/dicom/base/dicom`, { params: params }, { headers }).then(res => res.data)
}

//------------------- UI测试 -------------------
// UI测试用例列表
export const getAutoCase = (headers, params) => {
  return axios.get(`${test}/ui/auto/case`, { params: params }, { headers }).then(res => res.data)
}
// 添加UI测试用例
export const addAutoCase = (headers, params) => {
  return axios.post(`${test}/ui/auto/addcase`, params, headers).then(res => res.data)
}
// 修改UI测试用例
export const UpdateAutoCase = (headers, params) => {
  return axios.post(`${test}/ui/auto/updatecase`, params, headers).then(res => res.data)
}
// 启用UI测试用例
export const EnableAutoCase = (headers, params) => {
  return axios.post(`${test}/ui/auto/enablecase`, params, headers).then(res => res.data)
}
// 禁用UI测试用例
export const DisableAutoCase = (headers, params) => {
  return axios.post(`${test}/ui/auto/disablecase`, params, headers).then(res => res.data)
}
// 删除UI测试用例
export const DelAutoCase = (headers, params) => {
  return axios.post(`${test}/ui/auto/delcase`, params, headers).then(res => res.data)
}
// UI测试列表
export const getAuto = (headers, params) => {
  return axios.get(`${test}/ui/auto/autolist`, { params: params }, { headers }).then(res => res.data)
}
// 添加UI测试
export const addAuto = (headers, params) => {
  return axios.post(`${test}/ui/auto/addauto`, params, headers).then(res => res.data)
}
// 修改UI测试
export const UpdateAuto = (headers, params) => {
  return axios.post(`${test}/ui/auto/updateauto`, params, headers).then(res => res.data)
}
// 启用UI测试
export const EnableAuto = (headers, params) => {
  return axios.post(`${test}/ui/auto/enableauto`, params, headers).then(res => res.data)
}
// 停止UI测试
export const DisableAuto = (headers, params) => {
  return axios.post(`${test}/ui/auto/disableauto`, params, headers).then(res => res.data)
}
// 删除UI测试
export const DelAuto = (headers, params) => {
  return axios.post(`${test}/ui/auto/delauto`, params, headers).then(res => res.data)
}
// UI测试报告
export const getReport = (headers, params) => {
  return axios.get(`${test}/ui/auto/report`, { params: params }, { headers }).then(res => res.data)
}
// UI测试错误截图
export const getImage = (headers, params) => {
  return axios.get(`${test}/ui/auto/image`, { params: params }, { headers }).then(res => res.data)
}
// UI测试记录
export const getAutorecord = (headers, params) => {
  return axios.get(`${test}/ui/auto/record`, { params: params }, { headers }).then(res => res.data)
}
// 自动测试图表
export const getAutofigure = (headers, params) => {
  return axios.post(`${test}/api/auto/figure`, params, headers).then(res => res.data)
}

