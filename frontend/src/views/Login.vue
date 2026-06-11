<template>
  <div class="login-container">
    <!-- 背景图 -->
    <img src="../assets/login-bg.png" alt="" class="bg-img" />

    <!-- 动态粒子背景 -->
    <div class="particles">
      <div v-for="i in 12" :key="i" class="particle" :style="particleStyle(i)"></div>
    </div>

    <!-- 浮动光晕 -->
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>

    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- 浮动 Logo -->
      <div class="card-header">
        <div class="logo-float">
          <img src="../assets/logo.png" alt="Logo" class="card-logo" />
          <div class="logo-shadow"></div>
        </div>
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

      <!-- 卡片底部装饰线 -->
      <div class="card-deco-line"></div>
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

const particleStyle = (i) => ({
  '--delay': `${(i * 1.3) % 6}s`,
  '--x': `${(i * 17) % 100}%`,
  '--y': `${(i * 23) % 100}%`,
  '--size': `${3 + (i % 4) * 2}px`,
  '--duration': `${4 + (i % 3) * 2}s`,
})

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
  background: #e8f4fd;
}

.bg-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ========== 动态粒子 ========== */
.particles {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.particle {
  position: absolute;
  left: var(--x);
  top: var(--y);
  width: var(--size);
  height: var(--size);
  background: rgba(74, 158, 255, 0.4);
  border-radius: 50%;
  animation: particleFloat var(--duration) ease-in-out var(--delay) infinite alternate;
}

@keyframes particleFloat {
  0% { transform: translate(0, 0) scale(1); opacity: 0.3; }
  100% { transform: translate(20px, -30px) scale(1.5); opacity: 0.7; }
}

/* ========== 浮动光晕 ========== */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 1;
  pointer-events: none;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: rgba(74, 158, 255, 0.15);
  top: -100px;
  right: 10%;
  animation: glowDrift 8s ease-in-out infinite alternate;
}

.glow-2 {
  width: 300px;
  height: 300px;
  background: rgba(45, 130, 236, 0.12);
  bottom: -80px;
  left: 15%;
  animation: glowDrift 10s ease-in-out 2s infinite alternate;
}

.glow-3 {
  width: 200px;
  height: 200px;
  background: rgba(120, 180, 255, 0.1);
  top: 40%;
  left: 5%;
  animation: glowDrift 7s ease-in-out 1s infinite alternate;
}

@keyframes glowDrift {
  0% { transform: translate(0, 0); }
  100% { transform: translate(30px, -20px); }
}

/* ========== 登录卡片 ========== */
.login-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  padding: 44px 40px 36px;
  background: rgba(255, 255, 255, 0.82);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow:
    0 20px 60px rgba(45, 100, 180, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.3) inset;
  backdrop-filter: blur(16px);
  z-index: 10;
  animation: cardFadeIn 0.8s ease-out;
}

@keyframes cardFadeIn {
  from { opacity: 0; transform: translate(-50%, -48%); }
  to { opacity: 1; transform: translate(-50%, -50%); }
}

/* ========== 浮动 Logo ========== */
.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-float {
  position: relative;
  display: inline-block;
  margin-bottom: 14px;
}

.card-logo {
  width: 68px;
  height: 68px;
  object-fit: contain;
  animation: logoFloat 3s ease-in-out infinite;
}

.logo-shadow {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 8px;
  background: rgba(45, 120, 200, 0.15);
  border-radius: 50%;
  animation: shadowPulse 3s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@keyframes shadowPulse {
  0%, 100% { transform: translateX(-50%) scale(1); opacity: 0.4; }
  50% { transform: translateX(-50%) scale(0.85); opacity: 0.2; }
}

.card-title {
  font-size: 21px;
  font-weight: 600;
  color: #1a3a5c;
  margin: 0 0 6px 0;
}

.card-subtitle {
  font-size: 11px;
  color: #6a9fc8;
  margin: 0;
  letter-spacing: 1px;
}

/* ========== 表单 ========== */
.login-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 0 0 1px #d4e6f6 inset;
  background: rgba(255, 255, 255, 0.7);
  transition: all 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #4a9eff inset;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(74, 158, 255, 0.4) inset;
}

.login-btn {
  width: 100%;
  height: 46px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 6px;
  background: linear-gradient(135deg, #4a9eff 0%, #2b7de9 100%);
  border: none;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.login-btn:hover {
  background: linear-gradient(135deg, #6db3ff 0%, #4a9eff 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(45, 130, 236, 0.35);
}

.login-btn:active {
  transform: translateY(0);
}

/* ========== 卡片底部装饰线 ========== */
.card-deco-line {
  margin-top: 20px;
  height: 3px;
  border-radius: 2px;
  background: linear-gradient(90deg, transparent, #4a9eff, #2b7de9, transparent);
  opacity: 0.5;
}
</style>
