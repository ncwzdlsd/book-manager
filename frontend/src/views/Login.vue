<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="login-title">図書館管理システムログイン</h2>
      </template>
      
      <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="0">
        <el-form-item prop="role">
          <el-radio-group v-model="loginForm.role" class="role-group">
            <el-radio label="staff">職員</el-radio>
            <el-radio label="reader">読者</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username"
            placeholder="ユーザー名を入力してください"
            prefix-icon="el-icon-user">
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password"
            type="password"
            placeholder="パスワードを入力してください"
            prefix-icon="el-icon-lock"
            show-password>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleLogin" class="login-button">ログイン</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        role: 'staff'
      },
      rules: {
        username: [
          { required: true, message: 'ユーザー名を入力してください', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'パスワードを入力してください', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '役割を選択してください', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    async handleLogin() {
      try {
        const valid = await this.$refs.loginForm.validate()
        if (!valid) return

        const response = await axios.post('http://localhost:8000/login', this.loginForm)
        
        if (response.data.success) {
          // 保存用户信息和token
          localStorage.setItem('userInfo', JSON.stringify(response.data.user))
          localStorage.setItem('token', response.data.token)
          
          // 根据角色跳转到不同页面
          if (response.data.user.role === 'staff') {
            this.$router.push('/staff/reservation')
          } else if (response.data.user.role === 'reader') {
            this.$router.push('/reader/reservation')
          }
          
          ElMessage.success('ログインに成功しました')
        } else {
          ElMessage.error(response.data.message || 'ログインに失敗しました')
        }
      } catch (error) {
        console.error('Login error:', error)
        ElMessage.error(error.response?.data?.message || 'ログインに失敗しました')
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

.login-card {
  width: 400px;
}

.login-title {
  text-align: center;
  margin: 0;
  color: #303133;
}

.role-group {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
}
</style> 