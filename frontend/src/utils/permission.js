export const menuConfig = {
  admin: [
    { path: '/dashboard', icon: 'DataAnalysis', title: '仪表盘' },
    { path: '/students', icon: 'User', title: '学生管理' },
    { path: '/teachers', icon: 'Avatar', title: '教师管理' },
    { path: '/classes', icon: 'School', title: '班级管理' },
    { path: '/courses', icon: 'Reading', title: '课程管理' },
    { path: '/scores', icon: 'Document', title: '成绩管理' },
    { path: '/info-changes', icon: 'Checked', title: '信息审核' },
    { path: '/logs', icon: 'List', title: '操作日志' },
  ],
  teacher: [
    { path: '/dashboard', icon: 'DataAnalysis', title: '仪表盘' },
    { path: '/students', icon: 'User', title: '学生管理' },
    { path: '/courses', icon: 'Reading', title: '课程管理' },
    { path: '/scores', icon: 'Document', title: '成绩管理' },
    { path: '/info-changes', icon: 'Checked', title: '信息审核' },
  ],
  student: [
    { path: '/scores', icon: 'Document', title: '我的成绩' },
    { path: '/my-applications', icon: 'Edit', title: '我的申请' },
    { path: '/profile', icon: 'User', title: '个人信息' },
  ],
}
