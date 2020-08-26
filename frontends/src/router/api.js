import axios from 'axios';



export const test = 'http://127.0.0.1:8000';
//export const Autotest = 'http://192.168.2.38:9000';

// 记录访客
export const recordVisitor = params => { return axios.post(`${test}/api/user/VisitorRecord`, params).then(res => res.data) }
// 获取项目
export const getProject = (headers, params) => {
  return axios.get(`${test}/api/project/project_list`, { params: params, headers: headers }).then(res => res.data)
}
// 删除项目
export const delProject = (headers, params) => {
  return axios.post(`${test}/api/project/del_project`, params, { headers }).then(res => res.data)
}
// 禁用项目
export const disableProject = (headers, params) => {
  return axios.post(`${test}/api/project/disable_project`, params, { headers }).then(res => res.data)
}
// 启用项目
export const enableProject = (headers, params) => {
  return axios.post(`${test}/api/project/enable_project`, params, { headers }).then(res => res.data)
}
// 修改项目
export const updateProject = (headers, params) => {
  return axios.post(`${test}/api/project/update_project`, params, { headers }).then(res => res.data)
}
// 添加项目
export const addProject = (headers, params) => {
  return axios.post(`${test}/api/project/add_project`, params, { headers }).then(res => res.data)
}
// 获取项目详情
export const getProjectDetail = (headers, params) => {
  return axios.get(`${test}/api/title/project_info`, { params: params, headers: headers }).then(res => res.data)
}
// 获取测试地址列表
export const getHost = (headers, params) => {
  return axios.get(`${test}/api/global/host_total`, { params: params, headers: headers }).then(res => res.data)
}
// 删除测试地址列表
export const delHost = (headers, params) => {
  return axios.post(`${test}/api/global/del_host`, params, { headers }).then(res => res.data)
}
// 禁用测试地址列表
export const disableHost = (headers, params) => {
  return axios.post(`${test}/api/global/disable_host`, params, { headers }).then(res => res.data)
}
// 启用测试地址列表
export const enableHost = (headers, params) => {
  return axios.post(`${test}/api/global/enable_host`, params, { headers }).then(res => res.data)
}
// 修改测试地址列表
export const updateHost = (headers, params) => {
  return axios.post(`${test}/api/global/update_host`, params, { headers }).then(res => res.data)
}
// 添加测试地址列表
export const addHost = (headers, params) => {
  return axios.post(`${test}/api/global/add_host`, params, { headers }).then(res => res.data)
}
// 获取项目动态
export const getProjectDynamicList = (headers, params) => {
  return axios.get(`${test}/api/dynamic/dynamic`, { params: params, headers: headers }).then(res => res.data)
}
// 获取项目成员
export const getProjectMemberList = (headers, params) => {
  return axios.get(`${test}/api/member/project_member`, { params: params, headers: headers }).then(res => res.data)
}
// 获取发送邮件配置
export const getEmailConfigDetail = (headers, params) => {
  return axios.get(`${test}/api/member/get_email`, { params: params, headers: headers }).then(res => res.data)
}
// 删除邮件配置
export const delEmailConfig = (headers, params) => {
  return axios.post(`${test}/api/member/del_email`, params, { headers }).then(res => res.data)
}
// 添加邮件配置
export const addEmailConfig = (headers, params) => {
  return axios.post(`${test}/api/member/email_config`, params, { headers }).then(res => res.data)
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
// 下载地址
export const download = (headers, params) => {
  return axios.post(`${test}/api/download`, params, { headers }).then(res => res.data)
}
// tag相关工具
export const tagTool = (headers, params) => {
  return axios.post(`${test}/api/tag`, params, { headers }).then(res => res.data)
}
// tag 基础数据
export const tagBase = (headers, params) => {
  return axios.post(`${test}/api/base`, params, { headers }).then(res => res.data)
}
// 推送相关工具
export const pushTool = (headers, params) => {
  return axios.post(`${test}/api/push`, params, { headers }).then(res => res.data)
}
// 获取所有标签
export const getAllTags = (headers, params) => {
  return axios.get(`${test}/api/base`, { params: params }, { headers }).then(res => res.data)
}
// 获取所有标签

// 测试报告相关工具
// 加载版本列表
export const loadTestProject = (headers, params) => {
  return axios.get(`${test}/api/test_project `, { params: params }, headers).then(res => res.data)
}
// 删除版本
export const deleteTestProject = (headers, params) => {
  return axios.post(`${test}/api/deltest_project`, params, headers).then(res => res.data)
}
// 添加版本
export const addTestProject = (headers, params) => {
  return axios.post(`${test}/api/addtest_project`, params, { headers }).then(res => res.data)
}
// 修改版本
export const updateTestProject = (headers, params) => {
  return axios.post(`${test}/api/updatetest_project`, params, { headers }).then(res => res.data)
}
// 加载状态图
export const loadCharts = (headers, params) => {
  return axios.post(`${test}/api/jira/figure `, params, { headers }).then(res => res.data)
}
// 登录验证
export const requestLogin = (headers, params) => {
  return axios.post(`${test}/api/user/login`, params, headers).then(res => res.data)
}
/* 风险项*/
// 更新风险项
export const updateRisk = (headers, params) => {
  return axios.post(`${test}/api/risk/update`, params, { headers }).then(res => res.data)
}
// 增加风险项
export const addRisk = (headers, params) => {
  return axios.post(`${test}/api/risk/add`, params, { headers }).then(res => res.data)
}
// 显示风险项
export const disableRisk = (headers, params) => {
  return axios.post(`${test}/api/risk/del`, params, headers).then(res => res.data)
}
// 禁风险项
export const enableRisk = (headers, params) => {
  return axios.post(`${test}/api/risk/add`, params, { headers }).then(res => res.data)
}
// 删除风险项
export const deleteRisk = (headers, params) => {
  return axios.post(`${test}/api/risk/del`, params, headers).then(res => res.data)
}
// 加载风险列表
export const loadRisk = (headers, params) => {
  return axios.get(`${test}/api/risk `, { params: params }, headers).then(res => res.data)
}

// 获取jira图表数据
export const loadFigure = (headers, params) => {
  return axios.post(`${test}/api/jira/figure `, params, headers).then(res => res.data)
}

// 获取工作任务
export const loadtodo = (headers, params) => {
  return axios.get(`${test}/api/todo `, { params: params }, headers).then(res => res.data)
}

// 修改数据
export const updatedata = (headers, params) => {
  return axios.post(`${test}/api/updatedata`, params, headers).then(res => res.data)
}

// 获取邮件配置
export const loadreport = (headers, params) => {
  return axios.get(`${test}/api/report `, { params: params }, headers).then(res => res.data)
}

// 增加邮件配置
export const addreport = (headers, params) => {
  return axios.post(`${test}/api/addreport`, params, headers).then(res => res.data)
}

// 修改邮件配置
export const updatereport = (headers, params) => {
  return axios.post(`${test}/api/updatereport`, params, headers).then(res => res.data)
}

// 修改邮件配置
export const delreport = (headers, params) => {
  return axios.post(`${test}/api/delreport`, params, headers).then(res => res.data)
}

// 手动发送邮件
export const Send = (headers, params) => {
  return axios.post(`${test}/api/send`, params, headers).then(res => res.data)
}
// 手动调用压测脚本
export const stressTool = (headers, params) => {
  return axios.post(`${test}/api/tool/stresstool`, params, headers).then(res => res.data)
}
// 压测数据
export const getVersion = (headers, params) => {
  return axios.get(`${test}/api/tool/version`, { params: params }, { headers }).then(res => res.data)
}
// 删除压测数据
export const delstressdata = (headers, params) => {
  return axios.post(`${test}/api/tool/delete_stressdata`, params, headers).then(res => res.data)
}
// 修改压测数据
export const updatestressdata = (headers, params) => {
  return axios.post(`${test}/api/tool/update_stressdata`, params, headers).then(res => res.data)
}
// 新增压测数据
export const addstressdat = (headers, params) => {
  return axios.post(`${test}/api/tool/add_stressdata`, params, headers).then(res => res.data)
}
// 压测版本
export const getstressdata = (headers, params) => {
  return axios.get(`${test}/api/tool/stressdata`, { params: params }, { headers }).then(res => res.data)
}
// 删除patient数据
export const delete_patients = (headers, params) => {
  return axios.post(`${test}/api/tool/delete_patients`, params, headers).then(res => res.data)
}
// 获取duration数据
export const getduration = (headers, params) => {
    return axios.get(`${test}/api/tool/getduration`, { params: params }, { headers }).then(res => res.data)
}
//添加duration
export const addduration = (headers, params) => {
  return axios.post(`${test}/api/tool/add_duration`, params, headers).then(res => res.data)
}
// 修改duration
export const updateduration = (headers, params) => {
  return axios.post(`${test}/api/tool/update_duration`, params, headers).then(res => res.data)
}
// 删除duration
export const delduration = (headers, params) => {
  return axios.post(`${test}/api/tool/del_duration`, params, headers).then(res => res.data)
}
// 修改duration发送状态
export const enable_duration = (headers, params) => {
  return axios.post(`${test}/api/tool/enable_duration`, params, headers).then(res => res.data)
}
// 修改duration发送状态
export const disable_duration = (headers, params) => {
  return axios.post(`${test}/api/tool/disable_duration`, params, headers).then(res => res.data)
}
// 获取基础数据
export const getbase = (headers, params) => {
    return axios.get(`${test}/api/base/getdata`, { params: params }, { headers }).then(res => res.data)
}
// 添加基础数据
export const addbaseData = (headers, params) => {
  return axios.post(`${test}/api/base/AddData`, params, headers).then(res => res.data)
}
// 修改基础数据
export const UpdatebaseData = (headers, params) => {
  return axios.post(`${test}/api/base/UpdateData`, params, headers).then(res => res.data)
}

