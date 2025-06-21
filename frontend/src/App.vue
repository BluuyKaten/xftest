<template>
  <div id="app">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          router
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/users">用户管理</el-menu-item>
          <el-menu-item index="/posts">文章管理</el-menu-item>
          <el-menu-item index="/speech">语音识别</el-menu-item>
        </el-menu>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer>
        <p>&copy; 2024 Flask + Vue 全栈应用</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeIndex() {
      return this.$route.path
    }
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  background-color: #409EFF;
  color: white;
  line-height: 60px;
}

.el-menu {
  background-color: transparent;
}

.el-menu-item {
  color: white !important;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.el-footer {
  background-color: #f5f5f5;
  color: #666;
  text-align: center;
  line-height: 60px;
  border-top: 1px solid #e4e7ed;
}

.el-main {
  min-height: calc(100vh - 120px);
  padding: 20px;
}
</style> 