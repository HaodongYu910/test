(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d20ec22"],{b174:function(t,a,e){"use strict";e.r(a);var i=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("el-row",{staticClass:"dynamic-manage"},[e("el-col",{attrs:{span:24}},[e("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],staticStyle:{width:"100%"},attrs:{data:t.tableData,stripe:""}},[e("el-table-column",{attrs:{type:"index",label:"#","min-width":"10%"}}),e("el-table-column",{attrs:{prop:"time",label:"操作时间","min-width":"13%"}}),e("el-table-column",{attrs:{prop:"user",label:"操作人","min-width":"15%"}}),e("el-table-column",{attrs:{prop:"description",label:"描述","min-width":"47%"}})],1),e("el-pagination",{staticStyle:{float:"right"},attrs:{layout:"prev, pager, next","page-size":20,"page-count":t.total},on:{"current-change":t.handleCurrentChange}})],1)],1)},n=[],s=e("2d92"),l=e("1157"),o=e.n(l),r={data(){return{tableData:[],total:0,page:1,listLoading:!1}},methods:{handleCurrentChange(t){this.page=t,this.getApiDynamic()},getApiDynamic(){this.listLoading=!0;let t=this;o.a.ajax({type:"get",url:s["mb"]+"/api/api/operation_history",async:!0,data:{project_id:this.$route.params.project_id,page:t.page,api_id:this.$route.params.api_id},headers:{Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))},timeout:5e3,success:function(a){t.listLoading=!1,"0"===a.code?(t.total=a.data.total,t.tableData=a.data.data):t.$message.error({message:a.msg,center:!0})}})}},mounted(){this.getApiDynamic()}},p=r,d=e("2877"),c=Object(d["a"])(p,i,n,!1,null,"df36a5dc",null);a["default"]=c.exports}}]);