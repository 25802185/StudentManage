<template>
  <div class="page-container">
    <!-- 搜索栏 -->
    <div class="search-card">
      <div class="search-left">
        <div class="search-item">
          <label class="search-label">姓名</label>
          <el-input v-model="query.name" placeholder="请输入姓名" clearable @clear="loadData" class="search-input" />
        </div>
      </div>
      <div class="search-right">
        <el-button class="btn-primary" @click="loadData">
          <el-icon><Search /></el-icon>搜索
        </el-button>
        <el-button class="btn-mint" @click="showAdd">
          <el-icon><Plus /></el-icon>新增
        </el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="teacher_no" label="工号" width="120" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="gender" label="性别" width="70">
          <template #default="{ row }">
            <span class="gender-tag" :class="row.gender">{{ row.gender === 'male' ? '男' : '女' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="职称" width="100" />
        <el-table-column prop="class_name" label="所带班级" min-width="160" />
        <el-table-column prop="phone" label="电话" width="130" />
        <el-table-column prop="email" label="邮箱" min-width="160" />
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button size="small" class="btn-edit" @click="showEdit(row)">编辑</el-button>
            <el-button size="small" :class="row.is_active ? 'btn-warn' : 'btn-mint-sm'" @click="handleToggle(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button size="small" class="btn-warn" @click="showResetPwd(row)">重置密码</el-button>
            <el-button size="small" class="btn-delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination v-model:current-page="page" :total="total" layout="prev, pager, next" background @current-change="loadData" />
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑教师' : '新增教师'" width="520px" class="custom-dialog">
      <el-form :model="form" label-width="80px" class="dialog-form">
        <el-form-item label="工号"><el-input v-model="form.teacher_no" :disabled="isEdit" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="male">男</el-radio>
            <el-radio value="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="职称"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级" clearable style="width: 100%">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="密码" v-if="!isEdit">
          <el-input v-model="form.password" placeholder="留空则默认为工号后6位" show-password />
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
        <el-form-item label="教师">{{ resetPwdTarget?.name }}（{{ resetPwdTarget?.teacher_no }}）</el-form-item>
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
const query = reactive({ name: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const classList = ref([])
const form = reactive({ teacher_no: '', name: '', gender: 'male', title: '', class_ref: null, phone: '', email: '', password: '' })
const resetPwdVisible = ref(false)
const resetPwdTarget = ref(null)
const resetPwdForm = reactive({ new_password: '' })

const loadData = async () => {
  const params = { page: page.value }
  if (query.name) params.search = query.name
  const data = await request.get('/teachers/', { params })
  list.value = data.results
  total.value = data.count
}

const loadClasses = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { teacher_no: '', name: '', gender: 'male', title: '', class_ref: null, phone: '', email: '', password: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { teacher_no: row.teacher_no, name: row.name, gender: row.gender, title: row.title, class_ref: row.class_ref, phone: row.phone, email: row.email })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/teachers/${editId.value}/`, form)
    dialogVisible.value = false
    ElMessage.success('修改成功')
  } else {
    const res = await request.post('/teachers/', form)
    dialogVisible.value = false
    ElMessageBox.alert(
      `用户名：${res.username}\n密码：${res.password}`,
      '新增成功 — 登录凭证',
      { confirmButtonText: '我知道了', type: 'success' },
    )
  }
  loadData()
}

const handleToggle = async (row) => {
  await request.put(`/teachers/${row.id}/toggle/`)
  ElMessage.success('操作成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该教师？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/teachers/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
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
.page-container { display: flex; flex-direction: column; gap: 16px; }

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
.btn-mint { background: linear-gradient(135deg, #b7d9c8, #c8e6d6); border: none; border-radius: 8px; color: #3a6b52; }
.btn-mint:hover { background: linear-gradient(135deg, #a8cebb, #b7d9c8); }
.btn-mint-sm { background: rgba(183,217,200,0.2); border: none; color: #5a9a78; border-radius: 6px; }
.btn-mint-sm:hover { background: #b7d9c8; color: #3a6b52; }
.btn-warn { background: rgba(233,201,188,0.2); border: none; color: #c4887a; border-radius: 6px; }
.btn-warn:hover { background: #e9c9bc; color: #8a5a48; }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }
.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) { background: #fafbfc; }

.gender-tag { display: inline-block; width: 26px; height: 22px; line-height: 22px; text-align: center; border-radius: 6px; font-size: 12px; font-weight: 500; }
.gender-tag.male { background: rgba(99,136,160,0.1); color: #6388a0; }
.gender-tag.female { background: rgba(233,201,188,0.2); color: #c4887a; }

.btn-edit { background: rgba(99,136,160,0.1); border: none; color: #6388a0; border-radius: 6px; }
.btn-edit:hover { background: #6388a0; color: #fff; }
.btn-delete { background: rgba(233,201,188,0.2); border: none; color: #c4887a; border-radius: 6px; }
.btn-delete:hover { background: #e9c9bc; color: #8a5a48; }

.pagination-wrap { display: flex; justify-content: center; margin-top: 18px; }
.pagination-wrap :deep(.el-pager li.is-active) { background-color: #b7d9c8 !important; color: #fff !important; border-radius: 6px; }
.pagination-wrap :deep(.el-pager li) { border-radius: 6px; min-width: 32px; }

.custom-dialog :deep(.el-dialog) { border-radius: 16px; overflow: hidden; }
.custom-dialog :deep(.el-dialog__header) { background: rgba(99,136,160,0.06); padding: 16px 24px; margin: 0; }
.custom-dialog :deep(.el-dialog__title) { font-size: 15px; font-weight: 600; color: #3a4f63; }
.custom-dialog :deep(.el-dialog__body) { padding: 24px; }
.dialog-form :deep(.el-input__wrapper) { border-radius: 8px; }
.dialog-form :deep(.el-select .el-input__wrapper) { border-radius: 8px; }
.btn-cancel { border-radius: 8px; }
.btn-submit { background: linear-gradient(135deg, #6388a0, #7a9ab4); border: none; border-radius: 8px; }
.btn-submit:hover { background: linear-gradient(135deg, #577a92, #6388a0); }
</style>
