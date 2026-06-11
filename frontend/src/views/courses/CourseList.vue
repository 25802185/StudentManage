<template>
  <div class="page-container">
    <!-- 操作栏 -->
    <div class="search-card">
      <div class="search-left">
        <div class="search-item">
          <label class="search-label">班级</label>
          <el-select v-model="query.class_ref" placeholder="全部班级" clearable @change="loadData" class="search-input">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </div>
      </div>
      <div class="search-right">
        <el-button class="btn-mint" @click="showAdd">
          <el-icon><Plus /></el-icon>新增课程
        </el-button>
      </div>
    </div>

    <!-- 表格卡片 -->
    <div class="table-card">
      <el-table :data="list" style="width: 100%">
        <el-table-column prop="name" label="课程名称" min-width="160" />
        <el-table-column prop="credit" label="学分" width="80">
          <template #default="{ row }">
            <span class="credit-badge">{{ row.credit }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="class_name" label="班级" min-width="160" />
        <el-table-column prop="semester_name" label="学期" width="130" />
        <el-table-column prop="teacher_name" label="授课教师" width="100" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" class="btn-edit" @click="showEdit(row)">编辑</el-button>
            <el-button size="small" class="btn-mint-sm" @click="$router.push(`/scores/entry/${row.id}`)">录入成绩</el-button>
            <el-button size="small" class="btn-delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination v-model:current-page="page" :total="total" :page-size="10" layout="prev, pager, next" background @current-change="loadData" />
      </div>
    </div>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑课程' : '新增课程'" width="520px" class="custom-dialog">
      <el-form :model="form" label-width="80px" class="dialog-form">
        <el-form-item label="课程名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="学分"><el-input-number v-model="form.credit" :min="0.5" :step="0.5" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级" style="width: 100%">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="学期">
          <el-select v-model="form.semester" placeholder="选择学期" style="width: 100%">
            <el-option v-for="s in semesterOptions" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="form.teacher" placeholder="选择教师" clearable style="width: 100%">
            <el-option v-for="t in teacherList" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" class="btn-cancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit" class="btn-submit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import request from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const semesterOptions = ref([])

const list = ref([])
const total = ref(0)
const page = ref(1)
const classList = ref([])
const teacherList = ref([])
const query = reactive({ class_ref: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', credit: 1, class_ref: null, teacher: null, semester: null, description: '' })

const loadData = async () => {
  const params = { page: page.value }
  if (query.class_ref) params.class_ref = query.class_ref
  const data = await request.get('/courses/', { params })
  list.value = data.results
  total.value = data.count
}

const loadOptions = async () => {
  const [c, t, s] = await Promise.all([
    request.get('/classes/', { params: { page_size: 100 } }),
    request.get('/teachers/', { params: { page_size: 100 } }),
    request.get('/courses/semesters/'),
  ])
  classList.value = c.results
  teacherList.value = t.results
  semesterOptions.value = s.results || s
}

const showAdd = () => {
  isEdit.value = false
  const current = semesterOptions.value.find(s => s.is_current)
  Object.assign(form, { name: '', credit: 1, class_ref: null, teacher: null, semester: current ? current.id : null, description: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, credit: row.credit, class_ref: row.class_ref, teacher: row.teacher, semester: row.semester, description: row.description })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/courses/${editId.value}/`, form)
  } else {
    await request.post('/courses/', form)
  }
  dialogVisible.value = false
  ElMessage.success(isEdit.value ? '修改成功' : '新增成功')
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该课程？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/courses/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(() => { loadData(); loadOptions() })
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
.search-input :deep(.el-select .el-input__wrapper) { border-radius: 8px; }
.card-title-sm { font-size: 14px; font-weight: 600; color: #3a4f63; }
.search-right { display: flex; gap: 10px; }

.btn-mint { background: linear-gradient(135deg, #b7d9c8, #c8e6d6); border: none; border-radius: 8px; color: #3a6b52; }
.btn-mint:hover { background: linear-gradient(135deg, #a8cebb, #b7d9c8); }
.btn-mint-sm { background: rgba(183,217,200,0.2); border: none; color: #5a9a78; border-radius: 6px; }
.btn-mint-sm:hover { background: #b7d9c8; color: #3a6b52; }

.table-card { background: #fff; border-radius: 14px; padding: 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.045); }
.table-card :deep(.el-table) { border-radius: 10px; overflow: hidden; }
.table-card :deep(.el-table th.el-table__cell) { background: rgba(99,136,160,0.08) !important; color: #3a4f63; font-weight: 600; font-size: 13px; }
.table-card :deep(.el-table td.el-table__cell) { font-size: 13px; color: #555; border-bottom: 1px solid #f5f5f5; }
.table-card :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) { background: rgba(183,217,200,0.08) !important; }
.table-card :deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) { background: #fafbfc; }

.credit-badge { display: inline-block; min-width: 24px; height: 22px; line-height: 22px; text-align: center; background: rgba(197,184,217,0.2); color: #7a6299; border-radius: 10px; font-size: 12px; font-weight: 500; padding: 0 8px; }

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
