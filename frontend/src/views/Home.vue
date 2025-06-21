<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <template #header>
            <div class="card-header">
              <h2>欢迎使用 Flask + Vue 全栈应用</h2>
            </div>
          </template>
          <div class="welcome-content">
            <p>这是一个使用 Flask 后端和 Vue.js 前端构建的现代化全栈应用。</p>
            <p>主要功能包括：</p>
            <ul>
              <li>用户管理 - 创建和管理用户账户</li>
              <li>文章管理 - 发布和管理文章内容</li>
              <li>语音识别 - 基于科大讯飞API的语音转文字功能</li>
              <li>RESTful API - 提供完整的数据接口</li>
              <li>响应式设计 - 适配各种设备屏幕</li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>API 状态</h3>
            </div>
          </template>
          <div class="api-status">
            <el-tag :type="apiStatus === 'healthy' ? 'success' : 'danger'">
              {{ apiStatus === 'healthy' ? '正常' : '异常' }}
            </el-tag>
            <p v-if="apiStatus === 'healthy'">后端API服务运行正常</p>
            <p v-else>无法连接到后端API服务</p>
            <el-button @click="checkAPIStatus" :loading="checking">
              检查状态
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>快速操作</h3>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/users')">
              用户管理
            </el-button>
            <el-button type="success" @click="$router.push('/posts')">
              文章管理
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>语音识别</h3>
            </div>
          </template>
          <div class="speech-intro">
            <p>体验科大讯飞语音识别功能</p>
            <p>支持多种音频格式转换</p>
            <el-button type="warning" @click="$router.push('/speech')">
              开始识别
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { healthAPI } from '../api'

export default {
  name: 'Home',
  data() {
    return {
      apiStatus: 'unknown',
      checking: false
    }
  },
  mounted() {
    this.checkAPIStatus()
  },
  methods: {
    async checkAPIStatus() {
      this.checking = true
      try {
        const response = await healthAPI.check()
        this.apiStatus = response.status
      } catch (error) {
        this.apiStatus = 'error'
        console.error('API状态检查失败:', error)
      } finally {
        this.checking = false
      }
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-content {
  line-height: 1.6;
}

.welcome-content ul {
  margin: 10px 0;
  padding-left: 20px;
}

.welcome-content li {
  margin: 5px 0;
}

.api-status {
  text-align: center;
}

.api-status p {
  margin: 10px 0;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.speech-intro {
  text-align: center;
}

.speech-intro p {
  margin: 10px 0;
  color: #666;
}

.el-card {
  margin-bottom: 20px;
}
</style> 