<template>
  <div class="page-container">
    <div class="password-card">
      <div class="card-header-sm">
        <el-icon :size="20" color="#6388a0"><Lock /></el-icon>
        <span>修改密码</span>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" class="password-form">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="form.old_password" type="password" show-password placeholder="请输入旧密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="form.new_password" type="password" show-password placeholder="请输入新密码（至少6位）" />
        </el-form-item>
        <el-form-item>
          <el-button class="btn-submit" @click="handleSubmit">修改密码</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import request from '../api'
import { ElMessage } from 'element-plus'

const formRef = ref(null)
const form = reactive({ old_password: '', new_password: '' })
const rules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
}

const handleSubmit = async () => {
  await formRef.value.validate()
  await request.put('/auth/password/', form)
  ElMessage.success('密码修改成功')
  form.old_password = ''
  form.new_password = ''
}
</script>

<style scoped>
.page-container { max-width: 480px; }

.password-card {
  background: #fff; border-radius: 14px; padding: 28px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.045);
}

.card-header-sm {
  display: flex; align-items: center; gap: 8px;
  font-size: 15px; font-weight: 600; color: #3a4f63;
  padding-bottom: 20px; border-bottom: 1px solid #f0f0f0; margin-bottom: 24px;
}

.password-form :deep(.el-input__wrapper) { border-radius: 8px; }

.btn-submit {
  background: linear-gradient(135deg, #6388a0, #7a9ab4);
  border: none; border-radius: 8px; color: #fff;
}
.btn-submit:hover {
  background: linear-gradient(135deg, #577a92, #6388a0);
}
</style>
