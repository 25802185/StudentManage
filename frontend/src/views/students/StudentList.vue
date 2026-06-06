<template>
  <div>
    <el-form inline style="margin-bottom: 16px">
      <el-form-item label="姓名">
        <el-input v-model="query.name" placeholder="搜索姓名" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item label="学号">
        <el-input v-model="query.student_no" placeholder="搜索学号" clearable @clear="loadData" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">搜索</el-button>
        <el-button type="success" @click="showAdd">新增学生</el-button>
        <el-button @click="handleExport">导出 Excel</el-button>
        <el-upload :show-file-list="false" :before-upload="handleImport" accept=".xlsx,.xls">
          <el-button>导入 Excel</el-button>
        </el-upload>
      </el-form-item>
    </el-form>

    <el-table :data="list" border stripe>
      <el-table-column prop="student_no" label="学号" width="120" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="gender" label="性别" width="60">
        <template #default="{ row }">{{ row.gender === 'male' ? '男' : '女' }}</template>
      </el-table-column>
      <el-table-column prop="class_name" label="班级" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'normal' ? 'success' : 'warning'">
            {{ row.status === 'normal' ? '正常' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 16px; justify-content: center"
      v-model:current-page="page"
      :page-size="10"
      :total="total"
      layout="prev, pager, next"
      @current-change="loadData"
    />

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑学生' : '新增学生'" width="500px">
      <el-form :model="form" label-width="80px">
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
          <el-select v-model="form.class_ref_id" placeholder="选择班级">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="地址"><el-input v-model="form.address" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
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
const query = reactive({ name: '', student_no: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const classList = ref([])
const form = reactive({
  student_no: '', name: '', gender: 'male', age: null,
  class_ref_id: null, phone: '', email: '', address: '',
})

const loadData = async () => {
  const data = await request.get('/students/', { params: { page: page.value, ...query } })
  list.value = data.results
  total.value = data.count
}

const loadClasses = async () => {
  const data = await request.get('/classes/', { params: { page_size: 100 } })
  classList.value = data.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { student_no: '', name: '', gender: 'male', age: null, class_ref_id: null, phone: '', email: '', address: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, gender: row.gender, age: row.age, class_ref_id: row.class_ref, phone: row.phone, email: row.email, address: row.address })
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (isEdit.value) {
    await request.put(`/students/${editId.value}/`, form)
    ElMessage.success('修改成功')
  } else {
    await request.post('/students/', form)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  loadData()
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
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

onMounted(() => { loadData(); loadClasses() })
</script>
