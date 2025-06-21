import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 用户相关API
export const userAPI = {
  getUsers() {
    return api.get('/users')
  },
  createUser(userData) {
    return api.post('/users', userData)
  }
}

// 文章相关API
export const postAPI = {
  getPosts() {
    return api.get('/posts')
  },
  createPost(postData) {
    return api.post('/posts', postData)
  }
}

// 语音识别相关API
export const speechAPI = {
  recognize(data) {
    return api.post('/speech/recognize', data)
  },
  getRecords() {
    return api.get('/speech/records')
  },
  getRecord(recordId) {
    return api.get(`/speech/records/${recordId}`)
  }
}

// 健康检查API
export const healthAPI = {
  check() {
    return api.get('/health')
  }
}

export default api 