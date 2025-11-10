<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { api, type AlgoCategory, type AlgoProblem, type AlgoCategoryCreate, type AlgoProblemCreate, type AlgoProblemUpdate, type AlgoSolution, type AlgoSolutionCreate, type AlgoSolutionUpdate } from '../api'

type Difficulty = '简单' | '中等' | '困难'

const categories = ref<AlgoCategory[]>([])
const problems = ref<AlgoProblem[]>([])

const loading = ref(true)
const keyword = ref('')
const activeCategory = ref<number | 'all'>('all')
const filterDifficulty = ref<Difficulty | 'all'>('all')
const filterStatus = ref<'all' | '未开始' | '已掌握' | '再复习'>('all')

const showProblemForm = ref(false)
const editingProblemId = ref<number | null>(null)
const problemForm = ref<Omit<AlgoProblem, 'id'|'created_at'|'updated_at'>>({
  title: '',
  category_id: null,
  difficulty: '中等',
  companies: '',
  tags: '',
  status: '未开始',
  link: '',
  description: '',
  solution: ''
})

// 快速新增（仅描述 + 分类）
const quickDesc = ref('')
const quickCategoryId = ref<number | null>(null)

const showCategoryModal = ref(false)
const catName = ref('')
const editingCategoryId = ref<number | null>(null)

// 题解相关状态
const problemSolutions = ref<Record<number, AlgoSolution[]>>({})
const showSolutionModal = ref(false)
const editingSolutionId = ref<number | null>(null)
const currentProblemId = ref<number | null>(null)
const solutionForm = ref<Omit<AlgoSolution, 'id' | 'problem_id' | 'created_at' | 'updated_at'>>({
  title: '',
  content: '',
  language: '',
  complexity_time: '',
  complexity_space: '',
  order: 0
})
// 控制题解details的展开状态
const expandedSolutions = ref<Record<number, boolean>>({})

// 加载数据
async function loadCategories() {
  try {
    categories.value = await api.getAlgoCategories()
  } catch (error) {
    console.error('Failed to load categories:', error)
    alert('加载分类失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function loadProblems() {
  try {
    const params: any = {}
    if (activeCategory.value !== 'all') {
      params.category_id = activeCategory.value
    }
    if (filterDifficulty.value !== 'all') {
      params.difficulty = filterDifficulty.value
    }
    if (filterStatus.value !== 'all') {
      params.status = filterStatus.value
    }
    if (keyword.value.trim()) {
      params.keyword = keyword.value.trim()
    }
    problems.value = await api.getAlgoProblems(params)
  } catch (error) {
    console.error('Failed to load problems:', error)
    alert('加载题目失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function load() {
  loading.value = true
  try {
    await Promise.all([loadCategories(), loadProblems()])
    // 如果没有分类，初始化一些常见分类
    if (categories.value.length === 0) {
      const defaultCategories = ['数组', '链表', '二叉树', '动态规划', '图论']
      for (let i = 0; i < defaultCategories.length; i++) {
        try {
          await api.createAlgoCategory({ name: defaultCategories[i], order: i + 1 })
        } catch (error) {
          console.error('Failed to create default category:', error)
        }
      }
      await loadCategories()
    }
  } catch (error) {
    console.error('Failed to load data:', error)
    alert('加载数据失败：' + (error instanceof Error ? error.message : '未知错误'))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  load()
})

// 当筛选条件变化时重新加载题目
watch([activeCategory, filterDifficulty, filterStatus, keyword], () => {
  loadProblems()
})

const categoriesWithAll = computed(() => [{ id: 'all', name: '全部', order: 0 } as any].concat(categories.value))

const filteredProblems = computed(() => {
  // 后端已经进行了筛选，这里只做前端关键词过滤（如果后端不支持）
  const k = keyword.value.trim().toLowerCase()
  if (!k) return problems.value
  return problems.value.filter(p => {
    const text = [p.title, p.tags, p.companies, p.description, p.solution].filter(Boolean).join(' ').toLowerCase()
    return text.includes(k)
  })
})

function resetProblemForm() {
  editingProblemId.value = null
  problemForm.value = {
    title: '',
    category_id: activeCategory.value === 'all' ? null : activeCategory.value,
    difficulty: '中等',
    companies: '',
    tags: '',
    status: '未开始',
    link: '',
    description: '',
    solution: ''
  }
}

async function quickCreateProblem() {
  const desc = quickDesc.value.trim()
  if (!desc) { alert('请输入题目描述'); return }
  try {
    const title = desc.split(/\n/)[0].slice(0, 30) || '未命名题目'
    await api.createAlgoProblem({
      title,
      category_id: quickCategoryId.value,
      difficulty: '中等',
      companies: '',
      tags: '',
      status: '未开始',
      link: '',
      description: desc,
      solution: ''
    })
    // 重置
    quickDesc.value = ''
    quickCategoryId.value = null
    // 重新加载题目列表
    await loadProblems()
  } catch (error) {
    console.error('Failed to create problem:', error)
    alert('创建题目失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

function editProblem(p: AlgoProblem) {
  editingProblemId.value = p.id
  problemForm.value = {
    title: p.title,
    category_id: p.category_id,
    difficulty: p.difficulty,
    companies: p.companies,
    tags: p.tags,
    status: p.status,
    link: p.link || '',
    description: p.description || '',
    solution: p.solution || ''
  }
  showProblemForm.value = true
}

async function submitProblem() {
  if (!problemForm.value.title.trim()) { alert('请输入题目标题'); return }
  try {
    if (editingProblemId.value) {
      await api.updateAlgoProblem(editingProblemId.value, problemForm.value as AlgoProblemUpdate)
    } else {
      await api.createAlgoProblem(problemForm.value as AlgoProblemCreate)
    }
    showProblemForm.value = false
    resetProblemForm()
    // 重新加载题目列表
    await loadProblems()
  } catch (error) {
    console.error('Failed to save problem:', error)
    alert('保存题目失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function deleteProblem(id: number) {
  if (!confirm('确认删除该题目？')) return
  try {
    await api.deleteAlgoProblem(id)
    // 重新加载题目列表
    await loadProblems()
  } catch (error) {
    console.error('Failed to delete problem:', error)
    alert('删除题目失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function quickStatus(p: AlgoProblem) {
  const next: Record<AlgoProblem['status'], AlgoProblem['status']> = {
    '未开始': '再复习',
    '再复习': '已掌握',
    '已掌握': '未开始'
  }
  const newStatus = next[p.status]
  try {
    await api.updateAlgoProblem(p.id, { status: newStatus })
    // 更新本地状态
    p.status = newStatus
    // 重新加载以确保数据同步
    await loadProblems()
  } catch (error) {
    console.error('Failed to update status:', error)
    alert('更新状态失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

function openCategoryModal(c?: AlgoCategory) {
  if (c) {
    editingCategoryId.value = c.id
    catName.value = c.name
  } else {
    editingCategoryId.value = null
    catName.value = ''
  }
  showCategoryModal.value = true
}

async function submitCategory() {
  const name = catName.value.trim()
  if (!name) { alert('请输入分类名称'); return }
  try {
    if (editingCategoryId.value) {
      await api.updateAlgoCategory(editingCategoryId.value, { name })
    } else {
      const maxOrder = categories.value.reduce((m, c) => Math.max(m, c.order), 0)
      await api.createAlgoCategory({ name, order: maxOrder + 1 })
    }
    showCategoryModal.value = false
    catName.value = ''
    editingCategoryId.value = null
    // 重新加载分类列表
    await loadCategories()
  } catch (error) {
    console.error('Failed to save category:', error)
    alert('保存分类失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function deleteCategory(id: number) {
  if (!confirm('删除该分类？其下题目不会丢失，但会变为未分类。')) return
  try {
    await api.deleteAlgoCategory(id)
    // 重新加载分类列表和题目列表
    await Promise.all([loadCategories(), loadProblems()])
    if (activeCategory.value === id) activeCategory.value = 'all'
  } catch (error) {
    console.error('Failed to delete category:', error)
    alert('删除分类失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function moveCategory(id: number, dir: 'up' | 'down') {
  const idx = categories.value.findIndex(c => c.id === id)
  if (idx < 0) return
  const swapIdx = dir === 'up' ? idx - 1 : idx + 1
  if (swapIdx < 0 || swapIdx >= categories.value.length) return
  const a = categories.value[idx]
  const b = categories.value[swapIdx]
  // 交换顺序
  try {
    await Promise.all([
      api.updateAlgoCategory(a.id, { order: b.order }),
      api.updateAlgoCategory(b.id, { order: a.order })
    ])
    // 重新加载分类列表
    await loadCategories()
  } catch (error) {
    console.error('Failed to move category:', error)
    alert('移动分类失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

function exportJson() {
  const data = {
    categories: categories.value.map(c => ({
      id: c.id,
      name: c.name,
      order: c.order
    })),
    problems: problems.value.map(p => ({
      id: p.id,
      title: p.title,
      categoryId: p.category_id,
      difficulty: p.difficulty,
      companies: p.companies,
      tags: p.tags,
      status: p.status,
      link: p.link,
      description: p.description,
      solution: p.solution
    }))
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'algo-bank.json'
  a.click()
  URL.revokeObjectURL(url)
}

async function importJson(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files || !input.files[0]) return
  const file = input.files[0]
  const reader = new FileReader()
  reader.onload = async () => {
    try {
      const data = JSON.parse(String(reader.result))
      if (Array.isArray(data.categories) && Array.isArray(data.problems)) {
        // 导入分类
        for (const cat of data.categories) {
          try {
            await api.createAlgoCategory({ name: cat.name, order: cat.order || 0 })
          } catch (error) {
            console.error('Failed to import category:', error)
          }
        }
        // 导入题目
        for (const prob of data.problems) {
          try {
            await api.createAlgoProblem({
              title: prob.title,
              category_id: prob.categoryId,
              difficulty: prob.difficulty || '中等',
              companies: prob.companies || '',
              tags: prob.tags || '',
              status: prob.status || '未开始',
              link: prob.link || '',
              description: prob.description || '',
              solution: prob.solution || ''
            })
          } catch (error) {
            console.error('Failed to import problem:', error)
          }
        }
        // 重新加载数据
        await Promise.all([loadCategories(), loadProblems()])
        alert('导入成功')
      } else {
        alert('导入文件格式不正确')
      }
    } catch {
      alert('解析失败，请检查文件')
    } finally {
      ;(e.target as HTMLInputElement).value = ''
    }
  }
  reader.readAsText(file)
}

function categoryName(id: number | null) {
  if (!id) return '未分类'
  return categories.value.find(c => c.id === id)?.name || '未分类'
}

// 题解相关方法
async function loadSolutions(problemId: number) {
  try {
    const solutions = await api.getAlgoSolutions(problemId)
    problemSolutions.value[problemId] = solutions
  } catch (error) {
    console.error('Failed to load solutions:', error)
  }
}

async function openSolutionModal(problemId: number, solution?: AlgoSolution) {
  currentProblemId.value = problemId
  // 如果还没有加载过题解，先加载一下以获取数量
  if (!problemSolutions.value[problemId]) {
    await loadSolutions(problemId)
  }
  // 确保题解列表展开
  expandedSolutions.value[problemId] = true
  editingSolutionId.value = solution?.id || null
  solutionForm.value = {
    title: solution?.title || '',
    content: solution?.content || '',
    language: solution?.language || '',
    complexity_time: solution?.complexity_time || '',
    complexity_space: solution?.complexity_space || '',
    order: solution?.order || (problemSolutions.value[problemId]?.length || 0)
  }
  showSolutionModal.value = true
}

function resetSolutionForm() {
  editingSolutionId.value = null
  currentProblemId.value = null
  solutionForm.value = {
    title: '',
    content: '',
    language: '',
    complexity_time: '',
    complexity_space: '',
    order: 0
  }
}

async function submitSolution() {
  if (!solutionForm.value.content.trim()) { alert('请输入题解内容'); return }
  if (!currentProblemId.value) return
  
  const problemId = currentProblemId.value // 保存problemId，因为resetSolutionForm会清空它
  try {
    if (editingSolutionId.value) {
      await api.updateAlgoSolution(editingSolutionId.value, solutionForm.value as AlgoSolutionUpdate)
    } else {
      await api.createAlgoSolution({
        ...solutionForm.value,
        problem_id: problemId
      } as AlgoSolutionCreate)
    }
    showSolutionModal.value = false
    resetSolutionForm()
    // 重新加载题解
    await loadSolutions(problemId)
    // 确保题解列表展开（在nextTick中设置，确保DOM更新）
    await nextTick()
    expandedSolutions.value[problemId] = true
  } catch (error) {
    console.error('Failed to save solution:', error)
    alert('保存题解失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

async function deleteSolution(problemId: number, solutionId: number) {
  if (!confirm('确认删除该题解？')) return
  try {
    await api.deleteAlgoSolution(solutionId)
    await loadSolutions(problemId)
  } catch (error) {
    console.error('Failed to delete solution:', error)
    alert('删除题解失败：' + (error instanceof Error ? error.message : '未知错误'))
  }
}

// 当展开题目详情时，加载题解
function toggleProblemSolutions(problemId: number, event: Event) {
  const details = event.target as HTMLDetailsElement
  expandedSolutions.value[problemId] = details.open
  if (details.open) {
    // 如果还没有加载过，则加载题解
    if (!problemSolutions.value[problemId]) {
      loadSolutions(problemId)
    }
  }
}

</script>

<template>
  <div class="page">
    <div class="internal-nav">
      <nav class="tabs">
        <button class="active">🧩 刷题</button>
        <button @click="openCategoryModal()">📁 管理分类</button>
      </nav>
    </div>

    <main class="main">
      <section class="panel">
        <!-- 快速新增（仅描述 + 分类） -->
        <div class="quick-add card">
          <div class="qa-head">
            <div class="qa-title">➕ 快速新增题目</div>
            <div class="qa-tips">仅需描述和分类，其他信息可后续在编辑中补充</div>
          </div>
          <div class="qa-content">
            <textarea v-model="quickDesc" rows="3" placeholder="输入题目描述（支持换行）" />
            <div class="qa-actions">
              <select class="select" v-model="quickCategoryId">
                <option :value="null">未分类</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
              <button class="primary" @click="quickCreateProblem">创建</button>
            </div>
          </div>
        </div>

        <div class="toolbar card">
          <input class="search" v-model="keyword" placeholder="搜索题目/标签/公司/描述/解法 回车确认" @keyup.enter="()=>{}" />
          <select class="select" v-model="activeCategory">
            <option v-for="c in categoriesWithAll" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
          <select class="select" v-model="filterDifficulty">
            <option value="all">全部难度</option>
            <option value="简单">简单</option>
            <option value="中等">中等</option>
            <option value="困难">困难</option>
          </select>
          <select class="select" v-model="filterStatus">
            <option value="all">全部状态</option>
            <option value="未开始">未开始</option>
            <option value="再复习">再复习</option>
            <option value="已掌握">已掌握</option>
          </select>
          <div class="right-actions">
            <label class="import-btn">
              ⬆️ 导入
              <input type="file" accept="application/json" @change="importJson" />
            </label>
            <button class="ghost" @click="exportJson">⬇️ 导出</button>
          </div>
        </div>

        <div v-if="loading" class="empty">加载中...</div>
        <div v-else-if="filteredProblems.length===0" class="empty">暂无题目，点击“新建题目”开始</div>
        <div v-else class="grid">
          <div v-for="p in filteredProblems" :key="p.id" class="card problem-item">
            <div class="problem-head">
              <div class="title" :title="p.title">{{ p.title }}</div>
              <div class="badges">
                <span class="badge diff" :data-d="p.difficulty">{{ p.difficulty }}</span>
                <span class="badge status" :data-s="p.status" @click="quickStatus(p)" title="点击切换状态">{{ p.status }}</span>
              </div>
            </div>
            <div class="meta">
              <span>分类：{{ categoryName(p.category_id) }}</span>
              <span v-if="p.companies">公司：{{ p.companies }}</span>
              <span v-if="p.tags">标签：{{ p.tags }}</span>
            </div>
            <div v-if="p.description" class="desc">{{ p.description }}</div>
            <div class="ops">
              <a v-if="p.link" class="ghost" :href="p.link" target="_blank">题目链接</a>
              <button class="secondary" @click="editProblem(p)">编辑</button>
              <button class="danger" @click="deleteProblem(p.id)">删除</button>
            </div>
            <!-- 题解列表 -->
            <details :open="expandedSolutions[p.id]" @toggle="toggleProblemSolutions(p.id, $event)">
              <summary>
                <span>题解 ({{ problemSolutions[p.id]?.length || 0 }})</span>
                <button class="ghost small" @click.stop="openSolutionModal(p.id)">➕ 添加题解</button>
              </summary>
              <div class="solutions-list" v-if="problemSolutions[p.id] !== undefined">
                <div v-if="problemSolutions[p.id] && problemSolutions[p.id].length === 0" class="empty-solutions">暂无题解</div>
                <div v-for="sol in (problemSolutions[p.id] || [])" :key="sol.id" class="solution-item">
                  <div class="solution-header">
                    <div class="solution-title">
                      <strong v-if="sol.title">{{ sol.title }}</strong>
                      <span v-else class="solution-default-title">题解 #{{ sol.id }}</span>
                      <span v-if="sol.language" class="solution-lang">{{ sol.language }}</span>
                    </div>
                    <div class="solution-ops">
                      <button class="ghost small" @click="openSolutionModal(p.id, sol)">编辑</button>
                      <button class="ghost small danger" @click="deleteSolution(p.id, sol.id)">删除</button>
                    </div>
                  </div>
                  <div v-if="sol.complexity_time || sol.complexity_space" class="solution-complexity">
                    <span v-if="sol.complexity_time">时间复杂度: {{ sol.complexity_time }}</span>
                    <span v-if="sol.complexity_space">空间复杂度: {{ sol.complexity_space }}</span>
                  </div>
                  <pre class="solution-content">{{ sol.content }}</pre>
                </div>
              </div>
            </details>
            <!-- 保留原有solution字段的显示（向后兼容） -->
            <details v-if="p.solution && (!problemSolutions[p.id] || problemSolutions[p.id].length === 0)">
              <summary>查看解法（旧版本）</summary>
              <pre class="solution">{{ p.solution }}</pre>
            </details>
          </div>
        </div>
      </section>

      <!-- 分类管理 Modal -->
      <div v-if="showCategoryModal" class="modal" @click.self="showCategoryModal=false">
        <div class="modal-body">
          <div class="modal-head">
            <div class="modal-title">分类管理</div>
            <button class="ghost close" @click="showCategoryModal=false">✕</button>
          </div>
          <div class="cat-list">
            <div v-for="c in categories" :key="c.id" class="cat-row">
              <div class="left">
                <template v-if="editingCategoryId===c.id">
                  <input v-model="catName" class="cat-input" />
                </template>
                <template v-else>
                  <div class="name">{{ c.name }}</div>
                </template>
                <span class="count">{{ problems.filter(p=>p.category_id===c.id).length }}</span>
              </div>
              <div class="cat-ops">
                <button class="ghost" title="上移" @click="moveCategory(c.id, 'up')">↑</button>
                <button class="ghost" title="下移" @click="moveCategory(c.id, 'down')">↓</button>
                <template v-if="editingCategoryId===c.id">
                  <button class="primary" @click="submitCategory">保存</button>
                  <button class="ghost" @click="editingCategoryId=null">取消</button>
                </template>
                <template v-else>
                  <button class="secondary" @click="editingCategoryId=c.id; catName=c.name">编辑</button>
                </template>
                <button class="danger" @click="deleteCategory(c.id)">删除</button>
              </div>
            </div>
          </div>

          <div class="cat-add form">
            <div class="row inline-2">
              <div>
                <label>新增分类</label>
                <input v-model="catName" placeholder="如：堆/二分/位运算" />
              </div>
              <div class="actions">
                <button class="primary" @click="editingCategoryId=null; submitCategory()">新增</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 新建/编辑题目 Modal -->
      <div v-if="showProblemForm" class="modal" @click.self="showProblemForm=false">
        <form class="modal-body" @submit.prevent="submitProblem">
          <div class="modal-head">
            <div class="modal-title">{{ editingProblemId ? '编辑题目' : '新建题目' }}</div>
            <button class="ghost close" type="button" @click="showProblemForm=false">✕</button>
          </div>
          <div class="row">
            <label>标题</label>
            <input v-model="problemForm.title" required placeholder="如：两数之和" />
          </div>
          <div class="row inline">
            <div>
              <label>分类</label>
              <select v-model="problemForm.category_id">
                <option :value="null">未分类</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div>
              <label>难度</label>
              <select v-model="problemForm.difficulty">
                <option value="简单">简单</option>
                <option value="中等">中等</option>
                <option value="困难">困难</option>
              </select>
            </div>
            <div>
              <label>状态</label>
              <select v-model="problemForm.status">
                <option value="未开始">未开始</option>
                <option value="再复习">再复习</option>
                <option value="已掌握">已掌握</option>
              </select>
            </div>
          </div>
          <div class="row inline">
            <div>
              <label>公司(逗号分隔)</label>
              <input v-model="problemForm.companies" placeholder="如：字节,阿里,腾讯" />
            </div>
            <div>
              <label>标签(逗号分隔)</label>
              <input v-model="problemForm.tags" placeholder="如：哈希,双指针" />
            </div>
          </div>
          <div class="row">
            <label>题目链接</label>
            <input v-model="problemForm.link" placeholder="可选：LeetCode/牛客等链接" />
          </div>
          <div class="row">
            <label>题目描述</label>
            <textarea v-model="problemForm.description" rows="4" placeholder="简述题意/边界" />
          </div>
          <div class="row">
            <label>解法思路/代码</label>
            <textarea v-model="problemForm.solution" rows="8" placeholder="记录解题思路或代码片段" />
          </div>
          <div class="actions">
            <button class="primary" type="submit">{{ editingProblemId ? '保存' : '创建' }}</button>
            <button class="ghost" type="button" @click="showProblemForm=false">取消</button>
          </div>
        </form>
      </div>

      <!-- 题解编辑 Modal -->
      <div v-if="showSolutionModal" class="modal" @click.self="showSolutionModal=false">
        <form class="modal-body" @submit.prevent="submitSolution">
          <div class="modal-head">
            <div class="modal-title">{{ editingSolutionId ? '编辑题解' : '添加题解' }}</div>
            <button class="ghost close" type="button" @click="showSolutionModal=false; resetSolutionForm()">✕</button>
          </div>
          <div class="row">
            <label>题解标题（可选）</label>
            <input v-model="solutionForm.title" placeholder="如：方法1、动态规划解法等" />
          </div>
          <div class="row inline">
            <div>
              <label>编程语言</label>
              <input v-model="solutionForm.language" placeholder="如：Python、Java、C++" />
            </div>
            <div>
              <label>排序顺序</label>
              <input type="number" v-model.number="solutionForm.order" min="0" />
            </div>
          </div>
          <div class="row inline">
            <div>
              <label>时间复杂度</label>
              <input v-model="solutionForm.complexity_time" placeholder="如：O(n)" />
            </div>
            <div>
              <label>空间复杂度</label>
              <input v-model="solutionForm.complexity_space" placeholder="如：O(1)" />
            </div>
          </div>
          <div class="row">
            <label>题解内容 <span style="color:red">*</span></label>
            <textarea v-model="solutionForm.content" rows="12" placeholder="输入题解代码或思路（必填）" required />
          </div>
          <div class="actions">
            <button class="primary" type="submit">{{ editingSolutionId ? '保存' : '创建' }}</button>
            <button class="ghost" type="button" @click="showSolutionModal=false; resetSolutionForm()">取消</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; height: 100%; background: transparent; }
.internal-nav { display: flex; justify-content: center; margin-bottom: 20px; padding: 0 24px; }
.tabs { display: flex; gap: 8px; background: rgba(255,255,255,0.6); padding: 4px; border-radius: 12px; backdrop-filter: blur(10px); box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.tabs button { background: transparent; color: #64748b; border: 1px solid transparent; padding: 8px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; font-weight: 500; }
.tabs button.active { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; box-shadow: 0 2px 8px rgba(102,126,234,0.3); }
.main { padding: 0 24px 24px; overflow: auto; flex: 1; }
.panel { width: 100%; max-width: 1400px; margin: 0 auto; }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px; box-shadow: 0 1px 3px rgba(16,24,40,0.06); }
.toolbar { display: grid; grid-template-columns: 1fr 180px 140px 140px auto; gap: 10px; align-items: center; margin-bottom: 16px; }
.toolbar .search, .toolbar .select { height: 38px; }
.right-actions { display: flex; gap: 8px; justify-content: flex-end; }
.import-btn { position: relative; overflow: hidden; display: inline-flex; align-items: center; gap: 6px; padding: 8px 12px; border: 1px solid #e2e8f0; border-radius: 8px; background: #fff; cursor: pointer; }
.import-btn input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.problem-item .problem-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.problem-item .title { font-weight: 700; color: #111827; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.problem-item .badges { display: flex; gap: 6px; }
.badge { border-radius: 999px; padding: 4px 10px; font-size: 12px; font-weight: 600; }
.badge.diff[data-d="简单"] { background: #ecfeff; color: #0891b2; }
.badge.diff[data-d="中等"] { background: #eef2ff; color: #6366f1; }
.badge.diff[data-d="困难"] { background: #fee2e2; color: #ef4444; }
.badge.status[data-s="未开始"] { background: #f1f5f9; color: #334155; }
.badge.status[data-s="再复习"] { background: #fef3c7; color: #b45309; }
.badge.status[data-s="已掌握"] { background: #dcfce7; color: #15803d; }
.meta { color: #64748b; display: flex; gap: 12px; flex-wrap: wrap; margin: 8px 0; }
.desc { color: #374151; background: #f8fafc; padding: 8px; border: 1px solid #e5e7eb; border-radius: 8px; }
.ops { display: flex; gap: 8px; justify-content: flex-end; align-items: center; margin-top: 8px; }
a.ghost, button.ghost { background: #fff; color: #0f172a; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; }
button.secondary { background: #6b7280; color: #fff; border-radius: 8px; padding: 6px 10px; }
button.danger { background: #ef4444; color: #fff; border-radius: 8px; padding: 6px 10px; }
.solution { white-space: pre-wrap; background: #0f172a; color: #e5e7eb; padding: 12px; border-radius: 8px; border: 1px solid #0b1220; }
.solutions-list { margin-top: 12px; display: flex; flex-direction: column; gap: 16px; }
.solution-item { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; }
.solution-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; gap: 12px; }
.solution-title { display: flex; align-items: center; gap: 8px; flex: 1; }
.solution-title strong { color: #1e293b; font-size: 15px; }
.solution-default-title { color: #64748b; font-size: 14px; }
.solution-lang { background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }
.solution-ops { display: flex; gap: 4px; }
.solution-ops .ghost.small { padding: 4px 8px; font-size: 12px; }
.solution-complexity { display: flex; gap: 12px; margin-bottom: 8px; font-size: 12px; color: #64748b; }
.solution-content { white-space: pre-wrap; background: #0f172a; color: #e5e7eb; padding: 12px; border-radius: 8px; border: 1px solid #0b1220; font-size: 13px; line-height: 1.6; margin: 0; }
.empty-solutions { text-align: center; color: #94a3b8; padding: 20px; font-size: 14px; }
details summary { cursor: pointer; display: flex; justify-content: space-between; align-items: center; padding: 8px 0; font-weight: 500; color: #475569; }
details summary:hover { color: #1e293b; }
details summary button { margin-left: auto; }

/* 弹层 */
.modal { position: fixed; inset: 0; background: rgba(15,23,42,0.5); display: grid; place-items: center; z-index: 50; }
.modal-body { width: min(960px, 92vw); max-height: 86vh; overflow: auto; background: #fff; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 10px 30px rgba(0,0,0,0.18); padding: 16px 18px; color: #111; }
.modal-head { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 10px; }
.modal-title { font-size: 18px; font-weight: 700; color: #111827; }
.close { font-size: 18px; line-height: 1; padding: 6px 10px; }
.form .row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
.row.inline { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.form input, .form textarea, .form select { border: 1px solid #d1d5db; border-radius: 8px; padding: 10px 12px; font-size: 14px; background: #fff; color: #111; }
.actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px; }
.primary { background: #2563eb; color: #fff; border-radius: 8px; padding: 8px 12px; }

/* 分类列表 */
.cat-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }
.cat-row { display: grid; grid-template-columns: 1fr auto; align-items: center; padding: 8px 10px; border: 1px solid #eef2f7; border-radius: 8px; background: #fff; }
.cat-ops { display: flex; gap: 6px; }

/* 美化快速新增卡片 */
.quick-add {
  margin-bottom: 18px;
  padding: 18px 20px 14px 20px;
  border-radius: 12px;
  background: #f7fafd;
  border: none;
  box-shadow: 0 2px 10px rgba(136, 165, 255, .09), 0 1.5px 3px rgba(40, 53, 119, .03);
}
.qa-head {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  margin-bottom: 4px;
}
.qa-title {
  font-size: 17px;
  font-weight: 600;
  color: #2563eb;
  letter-spacing: .5px;
}
.qa-tips {
  font-size: 13px;
  color: #64748b;
  font-weight: 400;
  margin-bottom: 1.5px;
}
.qa-content {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  margin-top: 6px;
}
.qa-content textarea {
  flex: 1 1 320px;
  min-width: 0;
  resize: vertical;
  border: 1.5px solid #d1d5db;
  border-radius: 7px;
  font-size: 15px;
  padding: 9px 12px;
  box-shadow: none;
}
.qa-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 105px;
  margin-left: 5px;
}
.qa-actions .select {
  height: 36px;
  min-width: 92px;
  border-radius: 7px;
  font-size: 14px;
}
.qa-actions button {
  height: 36px;
  font-size: 15px;
  border-radius: 7px;
  font-weight: 600;
}
@media (max-width: 700px) {
  .qa-content { flex-direction: column; align-items: stretch; }
  .qa-actions { flex-direction: row; gap: 8px; margin-left:0; margin-top:6px; }
}

@media (max-width: 960px) {
  .toolbar { grid-template-columns: 1fr 1fr 1fr 1fr auto; }
  .row.inline { grid-template-columns: 1fr; }
}
</style>


