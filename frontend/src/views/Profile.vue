<template>
  <div style="max-width: 600px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="账号">
        <el-input :value="userStore.userInfo?.username" disabled />
      </el-form-item>
      <el-form-item label="角色">
        <el-input :value="roleMap[userStore.userInfo?.role]" disabled />
      </el-form-item>
      <template v-if="profile">
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
      </template>
      <el-form-item>
        <el-button v-if="canEdit" type="primary" @click="handleSubmit">保存修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import request from '../api'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const profile = ref(null)
const roleMap = { admin: '管理员', teacher: '教师', student: '学生' }

const canEdit = computed(() => userStore.userInfo?.role !== 'admin')

onMounted(async () => {
  const role = userStore.userInfo?.role
  if (role === 'student' && userStore.userInfo?.student_no) {
    // 学生通过学号查自己的信息
    const data = await request.get('/students/', { params: { student_no: userStore.userInfo.student_no } })
    if (data.results?.length) profile.value = data.results[0]
  } else if (role === 'teacher' && userStore.userInfo?.teacher_no) {
    const data = await request.get('/teachers/', { params: { search: userStore.userInfo.teacher_no } })
    if (data.results?.length) profile.value = data.results[0]
  }
})

const handleSubmit = async () => {
  const role = userStore.userInfo?.role
  if (role === 'student') {
    await request.post('/info-changes/', {
      student: profile.value.id,
      field_name: 'info',
      old_value: '当前信息',
      new_value: '提交修改',
    })
    ElMessage.success('修改已提交，等待审核')
  } else if (role === 'teacher') {
    await request.put(`/teachers/${profile.value.id}/`, profile.value)
    ElMessage.success('修改成功')
  }
}
</script>
