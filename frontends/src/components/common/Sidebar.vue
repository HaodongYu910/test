<template>
    <div class="sidebar">
        <el-menu class="sidebar-el-menu" :default-active="onRoutes" :collapse="collapse" background-color="#282828"
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
    import bus from '../../utils/bus';

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
                        title: '项目管理',
                        subs: [
                            {
                                index: 'project',
                                title: '项目列表'
                            },
                            {
                                index: 'projectVersion',
                                title: '版本管理'
                            },
                            {   index: 'Publish',
                                title: '持续集成'

                            },
                            {
                                index: 'deploy',
                                title: '安装部署',
                            },
                            {
                                index: 'host',
                                title: 'Host配置'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-s-flag',
                        index: 'interface',
                        title: '接口自动化',
                        subs: [
                            {
                                index: 'scene',
                                title: '接口场景'
                            },
                            {
                                index: 'api',
                                title: 'API管理'
                            },
                            {
                                index: 'automationTest',
                                title: 'API测试'
                            },
                            {
                                index: 'projectReport',
                                title: '测试报告'
                            },
                            {
                                index: 'SmokeList',
                                title: '金标准测试'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-picture-outline-round',
                        index: 'uiauto',
                        title: 'UI自动化',
                        subs: [
                            {
                                index: 'UICase',
                                title: 'UI用例'
                            },
                            {
                                index: 'UIList',
                                title: 'UI列表'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-odometer',
                        index: '3',
                        title: '性能测试',
                        subs: [
                            {
                                index: 'monitor',
                                title: '监控管理'
                            },
                            {
                                index: 'stressdata',
                                title: '性能数据'
                            },
                            {
                                index: 'stressHome',
                                title: '性能测试'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-camera-solid',
                        index: '4',
                        title: 'Dicom工具',
                        subs: [
                            {
                                index: 'base',
                                title: 'Dicom文件'
                            },
                            {
                                index: 'dicom',
                                title: 'Dicom数据'
                            },
                            {
                                index: 'deldicom',
                                title: 'Dicom删除'
                            },
                            {
                                index: 'DicomSend',
                                title: 'Dicom发送'
                            },
                            {
                                index: 'duration',
                                title: '持续化工具'
                            },
                        ]
                    },
                    {
                        icon: 'el-icon-s-tools',
                        index: '7',
                        title: '系统设置',
                        subs: [
                            {
                                index: 'Personal',
                                title: '用户中心'
                            },
                            {
                                index: 'projectMember',
                                title: '成员管理'
                            },
                            {
                                index: 'analysisReport',
                                title: '服务集成'
                            }
                            ,
                            {
                                index: 'dictionary',
                                title: '数据字典'
                            },
                            {
                                index: 'danger',
                                title: '邮件设置'
                            }
                            ,
                            {
                                index: 'reportdemo',
                                title: '测试报告模板'
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-message-solid',
                        index: 'message',
                        title: '消息中心'
                    },
                ]
            }
        },
        computed: {
            onRoutes() {
                return this.$route.path.replace('/', '');
            }
        },
        created() {
            // 通过 Event Bus 进行组件间通信，来折叠侧边栏
            bus.$on('collapse', msg => {
                this.collapse = msg;
            })
        }
    }
</script>

<style scoped>
    .sidebar {
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom: 0;
        overflow-y: scroll;
    }

    .sidebar::-webkit-scrollbar {
        width: 0;
    }

    .sidebar-el-menu:not(.el-menu--collapse) {
        width: 250px;
    }

    .sidebar > ul {
        height: 100%;
    }
</style>
