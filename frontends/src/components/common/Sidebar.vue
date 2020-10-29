<template>
    <div class="sidebar">
        <el-menu class="sidebar-el-menu" :default-active="onRoutes" :collapse="collapse" background-color="#324157"
            text-color="#bfcbd9" active-text-color="#20a0ff" unique-opened router>
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-submenu :index="item.index" :key="item.index">
                        <template slot="title">
                            <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu v-if="subItem.subs" :index="subItem.index" :key="subItem.index">
                                <template slot="title">{{ subItem.title }}</template>
                                <el-menu-item v-for="(threeItem,i) in subItem.subs" :key="i" :index="threeItem.index">
                                    {{ threeItem.title }}
                                </el-menu-item>
                            </el-submenu>
                            <el-menu-item v-else :index="subItem.index" :key="subItem.index">
                                {{ subItem.title }}
                            </el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index">
                        <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script>
    import bus from '../common/bus';
    export default {
        data() {
            return {
                collapse: false,
                items: [
                    {
                        icon: 'el-icon-s-home',
                        index: 'home',
                        title: '系统首页'
                    },
                    {
                        icon: 'el-icon-s-platform',
                        index: 'project',
                        title: '项目',
                        subs: [
                            {
                                index: 'project',
                                title: '项目列表'
                            },
                            {
                                index: 'host',
                                title: 'Host配置'
                            },
                            {
                                index: 'data',
                                title: '自动化测试报告'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-s-help',
                        index: '3',
                        title: '测试工具',
                        subs: [
                            {
                                index: 'data',
                                title: '测试数据'
                            },
                            {
                                index: 'dicom',
                                title: 'dicom工具'
                            },
                            {
                                index: 'stress',
                                title: '性能工具'
                            },
                             {
                                index: 'stressreport',
                                title: '图表结果'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-message',
                        index: '4',
                        title: '邮件管理',
                        subs: [
                            {
                                index: 'testreport',
                                title: '邮件配置'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-s-tools',
                        index: '5',
                        title: '系统设置',
                        subs: [
                            {
                                index: 'qrcode',
                                title: '用户配置'
                            },
                            {
                                index: 'base',
                                title: '基础配置'
                            },
                            {
                                index: 'mailconfig',
                                title: '其他配置'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-message-solid',
                        index: 'tabs',
                        title: '消息中心'
                    },
                ]
            }
        },
        computed:{
            onRoutes(){
                return this.$route.path.replace('/','');
            }
        },
        created(){
            // 通过 Event Bus 进行组件间通信，来折叠侧边栏
            bus.$on('collapse', msg => {
                this.collapse = msg;
            })
        }
    }
</script>

<style scoped>
    .sidebar{
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom:0;
        overflow-y: scroll;
    }
    .sidebar::-webkit-scrollbar{
        width: 0;
    }
    .sidebar-el-menu:not(.el-menu--collapse){
        width: 250px;
    }
    .sidebar > ul {
        height:100%;
    }
</style>
