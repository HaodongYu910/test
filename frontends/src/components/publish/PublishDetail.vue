<template>
  <div class="details">
    <div class="top">
      <div class="title">
        <div class="title-left">
          <span>神外-30-test</span>
          <span class="mode">web前端</span>
          <span class="mode">
            <i class="el-icon-suitcase"></i>
            测试</span
          >
        </div>
        <div class="title-right">
          <el-button type="primary" icon="el-icon-orange">构建</el-button>
          <el-button icon="el-icon-edit">编辑</el-button>
          <el-button type="danger" icon="el-icon-delete-solid">删除</el-button>
        </div>
      </div>
      <div class="status">
        <span>状态：</span>
        <span>打包成功</span>
      </div>
    </div>
    <div class="build bg-color">
      <el-steps
        :active="stepActive"
        finish-status="success"
        class="build-step"
        align-center
      >
        <el-step
          title="更新源码"
          :icon="stepActive === 0 ? 'el-icon-loading' : 'el-icon-refresh'"
        ></el-step>
        <el-step
          title="依赖集成"
          :icon="stepActive === 1 ? 'el-icon-loading' : 'el-icon-sold-out'"
        ></el-step>
        <el-step
          title="打包"
          :icon="stepActive === 2 ? 'el-icon-loading' : 'el-icon-s-cooperation'"
        ></el-step>
        <el-step
          title="打包成功"
          :icon="stepActive === 3 ? 'el-icon-loading' : 'el-icon-finished'"
        ></el-step>
      </el-steps>
      <div class="build-title">构建历史</div>
      <div class="build-list">
        <div class="build-item build-item-title">
          <span>构建序号</span>
          <span>状态</span>
          <span>发起人</span>
          <span>开始时间</span>
          <span>操作</span>
        </div>
        <div class="build-item">
          <span>01</span>
          <span>打包成功</span>
          <span>wangguanwei</span>
          <span>07-12 12:00</span>
          <span>
            <span class="highlight">
              <i class="el-icon-reading"></i>
              查看日志
            </span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "publishDetail",
  // el-icon-loading
  data() {
    return {
      stepActive: 1,
    };
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
}
</style>
