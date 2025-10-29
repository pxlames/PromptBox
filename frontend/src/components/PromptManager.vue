<script setup lang="ts">
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { api, type Prompt, type PromptCreate, type PromptUpdate } from '../api'

// 状态
const activeTab = ref<'list' | 'create'>('list')

const prompts = ref<Prompt[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// 查询/分页/排序
const query = ref('')
const sort = ref<'created_at:desc' | 'created_at:asc' | 'updated_at:desc' | 'updated_at:asc' | 'title:asc' | 'title:desc'>('created_at:desc')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const baseIndex = computed(() => (page.value - 1) * pageSize.value)

// 表单
const form = ref<PromptCreate>({ title: '', content: '', tags: '' })
const editingId = ref<number | null>(null)
const showDetail = ref(false)
const detailPrompt = ref<Prompt | null>(null)

function openDetail(p: Prompt) {
  detailPrompt.value = p
  showDetail.value = true
}

function closeDetail() {
  showDetail.value = false
  detailPrompt.value = null
}

function onEsc(e: KeyboardEvent) {
  if (e.key === 'Escape' && showDetail.value) closeDetail()
}
onMounted(() => window.addEventListener('keydown', onEsc))
onBeforeUnmount(() => window.removeEventListener('keydown', onEsc))

function truncate(text: string, n = 200) {
  if (!text) return ''
  return text.length > n ? text.slice(0, n) + '…' : text
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const skip = (page.value - 1) * pageSize.value
    prompts.value = await api.list({ skip, limit: pageSize.value, q: query.value || null, sort: sort.value })
    const cnt = await api.count(query.value || null)
    total.value = cnt.total
  } catch (e: any) {
    error.value = e?.message || '加载失败'
  } finally {
    loading.value = false
  }
}

async function submit() {
  try {
    if (editingId.value) {
      const data: PromptUpdate = { ...form.value }
      const updated = await api.update(editingId.value, data)
      const idx = prompts.value.findIndex(p => p.id === editingId.value)
      if (idx >= 0) prompts.value[idx] = updated
    } else {
      const created = await api.create(form.value)
      // 新增成功后刷新列表统计
      page.value = 1
      prompts.value.unshift(created)
      const cnt = await api.count(query.value || null)
      total.value = cnt.total
    }
    reset()
    activeTab.value = 'list'
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function edit(p: Prompt) {
  activeTab.value = 'create'
  editingId.value = p.id
  form.value = { title: p.title, content: p.content, tags: p.tags || '' }
}

function reset() {
  editingId.value = null
  form.value = { title: '', content: '', tags: '' }
}

async function removeItem(id: number) {
  if (!confirm('确定删除该Prompt？')) return
  try {
    await api.remove(id)
    prompts.value = prompts.value.filter(p => p.id !== id)
    const cnt = await api.count(query.value || null)
    total.value = cnt.total
    if (page.value > totalPages.value) {
      page.value = totalPages.value
      await load()
    }
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

onMounted(async () => {
  // 等待前端运行时配置加载完成后，再发起首个查询，避免 BASE_URL 仍是默认值
  await api.ready()
  await load()
})

function search() {
  page.value = 1
  load()
}

function changeSort(v: string) {
  sort.value = v as any
  page.value = 1
  load()
}

function goto(p: number) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  load()
}

async function copyText(text: string) {
  try {
    await navigator.clipboard.writeText(text)
    alert('已复制到剪贴板')
  } catch {
    alert('复制失败')
  }
}
</script>

<template>
  <div class="page">
    <!-- 内部导航栏 -->
    <div class="internal-nav">
      <nav class="tabs">
        <button :class="{ active: activeTab==='list' }" @click="activeTab='list'">📋 查询</button>
        <button :class="{ active: activeTab==='create' }" @click="activeTab='create'">➕ 新增</button>
      </nav>
    </div>

    <main class="main">
      <!-- 查询 Tab -->
      <section v-show="activeTab==='list'" class="panel">
        <div class="toolbar card">
          <input class="search" v-model="query" placeholder="搜索标题/标签/内容" @keyup.enter="search" />
          <select class="select" v-model="sort" @change="changeSort(($event.target as HTMLSelectElement).value)">
            <option value="created_at:desc">创建时间 ↓</option>
            <option value="created_at:asc">创建时间 ↑</option>
            <option value="updated_at:desc">更新时间 ↓</option>
            <option value="updated_at:asc">更新时间 ↑</option>
            <option value="title:asc">标题 A→Z</option>
            <option value="title:desc">标题 Z→A</option>
          </select>
          <button class="primary" @click="search">查询</button>
        </div>

        <div class="list card">
          <div class="list-head">
            <div>#</div>
            <div>标题</div>
            <div>内容</div>
            <div>标签</div>
            <div>创建时间</div>
            <div>操作</div>
          </div>
          <div v-if="loading" class="empty">加载中...</div>
          <div v-else-if="error" class="empty error">{{ error }}</div>
          <div v-else>
            <div v-if="prompts.length === 0" class="empty">暂无数据</div>
            <div v-for="(p, i) in prompts" :key="p.id" class="list-row">
              <div class="idx">{{ baseIndex + i + 1 }}</div>
              <div class="title" @click="openDetail(p)" title="点击查看详情">
                <div class="t">{{ truncate(p.title, 30) }}</div> <!-- 简短标题，仅30字 -->
              </div>
              <div class="content" @click="openDetail(p)">
                <div class="c multiline">{{ p.content }}</div> <!-- 新增内容列，展示正文，多行换行 -->
              </div>
              <div>{{ p.tags }}</div>
              <div>{{ new Date(p.created_at).toLocaleString() }}</div>
              <div class="ops">
                <button class="ghost" @click.stop="edit(p)">编辑</button>
                <button class="secondary" @click.stop="copyText(p.content)">复制</button>
                <button class="danger" @click.stop="removeItem(p.id)">删除</button>
              </div>
            </div>

            <div class="pager">
              <button :disabled="page===1" @click="goto(page-1)">上一页</button>
              <span>第 {{ page }} / {{ totalPages }} 页（共 {{ total }} 条）</span>
              <button :disabled="page>=totalPages" @click="goto(page+1)">下一页</button>
            </div>
          </div>
        </div>
      </section>

      <!-- 新增 Tab -->
      <section v-show="activeTab==='create'" class="panel create-panel">
        <form class="form card" @submit.prevent="submit">
          <div class="row">
            <label>标题</label>
            <input v-model="form.title" required maxlength="200" placeholder="请输入标题" />
          </div>
          <div class="row">
            <label>标签</label>
            <input v-model="form.tags" placeholder="逗号分隔，如: chat,code" />
          </div>
          <div class="row">
            <label>内容</label>
            <textarea v-model="form.content" required rows="12" placeholder="请输入Prompt内容" />
          </div>
          <div class="actions">
            <button class="primary" type="submit">{{ editingId ? '保存修改' : '新增' }}</button>
            <button class="ghost" type="button" @click="reset">重置</button>
          </div>
        </form>
      </section>
    </main>
    
    <!-- 浮动详情弹层 -->
    <div v-if="showDetail" class="modal" @click.self="closeDetail">
      <div class="modal-body">
        <div class="modal-head">
          <div class="badge">#{{ detailPrompt ? prompts.findIndex(x=>x.id===detailPrompt.id) + baseIndex + 1 : '' }}</div>
          <div class="modal-title">{{ detailPrompt?.title }}</div>
          <button class="ghost close" @click="closeDetail">✕</button>
        </div>
        <div class="modal-meta">
          <span>{{ detailPrompt?.tags }}</span>
          <span>创建于 {{ detailPrompt ? new Date(detailPrompt.created_at).toLocaleString() : '' }}</span>
        </div>
        <pre class="modal-content">{{ detailPrompt?.content }}</pre>
        <div class="modal-actions">
          <button class="secondary" @click="detailPrompt && copyText(detailPrompt.content)">复制内容</button>
          <button class="ghost" @click="closeDetail">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面布局 */
.page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: transparent;
}

/* 内部导航栏 */
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
.panel { width: 100%; max-width: none; margin: 0; }

.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(16,24,40,0.06);
}

/* 工具栏与列表 */
.toolbar { display: grid; grid-template-columns: 1fr 200px 100px; gap: 10px; align-items: center; margin-bottom: 16px; }
.toolbar .search, .toolbar .select { height: 38px; }

.list { overflow-x: auto; }
.list-head, .list-row {
  display: grid;
  grid-template-columns: 60px 1.4fr 3fr 1fr 1.2fr 180px; /* 新增“内容”列后调整比例，操作列固定 */
  gap: 12px;
  align-items: start;
}
.list-head { font-weight: 600; color: #374151; margin-bottom: 8px; }
.list-row { padding: 14px 12px; margin-bottom: 10px; border: 1px solid #eef2f7; background: #ffffff; border-radius: 10px; box-shadow: 0 1px 2px rgba(16,24,40,0.04); }
.idx { font-weight: 700; color: #6b7280; align-self: center; }
.title .t { font-weight: 600; margin-bottom: 6px; color: #111; /* 标题使用黑色 */ }
.title .c { color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.content .c.multiline { color: #64748b; white-space: pre-wrap; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; }
.ops { display: flex; gap: 8px; justify-content: flex-end; align-items: center; }
.list-head > :last-child { justify-self: end; }

/* 表单 */
.form .row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
label { font-size: 13px; color: #334155; }
input, textarea, select {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  background: #fff;
  color: #111; /* 强制深色文字，避免被全局暗色主题影响 */
  caret-color: #111; /* 输入光标颜色 */
}
/* 占位符颜色，增强对比度 */
input::placeholder, textarea::placeholder { color: #9ca3af; }

/* 按钮样式 */
button { border: none; border-radius: 8px; padding: 8px 12px; cursor: pointer; }
button.primary { background: #2563eb; color: #fff; }
button.secondary { background: #6b7280; color: #fff; }
button.ghost { background: #fff; color: #0f172a; border: 1px solid #e2e8f0; }
button.danger { background: #ef4444; color: #fff; }
button:disabled { opacity: 0.6; cursor: not-allowed; }

/* 其它 */
.empty { padding: 16px; color: #64748b; }
.error { color: #b91c1c; }
.pager { display: flex; gap: 12px; align-items: center; padding: 12px 0; }

/* 响应式：小屏堆叠 */
@media (max-width: 960px) {
  .toolbar { grid-template-columns: 1fr; }
  .list-head { display: none; }
  .list-row { grid-template-columns: 1fr; }
  .ops { justify-content: flex-end; }
}

@media (max-width: 600px) {
  .panel { margin: 0; }
  .main { padding: 12px; }
  .card { padding: 12px; }
  textarea { min-height: 160px; }
}

/* 新增面板：水平居中与更醒目字体 */
.create-panel { display: grid; grid-template-columns: 1fr min(1100px, 92vw) 1fr; }
.create-panel > .form { grid-column: 2; }
.create-panel .form .row label { font-size: 15px; }
.create-panel input, .create-panel textarea { font-size: 16px; color: #111; background: #fff; }
.create-panel .actions button { font-size: 16px; height: 40px; }

/* 弹层 */
.modal { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); display: grid; place-items: center; z-index: 50; }
.modal-body { width: min(960px, 92vw); max-height: 86vh; overflow: auto; background: #fff; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 10px 30px rgba(0,0,0,0.18); padding: 16px 18px; color: #111; /* 强制深色文字，避免继承全局浅色 */ }
.modal-head { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 10px; }
.badge { background: #eef2ff; color: #3b82f6; font-weight: 700; border-radius: 6px; padding: 4px 8px; }
.modal-title { font-size: 18px; font-weight: 700; color: #111827; }
.modal-meta { color: #6b7280; display: flex; gap: 12px; margin: 8px 0 12px; flex-wrap: wrap; }
.modal-content { white-space: pre-wrap; background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; color: #111; /* 内容文字深色 */ }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 12px; }
.close { font-size: 18px; line-height: 1; padding: 6px 10px; }
</style>

