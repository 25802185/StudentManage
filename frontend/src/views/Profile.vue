<template>
  <div class="page-container">
    <div class="profile-card" v-if="profile">
      <div class="profile-header">
        <el-avatar :size="64" class="profile-avatar">
          {{ profile.name?.charAt(0) }}
        </el-avatar>
        <div class="profile-info">
          <h2>{{ profile.name }}</h2>
          <p>{{ userStore.userInfo?.username }} | {{ roleMap[userStore.userInfo?.role] }}</p>
        </div>
      </div>

      <el-form :model="profile" label-width="80px" class="profile-form">
        <el-form-item label="姓名"><el-input v-model="profile.name" :disabled="!canEdit" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="profile.gender" :disabled="!canEdit">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="profile.phone" :disabled="!canEdit" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="profile.email" :disabled="!canEdit" /></el-form-item>
        <el-form-item label="地址" v-if="userStore.userInfo?.role === 'student'">
          <el-input v-model="profile.address" :disabled="!canEdit" />
        </el-form-item>
        <el-form-item v-if="canEdit">
          <el-button class="btn-submit" @click="handleSubmit">保存修改</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="profile-card" v-else-if="userStore.userInfo?.role === 'admin'">
      <div class="profile-header">
        <el-avatar :size="64" class="profile-avatar">
          {{ userStore.userInfo?.username?.charAt(0) }}
        </el-avatar>
        <div class="profile-info">
          <h2>{{ userStore.userInfo?.username }}</h2>
          <p>管理员</p>
        </div>
      </div>
      <p style="color: #999; font-size: 13px;">管理员账号无个人信息，请在用户管理中操作。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import request from '../api'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const profile = ref(null)
const originalProfile = ref(null)
const roleMap = { admin: '管理员', teacher: '教师', student: '学生' }

const canEdit = computed(() => userStore.userInfo?.role !== 'admin')

onMounted(async () => {
  const role = userStore.userInfo?.role
  if (role === 'student') {
    const data = await request.get('/students/my-info/')
    if (data) {
      profile.value = { ...data }
      originalProfile.value = { phone: data.phone, email: data.email, address: data.address }
    }
  } else if (role === 'teacher' && userStore.userInfo?.teacher_no) {
    const data = await request.get('/teachers/', { params: { search: userStore.userInfo.teacher_no } })
    if (data.results?.length) {
      profile.value = data.results[0]
      originalProfile.value = { phone: data.results[0].phone, email: data.results[0].email }
    }
  }
})

const handleSubmit = async () => {
  const role = userStore.userInfo?.role
  if (role === 'student') {
    // 学生直接通过 my-info 接口修改电话、邮箱、地址
    const changed = {}
    for (const field of ['phone', 'email', 'address']) {
      if (profile.value[field] !== originalProfile.value[field]) {
        changed[field] = profile.value[field]
      }
    }
    if (!Object.keys(changed).length) {
      ElMessage.warning('未修改任何信息')
      return
    }
    await request.put('/students/my-info/', changed)
    originalProfile.value = { phone: profile.value.phone, email: profile.value.email, address: profile.value.address }
    ElMessage.success('修改成功')
  } else if (role === 'teacher') {
    await request.put(`/teachers/${profile.value.id}/`, profile.value)
    ElMessage.success('修改成功')
  }
}
</script>

<style scoped>
.page-container { max-width: 640px; }

.profile-card {
  background: #fff; border-radius: 14px; padding: 28px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.045);
}

.profile-header {
  display: flex; align-items: center; gap: 18px;
  padding-bottom: 24px; border-bottom: 1px solid #f0f0f0; margin-bottom: 24px;
}

.profile-avatar {
  background: linear-gradient(135deg, #6388a0, #b7d9c8);
  color: #fff; font-size: 24px; font-weight: 600;
}

.profile-info h2 { font-size: 20px; font-weight: 600; color: #3a4f63; margin: 0; }
.profile-info p { font-size: 13px; color: #999; margin-top: 4px; }

.profile-form :deep(.el-input__wrapper) { border-radius: 8px; }
.profile-form :deep(.el-select .el-input__wrapper) { border-radius: 8px; }

.btn-submit {
  background: linear-gradient(135deg, #6388a0, #7a9ab4);
  border: none; border-radius: 8px; color: #fff;
}
.btn-submit:hover {
  background: linear-gradient(135deg, #577a92, #6388a0);
}
</style>
