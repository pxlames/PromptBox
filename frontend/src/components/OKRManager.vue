<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { api, type OKR, type OKRCreate, type OKRUpdate, type Task, type TaskCreate, type TaskUpdate } from '../api'

// 状态
const okrs = ref<OKR[]>([])
const tasks = ref<Record<number, Task[]>>({})  // 按OKR ID存储任务列表
const loading = ref(false)
const error = ref<string | null>(null)

// 表单状态
const showOkrForm = ref(false)
const showTaskForm = ref(false)
const okrForm = ref<OKRCreate>({ objective: '', due_date: undefined })
const taskForm = ref<TaskCreate>({ okr_id: 0, title: '', description: '' })
const editingOkrId = ref<number | null>(null)
const editingTaskId = ref<number | null>(null)
const currentOkrForTask = ref<number | null>(null)

// 计算属性
const okrsWithTasks = computed(() => {
  return okrs.value.map(okr => ({
    ...okr,
    tasks: tasks.value[okr.id] || []
  }))
})

// 加载OKR列表
async function loadOkrs() {
  try {
    loading.value = true
    okrs.value = await api.getOkrs()
    // 加载每个OKR的任务
    for (const okr of okrs.value) {
      await loadTasks(okr.id)
    }
  } catch (e: any) {
    error.value = e?.message || '加载OKR失败'
  } finally {
    loading.value = false
  }
}

// 加载指定OKR的任务
async function loadTasks(okrId: number) {
  try {
    tasks.value[okrId] = await api.getTasksByOkr(okrId)
  } catch (e: any) {
    console.error(`加载OKR ${okrId} 的任务失败:`, e)
  }
}

// OKR操作
async function submitOkr() {
  try {
    if (!okrForm.value.objective.trim()) {
      alert('请输入目标')
      return
    }

    const dueDate = okrForm.value.due_date || undefined

    if (editingOkrId.value) {
      const data: OKRUpdate = {
        objective: okrForm.value.objective,
        due_date: dueDate
      }
      const updated = await api.updateOkr(editingOkrId.value, data)
      const idx = okrs.value.findIndex(o => o.id === editingOkrId.value)
      if (idx >= 0) okrs.value[idx] = updated
    } else {
      const data: OKRCreate = {
        objective: okrForm.value.objective,
        due_date: dueDate
      }
      const created = await api.createOkr(data)
      okrs.value.unshift(created)
      tasks.value[created.id] = []
    }

    resetOkrForm()
    showOkrForm.value = false
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editOkr(okr: OKR) {
  editingOkrId.value = okr.id
  okrForm.value.objective = okr.objective
  okrForm.value.due_date = okr.due_date || undefined
  showOkrForm.value = true
}

function resetOkrForm() {
  editingOkrId.value = null
  okrForm.value = { objective: '', due_date: undefined }
}

async function deleteOkr(id: number) {
  if (!confirm('确定删除这个OKR？所有关联的任务也会被删除。')) return
  try {
    await api.deleteOkr(id)
    okrs.value = okrs.value.filter(o => o.id !== id)
    delete tasks.value[id]
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

async function toggleOkrCompleted(okr: OKR) {
  try {
    const updated = await api.toggleOkr(okr.id, !okr.completed)
    const idx = okrs.value.findIndex(o => o.id === okr.id)
    if (idx >= 0) okrs.value[idx] = updated
  } catch (e: any) {
    alert(e?.message || '更新失败')
  }
}

// 任务操作
function showAddTaskForm(okrId: number) {
  currentOkrForTask.value = okrId
  taskForm.value = { okr_id: okrId, title: '', description: '' }
  editingTaskId.value = null
  showTaskForm.value = true
}

async function submitTask() {
  try {
    if (!taskForm.value.title.trim()) {
      alert('请输入任务标题')
      return
    }

    if (editingTaskId.value) {
      const data: TaskUpdate = {
        title: taskForm.value.title,
        description: taskForm.value.description || undefined
      }
      const updated = await api.updateTask(editingTaskId.value, data)
      // 更新任务列表
      if (updated) {
        const okrId = updated.okr_id
        if (tasks.value[okrId]) {
          const idx = tasks.value[okrId].findIndex(t => t.id === updated.id)
          if (idx >= 0) tasks.value[okrId][idx] = updated
        }
      }
    } else {
      if (!currentOkrForTask.value) {
        alert('请先选择OKR')
        return
      }
      const data: TaskCreate = {
        okr_id: currentOkrForTask.value,
        title: taskForm.value.title,
        description: taskForm.value.description || undefined
      }
      const created = await api.createTask(data)
      if (!tasks.value[created.okr_id]) {
        tasks.value[created.okr_id] = []
      }
      tasks.value[created.okr_id].unshift(created)
    }

    resetTaskForm()
    showTaskForm.value = false
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editTask(task: Task) {
  editingTaskId.value = task.id
  currentOkrForTask.value = task.okr_id
  taskForm.value = {
    okr_id: task.okr_id,
    title: task.title,
    description: task.description || ''
  }
  showTaskForm.value = true
}

function resetTaskForm() {
  editingTaskId.value = null
  currentOkrForTask.value = null
  taskForm.value = { okr_id: 0, title: '', description: '' }
}

async function deleteTask(id: number, okrId: number) {
  if (!confirm('确定删除这个任务？')) return
  try {
    await api.deleteTask(id)
    if (tasks.value[okrId]) {
      tasks.value[okrId] = tasks.value[okrId].filter(t => t.id !== id)
    }
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

async function toggleTaskCompleted(task: Task) {
  try {
    const updated = await api.toggleTask(task.id, !task.completed)
    if (updated && tasks.value[updated.okr_id]) {
      const idx = tasks.value[updated.okr_id].findIndex(t => t.id === updated.id)
      if (idx >= 0) tasks.value[updated.okr_id][idx] = updated
    }
  } catch (e: any) {
    alert(e?.message || '更新失败')
  }
}

// 格式化日期
function formatDate(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 格式化日期时间
function formatDateTime(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

// 检查是否过期
function isOverdue(dueDate?: string) {
  if (!dueDate) return false
  return new Date(dueDate) < new Date()
}

onMounted(async () => {
  await api.ready()
  await loadOkrs()
})
</script>

<template>
  <div class="page">
    <div class="internal-nav">
      <nav class="tabs">
        <button :class="{ active: !showOkrForm && !showTaskForm }" @click="showOkrForm = false; showTaskForm = false">
          📋 OKR列表
        </button>
        <button :class="{ active: showOkrForm }" @click="resetOkrForm(); showOkrForm = true; showTaskForm = false">
          ➕ 新增OKR
        </button>
      </nav>
    </div>

    <main class="main">
      <!-- OKR列表 -->
      <section v-show="!showOkrForm && !showTaskForm" class="panel">
        <div class="section-header">
          <h2>🎯 OKR管理</h2>
          <p>目标与关键结果管理，追踪你的工作进度</p>
        </div>

        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="okrs.length === 0" class="empty">
          <div class="empty-icon">🎯</div>
          <p>暂无OKR记录</p>
          <small>点击"新增OKR"按钮开始添加</small>
        </div>
        <div v-else class="okr-list">
          <div v-for="okr in okrsWithTasks" :key="okr.id" class="okr-item" :class="{ completed: okr.completed }">
            <div class="okr-header">
              <div class="okr-checkbox">
                <input 
                  type="checkbox" 
                  :checked="okr.completed"
                  @change="toggleOkrCompleted(okr)"
                />
              </div>
              <div class="okr-content">
                <h3 class="okr-objective" :class="{ completed: okr.completed }">
                  {{ okr.objective }}
                </h3>
                <div class="okr-meta">
                  <span v-if="okr.due_date" class="okr-due-date" :class="{ overdue: isOverdue(okr.due_date) }">
                    📅 {{ formatDate(okr.due_date) }}
                    <span v-if="isOverdue(okr.due_date) && !okr.completed" class="overdue-label">已过期</span>
                  </span>
                  <span class="okr-created">创建于 {{ formatDateTime(okr.created_at) }}</span>
                </div>
              </div>
              <div class="okr-actions">
                <button class="btn-small btn-add-task" @click="showAddTaskForm(okr.id)">➕ 添加任务</button>
                <button class="btn-small btn-edit" @click="editOkr(okr)">编辑</button>
                <button class="btn-small btn-delete" @click="deleteOkr(okr.id)">删除</button>
              </div>
            </div>

            <!-- 任务列表 -->
            <div v-if="okr.tasks && okr.tasks.length > 0" class="task-list">
              <div v-for="task in okr.tasks" :key="task.id" class="task-item" :class="{ completed: task.completed }">
                <div class="task-content">
                  <div class="task-checkbox">
                    <input 
                      type="checkbox" 
                      :checked="task.completed"
                      @change="toggleTaskCompleted(task)"
                    />
                  </div>
                  <div class="task-info">
                    <div class="task-title" :class="{ completed: task.completed }">
                      {{ task.title }}
                    </div>
                    <div v-if="task.description" class="task-description">
                      {{ task.description }}
                    </div>
                  </div>
                </div>
                <div class="task-actions">
                  <button class="btn-tiny btn-edit" @click="editTask(task)">编辑</button>
                  <button class="btn-tiny btn-delete" @click="deleteTask(task.id, okr.id)">删除</button>
                </div>
              </div>
            </div>
            <div v-else class="task-empty">
              <small>暂无任务，点击"添加任务"开始</small>
            </div>
          </div>
        </div>
      </section>

      <!-- 新增/编辑OKR表单 -->
      <section v-show="showOkrForm" class="panel create-panel">
        <div class="section-header">
          <h2>{{ editingOkrId ? '编辑OKR' : '新增OKR' }}</h2>
        </div>

        <form @submit.prevent="submitOkr" class="form card">
          <div class="form-group">
            <label>目标 (Objective) *</label>
            <input 
              v-model="okrForm.objective" 
              required 
              maxlength="500"
              placeholder="输入你的目标，例如：完成前端项目重构"
            />
          </div>

          <div class="form-group">
            <label>截止日期</label>
            <input 
              type="date"
              v-model="okrForm.due_date"
              placeholder="选择截止日期（可选）"
            />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">
              {{ editingOkrId ? '保存修改' : '创建OKR' }}
            </button>
            <button type="button" class="btn-secondary" @click="resetOkrForm(); showOkrForm = false">
              取消
            </button>
          </div>
        </form>
      </section>

      <!-- 新增/编辑任务表单 -->
      <section v-show="showTaskForm" class="panel create-panel">
        <div class="section-header">
          <h2>{{ editingTaskId ? '编辑任务' : '新增任务' }}</h2>
        </div>

        <form @submit.prevent="submitTask" class="form card">
          <div class="form-group">
            <label>任务标题 *</label>
            <input 
              v-model="taskForm.title" 
              required 
              maxlength="500"
              placeholder="输入任务标题"
            />
          </div>

          <div class="form-group">
            <label>任务描述</label>
            <textarea 
              v-model="taskForm.description" 
              rows="4"
              placeholder="输入任务详细描述（可选）"
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary">
              {{ editingTaskId ? '保存修改' : '创建任务' }}
            </button>
            <button type="button" class="btn-secondary" @click="resetTaskForm(); showTaskForm = false">
              取消
            </button>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: transparent;
}

.internal-nav {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  padding: 0 24px;
}

.tabs {
  display: flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.6);
  padding: 4px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.tabs button {
  background: transparent;
  color: #64748b;
  border: 1px solid transparent;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.tabs button:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #334155;
}

.tabs button.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.main {
  padding: 0 24px 24px;
  overflow: auto;
  flex: 1;
}

.panel {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.section-header h2 {
  color: #1e293b;
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: 600;
}

.section-header p {
  color: #64748b;
  margin: 0;
  font-size: 16px;
}

.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.06);
}

.empty {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty p {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 500;
}

.empty small {
  font-size: 14px;
  opacity: 0.8;
}

.loading, .error {
  text-align: center;
  padding: 40px 20px;
  font-size: 16px;
}

.error {
  color: #ef4444;
}

.okr-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.okr-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 2px solid #e5e7eb;
  transition: all 0.2s ease;
}

.okr-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.okr-item.completed {
  border-color: #10b981;
  background: #f0fdf4;
}

.okr-header {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
}

.okr-checkbox {
  margin-top: 4px;
}

.okr-checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.okr-content {
  flex: 1;
}

.okr-objective {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.okr-objective.completed {
  text-decoration: line-through;
  color: #94a3b8;
}

.okr-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #64748b;
  flex-wrap: wrap;
}

.okr-due-date {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.okr-due-date.overdue {
  color: #ef4444;
  font-weight: 500;
}

.overdue-label {
  background: #fee2e2;
  color: #dc2626;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-left: 4px;
}

.okr-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.task-list {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.task-item.completed {
  background: #f0fdf4;
  border-color: #d1fae5;
}

.task-content {
  display: flex;
  gap: 12px;
  flex: 1;
}

.task-checkbox {
  margin-top: 2px;
}

.task-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.task-info {
  flex: 1;
}

.task-title {
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 4px;
}

.task-title.completed {
  text-decoration: line-through;
  color: #94a3b8;
}

.task-description {
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
}

.task-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.task-empty {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.form-group label {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  background: #fff;
  color: #111;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: rgba(0, 0, 0, 0.05);
  color: #64748b;
}

.btn-secondary:hover {
  background: rgba(0, 0, 0, 0.1);
}

.btn-small,
.btn-tiny {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-tiny {
  padding: 4px 8px;
  font-size: 11px;
}

.btn-add-task {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.btn-add-task:hover {
  background: rgba(102, 126, 234, 0.2);
}

.btn-edit {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.btn-edit:hover {
  background: rgba(59, 130, 246, 0.2);
}

.btn-delete {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.2);
}

.create-panel {
  max-width: 600px;
}

@media (max-width: 768px) {
  .main {
    padding: 0 16px 16px;
  }

  .okr-header {
    flex-direction: column;
    gap: 12px;
  }

  .okr-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .task-item {
    flex-direction: column;
    gap: 8px;
  }

  .task-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>

