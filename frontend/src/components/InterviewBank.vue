<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { api, type InterviewQuestion, type InterviewCategory, type InterviewAnswer, type InterviewQuestionCreate, type InterviewCategoryCreate, type InterviewCategoryUpdate, type InterviewAnswerCreate, type InterviewAnswerUpdate } from '../api'

const questions = ref<InterviewQuestion[]>([])
const categories = ref<InterviewCategory[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const activeCategory = ref<string | number>('all')
const showCatModal = ref(false)
const categoryName = ref('')
const editingCatId = ref<number | null>(null)

// 快速添加状态
const quickQuestion = ref('')
const quickCategoryId = ref<number | null>(null)

// 答案编辑状态
const editingAnswerId = ref<number | null>(null)
const editingAnswerContent = ref('')
const editingQuestionId = ref<number | null>(null)
const showAnswerModal = ref(false)

// 拖拽相关状态
const dragCatId = ref<number | null>(null)
const dropCatIndex = ref<number | null>(null)

// 加载数据
async function loadCategories() {
  try {
    categories.value = await api.getInterviewCategories()
  } catch (e: any) {
    console.error('加载分类失败:', e)
    error.value = '加载分类失败'
  }
}

async function loadQuestions() {
  try {
    const categoryId = activeCategory.value === 'all' ? null : Number(activeCategory.value)
    questions.value = await api.getInterviewQuestions({ category_id: categoryId })
  } catch (e: any) {
    console.error('加载问题失败:', e)
    error.value = '加载问题失败'
  }
}

async function load() {
  loading.value = true
  error.value = null
  await api.ready()
  await loadCategories()
  await loadQuestions()
  loading.value = false
}

onMounted(load)

// 监听分类切换
watch(() => activeCategory.value, async () => {
  await loadQuestions()
})

const questionsFiltered = computed(() => questions.value)
const sortedCategories = computed(() => [...categories.value].sort((a, b) => a.order - b.order))

// 分类管理
function openEditCat(cat?: InterviewCategory) {
  editingCatId.value = cat?.id || null
  categoryName.value = cat?.name || ''
  showCatModal.value = true
}

async function saveCat() {
  const name = categoryName.value.trim()
  if (!name) { alert('请输入分类名！'); return }
  try {
    if (editingCatId.value) {
      await api.updateInterviewCategory(editingCatId.value, { name })
    } else {
      const maxOrder = categories.value.reduce((m, c) => Math.max(m, c.order), 0)
      await api.createInterviewCategory({ name, order: maxOrder + 1 })
    }
    await loadCategories()
    showCatModal.value = false
    categoryName.value = ''
    editingCatId.value = null
  } catch (e: any) {
    alert('保存分类失败: ' + (e?.message || '未知错误'))
  }
}

async function removeCat(id: number) {
  if (!confirm('确定删除该分类？')) return
  try {
    await api.deleteInterviewCategory(id)
    await loadCategories()
    await loadQuestions()
  } catch (e: any) {
    alert('删除分类失败: ' + (e?.message || '未知错误'))
  }
}

async function onDrop(idx: number) {
  if (dragCatId.value == null) return
  const from = categories.value.findIndex(c => c.id === dragCatId.value)
  if (from === -1) return
  const to = idx
  if (from !== to) {
    const tmp = categories.value.splice(from, 1)[0]
    categories.value.splice(to, 0, tmp)
    // 更新所有分类的order
    categories.value.forEach((c, i) => {
      if (c.order !== i + 1) {
        api.updateInterviewCategory(c.id, { order: i + 1 }).catch(console.error)
      }
    })
  }
  dragCatId.value = null
  dropCatIndex.value = null
}

function onDragStart(id: number) {
  dragCatId.value = id
}

function onDragOver(idx: number, e: DragEvent) {
  e.preventDefault()
  dropCatIndex.value = idx
}

// 快速添加问题
async function addQuick() {
  if (!quickQuestion.value.trim()) {
    alert('请输入问题')
    return
  }
  try {
    const categoryId = quickCategoryId.value || (activeCategory.value !== 'all' ? Number(activeCategory.value) : null)
    await api.createInterviewQuestion({
      description: quickQuestion.value.trim(),
      category_id: categoryId,
      company: '',
      tags: '',
      difficulty: '中等',
      round: ''
    })
    quickQuestion.value = ''
    quickCategoryId.value = activeCategory.value !== 'all' ? Number(activeCategory.value) : null
    await loadQuestions()
  } catch (e: any) {
    alert('添加问题失败: ' + (e?.message || '未知错误'))
  }
}

// 监听分类切换，自动更新快速添加的分类选择
watch(() => activeCategory.value, (newVal) => {
  if (newVal !== 'all' && !quickCategoryId.value) {
    quickCategoryId.value = Number(newVal)
  }
})

// 答案管理
function addAnswer(questionId: number) {
  editingQuestionId.value = questionId
  editingAnswerId.value = null
  editingAnswerContent.value = ''
  showAnswerModal.value = true
}

function editAnswer(questionId: number, answer: InterviewAnswer) {
  editingQuestionId.value = questionId
  editingAnswerId.value = answer.id
  editingAnswerContent.value = answer.content
  showAnswerModal.value = true
}

async function saveAnswer() {
  if (!editingAnswerContent.value.trim()) {
    alert('请输入答案内容')
    return
  }
  if (!editingQuestionId.value) return
  try {
    if (editingAnswerId.value) {
      await api.updateInterviewAnswer(editingAnswerId.value, { content: editingAnswerContent.value.trim() })
    } else {
      await api.createInterviewAnswer({
        question_id: editingQuestionId.value,
        content: editingAnswerContent.value.trim()
      })
    }
    showAnswerModal.value = false
    editingAnswerContent.value = ''
    editingAnswerId.value = null
    editingQuestionId.value = null
    await loadQuestions()
  } catch (e: any) {
    alert('保存答案失败: ' + (e?.message || '未知错误'))
  }
}

async function deleteAnswer(questionId: number, answerId: number) {
  if (!confirm('确定删除该答案？')) return
  try {
    await api.deleteInterviewAnswer(answerId)
    await loadQuestions()
  } catch (e: any) {
    alert('删除答案失败: ' + (e?.message || '未知错误'))
  }
}

function getCategoryName(id: number | null) {
  if (!id) return '未分类'
  return categories.value.find(c => c.id === id)?.name || '未分类'
}
</script>

<template>
  <div class="iv-root">
    <aside class="sidebar">
      <div class="cat-bar-head">
        <span>分类</span>
        <button class="cat-add-btn" @click="openEditCat()">＋</button>
      </div>
      <ul class="cat-list">
        <li
          :class="['cat-item', {active:activeCategory==='all'}]"
          @click="activeCategory='all'"
        >全部 <span class="count">{{questions.length}}</span></li>
        <li v-for="(cat,idx) in sortedCategories" :key="cat.id" 
          class="cat-item"
          :class="{active:activeCategory===cat.id, dragover:dropCatIndex===idx}"
          draggable="true"
          @dragstart="onDragStart(cat.id)"
          @dragover.prevent="onDragOver(idx,$event)"
          @drop="onDrop(idx)"
          @click="activeCategory=cat.id"
        >
          <span class="cat-name">{{cat.name}}</span>
          <span class="count">{{questions.filter(q=>q.category_id===cat.id).length}}</span>
          <div class="cat-actions">
            <button class="cat-edit" title="编辑" @click.stop="openEditCat(cat)">✎</button>
            <button class="cat-rem" title="删除" @click.stop="removeCat(cat.id)">🗑</button>
          </div>
        </li>
      </ul>
    </aside>
    <main class="main">
      <!-- 快速录入 -->
      <div class="quick-add-bar card">
        <div class="qa-title">➕ 快速添加面试题</div>
        <div class="qa-form">
          <input 
            v-model="quickQuestion" 
            placeholder="输入问题" 
            @keyup.enter="addQuick"
            class="qa-input"
          />
          <select v-model="quickCategoryId" class="qa-select">
            <option :value="null">未分类</option>
            <option v-for="cat in sortedCategories" :key="cat.id" :value="cat.id">{{cat.name}}</option>
          </select>
          <button class="qa-btn" @click="addQuick">添加</button>
        </div>
      </div>
      
      <!-- 面试题卡片区 -->
      <div v-if="loading" class="empty">加载中...</div>
      <div v-else-if="error" class="empty error">{{error}}</div>
      <div v-else class="list">
        <div v-for="q in questionsFiltered" :key="q.id" class="iv-card">
          <div class="card-header">
            <div class="desc">{{q.description}}</div>
            <button class="add-answer-btn" @click="addAnswer(q.id)" title="添加答案">➕ 答案</button>
          </div>
          
          <!-- 答案列表 -->
          <div v-if="q.answers && q.answers.length > 0" class="answers-section">
            <div 
              v-for="answer in q.answers" 
              :key="answer.id" 
              class="answer-item"
            >
              <div class="answer-content">{{answer.content}}</div>
              <div class="answer-actions">
                <button class="answer-edit" @click="editAnswer(q.id, answer)">编辑</button>
                <button class="answer-delete" @click="deleteAnswer(q.id, answer.id)">删除</button>
              </div>
            </div>
          </div>
          <div v-else class="no-answer">暂无答案，点击"➕ 答案"添加</div>
          
          <div class="meta-bar">
            <span v-if="q.company">🏢 {{q.company}}</span>
            <span v-if="q.tags">🏷{{q.tags}}</span>
            <span class="diff" :data-d="q.difficulty">{{q.difficulty}}</span>
            <span v-if="q.round">🎯{{q.round}}</span>
            <span class="date">{{new Date(q.created_at).toLocaleDateString()}}</span>
          </div>
        </div>
        <div v-if="questionsFiltered.length===0" class="nodata">
          暂无面试题，赶紧录入/切换分类试试吧！
        </div>
      </div>
    </main>
    
    <!-- 分类管理 Modal -->
    <div class="modal" v-if="showCatModal" @click.self="showCatModal=false">
      <div class="modal-body">
        <div class="modal-head">{{editingCatId ? '编辑分类' : '新增分类'}}</div>
        <input v-model="categoryName" placeholder="分类名称" />
        <div class="modal-actions">
          <button class="save" @click="saveCat">保存</button>
          <button @click="showCatModal=false">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 答案编辑 Modal -->
    <div class="modal" v-if="showAnswerModal" @click.self="showAnswerModal=false">
      <div class="modal-body">
        <div class="modal-head">{{editingAnswerId ? '编辑答案' : '新增答案'}}</div>
        <textarea 
          v-model="editingAnswerContent" 
          placeholder="输入答案内容（支持多行）"
          rows="8"
          class="answer-textarea"
        ></textarea>
        <div class="modal-actions">
          <button class="save" @click="saveAnswer">保存</button>
          <button @click="showAnswerModal=false; editingAnswerContent=''">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.iv-root {
  display:flex; height:100%; width:100%; min-height:68vh;
  background: #fcfcff;
}
.sidebar {
  width:260px; min-width:220px; background: #f5f7fa; border-right: 1.2px solid #e6e8f3; box-shadow:0 0 4px #a2b3e726; padding:18px 0 0 0;
  display:flex; flex-direction:column;
  overflow-y:auto;
}
.cat-bar-head { display:flex; align-items: center; justify-content:space-between; padding:0 16px; font-weight:600; color: #3e4379; margin-bottom:8px; }
.cat-add-btn {border:none; background: #6894eb; color:white; font-size:18px; width:28px; height:28px; border-radius:8px; cursor:pointer; flex-shrink:0;}
.cat-list{ list-style:none; padding:0 8px; margin:0; }
.cat-item { 
  display:flex; 
  align-items:center; 
  gap:8px; 
  cursor:pointer; 
  background: none; 
  border-radius:8px; 
  padding:10px 14px; 
  margin-bottom:4px; 
  transition:.12s;
  position:relative;
}
.cat-item:hover .cat-actions,
.cat-item.active .cat-actions {
  opacity:1;
  visibility:visible;
}
.cat-item.active{ background: linear-gradient(92deg,#eaf2ff,#ebf3ff 70%); color:#3577dd !important;}
.cat-item.active .cat-name {
  color:#3577dd;
  font-weight:600;
}
.cat-item.dragover{ outline:2px dashed #8ebbfb; background:#f0f7ff;}
.cat-name{
  flex:1;
  font-size:15px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  min-width:0;
  font-weight:500;
}
.count{
  color:#8192b9;
  font-size:12px;
  font-weight:600;
  min-width:24px;
  text-align:right;
  flex-shrink:0;
}
.cat-actions {
  display:flex;
  gap:4px;
  opacity:0;
  visibility:hidden;
  transition:opacity .15s, visibility .15s;
  flex-shrink:0;
  margin-left:4px;
}
.cat-edit,.cat-rem{
  background:none;
  border:none;
  color:#888;
  font-size:14px;
  cursor:pointer;
  border-radius:4px;
  transition:.13s;
  width:22px;
  height:22px;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:0;
}
.cat-edit:hover{background:#f0f7ff;color:#3577dd;}
.cat-rem:hover{background:#fff1f0;color:#e14543;}
.main{flex:1;padding:34px 34px;overflow-x:auto;}
.quick-add-bar{margin-bottom:20px;padding:20px;}
.qa-title{font-size:16px;font-weight:600;color:#2563eb;margin-bottom:12px;}
.qa-form{display:flex;gap:10px;align-items:center;}
.qa-input{flex:2;padding:12px 14px;border-radius:8px;border:1.5px solid #bfcae9;font-size:15px;background:#fafdff;outline:none;transition:.14s;}
.qa-input:focus{border-color:#5d78e6;background:#fff;}
.qa-select{flex:1;padding:12px 14px;border-radius:8px;border:1.5px solid #bfcae9;font-size:15px;background:#fafdff;outline:none;cursor:pointer;}
.qa-btn{padding:12px 24px;border-radius:8px;background:linear-gradient(90deg,#5f80ee,#7345e6);color:white;font-weight:600;font-size:15px;border:none;cursor:pointer;transition:.18s;}
.qa-btn:hover{filter:brightness(1.1);box-shadow:0 3px 11px rgba(102,126,234,0.25);}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:22px;}
.iv-card{background:white;box-shadow:0 2px 18px #dae7fd1a; border-radius:13px;padding:20px;min-height:90px;border:1.4px solid #f5f5fd;transition:.14s;}
.iv-card:hover{box-shadow:0 7px 24px #6894eb25; border-color:#bedaef;}
.card-header{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px;}
.desc{flex:1;font-weight:600;color:#232c4d;font-size:16.7px;line-height:1.5;}
.add-answer-btn{padding:6px 14px;border-radius:6px;background:#f0f7ff;color:#3577dd;font-size:13px;font-weight:500;border:1px solid #e0eaff;cursor:pointer;transition:.13s;flex-shrink:0;}
.add-answer-btn:hover{background:#e0eaff;border-color:#3577dd;}
.answers-section{margin:12px 0;border-top:1px solid #eef2f7;padding-top:12px;}
.answer-item{background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;padding:12px;margin-bottom:10px;}
.answer-item:last-child{margin-bottom:0;}
.answer-content{color:#374151;font-size:14.5px;line-height:1.6;margin-bottom:8px;white-space:pre-wrap;word-break:break-word;}
.answer-actions{display:flex;gap:8px;justify-content:flex-end;}
.answer-edit,.answer-delete{padding:5px 12px;border-radius:6px;font-size:12px;cursor:pointer;border:none;transition:.13s;}
.answer-edit{background:#e0eaff;color:#3577dd;}
.answer-edit:hover{background:#d0daff;}
.answer-delete{background:#fff1f0;color:#e14543;}
.answer-delete:hover{background:#ffe0df;}
.no-answer{color:#adb7d1;font-size:13px;text-align:center;padding:12px;font-style:italic;}
.meta-bar{color:#7991c1;font-size:13px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid #eef2f7;}
.diff[data-d="简单"]{color:#119e5a;font-weight:700;}
.diff[data-d="中等"]{color:#3962b2;font-weight:700;}
.diff[data-d="困难"]{color:#e14d36;font-weight:700;}
.nodata{padding:50px 10px;color:#adb7d1;font-size:18px;text-align:center;}
.empty{padding:50px 10px;color:#adb7d1;font-size:18px;text-align:center;}
.empty.error{color:#e14543;}
.modal{position:fixed;inset:0;z-index:40;background:rgba(50,70,160,.13);display:grid;place-items:center;}
.modal-body{background:white;padding:30px 40px 22px 40px;border-radius:12px;box-shadow:0 10px 32px #b7cafd3a;min-width:240px;max-width:92vw;}
.modal-head{font-size:20px;font-weight:700;color:#2e3863;margin-bottom:13px;}
.modal-actions{margin-top:16px;display:flex;gap:10px;justify-content:flex-end;}
.save{background:#4f71eb;color:white;padding:0 25px;height:36px;border-radius:8px;font-size:15px;font-weight:500;border:none;cursor:pointer;}
.answer-textarea{width:100%;padding:12px;border:1.5px solid #d1d5db;border-radius:8px;font-size:15px;font-family:inherit;line-height:1.6;resize:vertical;outline:none;transition:.14s;margin-bottom:12px;}
.answer-textarea:focus{border-color:#5d78e6;box-shadow:0 0 0 3px rgba(93,120,230,0.1);}
</style>
