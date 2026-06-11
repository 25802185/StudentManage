<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <!-- 顶部品牌区 -->
      <div class="sidebar-brand">
        <div class="brand-icon">
          <el-icon :size="22"><Notebook /></el-icon>
        </div>
        <div class="brand-text">
          <span class="brand-name">学生管理系统</span>
          <span class="brand-sub">Student Management</span>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in menus"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <span class="nav-indicator"></span>
          <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
          <span class="nav-label">{{ item.title }}</span>
        </router-link>
      </nav>

      <!-- 底部用户/版权区 -->
      <div class="sidebar-footer">
        <div class="footer-divider"></div>
        <div class="footer-user">
          <el-avatar :size="28" class="footer-avatar">
            {{ (userStore.userInfo?.name || userStore.userInfo?.username || '').charAt(0) }}
          </el-avatar>
          <span class="footer-name">{{ userStore.userInfo?.name || userStore.userInfo?.username }}</span>
        </div>
      </div>
    </el-aside>

    <el-container>
      <el-header class="header">
        <span class="page-title">{{ $route.meta.title }}</span>
        <el-dropdown @command="handleCommand" class="user-dropdown">
          <span class="user-info">
            <el-avatar :size="32" class="user-avatar">
              {{ (userStore.userInfo?.name || userStore.userInfo?.username || '').charAt(0) }}
            </el-avatar>
            <span class="user-name">{{ userStore.userInfo?.name || userStore.userInfo?.username }}</span>
            <el-icon class="user-arrow"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>个人信息
              </el-dropdown-item>
              <el-dropdown-item command="password">
                <el-icon><Lock /></el-icon>修改密码
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided>
                <el-icon><SwitchButton /></el-icon>退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { menuConfig } from '../utils/permission'

const router = useRouter()
const userStore = useUserStore()

const menus = computed(() => {
  const role = userStore.userInfo?.role
  return menuConfig[role] || []
})

const handleCommand = async (cmd) => {
  if (cmd === 'profile') router.push('/profile')
  else if (cmd === 'password') router.push('/change-password')
  else if (cmd === 'logout') {
    await userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

/* ===== 侧边栏 ===== */
.sidebar {
  background: linear-gradient(180deg, #3a4f63 0%, #5a7a94 45%, #7a9ab4 100%);
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.08);
}

.sidebar::-webkit-scrollbar {
  width: 0;
}

/* ===== 品牌区 ===== */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 22px 20px 20px;
  flex-shrink: 0;
}

.brand-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #6388a0 0%, #b7d9c8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(99, 136, 160, 0.4);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-name {
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.5px;
  line-height: 1.3;
}

.brand-sub {
  color: rgba(255, 255, 255, 0.45);
  font-size: 10px;
  letter-spacing: 0.3px;
  margin-top: 2px;
}

/* ===== 导航菜单 ===== */
.sidebar-nav {
  flex: 1;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  height: 42px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.58);
  text-decoration: none;
  font-size: 13.5px;
  transition: all 0.2s ease;
}

.nav-item:hover {
  color: rgba(255, 255, 255, 0.92);
  background: rgba(255, 255, 255, 0.08);
}

.nav-item.active {
  color: #fff;
  background: rgba(183, 217, 200, 0.15);
}

/* 左侧薄荷绿高亮竖线 */
.nav-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 3px;
  height: 18px;
  border-radius: 0 3px 3px 0;
  background: #b7d9c8;
  transition: transform 0.25s ease;
}

.nav-item.active .nav-indicator {
  transform: translateY(-50%) scaleY(1);
}

.nav-icon {
  font-size: 17px;
  flex-shrink: 0;
}

.nav-label {
  font-weight: 400;
  white-space: nowrap;
}

.nav-item.active .nav-label {
  font-weight: 500;
}

/* ===== 底部区域 ===== */
.sidebar-footer {
  padding: 0 16px 16px;
  flex-shrink: 0;
}

.footer-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin-bottom: 14px;
}

.footer-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 4px;
}

.footer-avatar {
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  font-weight: 600;
}

.footer-name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

/* ===== Header ===== */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 28px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}

.page-title {
  font-size: 15px;
  font-weight: 600;
  color: #3a4f63;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 10px;
  border-radius: 8px;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f5f6fa;
}

.user-avatar {
  background: linear-gradient(135deg, #6388a0 0%, #b7d9c8 100%);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
}

.user-name {
  font-size: 13px;
  color: #555;
  font-weight: 500;
}

.user-arrow {
  font-size: 11px;
  color: #aaa;
}

/* ===== 主内容区 ===== */
.main-content {
  background: #f5f6fa;
  padding: 20px;
  overflow-y: auto;
}
</style>
