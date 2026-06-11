<template>
  <div class="page-container">
    <!-- 搜索栏 -->
    <div class="search-card">
      <div class="search-left">
        <div class="search-item">
          <label class="search-label">班级</label>
          <el-select v-model="query.class_ref" placeholder="全部班级" clearable @change="loadData" class="search-input">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </div>
        <div class="search-item">
          <label class="search-label">搜索</label>
          <el-input v-model="query.search" placeholder="姓名或学号" clearable @clear="loadData" class="search-input" />
        </div>
      </div>
      <div class="search-right">
        <el-button type="primary" class="btn-primary" @click="loadData">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button class="btn-mint" @click="showAdd">
          <el-icon><Plus /></el-icon>新增
        </el-button>
        <el-button class="btn-lavender" @click="handleExport">
          <el-icon><Download /></el-icon>导出
        </el-button>
        <el-upload :show-file-list="false" :before-upload="handleImport" accept=".xlsx,.xls">
          <el-button class="btn-pink">
            <el-icon><Upload /></el-icon>导入
          </el-button>
        </el-upload>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="student_no" label="学号" width="130" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="gender" label="性别" width="70">
          <template #default="{ row }">
            <span class="gender-tag" :class="row.gender">{{ row.gender === 'male' ? '男' : '女' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="class_name" label="班级" min-width="160" />
        <el-table-column prop="phone" label="电话" width="130" />
        <el-table-column prop="email" label="邮箱" min-width="160" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <span class="status-tag" :class="row.status">
              {{ row.status === 'normal' ? '正常' : '待审核' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" class="btn-edit" @click="showEdit(row)">编辑</el-button>
            <el-button size="small" class="btn-warn" @click="showResetPwd(row)">重置密码</el-button>
            <el-button size="small" class="btn-delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="page"
          :page-size="10"
          :total="total"
          layout="prev, pager, next"
          background
          @current-change="loadData"
        />
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学生' : '新增学生'" width="520px" class="custom-dialog">
      <el-form :model="form" label-width="80px" class="dialog-form">
        <el-form-item label="学号"><el-input v-model="form.student_no" :disabled="isEdit" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄"><el-input-number v-model="form.age" :min="1" :max="100" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级" style="width: 100%">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="地址"><el-input v-model="form.address" /></el-form-item>
        <el-form-item label="密码" v-if="!isEdit">
          <el-input v-model="form.password" placeholder="留空则默认为学号后6位" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" class="btn-cancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit" class="btn-submit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 重置密码弹窗 -->
    <el-dialog v-model="resetPwdVisible" title="重置密码" width="400px" class="custom-dialog">
      <el-form label-width="80px" class="dialog-form">
        <el-form-item label="学生">{{ resetPwdTarget?.name }}（{{ resetPwdTarget?.student_no }}）</el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="resetPwdForm.new_password" placeholder="请输入新密码（至少6位）" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resetPwdVisible = false" class="btn-cancel">取消</el-button>
        <el-button type="primary" @click="handleResetPwd" class="btn-submit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const list = ref([])
const total = ref(0)
const page = ref(1)
const query = reactive({ class_ref: '', search: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const classList = ref([])
const form = reactive({
  student_no: '', name: '', gender: 'male', age: null,
  class_ref: null, phone: '', email: '', address: '', password: '',
})
const resetPwdVisible = ref(false)
const resetPwdTarget = ref(null)
const resetPwdForm = reactive({ new_password: '' })

const loadData = async () => {
  const params = { page: page.value }
  if (query.class_ref) params.class_ref = query.class_ref
  if (query.search) params.search = query.search
  const data = await request.get('/students/', { params })
  list.value = data.results
  total.value = data.count
}

const loadClasses = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { student_no: '', name: '', gender: 'male', age: null, class_ref: null, phone: '', email: '', address: '', password: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { student_no: row.student_no, name: row.name, gender: row.gender, age: row.age, class_ref: row.class_ref, phone: row.phone, email: row.email, address: row.address })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/students/${editId.value}/`, form)
    dialogVisible.value = false
    ElMessage.success('修改成功')
  } else {
    const res = await request.post('/students/', form)
    dialogVisible.value = false
    ElMessageBox.alert(
      `用户名：${res.username}\n密码：${res.password}`,
      '新增成功 — 登录凭证',
      { confirmButtonText: '我知道了', type: 'success' },
    )
  }
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该学生？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/students/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

const handleExport = () => {
  window.open('/api/students/export/', '_blank')
}

const handleImport = async (file) => {
  const fd = new FormData()
  fd.append('file', file)
  await request.post('/students/import/', fd)
  ElMessage.success('导入完成')
  loadData()
  return false
}

const showResetPwd = (row) => {
  resetPwdTarget.value = row
  resetPwdForm.new_password = ''
  resetPwdVisible.value = true
}

const handleResetPwd = async () => {
  if (resetPwdForm.new_password.length < 6) {
    ElMessage.warning('密码长度不能少于6位')
    return
  }
  await request.put('/auth/reset-password/', {
    user_id: resetPwdTarget.value.user,
    new_password: resetPwdForm.new_password,
  })
  ElMessage.success('密码重置成功')
  resetPwdVisible.value = false
}

onMounted(() => { loadData(); loadClasses() })
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ===== 搜索卡片 ===== */
.search-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.search-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-label {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
}

.search-input {
  width: 180px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #e8e8e8 inset;
}

.search-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #b7d9c8 inset;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(183, 217, 200, 0.4) inset;
}

.search-right {
  display: flex;
  gap: 10px;
}

/* ===== 主题色按钮 ===== */
.btn-primary {
  background: linear-gradient(135deg, #6388a0 0%, #7a9ab4 100%);
  border: none;
  border-radius: 8px;
  color: #fff;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #577a92 0%, #6388a0 100%);
}

.btn-mint {
  background: linear-gradient(135deg, #b7d9c8 0%, #c8e6d6 100%);
  border: none;
  border-radius: 8px;
  color: #3a6b52;
}

.btn-mint:hover {
  background: linear-gradient(135deg, #a8cebb 0%, #b7d9c8 100%);
}

.btn-lavender {
  background: linear-gradient(135deg, #c5b8d9 0%, #d4c8e6 100%);
  border: none;
  border-radius: 8px;
  color: #5a4a72;
}

.btn-lavender:hover {
  background: linear-gradient(135deg, #b8a8ce 0%, #c5b8d9 100%);
}

.btn-pink {
  background: linear-gradient(135deg, #e9c9bc 0%, #f2ddd3 100%);
  border: none;
  border-radius: 8px;
  color: #8a5a48;
}

.btn-pink:hover {
  background: linear-gradient(135deg, #debbad 0%, #e9c9bc 100%);
}

/* ===== 表格卡片 ===== */
.table-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.045);
}

.table-card :deep(.el-table) {
  border-radius: 10px;
  overflow: hidden;
}

.table-card :deep(.el-table th.el-table__cell) {
  background: rgba(99, 136, 160, 0.08) !important;
  color: #3a4f63;
  font-weight: 600;
  font-size: 13px;
  border-bottom: 1px solid rgba(99, 136, 160, 0.12);
}

.table-card :deep(.el-table td.el-table__cell) {
  font-size: 13px;
  color: #555;
  border-bottom: 1px solid #f5f5f5;
}

.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) {
  background: rgba(183, 217, 200, 0.08) !important;
}

.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background: #fafbfc;
}

/* 性别标签 */
.gender-tag {
  display: inline-block;
  width: 26px;
  height: 22px;
  line-height: 22px;
  text-align: center;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.gender-tag.male {
  background: rgba(99, 136, 160, 0.1);
  color: #6388a0;
}

.gender-tag.female {
  background: rgba(233, 201, 188, 0.2);
  color: #c4887a;
}

/* 状态标签 */
.status-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.normal {
  background: rgba(183, 217, 200, 0.2);
  color: #5a9a78;
}

.status-tag.pending {
  background: rgba(233, 201, 188, 0.2);
  color: #c4887a;
}

/* 操作按钮 */
.btn-edit {
  background: rgba(99, 136, 160, 0.1);
  border: none;
  color: #6388a0;
  border-radius: 6px;
}

.btn-edit:hover {
  background: #6388a0;
  color: #fff;
}

.btn-warn {
  background: rgba(233, 201, 188, 0.2);
  border: none;
  color: #c4887a;
  border-radius: 6px;
}

.btn-warn:hover {
  background: #e9c9bc;
  color: #8a5a48;
}

.btn-delete {
  background: rgba(233, 201, 188, 0.2);
  border: none;
  color: #c4887a;
  border-radius: 6px;
}

.btn-delete:hover {
  background: #e9c9bc;
  color: #8a5a48;
}

/* ===== 分页 ===== */
.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 18px;
}

.pagination-wrap :deep(.el-pagination) {
  --el-pagination-bg-color: transparent;
  --el-pagination-hover-color: #b7d9c8;
}

.pagination-wrap :deep(.el-pager li.is-active) {
  background-color: #b7d9c8 !important;
  color: #fff !important;
  border-radius: 6px;
}

.pagination-wrap :deep(.el-pager li) {
  border-radius: 6px;
  min-width: 32px;
}

/* ===== 弹窗 ===== */
.custom-dialog :deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

.custom-dialog :deep(.el-dialog__header) {
  background: rgba(99, 136, 160, 0.06);
  padding: 16px 24px;
  margin: 0;
}

.custom-dialog :deep(.el-dialog__title) {
  font-size: 15px;
  font-weight: 600;
  color: #3a4f63;
}

.custom-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.dialog-form :deep(.el-input__wrapper) {
  border-radius: 8px;
}

.dialog-form :deep(.el-select .el-input__wrapper) {
  border-radius: 8px;
}

.btn-cancel {
  border-radius: 8px;
}

.btn-submit {
  background: linear-gradient(135deg, #6388a0 0%, #7a9ab4 100%);
  border: none;
  border-radius: 8px;
}

.btn-submit:hover {
  background: linear-gradient(135deg, #577a92 0%, #6388a0 100%);
}
</style>
