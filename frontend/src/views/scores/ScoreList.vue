<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="课程">
        <el-select v-model="query.course" placeholder="全部课程" clearable @change="loadData">
          <el-option v-for="c in courseList" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="学期">
        <el-input v-model="query.semester" placeholder="如 2025-2026-1" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">查询</el-button>
        <el-button @click="handleExport">导出 Excel</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="list" border stripe>
      <el-table-column prop="student_no" label="学号" />
      <el-table-column prop="student_name" label="姓名" />
      <el-table-column prop="course_name" label="课程" />
      <el-table-column prop="score" label="成绩" width="80" />
      <el-table-column prop="semester" label="学期" />
      <el-table-column label="操作" width="100" v-if="userStore.userInfo?.role !== 'student'">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination style="margin-top: 16px; justify-content: center" v-model:current-page="page" :total="total" layout="prev, pager, next" @current-change="loadData" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { useUserStore } from '../../store/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const list = ref([])
const total = ref(0)
const page = ref(1)
const courseList = ref([])
const query = reactive({ course: null, semester: '' })

const loadData = async () => {
  const params = { page: page.value }
  if (query.course) params.course = query.course
  if (query.semester) params.semester = query.semester
  const data = await request.get('/scores/', { params })
  list.value = data.results
  total.value = data.count
}

const loadCourses = async () => {
  const data = await request.get('/courses/', { params: { page_size: 100 } })
  courseList.value = data.results
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/scores/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

const handleExport = () => {
  const params = new URLSearchParams()
  if (query.course) params.append('course', query.course)
  window.open(`/api/scores/export/?${params}`, '_blank')
}

onMounted(() => { loadData(); loadCourses() })
</script>
