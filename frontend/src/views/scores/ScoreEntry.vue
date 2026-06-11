<template>
  <div class="page-container">
    <!-- 顶部信息栏 -->
    <div class="search-card">
      <div class="search-left">
        <span class="card-title-sm" v-if="courseInfo">
          {{ courseInfo.name }} — {{ courseInfo.semester_name }}
        </span>
        <span class="card-title-sm" v-else>加载中...</span>
      </div>
      <div class="search-right">
        <el-button class="btn-mint" @click="handleSubmit" :disabled="!changedScores.length">
          <el-icon><Check /></el-icon>提交成绩（{{ changedScores.length }} 条）
        </el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card" v-if="scores.length">
      <div class="table-info">
        <span class="info-text">共 {{ scores.length }} 名学生</span>
        <span class="info-text" v-if="courseInfo">班级：{{ courseInfo.class_name }}</span>
        <span class="info-text">{{ statsText }}</span>
      </div>
      <el-table :data="scores" style="width: 100%">
        <el-table-column prop="student_no" label="学号" width="140" />
        <el-table-column prop="student_name" label="姓名" width="120" />
        <el-table-column label="成绩" width="160">
          <template #default="{ row }">
            <el-input-number v-model="row.score" :min="0" :max="100" :precision="1" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <span v-if="getScoreStatus(row) === 'new'" class="status-new">新增</span>
            <span v-else-if="getScoreStatus(row) === 'modified'" class="status-modified">已修改</span>
            <span v-else-if="getScoreStatus(row) === 'existing'" class="status-existing">未改动</span>
            <span v-else class="status-empty">未填写</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div v-else class="empty-card">
      <el-icon :size="48" color="#ccc"><Document /></el-icon>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '../../api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const courseId = computed(() => route.params.courseId)
const scores = ref([])
const courseInfo = ref(null)

// 记录原始分数，用于对比变化
const originalMap = {}

const changedScores = computed(() => {
  return scores.value.filter(s => {
    if (s.score === null || s.score === undefined) return false
    const orig = originalMap[s.student]
    return orig === undefined || orig !== s.score
  })
})

const getScoreStatus = (row) => {
  if (row.score === null || row.score === undefined) return 'empty'
  const orig = originalMap[row.student]
  if (orig === undefined) return 'new'
  if (orig !== row.score) return 'modified'
  return 'existing'
}

const statsText = computed(() => {
  const total = scores.value.length
  const filled = scores.value.filter(s => s.score !== null && s.score !== undefined).length
  const changed = changedScores.value.length
  return `已填写 ${filled}/${total}，待提交 ${changed} 条`
})

const loadData = async () => {
  try {
    const course = await request.get(`/courses/${courseId.value}/`)
    courseInfo.value = course
    if (!course.class_ref) {
      ElMessage.error('该课程未关联班级')
      return
    }

    const data = await request.get('/students/', { params: { class_ref: course.class_ref, page_size: 1000 } })
    if (!data.results || data.results.length === 0) {
      ElMessage.warning('该班级暂无学生')
      scores.value = []
      return
    }

    // 加载已有成绩
    let existingScores = []
    try {
      const scoreData = await request.get('/scores/', {
        params: { course: courseId.value, page_size: 1000 }
      })
      existingScores = scoreData.results || []
    } catch {
      existingScores = []
    }

    // 构建原始分数 map
    Object.keys(originalMap).forEach(k => delete originalMap[k])
    const scoreMap = {}
    existingScores.forEach(s => {
      scoreMap[s.student] = s.score
      originalMap[s.student] = s.score
    })

    scores.value = data.results.map(s => ({
      student: s.id,
      student_no: s.student_no,
      student_name: s.name,
      score: scoreMap[s.id] !== undefined ? scoreMap[s.id] : null,
    }))
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

const handleSubmit = async () => {
  const toSubmit = changedScores.value
  if (!toSubmit.length) {
    ElMessage.warning('没有需要提交的成绩')
    return
  }
  await request.post('/scores/batch/', {
    course: parseInt(courseId.value),
    scores: toSubmit.map(s => ({ student: s.student, score: s.score })),
  })
  ElMessage.success(`成功提交 ${toSubmit.length} 条成绩`)
  // 留在当前页面，重新加载数据
  await loadData()
}

watch(courseId, () => {
  if (courseId.value) loadData()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; }

.search-card {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 22px; background: #fff; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.search-left { display: flex; align-items: center; gap: 20px; }
.card-title-sm { font-size: 14px; font-weight: 600; color: #3a4f63; }
.search-right { display: flex; gap: 10px; }

.btn-mint { background: linear-gradient(135deg, #b7d9c8, #c8e6d6); border: none; border-radius: 8px; color: #3a6b52; }
.btn-mint:hover { background: linear-gradient(135deg, #a8cebb, #b7d9c8); }
.btn-mint:disabled { opacity: 0.5; cursor: not-allowed; }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-info { display: flex; justify-content: space-between; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0; }
.info-text { font-size: 13px; color: #888; }

.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }

.status-existing { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; background: rgba(183,217,200,0.2); color: #5a9a78; }
.status-modified { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; background: rgba(197,184,217,0.2); color: #7a6299; }
.status-new { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; background: rgba(99,136,160,0.1); color: #6388a0; }
.status-empty { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; background: rgba(0,0,0,0.03); color: #ccc; }

.empty-card {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 60px; background: #fff; border-radius: 14px; box-shadow: 0 2px 16px rgba(0,0,0,0.045);
}
.empty-card p { margin-top: 12px; color: #bbb; font-size: 13px; }
</style>
