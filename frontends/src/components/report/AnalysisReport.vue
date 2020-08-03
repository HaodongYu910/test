<template>
    <div class="wid-2000 " for="pc">
        <el-container style="height: 2000px; border: 1px solid #eee">
            <el-container>
                <el-header style="text-align: center; color: #FFFFFF; font-size: 24px">
                    <el-dropdown>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item>查看</el-dropdown-item>
                            <el-dropdown-item>新增</el-dropdown-item>
                            <el-dropdown-item>删除</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                    <span>Boimind【2.8.5】& CoinNess【2.1.5】质量分析报告</span>
                </el-header>
                <el-main>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">项目介绍</span>
                            <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    </div>
                    <el-input
                            type="textarea"
                            :rows="5"
                            placeholder="请输入内容"
                            v-model="textarea">
                    </el-input>
                    <div>
                        <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                            <span class="bug-ex-item">概述</span>
                            <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    </div>
                    <el-input
                            type="textarea"
                            :rows="5"
                            placeholder="请输入内容"
                            v-model="textarea">
                    </el-input>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">2 上线问题缺陷</span><img src="../../assets/img/bug-10.png"></p>
                    <el-table :data="tableData" border style="width: 100%">
                        <el-table-column
                                prop="business"
                                label="问题ID"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="product"
                                label="问题内容">
                        </el-table-column>
                        <el-table-column
                                prop="pm"
                                label="经办人"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="测试人员"
                                label="缺陷等级">
                        </el-table-column>
                        <el-table-column
                                prop="online"
                                label="解决状态"
                                width="180">
                        </el-table-column>
                    </el-table>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">3 Case执行情况</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    <el-table :data="tableData" border style="width: 100%">
                        <el-table-column
                                prop="project"
                                label="项目列"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="param"
                                label="相关参数">
                        </el-table-column>
                        <el-table-column
                                prop="device"
                                label="覆盖设备"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="check"
                                label="验收负责人">
                        </el-table-column>
                    </el-table>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">4  Bug明细</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                    <el-table :data="tableData" border style="width: 100%">
                        <el-table-column
                                prop="priority"
                                label="方向/优先级"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="Highest"
                                label="Highest">
                        </el-table-column>
                        <el-table-column
                                prop="High"
                                label="High"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="Medium"
                                label="Medium">
                        </el-table-column>
                        <el-table-column
                                prop="Low"
                                label="Low"
                                width="180">
                        </el-table-column>
                        <el-table-column
                                prop="Lowest"
                                label="Lowest">
                        </el-table-column>
                    </el-table>
                    <p class="bug-exp-step p-t-20 p-b-10"><img src="../../assets/img/bug-10.png">
                        <span class="bug-ex-item">5 性能/压力测试</span>
                        <img class="img-revers" src="../../assets/img/bug-10.png"></p>
                </el-main>

            </el-container>
        </el-container>

    </div>
</template>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }

    .el-aside {
        color: #333;
    }
</style>

<script>
    export default {
        data() {
            return {
                textarea: '1.Boimind 2.8.5 & CoinNess 2.1.5 版本已于8月2日测试完成\n' +
                '2.Android已提交给渠道同学、iOS已提交App Store等待审核；\n' +
                '3.当前版本共消化 糖果红包权益、快讯+图片、热门频道、行情侧需求、广告也无需求、平台基础需求等；\n' +
                '4.本版本共 328个 bug，己解决 307个 ，部分Server Bug 与 P3Bug待到下版本修复。',
                tableData: [{
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '用例执行情况',
                    product: '用例执行情况',
                    param: 'Boimind：\n' +
                    '总共执行用例数：1453\n' +
                    '通过数：1281\n' +
                    '未通过：172\n' +
                    '\n' +
                    'CoinNess:\n' +
                    '总共执行用例数：433\n' +
                    '通过数：372\n' +
                    '未通过：61',
                    device: 'Android：三星S7、vivo X9i、红米note 4x、\n' +
                    '小米 MI 5、华为 P10、华为 P10 Plus、华为Mate 9、\n' +
                    'vivo X20、一加 5T、华为mate10、小米 MI 5等\n' +
                    '\n' +
                    'iOS：iPhone SE、5s、6s plus、6s、7 plus、8 plus、iPhoneX，\n' +
                    'iPhone XS max',
                    check: '尹航\n' +
                    '李虎\n' +
                    '刘畅\n' +
                    '柯尊森\n' +
                    '李兰兰\n' +
                    '蒋银山\n',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }, {
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '',
                    product: '',
                    parameter: '',
                    device: '',
                    check: '',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }, {
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '',
                    product: '',
                    param: '',
                    device: '',
                    check: '',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }, {
                    business: '1.糖果红包积分权益',
                    product: '1.糖果红包积分权益\n' +
                    '2.积分权益后台\n' +
                    '3.数据需求',
                    pm: '王晓东',
                    qa: '李兰兰',
                    online: '已上线',
                    status: ' ',
                    project: '',
                    product: '',
                    param: '',
                    device: '',
                    check: '',
                    priority: 'Boimind',
                    Highest: '12',
                    High: '32',
                    Medium: '23',
                    Low: '4',
                    Lowest: '1'
                }]
            }
        }
    }
</script>