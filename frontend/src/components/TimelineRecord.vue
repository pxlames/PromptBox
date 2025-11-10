<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { api, type TimelineTopic, type TimelineEntry, type TimelineSubEntry, type TimelineTopicCreate, type TimelineEntryCreate, type TimelineSubEntryCreate } from '../api'

const topics = ref<TimelineTopic[]>([])
const entriesMap = ref<Map<number, TimelineEntry[]>>(new Map())
const subEntriesMap = ref<Map<number, TimelineSubEntry[]>>(new Map())
const loading = ref(true)
const error = ref<string | null>(null)

// 主题管理
const showTopicModal = ref(false)
const editingTopicId = ref<number | null>(null)
const topicTitle = ref('')

// 条目管理
const showEntryModal = ref(false)
const editingEntryId = ref<number | null>(null)
const editingTopicIdForEntry = ref<number | null>(null)
const entrySubtitle = ref('')
const entryConclusion = ref('')
const entryContent = ref('')
const entryImages = ref<string[]>([])

// 子条目管理
const showSubEntryModal = ref(false)
const editingSubEntryId = ref<number | null>(null)
const editingEntryIdForSubEntry = ref<number | null>(null)
const subEntrySubtitle = ref('')
const subEntryConclusion = ref('')
const subEntryContent = ref('')
const subEntryImages = ref<string[]>([])

const uploadingImages = ref(false)
const imagePreviewUrl = ref<string | null>(null)

// 文本区域引用
const conclusionTextareaRef = ref<HTMLTextAreaElement | null>(null)
const contentTextareaRef = ref<HTMLTextAreaElement | null>(null)
const subEntryConclusionTextareaRef = ref<HTMLTextAreaElement | null>(null)
const subEntryContentTextareaRef = ref<HTMLTextAreaElement | null>(null)

// 加载数据
async function loadTopics() {
  try {
    topics.value = await api.getTimelineTopics()
    // 加载每个主题的条目
    for (const topic of topics.value) {
      await loadEntries(topic.id)
    }
  } catch (e: any) {
    console.error('加载主题失败:', e)
    error.value = '加载主题失败'
  }
}

async function loadEntries(topicId: number) {
  try {
    const entries = await api.getTimelineEntries(topicId)
    entriesMap.value.set(topicId, entries)
    // 加载每个条目的子条目
    for (const entry of entries) {
      await loadSubEntries(entry.id)
    }
  } catch (e: any) {
    console.error('加载条目失败:', e)
  }
}

async function loadSubEntries(entryId: number) {
  try {
    const subEntries = await api.getTimelineSubEntries(entryId)
    subEntriesMap.value.set(entryId, subEntries)
  } catch (e: any) {
    console.error('加载子条目失败:', e)
  }
}

async function load() {
  loading.value = true
  error.value = null
  await api.ready()
  await loadTopics()
  loading.value = false
}

onMounted(() => {
  load()
  // 监听全局粘贴事件
  document.addEventListener('paste', handleGlobalPaste)
})

// 清理事件监听
watch(() => showEntryModal.value, (isOpen, wasOpen) => {
  if (isOpen && !wasOpen) {
    // 模态框打开时，为文本区域添加粘贴监听
    nextTick(() => {
      if (contentTextareaRef.value) {
        contentTextareaRef.value.addEventListener('paste', handleTextareaPaste)
      }
      if (conclusionTextareaRef.value) {
        conclusionTextareaRef.value.addEventListener('paste', handleTextareaPaste)
      }
    })
  } else if (!isOpen && wasOpen) {
    // 模态框关闭时，移除事件监听
    if (contentTextareaRef.value) {
      contentTextareaRef.value.removeEventListener('paste', handleTextareaPaste)
    }
    if (conclusionTextareaRef.value) {
      conclusionTextareaRef.value.removeEventListener('paste', handleTextareaPaste)
    }
  }
})

// 子条目模态框事件监听
watch(() => showSubEntryModal.value, (isOpen, wasOpen) => {
  if (isOpen && !wasOpen) {
    // 模态框打开时，为文本区域添加粘贴监听
    nextTick(() => {
      if (subEntryContentTextareaRef.value) {
        subEntryContentTextareaRef.value.addEventListener('paste', handleSubEntryTextareaPaste)
      }
      if (subEntryConclusionTextareaRef.value) {
        subEntryConclusionTextareaRef.value.addEventListener('paste', handleSubEntryTextareaPaste)
      }
    })
  } else if (!isOpen && wasOpen) {
    // 模态框关闭时，移除事件监听
    if (subEntryContentTextareaRef.value) {
      subEntryContentTextareaRef.value.removeEventListener('paste', handleSubEntryTextareaPaste)
    }
    if (subEntryConclusionTextareaRef.value) {
      subEntryConclusionTextareaRef.value.removeEventListener('paste', handleSubEntryTextareaPaste)
    }
  }
})

const sortedTopics = computed(() => [...topics.value].sort((a, b) => a.order - b.order))

// 主题管理
function openTopicModal(topic?: TimelineTopic) {
  editingTopicId.value = topic?.id || null
  topicTitle.value = topic?.title || ''
  showTopicModal.value = true
}

async function saveTopic() {
  const title = topicTitle.value.trim()
  if (!title) {
    alert('请输入主题标题！')
    return
  }
  try {
    if (editingTopicId.value) {
      await api.updateTimelineTopic(editingTopicId.value, { title })
    } else {
      const maxOrder = topics.value.reduce((m, t) => Math.max(m, t.order), 0)
      await api.createTimelineTopic({ title, order: maxOrder + 1 })
    }
    await loadTopics()
    showTopicModal.value = false
    topicTitle.value = ''
    editingTopicId.value = null
  } catch (e: any) {
    alert('保存主题失败: ' + (e?.message || '未知错误'))
  }
}

async function deleteTopic(id: number) {
  if (!confirm('确定删除该主题？将同时删除主题下的所有条目。')) return
  try {
    await api.deleteTimelineTopic(id)
    await loadTopics()
  } catch (e: any) {
    alert('删除主题失败: ' + (e?.message || '未知错误'))
  }
}

// 条目管理
function openEntryModal(topicId: number, entry?: TimelineEntry) {
  editingTopicIdForEntry.value = topicId
  editingEntryId.value = entry?.id || null
  entrySubtitle.value = entry?.subtitle || ''
  entryConclusion.value = entry?.conclusion || ''
  entryContent.value = entry?.content || ''
  entryImages.value = entry?.image_paths ? entry.image_paths.split(',').filter(p => p.trim()) : []
  showEntryModal.value = true
}

async function saveEntry() {
  const subtitle = entrySubtitle.value.trim()
  if (!subtitle) {
    alert('请输入小标题！')
    return
  }
  if (!editingTopicIdForEntry.value) {
    alert('请选择主题！')
    return
  }
  try {
    const topicId = editingTopicIdForEntry.value
    const imagePaths = entryImages.value.length > 0 ? entryImages.value.join(',') : null
    let entryId = editingEntryId.value
    if (entryId) {
      await api.updateTimelineEntry(entryId, {
        subtitle,
        conclusion: entryConclusion.value.trim() || null,
        content: entryContent.value.trim() || null,
        image_paths: imagePaths
      })
    } else {
      const entries = entriesMap.value.get(topicId) || []
      const maxOrder = entries.reduce((m, e) => Math.max(m, e.order), 0)
      const newEntry = await api.createTimelineEntry({
        topic_id: topicId,
        subtitle,
        conclusion: entryConclusion.value.trim() || null,
        content: entryContent.value.trim() || null,
        image_paths: imagePaths,
        order: maxOrder + 1
      })
      entryId = newEntry.id
    }
    await loadEntries(topicId)
    if (entryId) {
      await loadSubEntries(entryId)
    }
    showEntryModal.value = false
    entrySubtitle.value = ''
    entryConclusion.value = ''
    entryContent.value = ''
    entryImages.value = []
    editingEntryId.value = null
    editingTopicIdForEntry.value = null
  } catch (e: any) {
    alert('保存条目失败: ' + (e?.message || '未知错误'))
  }
}

async function deleteEntry(topicId: number, entryId: number) {
  if (!confirm('确定删除该条目？')) return
  try {
    await api.deleteTimelineEntry(entryId)
    await loadEntries(topicId)
  } catch (e: any) {
    alert('删除条目失败: ' + (e?.message || '未知错误'))
  }
}

function getEntries(topicId: number): TimelineEntry[] {
  return entriesMap.value.get(topicId) || []
}

function getSubEntries(entryId: number): TimelineSubEntry[] {
  return subEntriesMap.value.get(entryId) || []
}

// 图片处理函数
function getImageUrl(path: string) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  return path.startsWith('/') ? `/api${path}` : `/api/uploads/${path}`
}

function getImagePaths(entry: TimelineEntry): string[] {
  if (!entry.image_paths) return []
  return entry.image_paths.split(',').filter(p => p.trim())
}

// 处理全局粘贴事件（用于图片上传区域）
async function handleGlobalPaste(e: ClipboardEvent) {
  // 只有在条目或子条目编辑模态框打开时才处理
  if (!showEntryModal.value && !showSubEntryModal.value) return
  
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type.indexOf('image') !== -1) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) {
        if (showEntryModal.value) {
          await uploadImage(file)
        } else if (showSubEntryModal.value) {
          await uploadSubEntryImage(file)
        }
      }
    }
  }
}

// 处理文本区域中的粘贴（在内容或结论文本框中粘贴图片）
async function handleTextareaPaste(e: ClipboardEvent) {
  if (!showEntryModal.value) return
  
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type.indexOf('image') !== -1) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) {
        await uploadImage(file)
      }
    }
  }
}

// 处理子条目文本区域中的粘贴
async function handleSubEntryTextareaPaste(e: ClipboardEvent) {
  if (!showSubEntryModal.value) return
  
  const items = e.clipboardData?.items
  if (!items) return

  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type.indexOf('image') !== -1) {
      e.preventDefault()
      const file = item.getAsFile()
      if (file) {
        await uploadSubEntryImage(file)
      }
    }
  }
}

// 上传子条目图片
async function uploadSubEntryImage(file: File) {
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const result = await api.uploadTimelineImages([file])
    if (result.filenames && result.filenames.length > 0) {
      subEntryImages.value.push(...result.filenames)
    }
  } catch (e: any) {
    alert('图片上传失败: ' + (e?.message || '未知错误'))
  } finally {
    uploadingImages.value = false
  }
}

// 上传图片
async function uploadImage(file: File) {
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const result = await api.uploadTimelineImages([file])
    if (result.filenames && result.filenames.length > 0) {
      entryImages.value.push(...result.filenames)
    }
  } catch (e: any) {
    alert('图片上传失败: ' + (e?.message || '未知错误'))
  } finally {
    uploadingImages.value = false
  }
}

// 处理文件选择
async function handleFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0) return
  
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const fileArray = Array.from(files)
    const result = await api.uploadTimelineImages(fileArray)
    if (result.filenames && result.filenames.length > 0) {
      entryImages.value.push(...result.filenames)
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

// 删除图片
function removeImage(index: number) {
  entryImages.value.splice(index, 1)
}

// 预览图片
function previewImage(path: string) {
  imagePreviewUrl.value = getImageUrl(path)
}

function closeImagePreview() {
  imagePreviewUrl.value = null
}

// 子条目管理
function openSubEntryModal(entryId: number, subEntry?: TimelineSubEntry) {
  editingEntryIdForSubEntry.value = entryId
  editingSubEntryId.value = subEntry?.id || null
  subEntrySubtitle.value = subEntry?.subtitle || ''
  subEntryConclusion.value = subEntry?.conclusion || ''
  subEntryContent.value = subEntry?.content || ''
  subEntryImages.value = subEntry?.image_paths ? subEntry.image_paths.split(',').filter(p => p.trim()) : []
  showSubEntryModal.value = true
}

async function saveSubEntry() {
  const subtitle = subEntrySubtitle.value.trim()
  if (!subtitle) {
    alert('请输入子标题！')
    return
  }
  if (!editingEntryIdForSubEntry.value) {
    alert('请选择条目！')
    return
  }
  try {
    const entryId = editingEntryIdForSubEntry.value
    const imagePaths = subEntryImages.value.length > 0 ? subEntryImages.value.join(',') : null
    if (editingSubEntryId.value) {
      await api.updateTimelineSubEntry(editingSubEntryId.value, {
        subtitle,
        conclusion: subEntryConclusion.value.trim() || null,
        content: subEntryContent.value.trim() || null,
        image_paths: imagePaths
      })
    } else {
      const subEntries = subEntriesMap.value.get(entryId) || []
      const maxOrder = subEntries.reduce((m, e) => Math.max(m, e.order), 0)
      await api.createTimelineSubEntry({
        entry_id: entryId,
        subtitle,
        conclusion: subEntryConclusion.value.trim() || null,
        content: subEntryContent.value.trim() || null,
        image_paths: imagePaths,
        order: maxOrder + 1
      })
    }
    await loadSubEntries(entryId)
    showSubEntryModal.value = false
    subEntrySubtitle.value = ''
    subEntryConclusion.value = ''
    subEntryContent.value = ''
    subEntryImages.value = []
    editingSubEntryId.value = null
    editingEntryIdForSubEntry.value = null
  } catch (e: any) {
    alert('保存子条目失败: ' + (e?.message || '未知错误'))
  }
}

async function deleteSubEntry(entryId: number, subEntryId: number) {
  if (!confirm('确定删除该子条目？')) return
  try {
    await api.deleteTimelineSubEntry(subEntryId)
    await loadSubEntries(entryId)
  } catch (e: any) {
    alert('删除子条目失败: ' + (e?.message || '未知错误'))
  }
}

function getImagePathsForSubEntry(subEntry: TimelineSubEntry): string[] {
  if (!subEntry.image_paths) return []
  return subEntry.image_paths.split(',').filter(p => p.trim())
}

// 处理子条目文件选择
async function handleSubEntryFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0) return
  
  if (uploadingImages.value) return
  uploadingImages.value = true
  try {
    const fileArray = Array.from(files)
    const result = await api.uploadTimelineImages(fileArray)
    if (result.filenames && result.filenames.length > 0) {
      subEntryImages.value.push(...result.filenames)
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
</script>

<template>
  <div class="timeline-root">
    <div class="header-bar">
      <h2 class="page-title">📋 记录线</h2>
      <button class="add-topic-btn" @click="openTopicModal()">➕ 新增主题</button>
    </div>

    <div v-if="loading" class="empty">加载中...</div>
    <div v-else-if="error" class="empty error">{{ error }}</div>
    <div v-else class="timeline-container">
      <div v-if="sortedTopics.length === 0" class="nodata">
        暂无主题，点击"新增主题"开始记录吧！
      </div>
      
      <div v-for="topic in sortedTopics" :key="topic.id" class="topic-section">
        <div class="topic-wrapper">
          <div class="topic-header">
            <h3 class="topic-title">{{ topic.title }}</h3>
            <div class="topic-actions">
              <button class="btn-edit" @click="openTopicModal(topic)">编辑</button>
              <button class="btn-delete" @click="deleteTopic(topic.id)">删除</button>
              <button class="btn-add-entry" @click="openEntryModal(topic.id)">➕ 添加条目</button>
            </div>
          </div>
          
          <div class="timeline-line">
            <div class="timeline-start">|</div>
            <div class="timeline-start">|</div>
            <div v-for="(entry, index) in getEntries(topic.id)" :key="entry.id" class="timeline-entry">
              <div class="entry-wrapper">
                <div class="entry-prefix">— —</div>
                <div class="entry-content">
                  <div class="entry-subtitle">{{ entry.subtitle }}</div>
                  <div v-if="entry.conclusion" class="entry-conclusion">
                    <span class="label">调查结论：</span>{{ entry.conclusion }}
                  </div>
                  <div v-if="entry.content" class="entry-detail">{{ entry.content }}</div>
                  <div v-if="getImagePaths(entry).length > 0" class="entry-images">
                    <img 
                      v-for="(imgPath, idx) in getImagePaths(entry)" 
                      :key="idx"
                      :src="getImageUrl(imgPath)"
                      alt="条目图片"
                      class="entry-image"
                      @click="previewImage(imgPath)"
                    />
                  </div>
                </div>
                <div class="entry-actions">
                  <button class="btn-edit-small" @click="openEntryModal(topic.id, entry)">编辑</button>
                  <button class="btn-delete-small" @click="deleteEntry(topic.id, entry.id)">删除</button>
                  <button class="btn-add-sub-entry" @click="openSubEntryModal(entry.id)">➕ 添加子条目</button>
                </div>
              </div>
              
              <!-- 子条目显示 -->
              <div v-if="getSubEntries(entry.id).length > 0" class="sub-entries-wrapper">
                <div v-for="(subEntry, subIndex) in getSubEntries(entry.id)" :key="subEntry.id" class="sub-entry-item">
                  <div class="sub-entry-line">|</div>
                  <div class="sub-entry-wrapper">
                    <div class="sub-entry-prefix">— —</div>
                    <div class="sub-entry-content">
                      <div class="sub-entry-subtitle">{{ subEntry.subtitle }}</div>
                      <div v-if="subEntry.conclusion" class="sub-entry-conclusion">
                        <span class="label">调查结论：</span>{{ subEntry.conclusion }}
                      </div>
                      <div v-if="subEntry.content" class="sub-entry-detail">{{ subEntry.content }}</div>
                      <div v-if="getImagePathsForSubEntry(subEntry).length > 0" class="sub-entry-images">
                        <img 
                          v-for="(imgPath, idx) in getImagePathsForSubEntry(subEntry)" 
                          :key="idx"
                          :src="getImageUrl(imgPath)"
                          alt="子条目图片"
                          class="sub-entry-image"
                          @click="previewImage(imgPath)"
                        />
                      </div>
                    </div>
                    <div class="sub-entry-actions">
                      <button class="btn-edit-small" @click="openSubEntryModal(entry.id, subEntry)">编辑</button>
                      <button class="btn-delete-small" @click="deleteSubEntry(entry.id, subEntry.id)">删除</button>
                    </div>
                  </div>
                  <div v-if="subIndex < getSubEntries(entry.id).length - 1" class="sub-entry-line">|</div>
                </div>
              </div>
              
              <div v-if="index < getEntries(topic.id).length - 1" class="entry-line">|</div>
            </div>
            <div v-if="getEntries(topic.id).length === 0" class="no-entries">
              <div class="entry-line">|</div>
              <div class="no-entries-text">暂无条目，点击"添加条目"开始记录</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主题管理 Modal -->
    <div class="modal" v-if="showTopicModal" @click.self="showTopicModal = false">
      <div class="modal-body">
        <div class="modal-head">{{ editingTopicId ? '编辑主题' : '新增主题' }}</div>
        <input 
          v-model="topicTitle" 
          placeholder="主题标题（如：百度实习调查）" 
          class="modal-input"
          @keyup.enter="saveTopic"
        />
        <div class="modal-actions">
          <button class="btn-save" @click="saveTopic">保存</button>
          <button @click="showTopicModal = false">取消</button>
        </div>
      </div>
    </div>

    <!-- 条目管理 Modal -->
    <div class="modal" v-if="showEntryModal" @click.self="showEntryModal = false">
      <div class="modal-body entry-modal-body">
        <div class="modal-head">{{ editingEntryId ? '编辑条目' : '新增条目' }}</div>
        <input 
          v-model="entrySubtitle" 
          placeholder="小标题（如：部门情况）" 
          class="modal-input"
        />
        <textarea 
          v-model="entryConclusion" 
          placeholder="调查结论（可选，支持粘贴图片，Ctrl+V）" 
          rows="3"
          class="modal-textarea"
          ref="conclusionTextareaRef"
        ></textarea>
        <textarea 
          v-model="entryContent" 
          placeholder="详细内容（可选，支持粘贴图片，Ctrl+V）" 
          rows="5"
          class="modal-textarea"
          ref="contentTextareaRef"
        ></textarea>
        
        <!-- 图片上传区域 -->
        <div class="image-upload-area">
          <div class="image-preview-list">
            <div 
              v-for="(imgPath, idx) in entryImages" 
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
          <div class="paste-hint">💡 提示：在文本框中按 Ctrl+V 可粘贴图片，图片会自动上传</div>
        </div>
        
        <div class="modal-actions">
          <button class="btn-save" @click="saveEntry">保存</button>
          <button @click="showEntryModal = false">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 子条目管理 Modal -->
    <div class="modal" v-if="showSubEntryModal" @click.self="showSubEntryModal = false">
      <div class="modal-body entry-modal-body">
        <div class="modal-head">{{ editingSubEntryId ? '编辑子条目' : '新增子条目' }}</div>
        <input 
          v-model="subEntrySubtitle" 
          placeholder="子标题" 
          class="modal-input"
        />
        <textarea 
          v-model="subEntryConclusion" 
          placeholder="调查结论（可选，支持粘贴图片，Ctrl+V）" 
          rows="3"
          class="modal-textarea"
          ref="subEntryConclusionTextareaRef"
        ></textarea>
        <textarea 
          v-model="subEntryContent" 
          placeholder="详细内容（可选，支持粘贴图片，Ctrl+V）" 
          rows="5"
          class="modal-textarea"
          ref="subEntryContentTextareaRef"
        ></textarea>
        
        <!-- 图片上传区域 -->
        <div class="image-upload-area">
          <div class="image-preview-list">
            <div 
              v-for="(imgPath, idx) in subEntryImages" 
              :key="idx"
              class="image-preview-item"
            >
              <img :src="getImageUrl(imgPath)" alt="预览" />
              <button class="remove-image-btn" @click="subEntryImages.splice(idx, 1)">×</button>
            </div>
          </div>
          <label class="upload-btn" :class="{ uploading: uploadingImages }">
            <input 
              type="file" 
              accept="image/*" 
              multiple 
              @change="handleSubEntryFileSelect"
              :disabled="uploadingImages"
              style="display: none"
            />
            <span v-if="uploadingImages">⏳ 上传中...</span>
            <span v-else>📷 上传图片</span>
          </label>
          <div class="paste-hint">💡 提示：在文本框中按 Ctrl+V 可粘贴图片，图片会自动上传</div>
        </div>
        
        <div class="modal-actions">
          <button class="btn-save" @click="saveSubEntry">保存</button>
          <button @click="showSubEntryModal = false">取消</button>
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
.timeline-root {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  background: #fcfcff;
  min-height: 100%;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.add-topic-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.add-topic-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.empty {
  padding: 60px 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 16px;
}

.empty.error {
  color: #ef4444;
}

.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.nodata {
  padding: 60px 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 16px;
}

.topic-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.topic-wrapper {
  position: relative;
}

.topic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding-bottom: 16px;
}

.topic-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  padding-left: 0;
}

.topic-actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete, .btn-add-entry {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-edit {
  background: #e0eaff;
  color: #3577dd;
}

.btn-edit:hover {
  background: #d0daff;
}

.btn-delete {
  background: #fff1f0;
  color: #e14543;
}

.btn-delete:hover {
  background: #ffe0df;
}

.btn-add-entry {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-add-entry:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.btn-add-sub-entry {
  background: #f0f7ff;
  color: #3577dd;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-add-sub-entry:hover {
  background: #e0eaff;
}

.timeline-line {
  position: relative;
  padding-left: 0;
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.timeline-start {
  color: #667eea;
  font-size: 20px;
  font-weight: 400;
  line-height: 1.8;
  margin-bottom: 0;
  font-family: 'Courier New', monospace;
  text-align: left;
  width: auto;
  min-width: 20px;
}

.timeline-entry {
  position: relative;
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
}

.entry-line {
  color: #667eea;
  font-size: 20px;
  font-weight: 400;
  line-height: 1.8;
  margin-bottom: 0;
  margin-top: 4px;
  font-family: 'Courier New', monospace;
  text-align: left;
  width: auto;
  min-width: 20px;
}

.entry-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 0;
  margin-left: 0;
  width: 100%;
  margin-top: 4px;
}

.entry-prefix {
  color: #64748b;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.8;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 0;
  font-family: 'Courier New', monospace;
  width: auto;
  min-width: 50px;
}

.entry-content {
  flex: 1;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #667eea;
  min-width: 0;
}

.entry-subtitle {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
  line-height: 1.5;
}

.entry-conclusion {
  font-size: 14px;
  color: #475569;
  margin-bottom: 8px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.entry-conclusion .label {
  font-weight: 600;
  color: #64748b;
}

.entry-detail {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.entry-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  flex-shrink: 0;
  align-self: flex-start;
}

.btn-edit-small, .btn-delete-small {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-edit-small {
  background: #e0eaff;
  color: #3577dd;
}

.btn-edit-small:hover {
  background: #d0daff;
}

.btn-delete-small {
  background: #fff1f0;
  color: #e14543;
}

.btn-delete-small:hover {
  background: #ffe0df;
}

.no-entries {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 20px 0;
  width: 100%;
}

.no-entries-text {
  color: #94a3b8;
  font-size: 14px;
  font-style: italic;
  padding-top: 2px;
  margin-left: 50px;
}

.modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.5);
  display: grid;
  place-items: center;
}

.modal-body {
  background: white;
  padding: 30px 40px;
  border-radius: 12px;
  box-shadow: 0 10px 32px rgba(0, 0, 0, 0.2);
  min-width: 400px;
  max-width: 90vw;
}

.entry-modal-body {
  min-width: 500px;
  max-width: 700px;
}

.modal-head {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

.modal-input {
  width: 100%;
  padding: 12px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  background: #fff;
  outline: none;
  transition: all 0.2s;
  margin-bottom: 12px;
}

.modal-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.modal-textarea {
  width: 100%;
  padding: 12px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: all 0.2s;
  margin-bottom: 12px;
}

.modal-textarea:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.modal-actions button:last-child {
  background: #f1f5f9;
  color: #64748b;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-actions button:last-child:hover {
  background: #e2e8f0;
}

.entry-images {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.entry-image {
  max-width: 150px;
  max-height: 150px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.entry-image:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-upload-area {
  margin-bottom: 12px;
}

.image-preview-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.image-preview-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.image-preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.2s;
}

.remove-image-btn:hover {
  background: rgba(225, 69, 67, 0.9);
}

.upload-btn {
  display: inline-block;
  padding: 8px 16px;
  background: #f0f7ff;
  color: #3577dd;
  border: 1px dashed #bfcae9;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.upload-btn:hover {
  background: #e0eaff;
  border-color: #3577dd;
}

.upload-btn.uploading {
  opacity: 0.6;
  cursor: not-allowed;
}

.upload-btn input:disabled {
  cursor: not-allowed;
}

.paste-hint {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 8px;
}

.image-preview-modal {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.image-preview-modal img {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
}

.close-preview {
  position: absolute;
  top: -30px;
  right: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 子条目样式 */
.sub-entries-wrapper {
  margin-left: 60px;
  margin-top: 8px;
  margin-bottom: 8px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.sub-entry-item {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: flex-start;
}

.sub-entry-line {
  color: #94a3b8;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.8;
  margin-bottom: 0;
  margin-top: 4px;
  font-family: 'Courier New', monospace;
  text-align: left;
  width: auto;
  min-width: 20px;
}

.sub-entry-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 0;
  margin-left: 0;
  width: 100%;
  margin-top: 4px;
}

.sub-entry-prefix {
  color: #94a3b8;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.8;
  white-space: nowrap;
  flex-shrink: 0;
  margin-top: 0;
  font-family: 'Courier New', monospace;
  width: auto;
  min-width: 50px;
}

.sub-entry-content {
  flex: 1;
  background: #f1f5f9;
  padding: 12px;
  border-radius: 6px;
  border-left: 2px solid #94a3b8;
  min-width: 0;
}

.sub-entry-subtitle {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 6px;
  line-height: 1.5;
}

.sub-entry-conclusion {
  font-size: 13px;
  color: #475569;
  margin-bottom: 6px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.sub-entry-conclusion .label {
  font-weight: 600;
  color: #64748b;
}

.sub-entry-detail {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.sub-entry-images {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.sub-entry-image {
  max-width: 120px;
  max-height: 120px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

.sub-entry-image:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.sub-entry-actions {
  display: flex;
  gap: 6px;
  margin-top: 8px;
  flex-shrink: 0;
  align-self: flex-start;
}
</style>

