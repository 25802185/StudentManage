<template>
  <div>
    <el-button type="success" style="margin-bottom: 16px" @click="showAdd">新增课程</el-button>
    <el-table :data="list" border stripe>
      <el-table-column prop="name" label="课程名称" />
      <el-table-column prop="credit" label="学分" width="80" />
      <el-table-column prop="class_name" label="班级" />
      <el-table-column prop="teacher_name" label="授课教师" />
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="showEdit(row)">编辑</el-button>
          <el-button size="small" type="success" @click="$router.push(`/scores/entry/${row.id}`)">录入成绩</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑课程' : '新增课程'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="课程名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="学分"><el-input-number v-model="form.credit" :min="0.5" :step="0.5" /></el-form-item>
        <el-form-item label="班级">
          <el-select v-model="form.class_ref" placeholder="选择班级">
            <el-option v-for="c in classList" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="教师">
          <el-select v-model="form.teacher" placeholder="选择教师" clearable>
            <el-option v-for="t in teacherList" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
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
const classList = ref([])
const teacherList = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', credit: 1, class_ref: null, teacher: null, description: '' })

const loadData = async () => {
  const data = await request.get('/courses/')
  list.value = data.results
}

const loadOptions = async () => {
  const [c, t] = await Promise.all([
    request.get('/classes/', { params: { page_size: 100 } }),
    request.get('/teachers/', { params: { page_size: 100 } }),
  ])
  classList.value = c.results
  teacherList.value = t.results
}

const showAdd = () => {
  isEdit.value = false
  Object.assign(form, { name: '', credit: 1, class_ref: null, teacher: null, description: '' })
  dialogVisible.value = true
}

const showEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, { name: row.name, credit: row.credit, class_ref: row.class_ref, teacher: row.teacher, description: row.description })
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
  ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' }).then(async () => {
    await request.delete(`/courses/${row.id}/`)
    ElMessage.success('已删除')
    loadData()
  })
}

onMounted(() => { loadData(); loadOptions() })
</script>
