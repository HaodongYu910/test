<template>
  <div>
    <aside>
      <a href="http://192.168.2.22:3000/" target="_blank">性能监控</a>
    </aside>
    <div class="container">
      <div class="form-box">
        <el-form ref="form" :model="form" status-icon :rules="rules" label-width="150px">
          <el-form-item label="Server-AET" prop="aet">
            <el-col :span="4">
              <el-input id="aet" v-model="form.aet" />
            </el-col>
          </el-form-item>
          <el-form-item label="测试环境" prop="environment">
            <el-select v-model="form.environment" clearable placeholder="请选择">
              <el-option key="192.168.1.208" label="208" value="192.168.1.208" />
              <el-option key="192.168.1.122" label="122" value="192.168.1.122" />
            </el-select>
          </el-form-item>
          <el-form-item label="推送端" prop="app">
            <el-select v-model="form.app" clearable placeholder="请选择" @change="changeLang('form')">
              <el-option key="bishijie" label="Boimind" value="bishijie" />
              <el-option key="coinness" label="coinness" value="coinness" />
            </el-select>
          </el-form-item>

          <el-form-item label="推送类型" prop="moudle">
            <el-checkbox-group v-model="form.moudle">
              <el-checkbox
                v-for="(item,index) in moudles"
                :key="item.key"
                name="moudle"
                :label="item.value"
                :value="item.key"
              />

            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="选择语言" prop="languages">
            <el-select v-model="form.languages" placeholder="请选择">
              <el-option
                v-for="(item,index) in languages"
                :key="item.key"
                :label="item.value"
                :value="item.key"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit('form')">确定推送</el-button>
            <el-button @click="resetForm('form')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

  </div>
</template>

<script>
import { pushTool } from '../../router/api'
import { delete_patients } from '../../router/api'

export default {
  name: 'Baseform',
  data: function() {
    return {
      types: [
        {
          value: 'test',
          label: 'Boimind',
          children: [
            {
              value: 'test',
              label: 'test'
            },
            {
              value: 'test',
              label: 'test'
            },
            {
              value: 'test',
              label: 'test'
            },
            {
              value: 'monitor',
              label: 'monitor'
            }
          ]
        },
        {
          value: 'coinness',
          label: 'coinness',
          children: [
            {
              value: 'monitor',
              label: 'monitor'
            },
            {
              value: 'monitor',
              label: 'monitor'
            },
            {
              value: 'monitor',
              label: 'monitor'
            }
          ]
        }
      ],
      languages: [
        { key: 'zh_cn', value: '简体中文' },
        { key: 'zh_tw', value: '繁体' }
      ],
      form: {
        aet: '',
        environment: '',
        types: [],
        languages: [],
        app: 'monitor',
        moudle: []
      },
      rules: {
        aet: [
          { required: true, message: '请输入Server-AET', trigger: 'blur' }
        ],
        environment: [
          { required: true, message: '请选择环境', trigger: 'blur' }
        ],
        moudle: [
          { required: true, message: '请添加推送类型', trigger: 'blur' }
        ],
        languages: [
          { required: true, message: '请选择语言', trigger: 'blur' }
        ],
        app: [
          { required: true, message: '请选择推送端', trigger: 'blur' }
        ]
      },
      system: '',
      moudles: [
        { key: 'news', value: '快讯' },
        { key: 'shendu', value: '深度' },
        { key: 'apply', value: '币圈' },
        { key: 'monitor', value: '盯盘' }
      ]

    }
  },
  methods: {
    /* onSubmit(formName) {
           this.$refs[formName].validate((valid)=>{
               if(valid){
                   console.logs("语言："+this.form.languages);
                   console.logs("aet："+this.form.aet);
                   console.logs("APP："+this.form.types[0]);
                   console.logs("推送类型："+this.form.types[1]);
                   console.logs("environment："+this.form.environment);
                   this.$ajax.post('/bishijie/push',{
                       id:this.form.aet,
                       service:this.form.environment,
                       system:this.form.types[0],
                       module:this.form.types[1],
                       lang:this.form.languages,
                       rid:''
                   }).then((response) => {
                       if(response.data.code!='0'){
                           this.$message.error(response.data.msg);
                           return;
                       }
                       if(response.data.data!=null&&!response.data.data[0]){
                           this.$message.error(response.data.data[1]);
                           return;
                       }
                       this.$message.success('push成功！');
               }).catch(function(response) {
                   console.logs(response); //发生错误时执行的代码
               });

           }else{
               console.logs('error submit');
               return false;
           }
       });
       },*/
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const params = {
            id: this.form.aet,
            service: this.form.environment,
            system: this.form.app,
            module: this.form.moudle,
            lang: this.form.languages,
            rid: ''
          }
          const headers = {
            'Content-Type': 'application/json'
          }
          pushTool(headers, params).then(_data => {
            const { msg, code, data } = _data
            if (code != '0') {
              this.$message.error(msg)
              return
            }
            if (data != null && !data[0]) {
              this.$message.error(data[1])
              return
            }
            this.$message.success('push成功！')
          })
        } else {
          console.log('error submit')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    changeLang(formName) {
      this.languages = []
      this.moudles = []
      this.form.moudle = []
      this.form.languages = ''
      var lan_bishijie = [
        { key: 'zh_cn', value: '简体中文' },
        { key: 'zh_tw', value: '繁体' }]
      var lan_coniness = [
        { key: 'zh_cn', value: '简体中文' },
        { key: 'zh_tw', value: '繁体' },
        { key: 'en_gb', value: 'English' },
        { key: 'ko_kr', value: '한글' }]
      var moudles_test = [
        { key: 'news', value: '快讯' },
        { key: 'shendu', value: '深度' },
        { key: 'apply', value: '币圈' },
        { key: 'monitor', value: '盯盘' }
      ]
      var moudles_coinness = [
        { key: 'news', value: '快讯' },
        { key: 'shendu', value: '深度' },
        { key: 'monitor', value: '盯盘' }
      ]
      var type = this.form.app.toLowerCase()
      if (type == 'bishijie') {
        this.languages = lan_bishijie
        this.moudles = moudles_test
      } else if (type == 'coinness') {
        this.languages = lan_coniness
        this.moudles = moudles_coinness
        console.log(this.modules)
      }
    }
  }
}
</script>
<style scoped>
  <
  style >
  .el-input__inner, #aet {
    height: 10px;
  }
</style>

<!--<template>-->
<!--  <div class="components-container">-->
<!--    <el-drag-select v-model="value" style="width:250px;" multiple placeholder="请选择">-->
<!--      <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />-->
<!--    </el-drag-select>-->
<!--    <el-drag-select v-model="value" style="width:250px;" multiple placeholder="请选择">-->
<!--      <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />-->
<!--    </el-drag-select>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import ElDragSelect from '@/components/DragSelect' // base on element-ui-->

<!--export default {-->
<!--  name: 'DragSelectDemo',-->
<!--  components: { ElDragSelect },-->
<!--  data() {-->
<!--    return {-->
<!--      value: ['Apple', 'Banana', 'Orange'],-->
<!--      options: [{-->
<!--        value: 'Apple',-->
<!--        label: 'Apple'-->
<!--      }, {-->
<!--        value: 'Banana',-->
<!--        label: 'Banana'-->
<!--      }, {-->
<!--        value: 'Orange',-->
<!--        label: 'Orange'-->
<!--      }, {-->
<!--        value: 'Pear',-->
<!--        label: 'Pear'-->
<!--      }, {-->
<!--        value: 'Strawberry',-->
<!--        label: 'Strawberry'-->
<!--      }]-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->
