<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="学期">
        <el-input v-model="semester" placeholder="如 2025-2026-1" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadStudents">加载学生</el-button>
        <el-button type="success" @click="handleSubmit" :disabled="!scores.length">提交成绩</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="scores" border stripe>
      <el-table-column prop="student_no" label="学号" width="120" />
      <el-table-column prop="student_name" label="姓名" width="120" />
      <el-table-column label="成绩">
        <template #default="{ row }">
          <el-input-number v-model="row.score" :min="0" :max="100" :precision="1" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../../api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const courseId = route.params.courseId
const semester = ref('')
const scores = ref([])

const loadStudents = async () => {
  if (!semester.value) {
    ElMessage.warning('请填写学期')
    return
  }
  const course = await request.get(`/courses/${courseId}/`)
  const data = await request.get('/students/', { params: { class_ref: course.class_ref, page_size: 200 } })
  scores.value = data.results.map(s => ({
    student: s.id,
    student_no: s.student_no,
    student_name: s.name,
    score: null,
  }))
}

const handleSubmit = async () => {
  const validScores = scores.value.filter(s => s.score !== null)
  if (!validScores.length) {
    ElMessage.warning('请填写成绩')
    return
  }
  await request.post('/scores/batch/', {
    course: parseInt(courseId),
    semester: semester.value,
    scores: validScores.map(s => ({ student: s.student, score: s.score })),
  })
  ElMessage.success('成绩录入成功')
  router.push('/scores')
}
</script>
