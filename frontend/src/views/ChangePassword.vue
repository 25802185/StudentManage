<template>
  <div style="max-width: 400px">
    <el-form :model="form" label-width="80px">
      <el-form-item label="旧密码"><el-input v-model="form.old_password" type="password" show-password /></el-form-item>
      <el-form-item label="新密码"><el-input v-model="form.new_password" type="password" show-password /></el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">修改密码</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import request from '../api'
import { ElMessage } from 'element-plus'

const form = reactive({ old_password: '', new_password: '' })

const handleSubmit = async () => {
  await request.put('/auth/password/', form)
  ElMessage.success('密码修改成功')
}
</script>
