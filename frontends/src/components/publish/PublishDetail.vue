<template>
  <div class="details">
    <div class="top">
      <div class="title">
        <div class="title-left">
          <span>{{ taskName }}</span>
          <span class="mode">
            <i class="el-icon-monitor"></i>
            {{ taskUnit }}</span
          >
          <!-- <span class="mode">
            <i class="el-icon-suitcase"></i>
            {{ taskMode ? taskMode : "--" }}</span
          > -->
        </div>
        <div class="title-right">
          <el-button type="primary" icon="el-icon-orange" @click="buildStart">
            {{ stepStart ? "取消" : "构建" }}
          </el-button>
          <el-button
            icon="el-icon-edit"
            @click="editBtnClick"
            :disabled="startFlag"
            >编辑</el-button
          >
          <!-- <el-button
            type="danger"
            icon="el-icon-delete-solid"
            :disabled="startFlag"
            @click="submitDelete"
            :loading="deleteLoading"
            >删除</el-button
          > -->
        </div>
      </div>
      <div class="status">
        <span>状态：</span>
        <span>{{ this.statusText }}</span>
      </div>
    </div>
    <div class="build bg-color">
      <el-steps
        :active="stepActive"
        finish-status="success"
        class="build-step"
        align-center
        :process-status="progressFailActive ? 'error' : 'wait'"
      >
        <el-step
          v-for="item in progressList"
          :key="item.status"
          :title="item.name"
          :icon="
            stepActive === item.status && !progressFailActive
              ? 'el-icon-loading'
              : item.className
          "
        ></el-step>
      </el-steps>
      <div class="build-title">构建历史</div>
      <div class="build-list">
        <div class="build-item build-item-title">
          <span>构建序号</span>
          <span>构建分支</span>
          <span>发起人</span>
          <span>开始时间</span>
          <span>状态</span>

          <span>操作</span>
        </div>
        <div class="build-item" v-for="(item, index) in buildList" :key="index">
          <span>{{ item.job }}</span>
          <span>{{ item.branch }}</span>
          <span>{{ item.user }}</span>
          <span>{{ item.create_time }}</span>
          <span>{{
            item.packStatus === "0"
                ? "未构建"
                : item.packStatus === "1"
                ? "构建中"
                : item.packStatus === "2"
                ? "构建成功"
                : "构建失败"
          }}</span>
          <span class="highlight">
            <el-button
              type="text"
              class="operation-item"
              @click="checkExpress(item)"
            >
              查看日志
            </el-button>
          </span>
        </div>
      </div>
    </div>
    <el-dialog
      title="修改构建任务"
      :visible.sync="dialogVisible"
      width="55%"
      center
      class="dialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="dialog-item">
        <span>服务分支：</span>

        <el-cascader
          :options="groupOptions"
          v-model="branchName"
          filterable
          class="dialog-item-right"
        ></el-cascader>
      </div>
      <div class="dialog-item">
        <span class="left">部署环境：</span>
        <el-select
          v-model="createModeType"
          placeholder="请选择环境"
          @click.native="gethost()"
          class="dialog-item-right"
        >
          <el-option key="" label="" value=""></el-option>
          <el-option
            v-for="item in Hosts"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </div>
      <div class="dialog-item">
        <span>构建名称：</span>
        <el-input placeholder="请输入构建名称" v-model="buildName"></el-input>
      </div>
      <div class="dialog-item">
        <span>代码库：</span>
        <el-input placeholder="请输入git代码库" v-model="githubName">
        </el-input>
      </div>

      <div class="dialog-item">
        <span>附属依赖：</span>
        <el-upload
          class="upload-demo"
          drag
          multiple
          action="#"
          :on-change="upfileOnChange"
          :file-list="fileList"
          :limit="1"
          :http-request="subUploadFile"
          accept=".zip"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">
            <p>1. 如一些线上无法集成，需手动安装下载的依赖资源</p>
            <p>2. 只能上传zip文件</p>
          </div>
        </el-upload>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          class="btn"
          @click="submitPublishEditTask"
          :disabled="submitLoading"
          :loading="submitLoading"
          >修 改
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getBuildDetail,
  submitPublishAddTaskService,
  submitPublishUpdateTaskService,
  submitPublishDeleteTaskService,
  PublishEnableTaskService,
  PublishDisableTaskService,
  queryGitBranchService,
  queryGit,
  getHost,
  submitPublishEditTaskService,
  addupload,
  queryBuildStateService,
} from "./../../router/api";
import { buildStateMapFunc } from "./../../utils/index.js";
import bus from "./../../utils/bus";

export default {
  name: "publishDetail",
  // el-icon-loading
  data() {
    return {
      buildList: [],
      stepActive: null,
      progressList: buildStateMapFunc().stateList,
      startFlag: false,
      dialogVisible: false,
      groupOptions: [],
      branchName: "",
      fileList: [],
      githubName: "",
      buildName: "",
      Hosts: "",
      createModeType: "",
      taskName: "",
      taskMode: "",
      taskUnit: "",
      submitLoading: false,
      project_id: localStorage.getItem("project_id"),
      upfileId: "",
      deleteLoading: false,
      startLoading: false,
      stepStart: false,
      statusText: "",
      timer: null,
      progressFailActive: null,
    };
  },
  created() {
    this.getParams();
    this.getgroupbase();
    const { query } = this.$route;
    console.log("query", query);
    const { name = "", branch = "", Host = "", service = "", git = "" } = query;
    this.branchName = [+git, branch];
    this.buildName = name || "";
    this.createModeType = Host || "";
    this.taskName = name || "";
    this.taskUnit = service || "";
    this.taskMode = Host || "";
  },
  activated() {
    this.getParams();
  },
  mounted() {
    this.checkBuildState();
  },
  methods: {
    //获取由路由传递过来的参数
    getParams() {
      this.build_id = +this.$route.query.id;
      this.jenkins_job = this.$route.query.jenkins_job;
      this.jenkins_view = this.$route.query.jenkins_view;
      this.BuildDetail();
    },
    // 获取数据列表
    BuildDetail() {
      this.listLoading = true;
      const self = this;
      const params = {
        build_id: this.build_id,
      };
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      getBuildDetail(headers, params).then((res) => {
        self.listLoading = false;
        const { msg, code, data } = res;
        if (code === "0") {
          self.buildList = data.data;
        } else {
          self.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    //展示监控
    checkExpress: function(item) {
      const url =
        "http://10.10.10.2:8095/view/" +
        this.jenkins_view +
        "/job/" +
        this.jenkins_job +
        "/" +
        item.job +
        "/consoleText";
      const dualScreenLeft =
        window.screenLeft !== undefined ? window.screenLeft : screen.left;
      const dualScreenTop =
        window.screenTop !== undefined ? window.screenTop : screen.top;

      const width = window.innerWidth
        ? window.innerWidth
        : document.documentElement.clientWidth
        ? document.documentElement.clientWidth
        : screen.width;
      const height = window.innerHeight
        ? window.innerHeight
        : document.documentElement.clientHeight
        ? document.documentElement.clientHeight
        : screen.height;

      const left = width / 2 - 1500 / 2 + dualScreenLeft;
      const top = height / 2 - 800 / 2 + dualScreenTop;
      const newWindow = window.open(
        url,
        "集成日志",
        "toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=yes, copyhistory=no, width=" +
          "1500" +
          ", height=" +
          "800" +
          ", top=" +
          top +
          ", left=" +
          left
      );

      // Puts focus on the newWindow
      if (window.focus) {
        newWindow.focus();
      }
    },
    handleCurrentChange(val) {
      this.page = val;
      this.getDurationlist();
    },

    selsChange: function(sels) {
      this.sels = sels;
    },
    buildStart() {
      this.startFlag = true;
      this.startLoading = true;
      let self = this;
      this.listLoading = true;
      const { id = "" } = this.$route.query;
      let params = {
        build_package_id: +id,
        project_id: this.project_id,
      };
      let headers = {
        "Content-Type": "application/json",
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      if (this.stepStart) {
        PublishDisableTaskService(headers, params).then((_data) => {
          this.stepStart = !this.stepStart;
          let { msg, code, data } = _data;
          if (code === "0") {
            this.stepActive = null;
            this.startFlag = false;
            this.timer && clearTimeout(this.timer);
            self.$message({
              message: "停止成功",
              center: true,
              type: "success",
            });
          } else {
            self.$message.error({
              message: msg,
              center: true,
            });
          }
        });
      } else {
        PublishEnableTaskService(headers, params)
          .then((_data) => {
            let { msg, code, data } = _data;
            self.listLoading = false;
            if (code === "0") {
              this.stepStart = !this.stepStart;
              this.stepActive = 0;

              this.checkBuildState(3000);
            } else {
              this.changeBuildFailResult();
            }
          })
          .catch((err) => {
            this.changeBuildFailResult();
          });
      }
    },
    // 获取host数据列表
    gethost() {
      this.listLoading = true;
      const self = this;
      const params = {
        page_size: 900,
      };
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      getHost(headers, params).then((res) => {
        self.listLoading = false;
        const { msg, code, data } = res;
        if (code === "0") {
          self.total = data.total;
          self.list = data.data;
          var json = JSON.stringify(self.list);
          this.Hosts = JSON.parse(json);
          console.log(this.Hosts);
        } else {
          self.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    getgroupbase() {
      this.listLoading = true;
      const self = this;
      const params = {
        project_id: this.project_id,
      };
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      queryGitBranchService(headers, params).then((res) => {
        self.listLoading = false;
        const { msg, code, data } = res;
        if (code === "0") {
          this.groupOptions = data.groupOptions;
        } else {
          self.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    upfileOnChange(file, fileList) {
      console.log(file);
    },
    submitPublishEditTask() {
      let { buildName, createModeType = "", githubName, branchName } = this;
      if (!createModeType) {
        this.ModalAlert("请选择环境！");
        return;
      }
      if (!buildName) {
        this.ModalAlert("构建名称不能为空！");
        return;
      }

      if (!githubName) {
        this.ModalAlert("请输入git代码库ssh地址！");
        return;
      }
      if (!branchName) {
        this.ModalAlert("请输入代码分支！");
        return;
      }
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      const params = {
        name: this.buildName,
        code: this.githubName,
        git_id: this.branchName[0],
        branch: this.branchName[1],
        Host_id: this.createModeType,
        user_id: JSON.parse(sessionStorage.getItem("token")),
        Project_id: this.project_id,
        build_id: +this.build_id,
        file_id: this.upfileId,
      };
      this.submitLoading = true;
      submitPublishEditTaskService(headers, params)
        .then((res) => {
          const { data = {}, msg, code } = res;
          this.submitLoading = false;
          if (code === "0") {
            this.$message.success({
              message: msg,
              center: true,
            });
            this.dialogVisible = false;
            this.updateCurrTitleInfo();
          } else {
            this.$message.error({
              message: msg,
              center: true,
            });
          }
        })
        .catch((err) => {
          this.submitLoading = false;
        });
    },
    editBtnClick() {
      this.dialogVisible = !this.dialogVisible;
    },
    ModalAlert(message, type = "error") {
      this.$message({
        message,
        type,
      });
    },
    subUploadFile(data) {
      console.log(data);
      let params = new FormData();
      params.append("file", data.file);
      params.append("type", "build");
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      addupload(headers, params).then((res) => {
        const { msg, code, data } = res;
        if (code === "0") {
          this.upfileId = data.fileid || "";
        } else {
          this.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    updateCurrTitleInfo() {
      this.taskName = this.buildName || "";
      const hostList = this.Hosts;
      const { createModeType } = this;
      const unitName = hostList.filter((item) => +item.id === +createModeType);
      console.log("unitName", unitName);
      this.taskMode = unitName.length ? unitName[0].name : "";
    },
    checkBuildState(time = 0) {
      this.timer && clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        const { id = "" } = this.$route.query;
        let params = {
          build_id: +id,
          project_id: this.project_id,
        };
        let headers = {
          "Content-Type": "application/json",
          Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
        };

        queryBuildStateService(headers, params)
          .then((res) => {
            const { code, data } = res;
            if (code === "0") {
              this.stepActive = +data.step === 0 ? null : +data.step - 1;
              const statusMap =
                this.stepActive !== null
                  ? this.progressList[this.stepActive]
                  : { name: "未开始" };
              this.stepStart = this.stepActive !== null;

              this.statusText = statusMap.name;
              if (this.stepActive === 4) {
                this.startFlag = false;
                this.stepStart = false;
                this.BuildDetail();
              } else {
                this.checkBuildState(3000);
              }
            } else {
              this.timer && clearTimeout(this.timer);
              this.changeBuildFailResult();
            }
          })
          .catch((err) => {
            this.timer && clearTimeout(this.timer);
            this.changeBuildFailResult();
          });
      }, time);
    },
    changeBuildFailResult() {
      this.$message.error({
        message: "构建异常",
        center: true,
      });
      this.progressFailActive = true;
      this.startFlag = false;
      this.stepStart = false;
      this.progressList.splice(this.stepActive || 0, 1, {
        name: "构建异常",
        status: this.stepActive,
        className: "el-icon-error",
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.details {
  width: 100%;
  height: 100%;
  font-size: 15px;
  color: #333;
  display: flex;
  flex-direction: column;

  .top {
    background-color: #fff;
    padding: 15px;
    margin-bottom: 10px;
  }

  .title {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    background-color: #fff;

    &-left {
      > span {
        display: inline-block;
        margin-right: 20px;

        &:first-child {
          font-size: 16px;
          font-weight: bold;
        }
      }
    }
  }

  .bg-color {
    background-color: #fff;
  }

  .build {
    flex: 1;
    background-color: #fff;

    &-title {
      font-weight: 500;
      margin-bottom: 10px;
      padding: 15px;
    }

    &-list {
      width: 100%;
    }

    &-item {
      width: 100%;
      display: flex;
      align-items: center;
      font-size: 13px;
      height: 40px;
      border-bottom: 1px solid #f0f0f0;
      &:hover {
        background-color: #f1f1f1;
      }
      > span {
        flex: 1;
        text-align: center;
      }

      &-title {
        font-weight: 500;

        background-color: #fafafa;
        display: flex;
        align-items: center;
        font-size: 13px;
        font-weight: 500;

        > span {
          flex: 1;
          text-align: center;
          position: relative;

          &::after {
            position: absolute;
            right: 0;
            top: 10%;
            content: "";
            display: block;
            background-color: #ddd;
            width: 1px;
            height: 80%;
          }
          &:last-child {
            &::after {
              display: none;
            }
          }
        }
        &:hover {
          background-color: #fafafa;
        }
      }

      .highlight {
        color: #1890ff;
        cursor: pointer;
      }
    }

    &-step {
      padding-top: 20px;
    }

    .el-step__icon.is-icon {
      color: #1890ff;
    }

    .is-wait {
      font-size: 13px !important;
      font-weight: 500;
    }
  }
  .dialog {
    font-size: 15px;
    color: #333;
    width: 60%;
    left: 20%;

    &-item {
      > span {
        color: #333;
        display: inline-block;
        min-width: 110px;
      }

      display: flex;
      align-items: center;
      padding-bottom: 15px;

      .el-input {
        width: 360px;
      }
      &-right {
        width: 360px;
      }
    }

    &-footer {
      .btn {
        width: 60%;
        font-size: 14px;
        font-weight: 500;
      }
    }
  }
}
</style>
