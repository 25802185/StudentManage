<template>
  <div class="login-container">
    <!-- 背景图 -->
    <img src="../assets/login-bg.png" alt="" class="bg-img" />

    <!-- 登录卡片放在右侧空白区域 -->
    <div class="login-card">
      <div class="card-header">
        <img src="../assets/logo.png" alt="Logo" class="card-logo" />
        <h2 class="card-title">学生信息管理系统</h2>
        <p class="card-subtitle">Student Information Management System</p>
      </div>
      <el-form :model="form" @submit.prevent="handleLogin" class="login-form">
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="请输入账号"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            class="login-btn"
            :loading="loading"
            native-type="submit"
            size="large"
          >
            登 录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    router.push('/')
  } catch {
    ElMessage.error('登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #e8f0fe;
}

.bg-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: left center;
}

.login-card {
  position: absolute;
  right: 8%;
  top: 50%;
  transform: translateY(-50%);
  width: 380px;
  padding: 40px 36px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(10px);
}

.card-header {
  text-align: center;
  margin-bottom: 30px;
}

.card-logo {
  width: 64px;
  height: 64px;
  object-fit: contain;
  margin-bottom: 12px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 6px 0;
}

.card-subtitle {
  font-size: 11px;
  color: #909399;
  margin: 0;
  letter-spacing: 1px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 8px;
}

.login-btn {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #409eff 0%, #337ecc 100%);
  border: none;
}

.login-btn:hover {
  background: linear-gradient(135deg, #66b1ff 0%, #409eff 100%);
}
</style>
