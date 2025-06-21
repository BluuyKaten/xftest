<template>
  <div class="simple-recorder">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>实时语音识别</h3>
        </div>
      </template>

      <div class="recorder-content">
        <!-- 录音状态显示 -->
        <div class="status-display">
          <el-tag :type="recordingStatus.type" size="large">
            {{ recordingStatus.text }}
          </el-tag>
          <div v-if="isRecording" class="recording-indicator">
            <div class="pulse"></div>
            <span>正在录音...</span>
          </div>
        </div>

        <!-- 录音控制按钮 -->
        <div class="control-buttons">
          <el-button 
            type="primary" 
            size="large"
            :icon="isRecording ? 'Microphone' : 'Microphone'"
            @click="toggleRecording"
            :loading="processing"
            :disabled="!microphoneAvailable"
          >
            {{ isRecording ? '停止录音' : '开始录音' }}
          </el-button>
          
          <el-button 
            type="info" 
            size="large"
            @click="clearResults"
            :disabled="recognitionResults.length === 0"
          >
            清空结果
          </el-button>
        </div>

        <!-- 音量指示器 -->
        <div v-if="isRecording" class="volume-meter">
          <div class="volume-bar">
            <div 
              class="volume-fill" 
              :style="{ width: volumeLevel + '%' }"
            ></div>
          </div>
          <span>音量: {{ volumeLevel.toFixed(1) }}%</span>
        </div>

        <!-- 实时识别结果 -->
        <div class="results-section">
          <h4>识别结果</h4>
          <div class="results-container">
            <div 
              v-for="(result, index) in recognitionResults" 
              :key="index"
              class="result-item"
            >
              <div class="result-text">{{ result.text }}</div>
              <div class="result-time">{{ formatTime(result.timestamp) }}</div>
            </div>
            <div v-if="recognitionResults.length === 0" class="no-results">
              暂无识别结果
            </div>
          </div>
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
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'SimpleRecorder',
  setup() {
    const isRecording = ref(false)
    const processing = ref(false)
    const microphoneAvailable = ref(false)
    const volumeLevel = ref(0)
    const errorMessage = ref('')
    const recognitionResults = ref([])
    
    let mediaRecorder = null
    let audioContext = null
    let analyser = null
    let microphone = null
    let volumeInterval = null
    let recordingInterval = null

    const recordingStatus = ref({
      type: 'info',
      text: '准备就绪'
    })

    // 检查麦克风权限
    const checkMicrophonePermission = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        stream.getTracks().forEach(track => track.stop())
        microphoneAvailable.value = true
        recordingStatus.value = { type: 'success', text: '麦克风可用' }
      } catch (error) {
        console.error('麦克风权限检查失败:', error)
        microphoneAvailable.value = false
        recordingStatus.value = { type: 'danger', text: '麦克风不可用' }
        errorMessage.value = '无法访问麦克风，请检查权限设置'
      }
    }

    // 开始录音
    const startRecording = async () => {
      try {
        processing.value = true
        errorMessage.value = ''

        // 获取音频流
        const stream = await navigator.mediaDevices.getUserMedia({ 
          audio: {
            sampleRate: 16000,
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true
          } 
        })

        // 设置音频分析
        audioContext = new (window.AudioContext || window.webkitAudioContext)()
        analyser = audioContext.createAnalyser()
        microphone = audioContext.createMediaStreamSource(stream)
        microphone.connect(analyser)

        // 设置音量分析
        analyser.fftSize = 256
        const bufferLength = analyser.frequencyBinCount
        const dataArray = new Uint8Array(bufferLength)

        // 开始音量监控
        volumeInterval = setInterval(() => {
          analyser.getByteFrequencyData(dataArray)
          const average = dataArray.reduce((a, b) => a + b) / bufferLength
          volumeLevel.value = (average / 255) * 100
        }, 100)

        // 开始录音
        mediaRecorder = new MediaRecorder(stream, {
          mimeType: 'audio/webm;codecs=opus'
        })

        const audioChunks = []
        
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data)
          }
        }

        mediaRecorder.onstop = async () => {
          if (audioChunks.length > 0) {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
            await processAudioChunk(audioBlob)
          }
        }

        mediaRecorder.start()
        isRecording.value = true
        recordingStatus.value = { type: 'warning', text: '正在录音' }

        // 每5秒发送一次音频
        recordingInterval = setInterval(() => {
          if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop()
            mediaRecorder.start()
          }
        }, 5000)

      } catch (error) {
        console.error('开始录音失败:', error)
        errorMessage.value = '开始录音失败: ' + error.message
        recordingStatus.value = { type: 'danger', text: '录音失败' }
      } finally {
        processing.value = false
      }
    }

    // 停止录音
    const stopRecording = () => {
      if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop()
      }

      // 清理资源
      if (volumeInterval) {
        clearInterval(volumeInterval)
        volumeInterval = null
      }

      if (recordingInterval) {
        clearInterval(recordingInterval)
        recordingInterval = null
      }

      if (microphone) {
        microphone.disconnect()
        microphone = null
      }

      if (audioContext) {
        audioContext.close()
        audioContext = null
      }

      isRecording.value = false
      volumeLevel.value = 0
      recordingStatus.value = { type: 'success', text: '录音已停止' }
    }

    // 处理音频块
    const processAudioChunk = async (blob) => {
      try {
        // 创建FormData
        const formData = new FormData()
        formData.append('audio_file', blob, `realtime_${Date.now()}.webm`)

        // 上传音频
        const response = await fetch('/api/upload/audio', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          throw new Error('音频上传失败')
        }

        const uploadResult = await response.json()

        if (!uploadResult.success) {
          throw new Error(uploadResult.error || '音频上传失败')
        }

        // 发送语音识别请求
        const recognizeResponse = await fetch('/api/speech/recognize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            audio_file_path: uploadResult.filepath,
            user_id: 1,
            is_realtime: true
          })
        })

        if (!recognizeResponse.ok) {
          throw new Error('语音识别失败')
        }

        const recognizeResult = await recognizeResponse.json()

        if (recognizeResult.success && recognizeResult.text.trim()) {
          recognitionResults.value.push({
            text: recognizeResult.text,
            timestamp: new Date(),
            isFinal: false
          })
        }

      } catch (error) {
        console.error('处理音频块失败:', error)
        errorMessage.value = '语音识别失败: ' + error.message
      }
    }

    // 切换录音状态
    const toggleRecording = () => {
      if (isRecording.value) {
        stopRecording()
      } else {
        startRecording()
      }
    }

    // 清空结果
    const clearResults = () => {
      recognitionResults.value = []
    }

    // 格式化时间
    const formatTime = (timestamp) => {
      return timestamp.toLocaleTimeString()
    }

    // 组件挂载时检查麦克风权限
    onMounted(() => {
      checkMicrophonePermission()
    })

    // 组件卸载时清理资源
    onUnmounted(() => {
      if (isRecording.value) {
        stopRecording()
      }
    })

    return {
      isRecording,
      processing,
      microphoneAvailable,
      volumeLevel,
      errorMessage,
      recognitionResults,
      recordingStatus,
      toggleRecording,
      clearResults,
      formatTime
    }
  }
}
</script>

<style scoped>
.simple-recorder {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recorder-content {
  padding: 20px 0;
}

.status-display {
  text-align: center;
  margin-bottom: 20px;
}

.recording-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  gap: 10px;
}

.pulse {
  width: 12px;
  height: 12px;
  background-color: #f56c6c;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
}

.volume-meter {
  text-align: center;
  margin-bottom: 20px;
}

.volume-bar {
  width: 200px;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin: 0 auto 10px;
}

.volume-fill {
  height: 100%;
  background: linear-gradient(90deg, #67c23a, #e6a23c, #f56c6c);
  transition: width 0.1s ease;
}

.results-section {
  margin-top: 20px;
}

.results-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 10px;
  background-color: #fafafa;
}

.result-item {
  padding: 10px;
  margin-bottom: 10px;
  background-color: white;
  border-radius: 4px;
  border-left: 4px solid #409eff;
}

.result-text {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 5px;
}

.result-time {
  font-size: 12px;
  color: #909399;
}

.no-results {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.error-message {
  margin-top: 20px;
}
</style> 