<template>
  <div class="ai-assistant-container">
    <!-- 浮动助手精灵 -->
    <button 
      v-if="!isOpen"
      class="assistant-trigger"
      :style="{ left: triggerPosition.x + 'px', top: triggerPosition.y + 'px' }"
      @mousedown="startDragTrigger"
      @click="openDialog"
      :title="`AI助手 (${shortcutText}) - 可拖动`"
    >
      <span class="assistant-icon" :class="{ 'shaking': isLoading }">相信</span>
    </button>

    <!-- AI助手对话框 -->
    <transition name="dialog-fade">
      <div 
        v-if="isOpen && !showPostCenter"
        class="assistant-dialog"
        :style="{ 
          left: dialogPosition.x + 'px', 
          top: dialogPosition.y + 'px',
          width: dialogSize.width + 'px',
          height: dialogSize.height + 'px'
        }"
        ref="dialogRef"
      >
        <div 
          class="dialog-header"
          @mousedown="startDragDialog"
        >
          <div class="header-left">
            <button 
              class="history-button"
              @click="toggleHistorySidebar"
              title="聊天历史"
              v-if="!showHistorySidebar"
            >
              📜
            </button>
            <button 
              class="post-center-button"
              @click="goToPostCenter"
              title="查看高赞内容"
            >
              👍
            </button>
            <span class="dialog-icon">🤖</span>
            <h3 class="dialog-title">{{ currentHistoryTitle || 'AI助手' }}</h3>
          </div>
          <button class="close-button" @click="closeDialog" title="关闭">✕</button>
        </div>
        
        <!-- 历史记录侧边栏 -->
        <transition name="sidebar-slide">
          <div v-if="showHistorySidebar" class="history-sidebar">
            <div class="history-header">
              <h3>聊天历史</h3>
              <button class="close-history-button" @click="toggleHistorySidebar" title="关闭">✕</button>
            </div>
            <div class="history-search">
              <input 
                v-model="historySearchText"
                @input="searchHistories"
                type="text"
                placeholder="搜索历史记录..."
                class="history-search-input"
              />
            </div>
            <div class="history-list" ref="historyListRef">
              <div 
                v-for="history in chatHistories" 
                :key="history.id"
                :class="['history-item', { active: currentHistoryId === history.id }]"
                @click="loadHistory(history.id)"
              >
                <div class="history-item-title">{{ history.title || '新对话' }}</div>
                <div class="history-item-time">{{ formatTime(history.updated_at) }}</div>
                <button 
                  class="history-item-delete"
                  @click.stop="deleteHistory(history.id)"
                  title="删除"
                >
                  🗑️
                </button>
              </div>
              <div v-if="chatHistories.length === 0 && !loadingHistories" class="history-empty">
                暂无聊天历史
              </div>
              <div v-if="loadingHistories" class="history-loading">
                加载中...
              </div>
            </div>
            <div class="history-footer">
              <button class="new-chat-button" @click="startNewChat">
                ➕ 新对话
              </button>
            </div>
          </div>
        </transition>
        
        <!-- 调整大小手柄 -->
        <div 
          class="resize-handle"
          @mousedown="startResizeDialog"
          title="拖动调整大小"
        ></div>

        <div class="dialog-content" ref="contentRef">
          <div class="messages-container">
            <div 
              v-for="(message, index) in messages" 
              :key="index"
              :class="['message', `message-${message.role}`]"
            >
              <div class="message-avatar" :class="{ 'shaking': isLoading && message.role === 'assistant' && index === messages.length - 1 }">
                <span v-if="message.role === 'user'">👤</span>
                <span v-else>相信</span>
              </div>
              <div class="message-content">
                <div v-if="message.image_urls && message.image_urls.length > 0" class="message-images">
                  <img 
                    v-for="(imgUrl, imgIndex) in message.image_urls" 
                    :key="imgIndex"
                    :src="getImageUrl(imgUrl)"
                    alt="上传的图片"
                    class="message-image"
                    @click="previewImage(imgUrl)"
                  />
                </div>
                <!-- 如果是空的assistant消息且正在加载，显示输入指示器 -->
                <div v-if="message.role === 'assistant' && !message.content && isLoading && index === messages.length - 1" class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div v-if="message.content" class="message-text-wrapper">
                  <div class="message-text" v-html="formatMessage(message.content)"></div>
                  <!-- 点赞按钮（仅AI回复显示） -->
                  <button 
                    v-if="message.role === 'assistant' && message.content"
                    class="like-button"
                    :class="{ 'liked': message.liked }"
                    @click="toggleLike(index)"
                    :title="message.liked ? '取消点赞' : '点赞'"
                  >
                    {{ message.liked ? '👍' : '👍' }}
                    <span v-if="message.liked" class="like-text">已点赞</span>
                  </button>
                </div>
                <div v-if="message.role === 'assistant' && message.reasoning_content" class="message-reasoning">
                  <details>
                    <summary>思考过程</summary>
                    <pre>{{ message.reasoning_content }}</pre>
                  </details>
                </div>
              </div>
            </div>
            
            <!-- 正在输入指示器（仅当没有消息或最后一条消息不是assistant消息时显示） -->
            <div v-if="isLoading && (messages.length === 0 || messages[messages.length - 1].role !== 'assistant')" class="message message-assistant">
              <div class="message-avatar shaking">
                <span>相信</span>
              </div>
              <div class="message-content">
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="dialog-input">
          <div class="input-images" v-if="pendingImages.length > 0">
            <div 
              v-for="(img, index) in pendingImages" 
              :key="index"
              class="image-preview"
            >
              <img :src="img.preview" alt="预览" />
              <button class="remove-image" @click="removePendingImage(index)">✕</button>
            </div>
          </div>
          
          <div class="input-area">
            <button 
              class="dice-button"
              @click="rollDice"
              :disabled="isLoading || rollingDice"
              title="随机观点（筛子）"
            >
              <span v-if="rollingDice">⏳</span>
              <span v-else>🎲</span>
            </button>
            
            <label class="file-input-label">
              <input 
                type="file" 
                accept="image/*" 
                multiple 
                @change="handleImageSelect"
                ref="fileInputRef"
                style="display: none"
              />
              <span class="file-button" title="上传图片">📷</span>
            </label>
            
            <textarea
              v-model="inputText"
              @keydown="handleKeyDown"
              @input="adjustTextareaHeight"
              :placeholder="isLoading ? 'AI正在回复...' : '输入您的问题（支持图片）...'"
              :disabled="isLoading"
              class="input-textarea"
              ref="textareaRef"
              rows="1"
            ></textarea>
            
            <button 
              @click="sendMessage"
              :disabled="isLoading || (!inputText.trim() && pendingImages.length === 0)"
              class="send-button"
              title="发送消息"
            >
              <span v-if="isLoading">⏳</span>
              <span v-else>📤</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- 帖子中心视图 -->
    <transition name="dialog-fade">
      <div 
        v-if="isOpen && showPostCenter"
        class="assistant-dialog"
        :style="{ 
          left: dialogPosition.x + 'px', 
          top: dialogPosition.y + 'px',
          width: dialogSize.width + 'px',
          height: dialogSize.height + 'px'
        }"
      >
        <LikePostCenter @back="showPostCenter = false" />
      </div>
    </transition>
    

    <!-- 图片预览模态框 -->
    <transition name="modal-fade">
      <div v-if="previewImageUrl" class="image-preview-modal" @click="closeImagePreview">
        <img :src="getImageUrl(previewImageUrl)" alt="预览" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { api } from '../api'
import LikePostCenter from './LikePostCenter.vue'

const isOpen = ref(false)
const messages = ref([])
const inputText = ref('')
const isLoading = ref(false)
const pendingImages = ref([])
const previewImageUrl = ref(null)
const contentRef = ref(null)
const textareaRef = ref(null)
const fileInputRef = ref(null)
const dialogRef = ref(null)

// 聊天历史相关
const showHistorySidebar = ref(false)
const chatHistories = ref([])
const loadingHistories = ref(false)
const historySearchText = ref('')
const currentHistoryId = ref(null)
const currentHistoryTitle = ref(null)
const historyListRef = ref(null)
let saveTimer = null

// 筛子功能相关
const rollingDice = ref(false)
const selectedOpinion = ref(null)

// 高赞帖子中心相关
const showPostCenter = ref(false)

// 位置状态 - 先从 localStorage 读取，如果没有则使用默认位置
function getInitialPositions() {
  // 默认位置
  const defaultTrigger = { x: window.innerWidth - 80, y: window.innerHeight - 80 }
  const defaultDialog = { x: window.innerWidth - 504, y: window.innerHeight - 624 }
  
  // 尝试从 localStorage 读取
  try {
    const savedTriggerPos = localStorage.getItem('aiAssistant_triggerPosition')
    const savedDialogPos = localStorage.getItem('aiAssistant_dialogPosition')
    
    if (savedTriggerPos) {
      const parsed = JSON.parse(savedTriggerPos)
      // 验证位置是否在窗口内
      if (parsed.x >= 0 && parsed.y >= 0) {
        defaultTrigger.x = Math.min(parsed.x, window.innerWidth - 56)
        defaultTrigger.y = Math.min(parsed.y, window.innerHeight - 56)
      }
    }
    
    if (savedDialogPos) {
      const parsed = JSON.parse(savedDialogPos)
      // 验证位置是否在窗口内
      if (parsed.x >= 0 && parsed.y >= 0) {
        defaultDialog.x = Math.min(parsed.x, window.innerWidth - 480)
        defaultDialog.y = Math.min(parsed.y, window.innerHeight - 600)
      }
    }
  } catch (e) {
    console.warn('Failed to load positions from localStorage:', e)
  }
  
  return {
    trigger: defaultTrigger,
    dialog: defaultDialog
  }
}

const initialPositions = getInitialPositions()
const triggerPosition = ref({ ...initialPositions.trigger })
const dialogPosition = ref({ ...initialPositions.dialog })

// 对话框大小状态 - 从 localStorage 读取或使用默认值
function getInitialDialogSize() {
  const defaultSize = { width: 480, height: 600 }
  
  try {
    const savedSize = localStorage.getItem('aiAssistant_dialogSize')
    if (savedSize) {
      const parsed = JSON.parse(savedSize)
      // 验证大小是否合理（最小宽度300，最小高度400，最大不超过窗口）
      if (parsed.width >= 300 && parsed.width <= window.innerWidth - 20) {
        defaultSize.width = Math.max(300, Math.min(parsed.width, window.innerWidth - 20))
      }
      if (parsed.height >= 400 && parsed.height <= window.innerHeight - 20) {
        defaultSize.height = Math.max(400, Math.min(parsed.height, window.innerHeight - 20))
      }
    }
  } catch (e) {
    console.warn('Failed to load dialog size from localStorage:', e)
  }
  
  return defaultSize
}

const dialogSize = ref({ ...getInitialDialogSize() })

// 拖动状态
const isDraggingTrigger = ref(false)
const isDraggingDialog = ref(false)
const isResizingDialog = ref(false)
const hasDragged = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0 })

// 快捷键配置（默认 Ctrl+K 或 Cmd+K）
const shortcutKey = 'k'
const useMetaKey = true // macOS 用 Cmd，Windows/Linux 用 Ctrl

const shortcutText = useMetaKey 
  ? (navigator.platform.includes('Mac') ? '⌘K' : 'Ctrl+K')
  : (navigator.platform.includes('Mac') ? '⌘K' : 'Ctrl+K')

// 快捷键监听
function handleKeyDown(e) {
  // Ctrl+K 或 Cmd+K 打开/关闭对话框
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    if (isOpen.value) {
      closeDialog()
    } else {
      openDialog()
    }
  }
  
  // Enter 发送消息（Shift+Enter 换行）
  if (e.key === 'Enter' && !e.shiftKey && !isLoading.value) {
    if (inputText.value.trim() || pendingImages.value.length > 0) {
      e.preventDefault()
      sendMessage()
    }
  }
}

// 打开对话框
function openDialog(e) {
  // 如果刚刚发生了拖动，不打开对话框
  if (hasDragged.value || isDraggingTrigger.value) {
    if (e) {
      e.preventDefault()
      e.stopPropagation()
    }
    return
  }
  
  isOpen.value = true
  // 对话框位置跟随触发按钮（可选：设置为居中或其他位置）
  nextTick(() => {
    scrollToBottom()
    textareaRef.value?.focus()
    // 加载历史记录列表
    loadHistories()
  })
}

// 关闭对话框
function closeDialog() {
  // 保存当前对话
  saveCurrentChatHistory()
  isOpen.value = false
  showHistorySidebar.value = false
  showPostCenter.value = false
  // 可选择：清空输入但不重置历史消息
  // inputText.value = ''
  // pendingImages.value = []
}

// 切换历史记录侧边栏
function toggleHistorySidebar() {
  showHistorySidebar.value = !showHistorySidebar.value
  if (showHistorySidebar.value) {
    loadHistories()
  }
}

// 加载历史记录列表
async function loadHistories() {
  if (loadingHistories.value) return
  
  loadingHistories.value = true
  try {
    const histories = await api.getChatHistories({
      skip: 0,
      limit: 50,
      q: historySearchText.value || null
    })
    chatHistories.value = histories
  } catch (error) {
    console.error('Failed to load histories:', error)
  } finally {
    loadingHistories.value = false
  }
}

// 搜索历史记录
function searchHistories() {
  // 防抖搜索
  if (saveTimer) {
    clearTimeout(saveTimer)
  }
  saveTimer = setTimeout(() => {
    loadHistories()
  }, 300)
}

// 加载指定历史记录
async function loadHistory(historyId) {
  try {
    const history = await api.getChatHistory(historyId)
    messages.value = history.messages.map(msg => ({
      role: msg.role,
      content: msg.content,
      image_urls: msg.image_urls || [],
      reasoning_content: '',
      liked: false,
      likeRecordId: null,
      userQuestion: ''
    }))
    currentHistoryId.value = history.id
    currentHistoryTitle.value = history.title
    showHistorySidebar.value = false
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to load history:', error)
    alert('加载历史记录失败')
  }
}

// 删除历史记录
async function deleteHistory(historyId) {
  if (!confirm('确定删除这条聊天历史吗？')) return
  
  try {
    await api.deleteChatHistory(historyId)
    // 如果删除的是当前历史，清空消息
    if (currentHistoryId.value === historyId) {
      messages.value = []
      currentHistoryId.value = null
      currentHistoryTitle.value = null
    }
    // 重新加载历史列表
    await loadHistories()
  } catch (error) {
    console.error('Failed to delete history:', error)
    alert('删除历史记录失败')
  }
}

// 开始新对话
function startNewChat() {
  messages.value = []
  currentHistoryId.value = null
  currentHistoryTitle.value = null
  showHistorySidebar.value = false
  inputText.value = ''
  pendingImages.value = []
}

// 保存当前聊天历史
async function saveCurrentChatHistory() {
  // 如果没有消息，不保存
  if (messages.value.length === 0) return
  
  try {
    // 生成标题（使用第一条用户消息的前30个字符）
    let title = currentHistoryTitle.value || null
    if (!title) {
      for (const msg of messages.value) {
        if (msg.role === 'user' && msg.content) {
          title = msg.content.slice(0, 30)
          if (msg.content.length > 30) {
            title += '...'
          }
          break
        }
      }
    }
    
    // 准备消息数据
    const messagesData = messages.value.map(msg => ({
      role: msg.role,
      content: msg.content,
      image_urls: msg.image_urls || []
    }))
    
    if (currentHistoryId.value) {
      // 更新现有历史
      await api.updateChatHistory(currentHistoryId.value, title, messagesData)
    } else {
      // 创建新历史
      const result = await api.saveChatHistory(title, messagesData)
      currentHistoryId.value = result.id
      currentHistoryTitle.value = result.title
      // 重新加载历史列表
      await loadHistories()
    }
  } catch (error) {
    console.error('Failed to save chat history:', error)
    // 不显示错误提示，避免打断用户体验
  }
}

// 格式化时间
function formatTime(timeStr) {
  try {
    const date = new Date(timeStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    
    if (days === 0) {
      // 今天
      return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    } else if (days === 1) {
      return '昨天'
    } else if (days < 7) {
      return `${days}天前`
    } else {
      return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
    }
  } catch (e) {
    return timeStr
  }
}

// 跳转到帖子中心
function goToPostCenter() {
  showPostCenter.value = true
}

// 点赞功能
async function toggleLike(messageIndex) {
  const message = messages.value[messageIndex]
  if (!message || message.role !== 'assistant' || !message.content) return
  
  try {
    if (message.liked) {
      // 取消点赞 - 删除点赞记录
      if (message.likeRecordId) {
        await api.deleteLikeRecord(message.likeRecordId)
      }
      message.liked = false
      message.likeRecordId = null
    } else {
      // 点赞 - 创建点赞记录
      const userQuestion = message.userQuestion || (messageIndex > 0 ? messages.value[messageIndex - 1].content : '')
      const result = await api.createLikeRecord(userQuestion, message.content)
      message.liked = true
      message.likeRecordId = result.id
    }
  } catch (error) {
    console.error('Failed to toggle like:', error)
    alert('操作失败：' + (error.message || '未知错误'))
  }
}

// 筛子功能：随机获取观点
async function rollDice() {
  if (rollingDice.value || isLoading.value) return
  
  rollingDice.value = true
  try {
    const opinion = await api.getRandomOpinion()
    selectedOpinion.value = opinion
    
    // 将观点内容显示在对话框中
    // 作为一条系统提示消息显示
    messages.value.push({
      role: 'user',
      content: `🎲 随机观点：\n\n${opinion.description}\n\n---\n\n（您可以在此基础上继续提问）`,
      image_urls: []
    })
    
    // 自动滚动到底部
    await nextTick()
    scrollToBottom()
    
    // 将观点内容也添加到输入框，方便用户继续编辑
    inputText.value = opinion.description + '\n\n'
    adjustTextareaHeight()
    textareaRef.value?.focus()
    
  } catch (error) {
    console.error('Failed to get random opinion:', error)
    alert('获取随机观点失败：' + (error.message || '未知错误'))
  } finally {
    rollingDice.value = false
  }
}

// 发送消息
async function sendMessage() {
  if (isLoading.value) return
  
  // 保留原始格式，只去掉首尾空白，保留中间的换行和格式
  const text = inputText.value.trimEnd() // 只去掉末尾空白，保留开头格式和所有换行
  const images = [...pendingImages.value]
  
  if (!text.trim() && images.length === 0) return // 检查去除空白后是否为空
  
  // 添加用户消息（保留所有换行和格式）
  messages.value.push({
    role: 'user',
    content: text,
    image_urls: images.map(img => img.url),
    liked: false
  })
  
  // 保存用户问题（用于点赞时使用）
  const userQuestion = text
  
  // 清空输入
  inputText.value = ''
  pendingImages.value = []
  
  // 滚动到底部
  await nextTick()
  scrollToBottom()
  
  // 开始加载
  isLoading.value = true
  
  // 构建消息历史（只保留最近的消息，避免token过多）
  const messageHistory = messages.value.slice(-10).map(msg => ({
    role: msg.role,
    content: msg.content,
    image_urls: msg.image_urls || []
  }))
  
  // 调用流式API
  const assistantMessage = {
    role: 'assistant',
    content: '',
    reasoning_content: '',
    liked: false,
    likeRecordId: null,
    userQuestion: userQuestion  // 保存对应的用户问题
  }
  
  messages.value.push(assistantMessage)
  const assistantIndex = messages.value.length - 1
  
  await nextTick()
  scrollToBottom()
  
  try {
    await api.chatStream(
      messageHistory,
      (chunk) => {
        // 通过索引更新，确保Vue能检测到变化
        if (messages.value[assistantIndex] && chunk) {
          messages.value[assistantIndex].content += chunk
          // 仅在用户已经在底部附近时自动滚动（使用节流优化）
          scrollToBottom(false)
        }
      },
      async () => {
        isLoading.value = false
        // AI回复完成后，强制滚动到底部
        scrollToBottom(true)
        
        // 自动保存聊天历史
        await saveCurrentChatHistory()
        
      },
      (error) => {
        isLoading.value = false
        if (messages.value[assistantIndex]) {
          messages.value[assistantIndex].content = `❌ 错误: ${error}`
        }
        scrollToBottom(true)
      }
    )
  } catch (error) {
    isLoading.value = false
    if (messages.value[assistantIndex]) {
      messages.value[assistantIndex].content = `❌ 错误: ${error.message || '请求失败'}`
    }
    scrollToBottom()
  }
}

// 处理图片选择
async function handleImageSelect(e) {
  const files = Array.from(e.target.files || [])
  
  for (const file of files) {
    if (!file.type.startsWith('image/')) {
      alert('请选择图片文件')
      continue
    }
    
    // 创建预览
    const reader = new FileReader()
    reader.onload = (event) => {
      pendingImages.value.push({
        file,
        preview: event.target.result,
        url: '' // 上传后更新
      })
    }
    reader.readAsDataURL(file)
    
    // 上传图片
    try {
      const result = await api.uploadAssistantImage(file)
      const index = pendingImages.value.findIndex(img => img.file === file)
      if (index >= 0) {
        pendingImages.value[index].url = result.url
      }
    } catch (error) {
      alert(`图片上传失败: ${error.message || '未知错误'}`)
      // 移除预览
      const index = pendingImages.value.findIndex(img => img.file === file)
      if (index >= 0) {
        pendingImages.value.splice(index, 1)
      }
    }
  }
  
  // 清空文件选择器的值，允许重复选择同一文件
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

// 移除待发送的图片
function removePendingImage(index) {
  pendingImages.value.splice(index, 1)
}

// 预览图片
function previewImage(url) {
  previewImageUrl.value = url
}

// 关闭图片预览
function closeImagePreview() {
  previewImageUrl.value = null
}

// 获取图片URL
function getImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  // 如果是相对路径，通过 /api 前缀访问
  return url.startsWith('/') ? `/api${url}` : `/api/uploads/${url}`
}

// 格式化消息内容（完整Markdown渲染）
function formatMessage(content) {
  if (!content) return ''
  
  let html = content
  
  // 先处理代码块（避免被其他规则影响），使用特殊标记
  const codeBlocks = []
  html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
    const id = `__CODE_BLOCK_${codeBlocks.length}__`
    codeBlocks.push(code.trim())
    return id
  })
  
  // 转义HTML特殊字符（但保留代码块标记）
  html = html
    .replace(/&(?!__CODE_BLOCK_)/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  
  // 行内代码（`...`），但要避免匹配已标记的代码块
  html = html.replace(/`([^`\n]+)`/g, (match, code) => {
    // 转义代码内容中的HTML
    const escapedCode = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
    return `<code>${escapedCode}</code>`
  })
  
  // 标题（# ## ### 等）
  html = html.replace(/^(#{1,6})\s+(.+)$/gm, (match, hashes, title) => {
    const level = hashes.length
    return `<h${level}>${title}</h${level}>`
  })
  
  // 链接（[text](url)）
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
  
  // 粗体（**...**）
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  
  // 斜体（*...*，避免与粗体冲突）- 先处理粗体，再处理单独的*
  // 因为粗体已经处理过，这里只处理单独的*
  html = html.replace(/\*([^*<]+)\*/g, (match, text) => {
    // 检查是否在粗体或代码标签中
    if (match.includes('<strong>') || match.includes('<code>')) {
      return match
    }
    return `<em>${text}</em>`
  })
  
  // 水平线（--- 或 ***）
  html = html.replace(/^[-*]{3,}$/gm, '<hr>')
  
  // 处理表格（必须在列表处理之前）
  // 表格格式：| 列1 | 列2 | ... |
  //         |------|-----|-----|
  //         | 数据 | 数据 | ... |
  const tableLines = []
  const allLines = html.split('\n')
  let inTable = false
  let tableStartIndex = -1
  
  for (let i = 0; i < allLines.length; i++) {
    const line = allLines[i].trim()
    const isTableRow = line.startsWith('|') && line.endsWith('|')
    const isSeparatorRow = isTableRow && /^[\|\s\-:]+$/.test(line)
    
    if (isTableRow && !isSeparatorRow) {
      if (!inTable) {
        inTable = true
        tableStartIndex = i
      }
      tableLines.push(allLines[i])
    } else if (isSeparatorRow && inTable) {
      // 分隔行，跳过但保持inTable状态
      continue
    } else {
      // 非表格行，如果之前在表格中，结束表格
      if (inTable && tableLines.length > 0) {
        // 处理表格
        const tableHtml = parseTable(tableLines)
        // 替换表格行的HTML
        for (let j = tableStartIndex; j < i; j++) {
          allLines[j] = ''
        }
        allLines[tableStartIndex] = tableHtml
        tableLines.length = 0
        inTable = false
      }
    }
  }
  
  // 处理最后的表格
  if (inTable && tableLines.length > 0) {
    const tableHtml = parseTable(tableLines)
    for (let j = tableStartIndex; j < allLines.length; j++) {
      allLines[j] = ''
    }
    allLines[tableStartIndex] = tableHtml
  }
  
  html = allLines.join('\n')
  
  // 表格解析函数
  function parseTable(lines) {
    if (lines.length === 0) return ''
    
    // 第一行是表头
    const headerLine = lines[0]
    const headers = headerLine.split('|')
      .map(h => h.trim())
      .filter(h => h && !h.match(/^[\s\-:]+$/)) // 过滤掉分隔行
    
    if (headers.length === 0) return ''
    
    let tableHtml = '<table><thead><tr>'
    headers.forEach(header => {
      tableHtml += `<th>${header}</th>`
    })
    tableHtml += '</tr></thead><tbody>'
    
    // 处理数据行（跳过第二行的分隔行）
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim()
      // 跳过分隔行
      if (/^[\|\s\-:]+$/.test(line)) continue
      
      const cells = line.split('|')
        .map(c => c.trim())
        .filter((c, idx, arr) => {
          // 移除首尾空元素（因为|开头和结尾会产生空元素）
          return c
        })
      
      if (cells.length > 0) {
        tableHtml += '<tr>'
        headers.forEach((_, index) => {
          const cell = cells[index] || ''
          tableHtml += `<td>${cell}</td>`
        })
        tableHtml += '</tr>'
      }
    }
    
    tableHtml += '</tbody></table>'
    return tableHtml
  }
  
  // 无序列表（- 或 * 开头，但不在代码中）
  const lines = html.split('\n')
  const processed = []
  let inList = false
  let listItems = []
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]
    const trimmed = line.trim()
    
    // 检查是否是列表项（- 或 * 开头）
    const listMatch = trimmed.match(/^[-*]\s+(.+)$/)
    if (listMatch) {
      if (!inList) {
        inList = true
      }
      listItems.push(`<li>${listMatch[1]}</li>`)
      continue
    }
    
    // 检查是否是有序列表
    const orderedMatch = trimmed.match(/^\d+\.\s+(.+)$/)
    if (orderedMatch) {
      if (!inList) {
        inList = true
      }
      listItems.push(`<li>${orderedMatch[1]}</li>`)
      continue
    }
    
    // 如果不是列表项，先处理之前的列表
    if (inList && listItems.length > 0) {
      processed.push(`<ul>${listItems.join('')}</ul>`)
      listItems = []
      inList = false
    }
    
    // 如果是空行，跳过或结束段落
    if (!trimmed) {
      processed.push('')
      continue
    }
    
    // 如果已经是HTML标签，直接添加
    if (/^<(h[1-6]|p|pre|hr|blockquote)/.test(trimmed)) {
      processed.push(trimmed)
    } else {
      // 普通文本行
      processed.push(trimmed)
    }
  }
  
  // 处理最后的列表
  if (inList && listItems.length > 0) {
    processed.push(`<ul>${listItems.join('')}</ul>`)
  }
  
  html = processed.join('\n')
  
  // 恢复代码块
  codeBlocks.forEach((code, index) => {
    const escapedCode = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
    html = html.replace(`__CODE_BLOCK_${index}__`, `<pre><code>${escapedCode}</code></pre>`)
  })
  
  // 处理段落：保留换行格式
  const finalLines = html.split('\n')
  const finalProcessed = []
  let currentPara = []

  for (let i = 0; i < finalLines.length; i++) {
    const line = finalLines[i]
    
    if (!line.trim()) {
      // 空行，结束当前段落并保留空行
      if (currentPara.length > 0) {
        const paraText = currentPara.join('<br>') // 用 <br> 连接，保留换行
        if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(paraText)) {
          finalProcessed.push(paraText)
        } else {
          finalProcessed.push(`<p>${paraText}</p>`)
        }
        currentPara = []
      }
      // 保留空行，添加一个空段落
      if (i < finalLines.length - 1) { // 避免最后一个空行
        finalProcessed.push('<p><br></p>')
      }
      continue
    }
    
    // 如果行以块级元素开头，单独处理
    if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(line)) {
      if (currentPara.length > 0) {
        const paraText = currentPara.join('<br>') // 用 <br> 连接，保留换行
        if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(paraText)) {
          finalProcessed.push(paraText)
        } else {
          finalProcessed.push(`<p>${paraText}</p>`)
        }
        currentPara = []
      }
      finalProcessed.push(line)
    } else {
      currentPara.push(line)
    }
  }

  // 处理最后的段落
  if (currentPara.length > 0) {
    const paraText = currentPara.join('<br>') // 用 <br> 连接，保留换行
    if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(paraText)) {
      finalProcessed.push(paraText)
    } else {
      finalProcessed.push(`<p>${paraText}</p>`)
    }
  }

  html = finalProcessed.join('')

  return html
}

// 调整文本框高度
function adjustTextareaHeight() {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = `${Math.min(textareaRef.value.scrollHeight, 200)}px`
  }
}


// 滚动节流相关
let scrollTimer = null
let lastScrollTime = 0
const SCROLL_THROTTLE = 100 // 100ms节流

// 检查是否在底部附近（允许10px误差）
function isNearBottom() {
  if (!contentRef.value) return true
  const { scrollTop, scrollHeight, clientHeight } = contentRef.value
  return scrollHeight - scrollTop - clientHeight < 10
}

// 滚动到底部（仅在用户已经在底部附近时）
function scrollToBottom(force = false) {
  if (!contentRef.value) return
  // 如果用户手动滚动到顶部或中间，且不是强制滚动，则不自动滚动
  if (!force && !isNearBottom()) {
    return
  }
  
  // 强制滚动时直接执行，不需要节流
  if (force) {
    contentRef.value.scrollTop = contentRef.value.scrollHeight
    return
  }
  
  // 非强制滚动时使用节流，避免频繁操作DOM
  const now = Date.now()
  if (now - lastScrollTime < SCROLL_THROTTLE) {
    // 如果距离上次滚动时间太近，清除之前的定时器，设置新的定时器
    if (scrollTimer) {
      clearTimeout(scrollTimer)
    }
    scrollTimer = setTimeout(() => {
      if (contentRef.value && isNearBottom()) {
        contentRef.value.scrollTop = contentRef.value.scrollHeight
      }
      lastScrollTime = Date.now()
      scrollTimer = null
    }, SCROLL_THROTTLE - (now - lastScrollTime))
    return
  }
  
  // 可以直接滚动
  contentRef.value.scrollTop = contentRef.value.scrollHeight
  lastScrollTime = now
}

// 拖动触发器
function startDragTrigger(e) {
  hasDragged.value = false
  isDraggingTrigger.value = true
  dragStart.value = {
    x: e.clientX - triggerPosition.value.x,
    y: e.clientY - triggerPosition.value.y
  }
  
  document.addEventListener('mousemove', dragTrigger)
  document.addEventListener('mouseup', stopDragTrigger)
  e.preventDefault()
  e.stopPropagation()
}

function dragTrigger(e) {
  if (!isDraggingTrigger.value) return
  
  const newX = e.clientX - dragStart.value.x
  const newY = e.clientY - dragStart.value.y
  
  const dx = Math.abs(newX - triggerPosition.value.x)
  const dy = Math.abs(newY - triggerPosition.value.y)
  
  // 如果移动距离超过5px，认为是拖动
  if (dx > 5 || dy > 5) {
    hasDragged.value = true
  }
  
  // 限制在窗口内
  triggerPosition.value.x = Math.max(0, Math.min(window.innerWidth - 56, newX))
  triggerPosition.value.y = Math.max(0, Math.min(window.innerHeight - 56, newY))
}

function stopDragTrigger(e) {
  isDraggingTrigger.value = false
  document.removeEventListener('mousemove', dragTrigger)
  document.removeEventListener('mouseup', stopDragTrigger)
  
  // 如果发生了拖动，稍后重置标志（给点击事件时间检查）
  if (hasDragged.value && e) {
    e.preventDefault()
    e.stopPropagation()
    // 延迟重置，让点击事件有机会检查
    setTimeout(() => {
      hasDragged.value = false
    }, 100)
  } else {
    hasDragged.value = false
  }
}

// 拖动对话框
function startDragDialog(e) {
  // 如果点击的是关闭按钮或其他按钮，不拖动
  if (e.target.closest('button') || e.target.closest('input') || e.target.closest('textarea')) {
    return
  }
  
  isDraggingDialog.value = true
  dragStart.value = {
    x: e.clientX - dialogPosition.value.x,
    y: e.clientY - dialogPosition.value.y
  }
  
  document.addEventListener('mousemove', dragDialog)
  document.addEventListener('mouseup', stopDragDialog)
  e.preventDefault()
}

function dragDialog(e) {
  if (!isDraggingDialog.value) return
  
  const dialogWidth = 480
  const dialogHeight = 600
  
  const newX = e.clientX - dragStart.value.x
  const newY = e.clientY - dragStart.value.y
  
  // 限制在窗口内
  dialogPosition.value.x = Math.max(0, Math.min(window.innerWidth - dialogWidth, newX))
  dialogPosition.value.y = Math.max(0, Math.min(window.innerHeight - dialogHeight, newY))
}

function stopDragDialog() {
  isDraggingDialog.value = false
  document.removeEventListener('mousemove', dragDialog)
  document.removeEventListener('mouseup', stopDragDialog)
}

// 调整对话框大小
function startResizeDialog(e) {
  isResizingDialog.value = true
  resizeStart.value = {
    x: e.clientX,
    y: e.clientY,
    width: dialogSize.value.width,
    height: dialogSize.value.height
  }
  
  document.addEventListener('mousemove', resizeDialog)
  document.addEventListener('mouseup', stopResizeDialog)
  e.preventDefault()
  e.stopPropagation()
}

function resizeDialog(e) {
  if (!isResizingDialog.value) return
  
  const dx = e.clientX - resizeStart.value.x
  const dy = e.clientY - resizeStart.value.y
  
  let newWidth = resizeStart.value.width + dx
  let newHeight = resizeStart.value.height + dy
  
  // 限制最小和最大尺寸
  const minWidth = 300
  const minHeight = 400
  const maxWidth = window.innerWidth - dialogPosition.value.x - 20
  const maxHeight = window.innerHeight - dialogPosition.value.y - 20
  
  newWidth = Math.max(minWidth, Math.min(newWidth, maxWidth))
  newHeight = Math.max(minHeight, Math.min(newHeight, maxHeight))
  
  dialogSize.value.width = newWidth
  dialogSize.value.height = newHeight
  
  // 确保对话框不会超出窗口
  if (dialogPosition.value.x + newWidth > window.innerWidth) {
    dialogPosition.value.x = window.innerWidth - newWidth - 10
  }
  if (dialogPosition.value.y + newHeight > window.innerHeight) {
    dialogPosition.value.y = window.innerHeight - newHeight - 10
  }
}

function stopResizeDialog() {
  isResizingDialog.value = false
  document.removeEventListener('mousemove', resizeDialog)
  document.removeEventListener('mouseup', stopResizeDialog)
}

// 窗口大小改变时调整位置和大小
function handleResize() {
  // 确保触发器在窗口内
  if (triggerPosition.value.x > window.innerWidth - 56) {
    triggerPosition.value.x = window.innerWidth - 80
  }
  if (triggerPosition.value.y > window.innerHeight - 56) {
    triggerPosition.value.y = window.innerHeight - 80
  }
  
  // 确保对话框在窗口内，并调整大小
  const maxWidth = window.innerWidth - dialogPosition.value.x - 20
  const maxHeight = window.innerHeight - dialogPosition.value.y - 20
  
  if (dialogSize.value.width > maxWidth) {
    dialogSize.value.width = Math.max(300, maxWidth)
  }
  if (dialogSize.value.height > maxHeight) {
    dialogSize.value.height = Math.max(400, maxHeight)
  }
  
  if (dialogPosition.value.x + dialogSize.value.width > window.innerWidth) {
    dialogPosition.value.x = Math.max(0, window.innerWidth - dialogSize.value.width - 10)
  }
  if (dialogPosition.value.y + dialogSize.value.height > window.innerHeight) {
    dialogPosition.value.y = Math.max(0, window.innerHeight - dialogSize.value.height - 10)
  }
}

// 监听对话框打开状态，添加全局快捷键
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  
  window.addEventListener('resize', handleResize)
  
  // 位置已在初始化时从 localStorage 读取，这里只需要监听窗口大小变化
  // 当窗口大小改变时，确保位置仍然在窗口内
  handleResize()
})

// 保存位置和大小到 localStorage 的函数
function savePositions() {
  try {
    localStorage.setItem('aiAssistant_triggerPosition', JSON.stringify(triggerPosition.value))
    localStorage.setItem('aiAssistant_dialogPosition', JSON.stringify(dialogPosition.value))
    localStorage.setItem('aiAssistant_dialogSize', JSON.stringify(dialogSize.value))
  } catch (e) {
    console.warn('Failed to save positions to localStorage:', e)
  }
}

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  
  // 清理滚动定时器
  if (scrollTimer) {
    clearTimeout(scrollTimer)
    scrollTimer = null
  }
  
  window.removeEventListener('resize', handleResize)
  
  // 保存位置到localStorage
  savePositions()
  
  // 清理拖动事件监听器
  stopDragTrigger()
  stopDragDialog()
  stopResizeDialog()
})

// 监听位置和大小变化，自动保存到localStorage（使用防抖优化性能）
let positionSaveTimer = null
watch([triggerPosition, dialogPosition, dialogSize], () => {
  // 清除之前的定时器
  if (positionSaveTimer) {
    clearTimeout(positionSaveTimer)
  }
  
  // 300ms 后保存，避免频繁写入
  positionSaveTimer = setTimeout(() => {
    savePositions()
  }, 300)
}, { deep: true })

// 监听消息变化，自动保存聊天历史（使用防抖优化性能）
watch(messages, () => {
  // 如果正在加载或消息为空，不保存
  if (isLoading.value || messages.value.length === 0) return
  
  // 清除之前的定时器
  if (saveTimer) {
    clearTimeout(saveTimer)
  }
  
  // 3秒后保存，避免频繁保存
  saveTimer = setTimeout(() => {
    saveCurrentChatHistory()
  }, 3000)
}, { deep: true })

// 页面卸载前保存位置和聊天历史（确保不会丢失）
window.addEventListener('beforeunload', () => {
  savePositions()
  saveCurrentChatHistory()
})

// 页面可见性变化时保存位置和聊天历史
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') {
    savePositions()
    saveCurrentChatHistory()
  }
})
</script>

<style scoped>
.ai-assistant-container {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 1000;
}

/* 浮动助手精灵 */
.assistant-trigger {
  position: fixed;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.08);
  cursor: move;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1001;
  touch-action: none;
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

.assistant-trigger:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15), 0 2px 6px rgba(0, 0, 0, 0.1);
  background: #f5f5f7;
}

.assistant-trigger:active {
  cursor: grabbing;
  transform: scale(0.98);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.assistant-icon {
  font-size: 16px;
  font-weight: 600;
  color: #007AFF;
  letter-spacing: 0.05em;
  animation: pulse 2s infinite;
}

.assistant-icon.shaking {
  animation: shake 0.5s infinite;
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-2px) rotate(-1deg);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(2px) rotate(1deg);
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* 对话框 */
.assistant-dialog {
  position: fixed;
  min-width: 300px;
  max-width: calc(100vw - 20px);
  min-height: 400px;
  max-height: calc(100vh - 20px);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1001;
  resize: none;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: #1d1d1f;
  cursor: move;
  user-select: none;
}

.dialog-header:active {
  cursor: grabbing;
  background: rgba(250, 250, 250, 0.9);
}

/* 调整大小手柄 */
.resize-handle {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: nwse-resize;
  z-index: 1002;
  background: linear-gradient(135deg, transparent 40%, rgba(0, 0, 0, 0.15) 40%, rgba(0, 0, 0, 0.15) 45%, transparent 45%, transparent 55%, rgba(0, 0, 0, 0.15) 55%, rgba(0, 0, 0, 0.15) 60%, transparent 60%);
  border-bottom-right-radius: 20px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.resize-handle:hover {
  background: linear-gradient(135deg, transparent 40%, rgba(0, 122, 255, 0.4) 40%, rgba(0, 122, 255, 0.4) 45%, transparent 45%, transparent 55%, rgba(0, 122, 255, 0.4) 55%, rgba(0, 122, 255, 0.4) 60%, transparent 60%);
}

.resize-handle:active {
  background: linear-gradient(135deg, transparent 40%, rgba(0, 122, 255, 0.6) 40%, rgba(0, 122, 255, 0.6) 45%, transparent 45%, transparent 55%, rgba(0, 122, 255, 0.6) 55%, rgba(0, 122, 255, 0.6) 60%, transparent 60%);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.history-button {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  color: #1d1d1f;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.history-button:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.history-button:active {
  transform: scale(0.95);
}

.post-center-button {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(0, 122, 255, 0.1);
  border-radius: 8px;
  color: #007AFF;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.post-center-button:hover {
  background: rgba(0, 122, 255, 0.2);
  transform: scale(1.05);
}

.post-center-button:active {
  transform: scale(0.95);
}

.dialog-icon {
  font-size: 24px;
}

.dialog-title {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: -0.01em;
}

.close-button {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  color: #1d1d1f;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.close-button:active {
  transform: scale(0.95);
}

/* 消息容器 */
.dialog-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: rgba(248, 248, 250, 0.5);
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  gap: 12px;
  animation: messageSlide 0.3s ease;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.message-avatar.shaking {
  animation: shake 0.5s infinite;
  background: rgba(0, 122, 255, 0.1);
  border-color: rgba(0, 122, 255, 0.3);
}

.message-avatar span {
  display: block;
  letter-spacing: 0.05em;
}

.message-user .message-avatar {
  background: #007AFF;
  border: none;
}

.message-content {
  flex: 1;
  max-width: calc(100% - 48px);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
}

.message-user .message-content {
  align-items: flex-end;
  text-align: right;
}

.message-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.message-user .message-images {
  justify-content: flex-end;
}

.message-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 12px;
  cursor: pointer;
  object-fit: cover;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.message-text-wrapper {
  position: relative;
  display: inline-block;
  max-width: 80%;
}

.message-text {
  display: inline-block;
  max-width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.6;
  word-wrap: break-word;
  word-break: break-word;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.04);
  text-align: left;
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
  cursor: text;
}

.message-user .message-text {
  background: #007AFF;
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
  text-align: left;
}

.message-text :deep(code) {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.message-user .message-text :deep(code) {
  background: rgba(255, 255, 255, 0.2);
}

.message-text :deep(pre) {
  background: rgba(0, 0, 0, 0.05);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.message-text :deep(pre code) {
  background: transparent;
  padding: 0;
}

.message-user .message-text :deep(pre) {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.2);
}

.message-text :deep(h1),
.message-text :deep(h2),
.message-text :deep(h3),
.message-text :deep(h4),
.message-text :deep(h5),
.message-text :deep(h6) {
  margin: 12px 0 8px 0;
  font-weight: 600;
  line-height: 1.4;
}

.message-text :deep(h1) { font-size: 1.5em; }
.message-text :deep(h2) { font-size: 1.3em; }
.message-text :deep(h3) { font-size: 1.15em; }

.message-text :deep(ul),
.message-text :deep(ol) {
  margin: 8px 0;
  padding-left: 24px;
}

.message-text :deep(li) {
  margin: 4px 0;
}

.message-text :deep(p) {
  margin: 8px 0;
}

.message-text :deep(blockquote) {
  border-left: 3px solid rgba(0, 122, 255, 0.3);
  padding-left: 12px;
  margin: 8px 0;
  color: rgba(0, 0, 0, 0.7);
}

.message-user .message-text :deep(blockquote) {
  border-left-color: rgba(255, 255, 255, 0.5);
  color: rgba(255, 255, 255, 0.9);
}

.message-text :deep(a) {
  color: #007AFF;
  text-decoration: none;
  border-bottom: 1px solid rgba(0, 122, 255, 0.3);
}

.message-text :deep(a:hover) {
  border-bottom-color: #007AFF;
}

.message-user .message-text :deep(a) {
  color: rgba(255, 255, 255, 0.9);
  border-bottom-color: rgba(255, 255, 255, 0.5);
}

.message-text :deep(hr) {
  border: none;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  margin: 16px 0;
}

.message-user .message-text :deep(hr) {
  border-top-color: rgba(255, 255, 255, 0.3);
}

.message-text :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 0.9em;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.message-text :deep(table thead) {
  background: rgba(0, 122, 255, 0.08);
}

.message-text :deep(table th) {
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  color: #1d1d1f;
  border-bottom: 2px solid rgba(0, 122, 255, 0.2);
  font-size: 0.95em;
}

.message-text :deep(table td) {
  padding: 10px 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  color: #1d1d1f;
  line-height: 1.5;
}

.message-text :deep(table tr:last-child td) {
  border-bottom: none;
}

.message-text :deep(table tbody tr:hover) {
  background: rgba(0, 122, 255, 0.03);
}

.message-text :deep(table tbody tr:nth-child(even)) {
  background: rgba(0, 0, 0, 0.02);
}

.message-text :deep(table tbody tr:nth-child(even):hover) {
  background: rgba(0, 122, 255, 0.05);
}

.message-user .message-text :deep(table) {
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-user .message-text :deep(table thead) {
  background: rgba(255, 255, 255, 0.2);
}

.message-user .message-text :deep(table th) {
  color: rgba(255, 255, 255, 0.95);
  border-bottom-color: rgba(255, 255, 255, 0.3);
}

.message-user .message-text :deep(table td) {
  color: rgba(255, 255, 255, 0.9);
  border-bottom-color: rgba(255, 255, 255, 0.15);
}

.message-user .message-text :deep(table tbody tr:hover) {
  background: rgba(255, 255, 255, 0.1);
}

.message-user .message-text :deep(table tbody tr:nth-child(even)) {
  background: rgba(255, 255, 255, 0.08);
}

.message-user .message-text :deep(table tbody tr:nth-child(even):hover) {
  background: rgba(255, 255, 255, 0.12);
}

.like-button {
  position: absolute;
  bottom: -8px;
  right: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  z-index: 10;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.like-button:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.like-button:active {
  transform: translateY(0);
}

.like-button.liked {
  background: rgba(0, 122, 255, 0.1);
  border-color: rgba(0, 122, 255, 0.3);
  color: #007AFF;
}

.like-button.liked:hover {
  background: rgba(0, 122, 255, 0.15);
}

.like-text {
  font-size: 12px;
  font-weight: 500;
  color: #007AFF;
}

.message-user .message-text-wrapper .like-button {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.message-user .message-text-wrapper .like-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.message-user .message-text-wrapper .like-button.liked {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
}


.message-reasoning {
  margin-top: 8px;
  font-size: 12px;
  color: #8e8e93;
}

.message-reasoning details {
  background: rgba(0, 0, 0, 0.03);
  padding: 8px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.message-reasoning summary {
  cursor: pointer;
  font-weight: 500;
}

.message-reasoning pre {
  margin: 8px 0 0 0;
  white-space: pre-wrap;
  font-size: 11px;
}

/* 输入指示器 */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 18px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #8e8e93;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* 输入区域 */
.dialog-input {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 16px;
}

.input-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.image-preview {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ff3b30;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(255, 59, 48, 0.3);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.remove-image:hover {
  transform: scale(1.1);
  box-shadow: 0 3px 8px rgba(255, 59, 48, 0.4);
}

.input-area {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.dice-button {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.04);
  flex-shrink: 0;
}

.dice-button:hover:not(:disabled) {
  background: rgba(0, 122, 255, 0.1);
  border-color: rgba(0, 122, 255, 0.2);
  transform: scale(1.05);
}

.dice-button:active:not(:disabled) {
  transform: scale(0.95);
}

.dice-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.file-input-label {
  flex-shrink: 0;
}

.file-button {
  display: inline-block;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.file-button:hover {
  background: rgba(0, 0, 0, 0.08);
  transform: scale(1.05);
}

.file-button:active {
  transform: scale(0.95);
}

.input-textarea {
  flex: 1;
  min-height: 40px;
  max-height: 200px;
  padding: 10px 14px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 18px;
  font-size: 14px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  resize: none;
  outline: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.input-textarea:focus {
  border-color: #007AFF;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
  background: rgba(255, 255, 255, 1);
}

.input-textarea:disabled {
  background: rgba(0, 0, 0, 0.03);
  cursor: not-allowed;
  opacity: 0.6;
}

.send-button {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background: #007AFF;
  color: white;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
  background: #0051D5;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.send-button:active:not(:disabled) {
  transform: scale(0.95);
}

.send-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #8e8e93;
  box-shadow: none;
}

/* 图片预览模态框 */
.image-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  cursor: pointer;
}

.image-preview-modal img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
}

/* 动画 */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.dialog-fade-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.dialog-fade-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* 历史记录侧边栏 */
.history-sidebar {
  position: absolute;
  top: 0;
  left: 0;
  width: 280px;
  height: 100%;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  z-index: 1003;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.08);
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.history-header h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.close-history-button {
  width: 28px;
  height: 28px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  color: #1d1d1f;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-history-button:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.history-search {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.history-search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-size: 14px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  outline: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.9);
}

.history-search-input:focus {
  border-color: #007AFF;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.history-item {
  position: relative;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid transparent;
}

.history-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.history-item.active {
  background: rgba(0, 122, 255, 0.1);
  border-color: rgba(0, 122, 255, 0.2);
}

.history-item-title {
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-item-time {
  font-size: 12px;
  color: #8e8e93;
}

.history-item-delete {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.history-item:hover .history-item-delete {
  opacity: 1;
}

.history-item-delete:hover {
  background: rgba(255, 59, 48, 0.1);
  transform: scale(1.1);
}

.history-empty,
.history-loading {
  padding: 40px 20px;
  text-align: center;
  color: #8e8e93;
  font-size: 14px;
}

.history-footer {
  padding: 12px 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.new-chat-button {
  width: 100%;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  background: #007AFF;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.new-chat-button:hover {
  background: #0051D5;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.new-chat-button:active {
  transform: translateY(0);
}

/* 侧边栏动画 */
.sidebar-slide-enter-active,
.sidebar-slide-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-slide-enter-from {
  transform: translateX(-100%);
}

.sidebar-slide-leave-to {
  transform: translateX(-100%);
}

/* 响应式 */
@media (max-width: 640px) {
  .assistant-dialog {
    min-width: calc(100vw - 24px);
    min-height: calc(100vh - 24px);
    border-radius: 12px;
  }
  
  .assistant-trigger {
    width: 48px;
    height: 48px;
  }
  
  .assistant-icon {
    font-size: 14px;
  }
  
  .history-sidebar {
    width: 240px;
  }
}
</style>

