<template>
    <el-form>
        <el-row :gutter="24">
            <el-col :span="6">
                <el-form-item label="Name">
                    <el-input v-model.trim="user.username"/>
                </el-form-item>
            </el-col>
            <el-col :span="6">
                <el-form-item label="Phone">
                    <el-input v-model.trim="user.phone"/>
                </el-form-item>
            </el-col>
        </el-row>
        <el-row :gutter="24">
            <el-col :span="10">
                <el-form-item label="Email">
                    <el-input v-model.trim="user.email"/>
                </el-form-item>
            </el-col>
        </el-row>
        <el-row :gutter="24">
            <el-col :span="6">
                <el-form-item label="输入密码">
                    <el-input v-model="password"/>
                </el-form-item>
            </el-col>
        </el-row>
        <el-row :gutter="24">
            <el-col :span="6">
                <el-form-item label="再次输入密码">
                    <el-input v-model="passwd"/>
                </el-form-item>
            </el-col>
        </el-row>
        <!--        <el-form-item label="权限">-->
        <!--            <el-select v-model="user.roles" placeholder="请选择权限">-->
        <!--                <el-option label="开发" value="dev"></el-option>-->
        <!--                <el-option label="测试" value="test"></el-option>-->
        <!--                <el-option label="devOps" value="devOps"></el-option>-->
        <!--                <el-option label="admin" value="admin"></el-option>-->
        <!--            </el-select>-->
        <!--        </el-form-item>-->
        <!--        <el-form-item label="是否管理员">-->
        <!--            <el-switch v-model="user.delivery"></el-switch>-->
        <!--        </el-form-item>-->
        <!--        <el-form-item label="活动性质">-->
        <!--            <el-checkbox-group v-model="user.type">-->
        <!--                <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>-->
        <!--                <el-checkbox label="地推活动" name="type"></el-checkbox>-->
        <!--                <el-checkbox label="线下主题活动" name="type"></el-checkbox>-->
        <!--                <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>-->
        <!--            </el-checkbox-group>-->
        <!--        </el-form-item>-->
        <!--        <el-form-item label="特殊资源">-->
        <!--            <el-radio-group v-model="user.resource">-->
        <!--                <el-radio label="线上品牌商赞助"></el-radio>-->
        <!--                <el-radio label="线下场地免费"></el-radio>-->
        <!--            </el-radio-group>-->
        <!--        </el-form-item>-->
        <el-form-item label="其他">
            <el-input type="textarea" v-model="user.desc"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submit">修改</el-button>
            <el-button>取消</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
    import {getUserInfo, UpdateUserInfo} from "../../../../router/api";

    export default {
         data() {
            return {
                password:'',
                passwd: '',
            }
         },
        props: {
            user: {
                default: () => {
                    return {

                    }
                }
            }
        },
        methods: {
            submit() {
                let params = {
                    token: sessionStorage.getItem("token"),
                    username: this.user.username,
                    phone: this.user.phone,
                    password: this.password,
                    passwd: this.passwd,
                    email: this.user.email,

                };
                let headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                };
                UpdateUserInfo(headers, params).then(_data => {
                    let {msg, data, code} = _data;
                    console.log(code)
                    if (code === '0') {
                        this.$message({
                            message: '修改成功',
                            center: true,
                            type: 'success'
                        });
                    } else {
                        this.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
        }
    }
</script>
