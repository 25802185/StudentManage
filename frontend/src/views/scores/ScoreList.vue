<template>
  <div class="page-container">
    <!-- 统计卡片 -->
    <div class="stat-row">
      <div v-for="item in summaryCards" :key="item.label" class="stat-card" :style="{ background: item.bg }">
        <div class="stat-value">{{ item.value }}</div>
        <div class="stat-label">{{ item.label }}</div>
      </div>
    </div>

    <!-- 搜索栏 -->
    <div class="search-card">
      <div class="search-left">
        <div class="search-item" v-if="!isStudent">
          <label class="search-label">班级</label>
          <el-select v-model="query.class_ref" placeholder="全部班级" clearable @change="onClassChange" class="search-input">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </div>
        <div class="search-item">
          <label class="search-label">学期</label>
          <el-select v-model="query.semester" placeholder="全部学期" clearable @change="onSemesterChange" class="search-input">
            <el-option v-for="s in semesterList" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </div>
        <div class="search-item">
          <label class="search-label">课程</label>
          <el-select v-model="query.course" placeholder="全部课程" clearable @change="loadData(); loadSummary()" class="search-input">
            <el-option v-for="c in filteredCourseList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </div>
        <div class="search-item" v-if="!isStudent">
          <label class="search-label">等级</label>
          <el-select v-model="query.score_level" placeholder="全部等级" clearable @change="loadData" class="search-input">
            <el-option label="优秀" value="优秀" />
            <el-option label="良好" value="良好" />
            <el-option label="中等" value="中等" />
            <el-option label="及格" value="及格" />
            <el-option label="不及格" value="不及格" />
          </el-select>
        </div>
        <div class="search-item" v-if="!isStudent">
          <label class="search-label">搜索</label>
          <el-input v-model="query.search" placeholder="姓名或学号" clearable @clear="loadData(); loadSummary()" class="search-input" />
        </div>
      </div>
      <div class="search-right">
        <el-button class="btn-primary" @click="loadData(); loadSummary()">
          <el-icon><Search /></el-icon>查询
        </el-button>
        <el-button class="btn-lavender" @click="handleExport" v-if="!isStudent">
          <el-icon><Download /></el-icon>导出
        </el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="student_no" label="学号" width="120" v-if="!isStudent" />
        <el-table-column prop="student_name" label="姓名" width="100" v-if="!isStudent" />
        <el-table-column prop="course_name" label="课程" min-width="140" />
        <el-table-column prop="score" label="成绩" width="80">
          <template #default="{ row }">
            <span class="score-tag" :class="{ excellent: row.score >= 90, good: row.score >= 80, fail: row.score < 60 }">
              {{ row.score }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="semester" label="学期" width="130" />
        <el-table-column label="操作" width="100" fixed="right" v-if="!isStudent">
          <template #default="{ row }">
            <el-button size="small" class="btn-delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination v-model:current-page="page" :total="total" layout="prev, pager, next" background @current-change="loadData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '../../api'
import { useUserStore } from '../../store/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()
const isStudent = computed(() => userStore.userInfo?.role === 'student')
const list = ref([])
const total = ref(0)
const page = ref(1)
const courseList = ref([])
const allCourses = ref([])
const classList = ref([])
const semesterList = ref([])
const query = reactive({ class_ref: null, course: null, semester: null, search: '', score_level: '' })
const summary = ref({ total: 0, avg: 0, excellent_rate: 0, pass_rate: 0 })

const summaryCards = computed(() => [
  { label: '总记录数', value: summary.value.total, bg: 'linear-gradient(135deg, #6388a0 0%, #8aabbf 100%)' },
  { label: '平均分', value: summary.value.avg, bg: 'linear-gradient(135deg, #b7d9c8 0%, #cde8da 100%)' },
  { label: '优秀率', value: summary.value.excellent_rate + '%', bg: 'linear-gradient(135deg, #c5b8d9 0%, #d8cde8 100%)' },
  { label: '及格率', value: summary.value.pass_rate + '%', bg: 'linear-gradient(135deg, #d4a88c 0%, #e2c0ad 100%)' },
])

const filteredCourseList = computed(() => {
  let list = courseList.value
  if (query.semester) list = list.filter(c => c.semester === query.semester)
  return list
})

const onClassChange = () => {
  if (query.class_ref) {
    courseList.value = allCourses.value.filter(c => c.class_ref === query.class_ref)
    if (query.course) {
      const stillValid = courseList.value.some(c => c.id === query.course)
      if (!stillValid) query.course = null
    }
  } else {
    courseList.value = allCourses.value
  }
  loadData()
  loadSummary()
}

const onSemesterChange = () => {
  if (query.course) {
    const course = courseList.value.find(c => c.id === query.course)
    if (course && query.semester && course.semester !== query.semester) {
      query.course = null
    }
  }
  loadData()
  loadSummary()
}

const scoreLevelMap = { '优秀': s => s >= 90, '良好': s => s >= 80 && s < 90, '中等': s => s >= 70 && s < 80, '及格': s => s >= 60 && s < 70, '不及格': s => s < 60 }

const loadData = async () => {
  const params = { page: page.value }
  if (query.class_ref) params.student__class_ref = query.class_ref
  if (query.course) params.course = query.course
  if (query.semester) params['course__semester'] = query.semester
  if (query.search && !isStudent.value) params.search = query.search
  const data = await request.get('/scores/', { params })
  let results = data.results || []
  if (query.score_level && scoreLevelMap[query.score_level]) {
    results = results.filter(r => scoreLevelMap[query.score_level](r.score))
  }
  list.value = results
  total.value = data.count
}

const loadSummary = async () => {
  if (isStudent.value) return
  const params = {}
  if (query.class_ref) params.student__class_ref = query.class_ref
  if (query.course) params.course = query.course
  if (query.semester) params['course__semester'] = query.semester
  if (query.search) params.search = query.search
  summary.value = await request.get('/stats/score-summary/', { params })
}

const loadCourses = async () => {
  if (isStudent.value) {
    const data = await request.get('/scores/my-courses/')
    courseList.value = data
    allCourses.value = data
  } else {
    const data = await request.get('/courses/', { params: { page_size: 200 } })
    courseList.value = data.results
    allCourses.value = data.results
  }
}

const loadClasses = async () => {
  if (isStudent.value) return
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const loadSemesters = async () => {
  const data = await request.get('/courses/semesters/')
  semesterList.value = data.results || data
  // 默认选中当前学期
  const current = semesterList.value.find(s => s.is_current)
  if (current && !query.semester) {
    query.semester = current.id
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该成绩记录？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/scores/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
    loadSummary()
  })
}

const handleExport = () => {
  const params = new URLSearchParams()
  if (query.course) params.append('course', query.course)
  window.open(`/api/scores/export/?${params}`, '_blank')
}

onMounted(async () => {
  await loadClasses()
  await loadSemesters()
  await loadCourses()
  // 从 Dashboard 图表跳转过来时，读取 query 参数预填筛选条件
  if (route.query.class_ref) {
    query.class_ref = Number(route.query.class_ref)
    courseList.value = allCourses.value.filter(c => c.class_ref === query.class_ref)
  }
  if (route.query.course) {
    query.course = Number(route.query.course)
  }
  if (route.query.score_level) {
    query.score_level = route.query.score_level
  }
  loadData()
  loadSummary()
})
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; }

.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
.stat-card {
  padding: 18px 20px;
  border-radius: 12px;
  color: #fff;
  box-shadow: 0 4px 14px rgba(0,0,0,0.07);
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}
.stat-value {
  font-size: 26px;
  font-weight: 700;
  line-height: 1.2;
}
.stat-label {
  font-size: 12px;
  opacity: 0.8;
  margin-top: 4px;
}

.search-card {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px; background: #fff; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.search-left { display: flex; align-items: center; gap: 20px; }
.search-item { display: flex; align-items: center; gap: 8px; }
.search-label { font-size: 13px; color: #666; white-space: nowrap; }
.search-input { width: 180px; }
.search-input :deep(.el-input__wrapper) { border-radius: 8px; box-shadow: 0 0 0 1px #e8e8e8 inset; }
.search-input :deep(.el-input__wrapper:hover) { box-shadow: 0 0 0 1px #b7d9c8 inset; }
.search-input :deep(.el-input__wrapper.is-focus) { box-shadow: 0 0 0 2px rgba(183,217,200,0.4) inset; }
.search-right { display: flex; gap: 10px; }

.btn-primary { background: linear-gradient(135deg, #6388a0, #7a9ab4); border: none; border-radius: 8px; color: #fff; }
.btn-primary:hover { background: linear-gradient(135deg, #577a92, #6388a0); }
.btn-lavender { background: linear-gradient(135deg, #c5b8d9, #d4c8e6); border: none; border-radius: 8px; color: #5a4a72; }
.btn-lavender:hover { background: linear-gradient(135deg, #b8a8ce, #c5b8d9); }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }
.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) { background: #fafbfc; }

.score-tag { display: inline-block; min-width: 36px; height: 24px; line-height: 24px; text-align: center; border-radius: 6px; font-size: 13px; font-weight: 600; background: rgba(99,136,160,0.08); color: #6388a0; }
.score-tag.excellent { background: rgba(183,217,200,0.2); color: #5a9a78; }
.score-tag.good { background: rgba(99,136,160,0.1); color: #6388a0; }
.score-tag.fail { background: rgba(233,201,188,0.2); color: #c4887a; }

.btn-delete { background: rgba(233,201,188,0.2); border: none; color: #c4887a; border-radius: 6px; }
.btn-delete:hover { background: #e9c9bc; color: #8a5a48; }

.pagination-wrap { display: flex; justify-content: center; margin-top: 18px; }
.pagination-wrap :deep(.el-pager li.is-active) { background-color: #b7d9c8 !important; color: #fff !important; border-radius: 6px; }
.pagination-wrap :deep(.el-pager li) { border-radius: 6px; min-width: 32px; }
</style>
