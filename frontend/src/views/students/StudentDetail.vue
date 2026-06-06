<template>
  <div style="max-width: 600px">
    <el-descriptions :column="1" border v-if="student">
      <el-descriptions-item label="学号">{{ student.student_no }}</el-descriptions-item>
      <el-descriptions-item label="姓名">{{ student.name }}</el-descriptions-item>
      <el-descriptions-item label="性别">{{ student.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
      <el-descriptions-item label="年龄">{{ student.age }}</el-descriptions-item>
      <el-descriptions-item label="班级">{{ student.class_name }}</el-descriptions-item>
      <el-descriptions-item label="电话">{{ student.phone }}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{ student.email }}</el-descriptions-item>
      <el-descriptions-item label="地址">{{ student.address }}</el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '../../api'

const route = useRoute()
const student = ref(null)

onMounted(async () => {
  student.value = await request.get(`/students/${route.params.id}/`)
})
</script>
