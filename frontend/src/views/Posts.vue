<template>
  <div class="posts">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h2>文章管理</h2>
              <el-button type="primary" @click="showCreateDialog = true">
                发布文章
              </el-button>
            </div>
          </template>

          <el-table :data="posts" v-loading="loading" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="content" label="内容" show-overflow-tooltip />
            <el-table-column prop="author_id" label="作者ID" width="100" />
            <el-table-column prop="created_at" label="发布时间">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 创建文章对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="发布新文章"
      width="600px"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="createForm.title" placeholder="请输入文章标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="createForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入文章内容"
          />
        </el-form-item>
        <el-form-item label="作者" prop="author_id">
          <el-select v-model="createForm.author_id" placeholder="请选择作者">
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="createPost" :loading="creating">
            发布
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { postAPI, userAPI } from '../api'

export default {
  name: 'Posts',
  data() {
    return {
      posts: [],
      users: [],
      loading: false,
      creating: false,
      showCreateDialog: false,
      createForm: {
        title: '',
        content: '',
        author_id: ''
      },
      createRules: {
        title: [
          { required: true, message: '请输入文章标题', trigger: 'blur' },
          { min: 1, max: 200, message: '长度在 1 到 200 个字符', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入文章内容', trigger: 'blur' }
        ],
        author_id: [
          { required: true, message: '请选择作者', trigger: 'change' }
        ]
      }
    }
  },
  mounted() {
    this.loadPosts()
    this.loadUsers()
  },
  methods: {
    async loadPosts() {
      this.loading = true
      try {
        this.posts = await postAPI.getPosts()
      } catch (error) {
        this.$message.error('加载文章列表失败')
        console.error('加载文章失败:', error)
      } finally {
        this.loading = false
      }
    },
    async loadUsers() {
      try {
        this.users = await userAPI.getUsers()
      } catch (error) {
        console.error('加载用户列表失败:', error)
      }
    },
    async createPost() {
      const formRef = this.$refs.createFormRef
      if (!formRef) return

      try {
        await formRef.validate()
        this.creating = true
        
        await postAPI.createPost(this.createForm)
        this.$message.success('文章发布成功')
        this.showCreateDialog = false
        this.createForm = { title: '', content: '', author_id: '' }
        this.loadPosts()
      } catch (error) {
        if (error.response?.data?.error) {
          this.$message.error(error.response.data.error)
        } else {
          this.$message.error('发布文章失败')
        }
        console.error('发布文章失败:', error)
      } finally {
        this.creating = false
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.posts {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 