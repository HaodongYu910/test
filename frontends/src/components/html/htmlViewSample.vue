<template>
  <div>
    <v-html-panel :url.asyc="url1"></v-html-panel>
    <v-html-panel :url.asyc="url2"></v-html-panel>
  </div>
</template>
<script>
  export default{
    data () {
      return {
        url1: '',
        url2: ''
      }
    },
    mounted () {
      this.url1 = 'http://file.xxx.com/group1/M00/0C/F5/xxxxxxxx.html'
      this.url2 = 'http://file.xxx.com/group1/M00/0D/3B/yyyyyyy.html'
    },
    methods: {
    }
  }
</script>

<style scoped>

</style>