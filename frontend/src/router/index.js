import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

// 各角色允许访问的路由前缀
const roleAccess = {
  admin: ['/dashboard', '/students', '/teachers', '/classes', '/courses', '/semesters', '/scores', '/info-changes', '/logs', '/profile', '/change-password'],
  teacher: ['/dashboard', '/students', '/courses', '/scores', '/info-changes', '/profile', '/change-password'],
  student: ['/scores', '/my-applications', '/profile', '/change-password'],
}

const routes = [
  { path: '/login', component: () => import('../views/Login.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: (to) => {
      const store = useUserStore()
      if (store.userInfo?.role === 'student') return '/scores'
      return '/dashboard'
    },
    children: [
      { path: 'dashboard', component: () => import('../views/Dashboard.vue'), meta: { title: '仪表盘' } },
      { path: 'students', component: () => import('../views/students/StudentList.vue'), meta: { title: '学生管理' } },
      { path: 'students/:id', component: () => import('../views/students/StudentDetail.vue'), meta: { title: '学生详情' } },
      { path: 'teachers', component: () => import('../views/teachers/TeacherList.vue'), meta: { title: '教师管理' } },
      { path: 'classes', component: () => import('../views/classes/ClassList.vue'), meta: { title: '班级管理' } },
      { path: 'courses', component: () => import('../views/courses/CourseList.vue'), meta: { title: '课程管理' } },
      { path: 'semesters', component: () => import('../views/semesters/SemesterList.vue'), meta: { title: '学期管理' } },
      { path: 'scores', component: () => import('../views/scores/ScoreList.vue'), meta: { title: '成绩管理' } },
      { path: 'scores/entry/:courseId', component: () => import('../views/scores/ScoreEntry.vue'), meta: { title: '成绩录入' } },
      { path: 'info-changes', component: () => import('../views/info-changes/InfoChangeList.vue'), meta: { title: '信息审核' } },
      { path: 'my-applications', component: () => import('../views/info-changes/MyApplications.vue'), meta: { title: '我的申请' } },
      { path: 'profile', component: () => import('../views/Profile.vue'), meta: { title: '个人信息' } },
      { path: 'change-password', component: () => import('../views/ChangePassword.vue'), meta: { title: '修改密码' } },
      { path: 'logs', component: () => import('../views/logs/LogList.vue'), meta: { title: '操作日志' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.public) return next()
  const store = useUserStore()
  if (!store.isLoggedIn) {
    try {
      await store.fetchUserInfo()
    } catch {
      return next('/login')
    }
  }
  // 角色权限检查
  const role = store.userInfo?.role
  const allowed = roleAccess[role] || []
  const matched = allowed.some(prefix => to.path === prefix || to.path.startsWith(prefix + '/'))
  if (!matched) {
    // 无权限，跳转到该角色的默认页
    if (role === 'student') return next('/scores')
    return next('/dashboard')
  }
  next()
})

export default router
