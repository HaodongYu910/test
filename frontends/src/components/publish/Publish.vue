<template>
  <div class="publish">
    <div class="top">
      <div class="top-left">
        <div class="top-item">
          <span class="left">服务单元：</span>
          <el-select
            v-model="unitType"
            placeholder="请选择服务单元"
            @click.native="getqueryGit()"
          >
            <el-option key="" label="" value=""></el-option>
            <el-option
              v-for="item in unitList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </div>
        <div class="top-item">
          <span class="left">环境：</span>
          <el-select
            v-model="modeType"
            placeholder="请选择环境"
            @click.native="gethost()"
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
      </div>
      <div class="top-right">
        <el-button type="primary" round @click="dialogVisible = true"
          >新建 +
        </el-button>
      </div>
    </div>
    <div class="con">
      <div class="con-item con-title">
        <span class="con-name">构建名称</span>
        <span>服务单元</span>
        <span>分支</span>
        <span>环境</span>
        <span>创建时间</span>
        <span>状态</span>
        <span>操作</span>
      </div>

      <div class="con-item" v-for="(item, index) in buildList" :key="index">
        <span>{{ item.name }}</span>
        <span>{{ item.service }}</span>
        <span>{{ item.branch }}</span>
        <span>测试</span>
        <span>{{ item.create_time }}</span>
        <span>
          <span
            class="status"
            :class="
              item.packStatus === '0'
                ? 'not_built'
                : item.packStatus === '1'
                ? 'building'
                : item.packStatus === '2'
                ? 'success'
                : 'failed'
            "
            >{{
              item.packStatus === "0"
                ? "未构建"
                : item.packStatus === "1"
                ? "构建中"
                : item.packStatus === "2"
                ? "构建成功"
                : "构建失败"
            }}</span
          >
        </span>

        <span class="operation">
          <el-button
            type="text"
            class="operation-item"
            @click="handleChangeStatus(item)"
            :disabled="deleteLoading"
          >
            {{ item.build_status ? "停止" : "构建" }}
          </el-button>
          <el-button
            type="text"
            class="operation-item"
            @click="jumpDetail(item)"
            :disabled="deleteLoading"
            >流水线</el-button
          >
          <!-- <el-button type="text" class="operation-item">日志</el-button> -->
          <el-button
            type="text"
            class="operation-item"
            @click="submitDelete(index, item.id)"
            :disabled="deleteLoading"
            >删除</el-button

          >
        </span>
      </div>
    </div>
    <el-dialog
      title="新建构建任务"
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
          @click.native="getgroupbase()"
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

      <!--            <div class="dialog-item">-->
      <!--                <span>部署服务器：</span>-->
      <!--                <el-input placeholder="请输入部署服务器" v-model="serviceIp">-->
      <!--                </el-input>-->
      <!--            </div>-->

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
        <el-button type="primary" class="btn" @click="submitPublishAddTask"
          >新 建
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import {
  getPublishList,
  submitPublishAddTaskService,
  submitPublishUpdateTaskService,
  submitPublishDeleteTaskService,
  PublishEnableTaskService,
  PublishDisableTaskService,
  queryGitBranchService,
  queryGit,
  getHost,
  addupload,
} from "./../../router/api";

export default {
  name: "PublishRoute",
  data() {
    return {
      project_id: localStorage.getItem("project_id"),
      groupOptions: [],
      Hosts: [],
      unitList: ["web前端", "3D Service"],
      unitType: "web前端",
      modeList: ["开发测试", "测试", "生产"],
      modeType: "",
      dialogVisible: false,
      buildName: "",
      createUnitType: "",
      createModeType: "",
      githubName: "",
      branchName: "",
      serviceIp: "",
      fileList: [],
      pageIndex: 1,
      buildList: [],
      totalSize: 0,
      addLoadingFlag: true,
      upfileId: [],
      deleteLoading: false,
    };
  },
  mounted() {
    this.queryPublishList();
  },
  methods: {
    jumpDetail(query) {
      this.$router.push({
        path: "/PublishDetail",
        query,
      });
    },
    upfileOnChange(file, fileList) {
      console.log(fileList);
    },
    queryPublishList(pageIndex = 0) {
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      const query = {
        page_size: 20,
        page: pageIndex,
      };
      getPublishList(headers, query).then((res) => {
        const { data = {}, code } = res;
        if (code === "0") {
          this.buildList = data.data;
          this.totalSize = data.total || 1;
        }
      });
    },
    submitPublishAddTask() {
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      const params = {
        name: this.buildName,
        code: this.githubName,
        git: this.branchName[0],
        branch: this.branchName[1],
        Host: this.createModeType,
        user: JSON.parse(sessionStorage.getItem("token")),
        Project: this.project_id,
        status: true,
        file_id: this.upfileId,
      };
      submitPublishAddTaskService(headers, params).then((res) => {
        const { data = {}, msg, code } = res;
        if (code === "0") {
          this.dialogVisible = false;
          this.$message.success({
            message: msg,
            center: true,
          });
          this.queryPublishList();
        } else {
          this.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    // 获取级联 查询 分支列表
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
    // 获取服务
    getqueryGit() {
      this.listLoading = true;
      const self = this;
      const params = {
        page_size: 900,
        page: 1,
      };
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      queryGit(headers, params).then((res) => {
        self.listLoading = false;
        const { msg, code, data } = res;
        if (code === "0") {
          var json = JSON.stringify(data.data);
          this.unitList = JSON.parse(json);
        } else {
          self.$message.error({
            message: msg,
            center: true,
          });
        }
      });
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
        } else {
          self.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    submitAddTask() {
      let {
        buildName,
        createUnitType,
        createModeType,
        githubName,
        branchName,
        serviceIp,
      } = this;

      let ruler = /\r|\n|\s/g;

      buildName = buildName.replace(ruler, "");
      createUnitType = createUnitType.replace(ruler, "");
      createModeType = createModeType.replace(ruler, "");
      githubName = githubName.replace(ruler, "");
      branchName = branchName.replace(ruler, "");
      serviceIp = serviceIp.replace(ruler, "");

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
      // if (!serviceIp) {
      //     this.ModalAlert("请输入部署服务器IP！");
      //     return;
      // }
    },
    // 构建 : 停止
    handleChangeStatus: function(item) {
      let self = this;
      this.listLoading = true;
      let params = {
        build_package_id: item.id,
        project_id: this.project_id,
      };
      let headers = {
        "Content-Type": "application/json",
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      if (item.build_status) {
        PublishDisableTaskService(headers, params).then((_data) => {
          let { msg, code, data } = _data;
          self.listLoading = false;
          if (code === "0") {
            self.$message({
              message: "停止成功",
              center: true,
              type: "success",
            });
            item.build_status = !item.build_status;
            this.queryPublishList();
          } else {
            self.$message.error({
              message: msg,
              center: true,
            });
          }
        });
      } else {
        PublishEnableTaskService(headers, params).then((_data) => {
          let { msg, code, data } = _data;
          self.listLoading = false;
          if (code === "0") {
            self.$message({
              message: "构建开始",
              center: true,
              type: "success",
            });
            item.build_status = !item.build_status;
            this.queryPublishList();
          } else {
            self.$message.error({
              message: msg,
              center: true,
            });
          }
        });
      }
    },
    replaceSpace(str) {
      if (!str) return str;
      let rule = /\r|\n|\s/g;
      return str.replace(rule, "");
    },
    ModalAlert(message, type = "error") {
      this.$message({
        message,
        type,
      });
    },
    subUploadFile(data) {
      let params = new FormData();
      params.append("file", data.file);
      params.append("type", "build");
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      addupload(headers, params).then((res) => {
        const { msg, code, data } = res;
        if (code === "0") {
          const fileid = data.fileid || "";
          this.upfileId.push(fileid)
        } else {
          this.$message.error({
            message: msg,
            center: true,
          });
        }
      });
    },
    submitDelete(index, id) {
      this.$confirm("确定要删除当前构建任务?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteLoading = true;
          this.confirmDelete(index, id);
        })
        .catch(() => {});
    },
    confirmDelete(index, build_id) {
      const headers = {
        Authorization: "Token " + JSON.parse(sessionStorage.getItem("token")),
      };
      const params = {
        build_id,
      };
      submitPublishDeleteTaskService(headers, params)
        .then((res) => {
          this.startFlag = false;
          this.deleteLoading = false;
          const { code, data } = res;
          if (code === "0") {
            this.buildList.splice(index, 1);
          }
        })
        .catch((err) => {
          this.startFlag = false;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.publish {
  display: flex;
  flex-direction: column;
  flex: 1;

  .top {
    color: #333;
    padding: 0 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    &-left {
      display: flex;
    }

    &-item {
      margin-right: 15px;
      display: flex;
      align-items: center;
      justify-content: center;

      span {
        font-size: 15px;
        margin-right: 5px;
      }
    }
  }

  .con {
    padding: 0 10px;
    margin-top: 15px;
    background-color: #fff;
    border-radius: 5px;
    flex: 1;

    &-name {
      width: 230px;
    }

    &-item {
      display: flex;
      align-items: center;
      font-size: 13px;
      border-bottom: 1px solid #f0f0f0;
      min-height: 40px;
      &:hover {
        background-color: #f1f1f1;
      }
      > span {
        flex: 1;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px 0;
      }

      .operation {
        &-item {
          margin-right: 10px;
          font-size: 13px;
        }
      }

      .status {
        background-color: #97cd74;
        padding: 4px 8px;
        color: #fff;
        border-radius: 4px;
        font-size: 12px;
        &.failed {
          background-color: #f56c6c;
        }
        &.building {
          background-color: #e6a23c;
        }
      }
    }
    &-title {
      background-color: #fafafa;
      font-size: 14px;
      &:hover {
        background-color: #fafafa;
      }
      span {
        position: relative;
        font-weight: 500;

        &::after {
          position: absolute;
          right: 0;
          top: 30%;
          content: "";
          display: block;
          background-color: #ddd;
          width: 1px;
          height: 40%;
        }
        &:last-child {
          &::after {
            display: none;
          }
        }
      }
    }
  }

  .dialog {
    font-size: 15px;
    color: #333;
    width: 60%;

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
