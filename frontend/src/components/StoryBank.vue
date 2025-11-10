<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { api, type Story, type StoryCategory, type StoryCreate, type StoryCategoryCreate, type StoryCategoryUpdate } from '../api'

const stories = ref<Story[]>([])
const categories = ref<StoryCategory[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const activeCategory = ref<string | number>('all')
const showCatModal = ref(false)
const catName = ref('')
const editingCatId = ref<number | null>(null)

// 快速添加状态
const quickTitle = ref('')
const quickContent = ref('')
const quickCategoryId = ref<number | null>(null)

// 编辑状态
const editingStoryId = ref<number | null>(null)
const editingStoryTitle = ref('')
const editingStoryContent = ref('')
const editingStoryEssence = ref('')
const editingStoryCategoryId = ref<number | null>(null)
const editingStoryImages = ref<string[]>([])
const showStoryModal = ref(false)
const imagePreviewUrl = ref<string | null>(null)
const uploadingImages = ref(false)

// 快速添加区域的图片
const quickImages = ref<string[]>([])

// 拖拽相关状态
const dragCatId = ref<number | null>(null)
const dropCatIndex = ref<number | null>(null)

// 文本区域引用
const contentTextareaRef = ref<HTMLTextAreaElement | null>(null)
const quickContentTextareaRef = ref<HTMLTextAreaElement | null>(null)
const essenceTextareaRef = ref<HTMLTextAreaElement | null>(null)

// 加载数据
async function loadCategories() {
  try {
    categories.value = await api.getStoryCategories()
  } catch (e: any) {
    console.error('加载分类失败:', e)
    error.value = '加载分类失败'
  }
}

async function loadStories() {
  try {
    const categoryId = activeCategory.value === 'all' ? null : Number(activeCategory.value)
    stories.value = await api.getStories({ category_id: categoryId })
  } catch (e: any) {
    console.error('加载故事失败:', e)
    error.value = '加载故事失败'
  }
}

async function load() {
  loading.value = true
  error.value = null
  await api.ready()
  await loadCategories()
  await loadStories()
  loading.value = false
}

onMounted(() => {
  load()
  // 监听全局粘贴事件（用于编辑模态框）
  document.addEventListener('paste', handleGlobalPaste)
})

// 清理事件监听
watch(() => showStoryModal.value, (isOpen, wasOpen) => {
  if (isOpen && !wasOpen) {
    // 模态框打开时，为文本区域添加粘贴监听
    nextTick(() => {
      if (contentTextareaRef.value) {
        contentTextareaRef.value.addEventListener('paste', handleTextareaPaste)
      }
      if (essenceTextareaRef.value) {
        essenceTextareaRef.value.addEventListener('paste', handleTextareaPaste)
      }
    })
  } else if (!isOpen && wasOpen) {
    // 模态框关闭时，移除事件监听
    if (contentTextareaRef.value) {
      contentTextareaRef.value.removeEventListener('paste', handleTextareaPaste)
    }
    if (essenceTextareaRef.value) {
      essenceTextareaRef.value.removeEventListener('paste', handleTextareaPaste)
    }
  }
})

// 监听快速添加区域的文本区域
watch(() => quickContentTextareaRef.value, (textarea, oldTextarea) => {
  if (oldTextarea) {
    oldTextarea.removeEventListener('paste', handleQuickPaste)
  }
  if (textarea) {
    textarea.addEventListener('paste', handleQuickPaste)
  }
})

// 监听分类切换
watch(() => activeCategory.value, async () => {
  await loadStories()
})

const storiesFiltered = computed(() => stories.value)
const sortedCategories = computed(() => [...categories.value].sort((a, b) => a.order - b.order))

// 分类管理
function openEditCat(cat?: StoryCategory) {
  editingCatId.value = cat?.id || null
  catName.value = cat?.name || ''
  showCatModal.value = true
}

async function saveCat() {
  const name = catName.value.trim()
  if (!name) { alert('请输入分类名！'); return }
  try {
    if (editingCatId.value) {
      await api.updateStoryCategory(editingCatId.value, { name })
    } else {
      const maxOrder = categories.value.reduce((m, c) => Math.max(m, c.order), 0)
      await api.createStoryCategory({ name, order: maxOrder + 1 })
    }
    await loadCategories()
    showCatModal.value = false
    catName.value = ''
    editingCatId.value = null
  } catch (e: any) {
    alert('保存分类失败: ' + (e?.message || '未知错误'))
  }
}

async function removeCat(id: number) {
  if (!confirm('确定删除该分类？')) return
  try {
    await api.deleteStoryCategory(id)
    await loadCategories()
    await loadStories()
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
        api.updateStoryCategory(c.id, { order: i + 1 }).catch(console.error)
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

// 快速添加故事
async function addQuick() {
  if (!quickTitle.value.trim() || !quickContent.value.trim()) {
    alert('请输入故事标题和内容')
    return
  }
  try {
    const categoryId = quickCategoryId.value || (activeCategory.value !== 'all' ? Number(activeCategory.value) : null)
    const imagePaths = quickImages.value.length > 0 ? quickImages.value.join(',') : null
    await api.createStory({
      title: quickTitle.value.trim(),
      content: quickContent.value.trim(),
      category_id: categoryId,
      essence: null,
      image_paths: imagePaths
    })
    quickTitle.value = ''
    quickContent.value = ''
    quickImages.value = []
    quickCategoryId.value = activeCategory.value !== 'all' ? Number(activeCategory.value) : null
    await loadStories()
  } catch (e: any) {
    alert('添加故事失败: ' + (e?.message || '未知错误'))
  }
}

// 监听分类切换，自动更新快速添加的分类选择
watch(() => activeCategory.value, (newVal) => {
  if (newVal !== 'all' && !quickCategoryId.value) {
    quickCategoryId.value = Number(newVal)
  }
})

// 故事编辑
function editStory(story: Story) {
  editingStoryId.value = story.id
  editingStoryTitle.value = story.title
  editingStoryContent.value = story.content
  editingStoryEssence.value = story.essence || ''
  editingStoryCategoryId.value = story.category_id
  editingStoryImages.value = story.image_paths ? story.image_paths.split(',').filter(p => p.trim()) : []
  showStoryModal.value = true
}

function openNewStoryModal() {
  editingStoryId.value = null
  editingStoryTitle.value = ''
  editingStoryContent.value = ''
  editingStoryEssence.value = ''
  editingStoryCategoryId.value = activeCategory.value !== 'all' ? Number(activeCategory.value) : null
  editingStoryImages.value = []
  showStoryModal.value = true
}

async function saveStory() {
  if (!editingStoryTitle.value.trim() || !editingStoryContent.value.trim()) {
    alert('请输入故事标题和内容')
    return
  }
  try {
    const imagePaths = editingStoryImages.value.length > 0 ? editingStoryImages.value.join(',') : null
    if (editingStoryId.value) {
      await api.updateStory(editingStoryId.value, {
        title: editingStoryTitle.value.trim(),
        content: editingStoryContent.value.trim(),
        essence: editingStoryEssence.value.trim() || null,
        category_id: editingStoryCategoryId.value,
        image_paths: imagePaths
      })
    } else {
      await api.createStory({
        title: editingStoryTitle.value.trim(),
        content: editingStoryContent.value.trim(),
        essence: editingStoryEssence.value.trim() || null,
        category_id: editingStoryCategoryId.value,
        image_paths: imagePaths
      })
    }
    showStoryModal.value = false
    editingStoryTitle.value = ''
    editingStoryContent.value = ''
    editingStoryEssence.value = ''
    editingStoryCategoryId.value = null
    editingStoryImages.value = []
    editingStoryId.value = null
    await loadStories()
  } catch (e: any) {
    alert('保存故事失败: ' + (e?.message || '未知错误'))
  }
}

async function deleteStory(id: number) {
  if (!confirm('确定删除该故事？')) return
  try {
    await api.deleteStory(id)
    await loadStories()
  } catch (e: any) {
    alert('删除故事失败: ' + (e?.message || '未知错误'))
  }
}

function getCategoryName(id: number | null) {
  if (!id) return '未分类'
  return categories.value.find(c => c.id === id)?.name || '未分类'
}

function getImageUrl(path: string) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  return path.startsWith('/') ? `/api${path}` : `/api/uploads/${path}`
}

function getImagePaths(story: Story): string[] {
  if (!story.image_paths) return []
  return story.image_paths.split(',').filter(p => p.trim())
}

// 处理编辑模态框中的粘贴（全局监听，用于图片上传区域）
async function handleGlobalPaste(e: ClipboardEvent) {
  // 只有在编辑模态框打开时才处理
  if (!showStoryModal.value) return
  
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type.indexOf('image') !== -1) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) {
        await uploadImageToEditing(file)
      }
    }
  }
}

// 处理文本区域中的粘贴（在内容或本质文本框中粘贴图片）
async function handleTextareaPaste(e: ClipboardEvent) {
  if (!showStoryModal.value) return
  
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type.indexOf('image') !== -1) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) {
        await uploadImageToEditing(file)
        // 在文本框中插入提示文字
        const textarea = e.target as HTMLTextAreaElement
        const cursorPos = textarea.selectionStart
        const textBefore = textarea.value.substring(0, cursorPos)
        const textAfter = textarea.value.substring(textarea.selectionEnd)
        // 不插入文本，只上传图片
      }
    }
  }
}

// 处理快速添加区域的粘贴
async function handleQuickPaste(e: ClipboardEvent) {
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type.indexOf('image') !== -1) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) {
        await uploadImageToQuick(file)
      }
    }
  }
}

// 上传图片到编辑区域
async function uploadImageToEditing(file: File) {
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const result = await api.uploadStoryImages([file])
    if (result.filenames && result.filenames.length > 0) {
      editingStoryImages.value.push(...result.filenames)
    }
  } catch (e: any) {
    alert('图片上传失败: ' + (e?.message || '未知错误'))
  } finally {
    uploadingImages.value = false
  }
}

// 上传图片到快速添加区域
async function uploadImageToQuick(file: File) {
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const result = await api.uploadStoryImages([file])
    if (result.filenames && result.filenames.length > 0) {
      quickImages.value.push(...result.filenames)
    }
  } catch (e: any) {
    alert('图片上传失败: ' + (e?.message || '未知错误'))
  } finally {
    uploadingImages.value = false
  }
}

// 上传图片（通用方法，保持向后兼容）
async function uploadImage(file: File) {
  await uploadImageToEditing(file)
}

// 处理文件选择（编辑区域）
async function handleFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0) return
  
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const fileArray = Array.from(files)
    const result = await api.uploadStoryImages(fileArray)
    if (result.filenames && result.filenames.length > 0) {
      editingStoryImages.value.push(...result.filenames)
    }
  } catch (e: any) {
    alert('图片上传失败: ' + (e?.message || '未知错误'))
  } finally {
    uploadingImages.value = false
  }
  
  // 清空文件选择器
  if (input) {
    input.value = ''
  }
}

// 处理快速添加区域的文件选择
async function handleQuickFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0) return
  
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const fileArray = Array.from(files)
    const result = await api.uploadStoryImages(fileArray)
    if (result.filenames && result.filenames.length > 0) {
      quickImages.value.push(...result.filenames)
    }
  } catch (e: any) {
    alert('图片上传失败: ' + (e?.message || '未知错误'))
  } finally {
    uploadingImages.value = false
  }
  
  // 清空文件选择器
  if (input) {
    input.value = ''
  }
}

// 删除快速添加区域的图片
function removeQuickImage(index: number) {
  quickImages.value.splice(index, 1)
}

// 删除图片
function removeImage(index: number) {
  editingStoryImages.value.splice(index, 1)
}

// 预览图片
function previewImage(path: string) {
  imagePreviewUrl.value = getImageUrl(path)
}

function closeImagePreview() {
  imagePreviewUrl.value = null
}
</script>

<template>
  <div class="story-root">
    <aside class="sidebar">
      <div class="cat-bar-head">
        <span>分类</span>
        <button class="cat-add-btn" @click="openEditCat()">＋</button>
      </div>
      <ul class="cat-list">
        <li
          :class="['cat-item', {active:activeCategory==='all'}]"
          @click="activeCategory='all'"
        >全部 <span class="count">{{stories.length}}</span></li>
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
          <span class="count">{{stories.filter(s=>s.category_id===cat.id).length}}</span>
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
        <div class="qa-title">➕ 快速添加故事</div>
        <div class="qa-form">
          <input 
            v-model="quickTitle" 
            placeholder="故事标题" 
            class="qa-input-title"
          />
          <textarea 
            v-model="quickContent" 
            placeholder="故事内容（支持粘贴图片，Ctrl+V）" 
            rows="2"
            class="qa-textarea"
            ref="quickContentTextareaRef"
          ></textarea>
          <div v-if="quickImages.length > 0" class="qa-images">
            <div 
              v-for="(imgPath, idx) in quickImages" 
              :key="idx"
              class="qa-image-preview"
            >
              <img :src="getImageUrl(imgPath)" alt="预览" />
              <button class="qa-remove-image" @click="removeQuickImage(idx)">×</button>
            </div>
          </div>
          <div class="qa-footer">
            <label class="qa-upload-btn">
              <input 
                type="file" 
                accept="image/*" 
                multiple 
                @change="handleQuickFileSelect"
                style="display: none"
              />
              <span>📷 上传图片</span>
            </label>
            <select v-model="quickCategoryId" class="qa-select">
              <option :value="null">未分类</option>
              <option v-for="cat in sortedCategories" :key="cat.id" :value="cat.id">{{cat.name}}</option>
            </select>
            <button class="qa-btn" @click="addQuick" :disabled="uploadingImages">添加</button>
          </div>
        </div>
      </div>
      
      <!-- 故事卡片区 -->
      <div v-if="loading" class="empty">加载中...</div>
      <div v-else-if="error" class="empty error">{{error}}</div>
      <div v-else class="list">
        <div v-for="s in storiesFiltered" :key="s.id" class="story-card">
          <div class="card-header">
            <div class="story-title">{{s.title}}</div>
            <div class="story-actions">
              <button class="story-edit" @click="editStory(s)">编辑</button>
              <button class="story-delete" @click="deleteStory(s.id)">删除</button>
            </div>
          </div>
          <div class="story-content">{{s.content}}</div>
          <div v-if="getImagePaths(s).length > 0" class="story-images">
            <img 
              v-for="(imgPath, idx) in getImagePaths(s)" 
              :key="idx"
              :src="getImageUrl(imgPath)"
              alt="故事图片"
              class="story-image"
              @click="previewImage(imgPath)"
            />
          </div>
          <div v-if="s.essence" class="story-essence">
            <div class="essence-label">透过故事看本质：</div>
            <div class="essence-content">{{s.essence}}</div>
          </div>
          <div class="meta-bar">
            <span>分类：{{getCategoryName(s.category_id)}}</span>
            <span class="date">{{new Date(s.created_at).toLocaleDateString()}}</span>
          </div>
        </div>
        <div v-if="storiesFiltered.length===0" class="nodata">
          暂无故事记录，赶紧录入/切换分类试试吧！
        </div>
      </div>
    </main>
    
    <!-- 分类管理 Modal -->
    <div class="modal" v-if="showCatModal" @click.self="showCatModal=false">
      <div class="modal-body">
        <div class="modal-head">{{editingCatId ? '编辑分类' : '新增分类'}}</div>
        <input v-model="catName" placeholder="分类名称" />
        <div class="modal-actions">
          <button class="save" @click="saveCat">保存</button>
          <button @click="showCatModal=false">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 故事编辑 Modal -->
    <div class="modal" v-if="showStoryModal" @click.self="showStoryModal=false">
      <div class="modal-body story-modal-body">
        <div class="modal-head">{{editingStoryId ? '编辑故事' : '新增故事'}}</div>
        <input 
          v-model="editingStoryTitle" 
          placeholder="故事标题" 
          class="story-input"
        />
        <textarea 
          v-model="editingStoryContent" 
          placeholder="故事内容（支持粘贴图片，Ctrl+V）"
          rows="6"
          class="story-textarea"
          ref="contentTextareaRef"
        ></textarea>
        <textarea 
          v-model="editingStoryEssence" 
          placeholder="透过故事看本质（可选，支持粘贴图片，Ctrl+V）"
          rows="4"
          class="story-textarea"
          ref="essenceTextareaRef"
        ></textarea>
        
        <!-- 图片上传区域 -->
        <div class="image-upload-area">
          <div class="image-preview-list">
            <div 
              v-for="(imgPath, idx) in editingStoryImages" 
              :key="idx"
              class="image-preview-item"
            >
              <img :src="getImageUrl(imgPath)" alt="预览" />
              <button class="remove-image-btn" @click="removeImage(idx)">×</button>
            </div>
          </div>
          <label class="upload-btn" :class="{ uploading: uploadingImages }">
            <input 
              type="file" 
              accept="image/*" 
              multiple 
              @change="handleFileSelect"
              :disabled="uploadingImages"
              style="display: none"
            />
            <span v-if="uploadingImages">⏳ 上传中...</span>
            <span v-else>📷 上传图片</span>
          </label>
          <div class="paste-hint">💡 提示：在任何文本框中按 Ctrl+V 可粘贴图片，图片会自动上传</div>
        </div>
        
        <select v-model="editingStoryCategoryId" class="story-select">
          <option :value="null">未分类</option>
          <option v-for="cat in sortedCategories" :key="cat.id" :value="cat.id">{{cat.name}}</option>
        </select>
        <div class="modal-actions">
          <button class="save" @click="saveStory">保存</button>
          <button @click="showStoryModal=false">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 图片预览 Modal -->
    <div class="modal" v-if="imagePreviewUrl" @click="closeImagePreview">
      <div class="image-preview-modal" @click.stop>
        <img :src="imagePreviewUrl" alt="预览" />
        <button class="close-preview" @click="closeImagePreview">×</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.story-root {
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
.qa-form{display:flex;flex-direction:column;gap:10px;}
.qa-input-title{flex:1;padding:12px 14px;border-radius:8px;border:1.5px solid #bfcae9;font-size:15px;background:#fafdff;outline:none;transition:.14s;}
.qa-input-title:focus{border-color:#5d78e6;background:#fff;}
.qa-textarea{flex:1;padding:12px 14px;border-radius:8px;border:1.5px solid #bfcae9;font-size:15px;background:#fafdff;outline:none;transition:.14s;resize:vertical;font-family:inherit;}
.qa-textarea:focus{border-color:#5d78e6;background:#fff;}
.qa-footer{display:flex;gap:10px;align-items:center;}
.qa-select{flex:1;padding:12px 14px;border-radius:8px;border:1.5px solid #bfcae9;font-size:15px;background:#fafdff;outline:none;cursor:pointer;}
.qa-btn{padding:12px 24px;border-radius:8px;background:linear-gradient(90deg,#5f80ee,#7345e6);color:white;font-weight:600;font-size:15px;border:none;cursor:pointer;transition:.18s;}
.qa-btn:hover{filter:brightness(1.1);box-shadow:0 3px 11px rgba(102,126,234,0.25);}
.qa-btn:disabled{opacity:0.6;cursor:not-allowed;}
.qa-images{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;}
.qa-image-preview{position:relative;width:80px;height:80px;border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;}
.qa-image-preview img{width:100%;height:100%;object-fit:cover;}
.qa-remove-image{position:absolute;top:4px;right:4px;width:20px;height:20px;border-radius:50%;background:rgba(0,0,0,0.6);color:white;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:.2s;}
.qa-remove-image:hover{background:rgba(225,69,67,0.9);}
.qa-upload-btn{display:inline-block;padding:8px 16px;background:#f0f7ff;color:#3577dd;border:1px dashed #bfcae9;border-radius:6px;cursor:pointer;font-size:14px;transition:.2s;white-space:nowrap;}
.qa-upload-btn:hover{background:#e0eaff;border-color:#3577dd;}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:22px;}
.story-card{background:white;box-shadow:0 2px 18px #dae7fd1a; border-radius:13px;padding:20px;min-height:120px;border:1.4px solid #f5f5fd;transition:.14s;}
.story-card:hover{box-shadow:0 7px 24px #6894eb25; border-color:#bedaef;}
.card-header{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px;}
.story-title{flex:1;font-weight:700;color:#232c4d;font-size:18px;line-height:1.4;}
.story-actions{display:flex;gap:8px;flex-shrink:0;}
.story-edit,.story-delete{padding:6px 14px;border-radius:6px;font-size:13px;font-weight:500;cursor:pointer;border:none;transition:.13s;}
.story-edit{background:#e0eaff;color:#3577dd;}
.story-edit:hover{background:#d0daff;}
.story-delete{background:#fff1f0;color:#e14543;}
.story-delete:hover{background:#ffe0df;}
.story-content{color:#4a5568;font-size:15px;line-height:1.6;white-space:pre-wrap;word-break:break-word;margin-bottom:12px;}
.story-images{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;}
.story-image{max-width:150px;max-height:150px;object-fit:cover;border-radius:8px;cursor:pointer;border:1px solid #e2e8f0;transition:.2s;}
.story-image:hover{transform:scale(1.05);box-shadow:0 4px 12px rgba(0,0,0,0.15);}
.story-essence{margin-top:12px;padding-top:12px;border-top:1px solid #eef2f7;}
.essence-label{color:#7991c1;font-size:13px;font-weight:600;margin-bottom:6px;}
.essence-content{color:#5a6c7d;font-size:14px;line-height:1.6;white-space:pre-wrap;word-break:break-word;font-style:italic;}
.meta-bar{color:#7991c1;font-size:13px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid #eef2f7;}
.date{color:#94a3b8;}
.nodata{padding:50px 10px;color:#adb7d1;font-size:18px;text-align:center;}
.empty{padding:50px 10px;color:#adb7d1;font-size:18px;text-align:center;}
.empty.error{color:#e14543;}
.modal{position:fixed;inset:0;z-index:40;background:rgba(50,70,160,.13);display:grid;place-items:center;}
.modal-body{background:white;padding:30px 40px 22px 40px;border-radius:12px;box-shadow:0 10px 32px #b7cafd3a;min-width:300px;max-width:92vw;max-height:90vh;overflow-y:auto;}
.story-modal-body{min-width:500px;max-width:800px;}
.modal-head{font-size:20px;font-weight:700;color:#2e3863;margin-bottom:13px;}
.modal-actions{margin-top:16px;display:flex;gap:10px;justify-content:flex-end;}
.save{background:#4f71eb;color:white;padding:0 25px;height:36px;border-radius:8px;font-size:15px;font-weight:500;border:none;cursor:pointer;}
.story-input{width:100%;padding:12px;border:1.5px solid #d1d5db;border-radius:8px;font-size:15px;background:#fff;outline:none;transition:.14s;margin-bottom:12px;}
.story-input:focus{border-color:#5d78e6;box-shadow:0 0 0 3px rgba(93,120,230,0.1);}
.story-textarea{width:100%;padding:12px;border:1.5px solid #d1d5db;border-radius:8px;font-size:15px;font-family:inherit;line-height:1.6;resize:vertical;outline:none;transition:.14s;margin-bottom:12px;}
.story-textarea:focus{border-color:#5d78e6;box-shadow:0 0 0 3px rgba(93,120,230,0.1);}
.story-select{width:100%;padding:12px;border:1.5px solid #d1d5db;border-radius:8px;font-size:15px;background:#fff;outline:none;margin-bottom:12px;cursor:pointer;}
.story-select:focus{border-color:#5d78e6;}
.image-upload-area{margin-bottom:12px;}
.image-preview-list{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;}
.image-preview-item{position:relative;width:100px;height:100px;border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;}
.image-preview-item img{width:100%;height:100%;object-fit:cover;}
.remove-image-btn{position:absolute;top:4px;right:4px;width:24px;height:24px;border-radius:50%;background:rgba(0,0,0,0.6);color:white;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:.2s;}
.remove-image-btn:hover{background:rgba(225,69,67,0.9);}
.upload-btn{display:inline-block;padding:8px 16px;background:#f0f7ff;color:#3577dd;border:1px dashed #bfcae9;border-radius:6px;cursor:pointer;font-size:14px;transition:.2s;}
.upload-btn:hover{background:#e0eaff;border-color:#3577dd;}
.upload-btn.uploading{opacity:0.6;cursor:not-allowed;}
.upload-btn input:disabled{cursor:not-allowed;}
.paste-hint{font-size:12px;color:#94a3b8;margin-top:8px;}
.image-preview-modal{position:relative;max-width:90vw;max-height:90vh;}
.image-preview-modal img{max-width:100%;max-height:90vh;object-fit:contain;border-radius:8px;}
.close-preview{position:absolute;top:-30px;right:0;width:30px;height:30px;border-radius:50%;background:rgba(0,0,0,0.6);color:white;border:none;cursor:pointer;font-size:20px;display:flex;align-items:center;justify-content:center;}
</style>

