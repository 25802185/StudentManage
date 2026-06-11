<template>
  <div class="dashboard">
    <!-- 顶部统计卡片 -->
    <div class="stat-row">
      <div v-for="item in statCards" :key="item.label" class="stat-card" :style="{ background: item.bg }">
        <div class="stat-left">
          <div class="stat-icon-wrap" :style="{ background: item.iconBg }">
            <el-icon :size="22"><component :is="item.icon" /></el-icon>
          </div>
        </div>
        <div class="stat-right">
          <div class="stat-value">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </div>
        <div class="stat-deco"></div>
      </div>
    </div>

    <!-- 中部图表 -->
    <div class="chart-row">
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #8BA7C7"></span>
            <span class="card-title">成绩等级分布</span>
          </div>
          <div class="filter-group">
            <el-select v-model="scoreFilter.class_ref" placeholder="全部班级" clearable size="small" class="filter-select" @change="onClassChange">
              <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
            </el-select>
            <el-select v-model="scoreFilter.course" placeholder="全部课程" clearable size="small" class="filter-select" @change="loadScoreChart">
              <el-option v-for="c in courseList" :key="c.id" :label="c.name" :value="c.id" />
            </el-select>
          </div>
        </div>
        <div ref="scoreChart" class="chart-body"></div>
      </div>
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #A8C5B8"></span>
            <span class="card-title">班级学生人数</span>
          </div>
          <span class="card-tag tag-green">各班概览</span>
        </div>
        <div ref="classChart" class="chart-body"></div>
      </div>
    </div>

    <!-- 新增图表行 -->
    <div class="chart-triple-row">
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #d4a88c"></span>
            <span class="card-title">成绩趋势</span>
          </div>
          <span class="card-tag tag-orange">按学期</span>
        </div>
        <div ref="trendChart" class="chart-body"></div>
      </div>
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #c5b8d9"></span>
            <span class="card-title">性别分布</span>
          </div>
          <span class="card-tag tag-purple">学生占比</span>
        </div>
        <div ref="genderChart" class="chart-body"></div>
      </div>
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #b7d9c8"></span>
            <span class="card-title">班级平均分</span>
          </div>
          <span class="card-tag tag-green">横向对比</span>
        </div>
        <div ref="classAvgChart" class="chart-body"></div>
      </div>
    </div>

    <!-- 底部待审核 + 操作日志 -->
    <div class="bottom-row">
      <!-- 待审核动态 -->
      <div class="info-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #e9c9bc"></span>
            <span class="card-title">待审核动态</span>
          </div>
          <router-link to="/info-changes" class="card-more">查看全部</router-link>
        </div>
        <div class="notice-list">
          <div v-if="reviews.length === 0" class="empty-tip">暂无待审核申请</div>
          <div v-for="item in reviews" :key="item.id" class="notice-item">
            <div class="notice-dot" style="background: #e9c9bc"></div>
            <div class="notice-content">
              <div class="notice-text">
                <span class="highlight">{{ item.student_name }}</span> 申请修改
                <span class="field-tag">{{ item.field_name }}</span>
              </div>
              <div class="notice-time">{{ item.created_at }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近操作日志 -->
      <div class="info-card">
        <div class="card-header">
          <div class="card-title-group">
            <span class="card-dot" style="background: #6388a0"></span>
            <span class="card-title">最近操作</span>
          </div>
          <router-link to="/logs" class="card-more">查看全部</router-link>
        </div>
        <div class="todo-list">
          <div v-if="logs.length === 0" class="empty-tip">暂无操作记录</div>
          <div v-for="item in logs" :key="item.id" class="todo-item">
            <div class="todo-left">
              <div class="todo-type" style="background: rgba(99,136,160,0.12); color: #6388a0">
                {{ item.user }}
              </div>
              <span class="todo-text">{{ item.action }} {{ item.target }}</span>
            </div>
            <span class="log-time">{{ item.created_at }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import request from '../api'

const router = useRouter()
const statCards = ref([])
const scoreChart = ref(null)
const classChart = ref(null)
const trendChart = ref(null)
const genderChart = ref(null)
const classAvgChart = ref(null)
let pieInstance = null

const morandi = {
  hazeBlue: '#6388a0',
  mintGreen: '#b7d9c8',
  nudePink: '#e9c9bc',
  softLavender: '#c5b8d9',
  warmPeach: '#d4a88c',
}

const reviews = ref([])
const logs = ref([])

const classList = ref([])
const courseList = ref([])
const allCourses = ref([])
const scoreFilter = reactive({ class_ref: null, course: null })

const onClassChange = (val) => {
  if (val) {
    courseList.value = allCourses.value.filter(c => c.class_ref === val)
    if (scoreFilter.course) {
      const stillValid = courseList.value.some(c => c.id === scoreFilter.course)
      if (!stillValid) scoreFilter.course = null
    }
  } else {
    courseList.value = allCourses.value
  }
  loadScoreChart()
}

const loadScoreChart = async () => {
  const params = {}
  if (scoreFilter.course) params.course = scoreFilter.course
  if (scoreFilter.class_ref) params.class_ref = scoreFilter.class_ref
  const scoreData = await request.get('/stats/score-distribution/', { params })

  if (!pieInstance) {
    pieInstance = echarts.init(scoreChart.value)
    pieInstance.on('click', (params) => {
      const query = { score_level: params.name }
      if (scoreFilter.class_ref) query.class_ref = scoreFilter.class_ref
      if (scoreFilter.course) query.course = scoreFilter.course
      router.push({ path: '/scores', query })
    })
  }
  pieInstance.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: '#f0f0f0', borderWidth: 1,
      textStyle: { color: '#555', fontSize: 13 },
      formatter: '{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical', right: '6%', top: 'middle',
      itemWidth: 10, itemHeight: 10, itemGap: 14,
      textStyle: { color: '#777', fontSize: 13 },
    },
    series: [{
      type: 'pie',
      radius: ['38%', '64%'],
      center: ['38%', '50%'],
      padAngle: 2,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#fff',
        borderWidth: 2,
      },
      label: { show: false },
      emphasis: {
        scale: true, scaleSize: 6,
        itemStyle: { shadowBlur: 12, shadowColor: 'rgba(0,0,0,0.1)' },
      },
      data: Object.entries(scoreData).map(([name, value], i) => ({
        name, value,
        itemStyle: { color: Object.values(morandi)[i % 5] },
      })),
    }],
  })
}

onMounted(async () => {
  const data = await request.get('/stats/dashboard/')
  statCards.value = [
    {
      label: '学生总数', value: data.student_count, icon: 'User',
      bg: 'linear-gradient(135deg, #6388a0 0%, #8aabbf 100%)',
      iconBg: 'rgba(255,255,255,0.25)',
    },
    {
      label: '教师总数', value: data.teacher_count, icon: 'Avatar',
      bg: 'linear-gradient(135deg, #b7d9c8 0%, #cde8da 100%)',
      iconBg: 'rgba(255,255,255,0.25)',
    },
    {
      label: '班级数量', value: data.class_count, icon: 'School',
      bg: 'linear-gradient(135deg, #e9c9bc 0%, #f2ddd3 100%)',
      iconBg: 'rgba(255,255,255,0.25)',
    },
    {
      label: '课程数量', value: data.course_count, icon: 'Reading',
      bg: 'linear-gradient(135deg, #c5b8d9 0%, #d8cde8 100%)',
      iconBg: 'rgba(255,255,255,0.25)',
    },
  ]

  const [reviewsData, logsData, classesData, coursesData] = await Promise.all([
    request.get('/stats/pending-reviews/'),
    request.get('/stats/recent-logs/'),
    request.get('/classes/', { params: { page_size: 100 } }),
    request.get('/courses/', { params: { page_size: 200 } }),
  ])
  reviews.value = reviewsData
  logs.value = logsData
  classList.value = classesData.results
  allCourses.value = coursesData.results
  courseList.value = coursesData.results

  await nextTick()

  await loadScoreChart()

  // 班级柱状图
  const classData = await request.get('/stats/class-students/')
  const bar = echarts.init(classChart.value)
  bar.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: '#f0f0f0', borderWidth: 1,
      textStyle: { color: '#555', fontSize: 13 },
    },
    grid: { left: '2%', right: '3%', bottom: '2%', top: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      data: classData.map(c => c.name),
      axisLine: { lineStyle: { color: '#e8e8e8' } },
      axisTick: { show: false },
      axisLabel: { color: '#999', fontSize: 12 },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#bbb', fontSize: 12 },
      splitLine: { lineStyle: { color: '#f5f5f5', type: 'dashed' } },
    },
    series: [{
      type: 'bar',
      barWidth: '40%',
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#6388a0' },
          { offset: 1, color: '#9abdd4' },
        ]),
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#577a92' },
            { offset: 1, color: '#6388a0' },
          ]),
        },
      },
      data: classData.map(c => c.count),
    }],
  })

  // 成绩趋势折线图
  const trendData = await request.get('/stats/score-trend/')
  const trend = echarts.init(trendChart.value)
  trend.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: '#f0f0f0', borderWidth: 1,
      textStyle: { color: '#555', fontSize: 13 },
      formatter: (params) => `${params[0].name}<br/>平均分: <b>${params[0].value}</b>`,
    },
    grid: { left: '2%', right: '4%', bottom: '14%', top: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: trendData.map(t => t.semester),
      axisLine: { lineStyle: { color: '#e8e8e8' } },
      axisTick: { show: false },
      axisLabel: { color: '#999', fontSize: 11, interval: 0, rotate: trendData.length > 6 ? 30 : 0 },
    },
    yAxis: {
      type: 'value',
      min: (value) => Math.max(0, Math.floor(value.min - 10)),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#bbb', fontSize: 12 },
      splitLine: { lineStyle: { color: '#f5f5f5', type: 'dashed' } },
    },
    series: [{
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { width: 3, color: '#d4a88c' },
      itemStyle: { color: '#d4a88c', borderColor: '#fff', borderWidth: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(212,168,140,0.35)' },
          { offset: 1, color: 'rgba(212,168,140,0.02)' },
        ]),
      },
      data: trendData.map(t => t.avg),
    }],
  })

  // 性别分布饼图
  const genderData = await request.get('/stats/gender-distribution/')
  const gender = echarts.init(genderChart.value)
  gender.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: '#f0f0f0', borderWidth: 1,
      textStyle: { color: '#555', fontSize: 13 },
      formatter: '{b}: {c}人 ({d}%)',
    },
    legend: {
      orient: 'vertical', right: '6%', top: 'middle',
      itemWidth: 10, itemHeight: 10, itemGap: 14,
      textStyle: { color: '#777', fontSize: 13 },
    },
    series: [{
      type: 'pie',
      radius: ['38%', '64%'],
      center: ['38%', '50%'],
      padAngle: 2,
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: {
        scale: true, scaleSize: 6,
        itemStyle: { shadowBlur: 12, shadowColor: 'rgba(0,0,0,0.1)' },
      },
      data: [
        { name: '男', value: genderData['男'], itemStyle: { color: '#6388a0' } },
        { name: '女', value: genderData['女'], itemStyle: { color: '#e9c9bc' } },
      ],
    }],
  })

  // 班级平均分柱状图
  const classAvgData = await request.get('/stats/class-avg-scores/')
  const classAvg = echarts.init(classAvgChart.value)
  classAvg.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: '#f0f0f0', borderWidth: 1,
      textStyle: { color: '#555', fontSize: 13 },
      formatter: (params) => `${params[0].name}<br/>平均分: <b>${params[0].value}</b>`,
    },
    grid: { left: '2%', right: '3%', bottom: '14%', top: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      data: classAvgData.map(c => c.name),
      axisLine: { lineStyle: { color: '#e8e8e8' } },
      axisTick: { show: false },
      axisLabel: { color: '#999', fontSize: 11, interval: 0, rotate: classAvgData.length > 6 ? 30 : 0, overflow: 'truncate', width: 60 },
    },
    yAxis: {
      type: 'value',
      min: (value) => Math.max(0, Math.floor(value.min - 10)),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#bbb', fontSize: 12 },
      splitLine: { lineStyle: { color: '#f5f5f5', type: 'dashed' } },
    },
    series: [{
      type: 'bar',
      barWidth: '40%',
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#c5b8d9' },
          { offset: 1, color: '#ddd2ec' },
        ]),
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#a89ac0' },
            { offset: 1, color: '#c5b8d9' },
          ]),
        },
      },
      data: classAvgData.map(c => c.avg),
    }],
  })
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 100%;
}

/* ========== 统计卡片 ========== */
.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.stat-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 22px 20px;
  border-radius: 14px;
  color: #fff;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
  transition: transform 0.25s, box-shadow 0.25s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.1);
}

.stat-deco {
  position: absolute;
  top: -20px;
  right: -20px;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.stat-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  opacity: 0.8;
  margin-top: 3px;
}

/* ========== 图表卡片 ========== */
.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.chart-triple-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.chart-card {
  background: #fff;
  border-radius: 14px;
  padding: 22px 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.035);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #2c3e50;
}

.card-tag {
  font-size: 11px;
  color: #6388a0;
  background: rgba(99, 136, 160, 0.1);
  padding: 3px 10px;
  border-radius: 20px;
  font-weight: 500;
}

.tag-green {
  color: #5a9a78;
  background: rgba(183, 217, 200, 0.15);
}

.tag-orange {
  color: #c4887a;
  background: rgba(233, 201, 188, 0.15);
}

.tag-purple {
  color: #8a7ab0;
  background: rgba(197, 184, 217, 0.15);
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-select {
  width: 120px;
}

.filter-select :deep(.el-input__wrapper) {
  border-radius: 6px;
  box-shadow: 0 0 0 1px #e8e8e8 inset;
}

.filter-select :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #b7d9c8 inset;
}

.filter-select :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(183, 217, 200, 0.4) inset;
}

.chart-body {
  height: 280px;
}

/* ========== 底部信息卡片 ========== */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.info-card {
  background: #fff;
  border-radius: 14px;
  padding: 22px 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.035);
}

.card-more {
  font-size: 12px;
  color: #aaa;
  cursor: pointer;
  transition: color 0.2s;
}

.card-more:hover {
  color: #6388a0;
}

/* 公告列表 */
.notice-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.notice-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
  transition: background 0.15s;
}

.notice-item:last-child {
  border-bottom: none;
}

.notice-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.notice-content {
  flex: 1;
  min-width: 0;
}

.notice-text {
  font-size: 13px;
  color: #444;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notice-time {
  font-size: 11px;
  color: #bbb;
  margin-top: 3px;
}

/* 待办列表 */
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 0;
  border-bottom: 1px solid #f5f5f5;
}

.todo-item:last-child {
  border-bottom: none;
}

.todo-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.todo-type {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}

.todo-text {
  font-size: 13px;
  color: #444;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.todo-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  flex-shrink: 0;
  font-weight: 500;
}

/* 新增样式 */
.highlight {
  color: #2c3e50;
  font-weight: 500;
}

.field-tag {
  font-size: 11px;
  color: #6388a0;
  background: rgba(99, 136, 160, 0.1);
  padding: 1px 6px;
  border-radius: 4px;
  margin-left: 4px;
}

.log-time {
  font-size: 11px;
  color: #bbb;
  flex-shrink: 0;
}

.empty-tip {
  text-align: center;
  color: #ccc;
  font-size: 13px;
  padding: 32px 0;
}
</style>
