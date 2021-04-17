<template>
	<section>
		<el-col :span="24">
			<template :index='project_id'>
				<el-menu class="el-menu-demo" mode="horizontal" :default-active="activeIndex" :collapse="collapse" background-color="#fff"
					text-color="#000000" active-text-color="#20a0ff" unique-opened router>
					<template v-for="item in items">
						<template v-if="item.subs">
							<el-submenu :index="item.index +project_id" :key="item.index +project_id">
								<template slot="title">
									<i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
								</template>
								<template v-for="subItem in item.subs">
									<el-submenu v-if="subItem.subs" :index="subItem.index" :key="subItem.index">
										<template slot="title">{{ subItem.title }}</template>
										<el-menu-item v-for="(threeItem,i) in subItem.subs" :key="i" :index="threeItem.index">
											{{ threeItem.title }}{{ threeItem.index }}{{ i }}
										</el-menu-item>
									</el-submenu>
									<el-menu-item v-else :index="subItem.index" :key="subItem.index">
										{{ subItem.title }}{{ subItem.index }}{{ threeItem.index }}
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
				<el-menu :default-active="$route.path" class="el-menu-demo" mode="horizontal" @select="handleselect">
					<template v-for="item in $router.options.routes" v-if="!item.projectHidden">
						<template v-for="(items,index) in item.children">
							<el-menu-item :index="items.path" v-if="items.leaf" :key="items.path">
								<template v-if="!items.child">
									<router-link :to="{ name: items.name, params: {id: project_id}}">
										<div>
											{{items.name }}
										</div>
									</router-link>
								</template>
								<template v-if="items.child">
									<router-link :to="{ name: items.children[0].name, params: {id: project_id}}">
										<div>
											{{items.name }}
										</div>
									</router-link>
								</template>
							</el-menu-item>
<!--							<el-submenu :index="index+''" v-if="!items.leaf">-->
<!--								<template >{{items.name}}</template>-->
<!--								<el-menu-item v-for="child in items.children" :key="child.path" :index="child.path">-->
<!--									{{child.name}}-->
<!--								</el-menu-item>-->
<!--							</el-submenu>-->
						</template>
					</template>
				</el-menu>
			</template>
		</el-col>
		<el-col :span="24">
			<transition name="fade" mode="out-in">
				<router-view></router-view>
			</transition>
		</el-col>

		</section>
</template>

<script>
    export default {
        data() {
            return {
                tabPosition: 'top',
                project_id:'',
                sysName:'自动化测试工具',
                collapsed:false,
                sysUserName: '',
                sysUserAvatar: '',
				items: [
                    {
                        icon: 'el-icon-s-platform',
                        index: '/ProjectTitle/project=1',
                        title: '项目详情'
                    },
						{
                        icon: 'el-icon-s-platform',
                        index: '/apiList/project=1',
                        title: 'API接口'
                    },
						{
                        icon: 'el-icon-s-platform',
                        index: '/automationTest/project=1',
                        title: '自动化测试'
                    },
						{
                        icon: 'el-icon-s-platform',
                        index: '/projectMember/project=1',
                        title: '成员管理'
                    },
						{
                        icon: 'el-icon-s-platform',
                        index: '/projectDynamic/project=1',
                        title: '项目记录'
                    },
						{
                        icon: '',
                        index: '/projectReport/project=1',
                        title: '自动化报告'
                    }
				]
            }
        },
		created(){
			  this.getParams();
			  },
		activated() {
			  this.getParams();
			  },
        methods: {
            handleselect: function (a, b) {
            },
            onSubmit() {
                console.log('submit!');
            },
			getParams(){
              this.routerParams=this.$route.query;
              },
            //退出登录
            logout: function () {
                let _this = this;
                this.$confirm('确认退出吗?', '提示', {
                    //type: 'warning'
                }).then(() => {
                    sessionStorage.removeItem('token');
                    _this.$router.push('/login');
                }).catch(() => {

                });
            },
            showMenu(i,status){
                this.$refs.menuCollapsed.getElementsByClassName('submenu-hook-'+i)[0].style.display=status?'block':'none';
            },
        },
        mounted() {
            let user = sessionStorage.getItem('username');
            if (user) {
                name = JSON.parse(user);
                this.sysUserName = name || '';
//				this.sysUserAvatar = '../assets/user.png';
            }
            this.project_id = this.$route.params.project_id
        }
    }

</script>

<style scoped lang="scss">


	.container {
		position: absolute;
		top: 0px;
		bottom: 0px;
		width: 100%;
		.header {
			height: 60px;
			line-height: 60px;
			color:#fff;
			.userinfo {
				text-align: right;
				padding-right: 35px;
				float: right;
				.userinfo-inner {
					cursor: pointer;
					color:#fff;
					img {
						width: 40px;
						height: 40px;
						border-radius: 20px;
						margin: 10px 0px 10px 10px;
						float: right;
					}
				}
			}
			.logo {
				//width:230px;
				height:60px;
				font-size: 22px;
				padding-left:20px;
				padding-right:20px;
				border-color: rgba(238,241,146,0.3);
				border-right-width: 1px;
				border-right-style: solid;
				img {
					width: 40px;
					float: left;
					margin: 10px 10px 10px 18px;
				}
				.txt {
					color:#fff;
				}
			}
			.logo-width{
				width:230px;
			}
			.logo-collapse-width{
				width:60px
			}
			.tools{
				padding: 0px 23px;
				width:14px;
				height: 60px;
				line-height: 60px;
				cursor: pointer;
			}
		}
		.title {
			width: 200px;
			float: left;
			color: #475669;
			font-size: 25px;
			margin: 15px;
			margin-left: 35px;
			margin-bottom: 0px;
			font-family: PingFang SC;
		}
	}
</style>