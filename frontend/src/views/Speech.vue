<template>
  <div class="speech">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 文件上传识别标签页 -->
      <el-tab-pane label="文件上传识别" name="file">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-card>
              <template #header>
                <div class="card-header">
                  <h2>音频文件识别</h2>
                </div>
              </template>

              <div class="speech-content">
                <!-- 音频文件上传 -->
                <el-upload
                  class="upload-demo"
                  drag
                  action="#"
                  :auto-upload="false"
                  :on-change="handleFileChange"
                  :show-file-list="false"
                  accept=".wav,.mp3,.m4a,.aac,.flac"
                >
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">
                    将音频文件拖到此处，或<em>点击上传</em>
                  </div>
                  <template #tip>
                    <div class="el-upload__tip">
                      支持 wav、mp3、m4a、aac、flac 格式的音频文件
                    </div>
                  </template>
                </el-upload>

                <!-- 已选择的文件 -->
                <div v-if="selectedFile" class="selected-file">
                  <el-alert
                    :title="`已选择文件: ${selectedFile.name}`"
                    type="info"
                    :closable="false"
                    show-icon
                  />
                  <el-button 
                    type="primary" 
                    @click="uploadAndRecognize" 
                    :loading="processing"
                    style="margin-top: 10px;"
                  >
                    上传并识别
                  </el-button>
                </div>

                <!-- 识别结果 -->
                <div v-if="recognitionResult" class="recognition-result">
                  <el-divider content-position="left">识别结果</el-divider>
                  <el-card class="result-card">
                    <div class="result-text">{{ recognitionResult.text }}</div>
                    <div class="result-meta">
                      <el-tag :type="recognitionResult.success ? 'success' : 'danger'">
                        {{ recognitionResult.success ? '识别成功' : '识别失败' }}
                      </el-tag>
                      <span v-if="recognitionResult.record_id" class="record-id">
                        记录ID: {{ recognitionResult.record_id }}
                      </span>
                    </div>
                  </el-card>
                </div>

                <!-- 错误信息 -->
                <div v-if="errorMessage" class="error-message">
                  <el-alert
                    :title="errorMessage"
                    type="error"
                    :closable="false"
                    show-icon
                  />
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <!-- 实时录音识别标签页 -->
      <el-tab-pane label="实时录音识别" name="realtime">
        <SimpleRecorder />
      </el-tab-pane>
    </el-tabs>

    <!-- 历史记录 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>识别历史</h3>
              <el-button @click="loadSpeechRecords" :loading="loadingRecords">
                刷新
              </el-button>
            </div>
          </template>

          <el-table :data="speechRecords" v-loading="loadingRecords" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="audio_file" label="音频文件" />
            <el-table-column prop="recognized_text" label="识别文本" show-overflow-tooltip />
            <el-table-column prop="user_id" label="用户ID" width="100" />
            <el-table-column prop="created_at" label="识别时间">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button 
                  size="small" 
                  @click="viewRecord(scope.row)"
                >
                  查看
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 查看记录详情对话框 -->
    <el-dialog
      v-model="showRecordDialog"
      title="识别记录详情"
      width="600px"
    >
      <div v-if="selectedRecord">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="记录ID">{{ selectedRecord.id }}</el-descriptions-item>
          <el-descriptions-item label="音频文件">{{ selectedRecord.audio_file }}</el-descriptions-item>
          <el-descriptions-item label="识别文本">{{ selectedRecord.recognized_text }}</el-descriptions-item>
          <el-descriptions-item label="用户ID">{{ selectedRecord.user_id || '未指定' }}</el-descriptions-item>
          <el-descriptions-item label="识别时间">{{ formatDate(selectedRecord.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { UploadFilled } from '@element-plus/icons-vue'
import { speechAPI } from '../api'
import axios from 'axios'
import SimpleRecorder from '../components/SimpleRecorder.vue'

export default {
  name: 'Speech',
  components: {
    UploadFilled,
    SimpleRecorder
  },
  data() {
    return {
      activeTab: 'file',
      selectedFile: null,
      processing: false,
      recognitionResult: null,
      errorMessage: '',
      speechRecords: [],
      loadingRecords: false,
      showRecordDialog: false,
      selectedRecord: null
    }
  },
  mounted() {
    this.loadSpeechRecords()
  },
  methods: {
    handleFileChange(file) {
      this.selectedFile = file.raw
      this.recognitionResult = null
      this.errorMessage = ''
    },
    async uploadAndRecognize() {
      if (!this.selectedFile) {
        this.$message.warning('请先选择音频文件')
        return
      }

      this.processing = true
      this.errorMessage = ''
      
      try {
        // 第一步：上传文件
        const formData = new FormData()
        formData.append('audio_file', this.selectedFile)
        
        console.log('开始上传文件:', this.selectedFile.name)
        
        const uploadResponse = await axios.post('/api/upload/audio', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        console.log('文件上传响应:', uploadResponse.data)
        
        if (!uploadResponse.data.success) {
          throw new Error(uploadResponse.data.error || '文件上传失败')
        }
        
        // 第二步：语音识别
        const recognizeData = {
          audio_file_path: uploadResponse.data.filepath,
          user_id: 1 // 可以从用户登录状态获取
        }
        
        console.log('发送语音识别请求:', recognizeData)
        
        const result = await speechAPI.recognize(recognizeData)
        
        console.log('语音识别响应:', result)
        
        this.recognitionResult = result
        if (result.success) {
          this.$message.success('语音识别成功')
          this.loadSpeechRecords() // 刷新历史记录
        } else {
          this.errorMessage = result.error
        }
      } catch (error) {
        console.error('详细错误信息:', error)
        console.error('错误响应数据:', error.response?.data)
        this.errorMessage = error.response?.data?.error || error.message || '处理失败'
        console.error('处理失败:', error)
      } finally {
        this.processing = false
      }
    },
    async loadSpeechRecords() {
      this.loadingRecords = true
      try {
        this.speechRecords = await speechAPI.getRecords()
      } catch (error) {
        this.$message.error('加载历史记录失败')
        console.error('加载历史记录失败:', error)
      } finally {
        this.loadingRecords = false
      }
    },
    viewRecord(record) {
      this.selectedRecord = record
      this.showRecordDialog = true
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.speech {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.speech-content {
  padding: 20px 0;
}

.selected-file {
  margin-top: 20px;
}

.recognition-result {
  margin-top: 20px;
}

.result-card {
  background-color: #f8f9fa;
}

.result-text {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 10px;
  padding: 10px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.result-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-id {
  color: #909399;
  font-size: 14px;
}

.error-message {
  margin-top: 20px;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 7px;
}
</style> 