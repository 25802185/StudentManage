<template>
  <div class="login-container">
    <!-- 左侧：登录卡片 -->
    <div class="login-left">
      <div class="login-card">
        <div class="login-logo">
          <img src="../assets/logo.png" alt="Logo" class="logo-img" />
        </div>
        <h2 class="login-title">学生信息管理系统</h2>
        <p class="login-subtitle">Student Information Management System</p>
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

    <!-- 右侧：装饰图 -->
    <div class="login-right">
      <img src="../assets/login-bg.png" alt="Decor" class="decor-img" />
      <div class="right-text">
        <h3>欢迎使用学生信息管理系统</h3>
        <p>高效管理 · 智能分析 · 便捷操作</p>
      </div>
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
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.login-left {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f0f2f5;
}

.login-card {
  width: 420px;
  padding: 50px 40px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
}

.login-logo {
  text-align: center;
  margin-bottom: 16px;
}

.logo-img {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.login-title {
  text-align: center;
  font-size: 22px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 6px 0;
}

.login-subtitle {
  text-align: center;
  font-size: 12px;
  color: #909399;
  margin: 0 0 36px 0;
}

.login-form {
  width: 100%;
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

.login-right {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e8f4fd 0%, #d6eaf8 50%, #e8f0fe 100%);
  position: relative;
  overflow: hidden;
}

.decor-img {
  width: 85%;
  max-width: 600px;
  object-fit: contain;
  z-index: 1;
}

.right-text {
  position: absolute;
  bottom: 60px;
  text-align: center;
  z-index: 2;
}

.right-text h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2c6fbb;
  margin: 0 0 8px 0;
}

.right-text p {
  font-size: 14px;
  color: #5a9fd4;
  margin: 0;
  letter-spacing: 2px;
}
</style>
