<template>
  <div class="users">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h2>用户管理</h2>
              <el-button type="primary" @click="showCreateDialog = true">
                添加用户
              </el-button>
            </div>
          </template>

          <el-table :data="users" v-loading="loading" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="created_at" label="创建时间">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 创建用户对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="创建新用户"
      width="500px"
    >
      <el-form
        ref="createFormRef"
        :model="createForm"
        :rules="createRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="createForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="createForm.email" placeholder="请输入邮箱" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="createUser" :loading="creating">
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { userAPI } from '../api'

export default {
  name: 'Users',
  data() {
    return {
      users: [],
      loading: false,
      creating: false,
      showCreateDialog: false,
      createForm: {
        username: '',
        email: ''
      },
      createRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loading = true
      try {
        this.users = await userAPI.getUsers()
      } catch (error) {
        this.$message.error('加载用户列表失败')
        console.error('加载用户失败:', error)
      } finally {
        this.loading = false
      }
    },
    async createUser() {
      const formRef = this.$refs.createFormRef
      if (!formRef) return

      try {
        await formRef.validate()
        this.creating = true
        
        await userAPI.createUser(this.createForm)
        this.$message.success('用户创建成功')
        this.showCreateDialog = false
        this.createForm = { username: '', email: '' }
        this.loadUsers()
      } catch (error) {
        if (error.response?.data?.error) {
          this.$message.error(error.response.data.error)
        } else {
          this.$message.error('创建用户失败')
        }
        console.error('创建用户失败:', error)
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
.users {
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