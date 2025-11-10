<template>
  <div class="post-center">
    <div class="post-center-header">
      <button class="back-button" @click="$emit('back')" title="返回对话">
        ← 返回对话
      </button>
      <h2 class="post-center-title">高赞内容</h2>
    </div>
    
    <div class="post-center-content" ref="contentRef">
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="posts.length === 0" class="empty-container">
        <div class="empty-icon">📝</div>
        <p class="empty-text">还没有高赞内容</p>
        <p class="empty-hint">去对话中为AI回复点赞吧～</p>
      </div>
      
      <div v-else class="posts-grid">
        <div
          v-for="post in posts"
          :key="post.id"
          class="post-card"
          @click="openPostDetail(post)"
        >
          <div class="post-card-header">
            <div class="post-date">{{ formatDate(post.created_at) }}</div>
            <button class="post-delete" @click.stop="deletePost(post.id)" title="删除">
              ✕
            </button>
          </div>
          <div class="post-question">
            <div class="post-label">💭 问题</div>
            <div class="post-text" v-html="truncateMarkdown(post.question, 100)"></div>
          </div>
          <div class="post-answer">
            <div class="post-label">🤖 回答</div>
            <div class="post-text post-answer-content" v-html="truncateMarkdown(post.answer, 200)"></div>
          </div>
          <div class="post-footer">
            <span class="post-like-icon">👍</span>
            <span class="post-like-text">已点赞</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 帖子详情弹窗 -->
    <div v-if="selectedPost" class="post-detail-overlay" @click="closePostDetail">
      <div class="post-detail-modal" @click.stop>
        <div class="post-detail-header">
          <h3>高赞内容详情</h3>
          <button class="close-button" @click="closePostDetail">✕</button>
        </div>
        <div class="post-detail-content">
          <div class="post-detail-section">
            <div class="post-detail-label">💭 问题</div>
            <div class="post-detail-text" v-html="formatMarkdown(selectedPost.question)"></div>
          </div>
          <div class="post-detail-section">
            <div class="post-detail-label">🤖 回答</div>
            <div class="post-detail-text post-detail-answer" v-html="formatMarkdown(selectedPost.answer)"></div>
          </div>
          <div class="post-detail-footer">
            <span class="post-detail-date">创建时间：{{ formatDateTime(selectedPost.created_at) }}</span>
            <button class="post-detail-delete" @click="deletePostFromDetail">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { api } from '../api'

defineEmits(['back'])

const loading = ref(false)
const posts = ref([])
const contentRef = ref(null)
const selectedPost = ref(null)

// 加载点赞记录
async function loadPosts() {
  loading.value = true
  try {
    // 等待API配置就绪
    await api.ready()
    const data = await api.getLikeRecords({ skip: 0, limit: 1000 })
    posts.value = data
    await nextTick()
    scrollToTop()
  } catch (error) {
    console.error('Failed to load posts:', error)
    // 不显示alert，避免打断用户体验
    // 只在控制台输出错误，UI会显示空状态
  } finally {
    loading.value = false
  }
}

// 滚动到顶部
function scrollToTop() {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0
  }
}

// 打开帖子详情
function openPostDetail(post) {
  selectedPost.value = post
}

// 关闭帖子详情
function closePostDetail() {
  selectedPost.value = null
}

// 删除帖子
async function deletePost(postId) {
  if (!confirm('确定删除这条高赞内容吗？')) return
  
  try {
    await api.deleteLikeRecord(postId)
    posts.value = posts.value.filter(p => p.id !== postId)
    if (selectedPost.value && selectedPost.value.id === postId) {
      closePostDetail()
    }
  } catch (error) {
    console.error('Failed to delete post:', error)
    alert('删除失败：' + (error.message || '未知错误'))
  }
}

// 从详情中删除
function deletePostFromDetail() {
  if (selectedPost.value) {
    deletePost(selectedPost.value.id)
  }
}

// 格式化日期
function formatDate(dateStr) {
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    
    if (days === 0) {
      return '今天'
    } else if (days === 1) {
      return '昨天'
    } else if (days < 7) {
      return `${days}天前`
    } else {
      return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
    }
  } catch (e) {
    return dateStr
  }
}

// 格式化日期时间
function formatDateTime(dateStr) {
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateStr
  }
}

// 截断文本
function truncateText(text, maxLength) {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// 截断Markdown（先格式化再截断，智能处理）
function truncateMarkdown(content, maxLength) {
  if (!content) return ''
  
  // 先格式化Markdown
  const formattedHtml = formatMessage(content)
  
  // 创建一个临时DOM元素来提取纯文本长度
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = formattedHtml
  const textContent = tempDiv.textContent || tempDiv.innerText || ''
  
  // 如果内容长度在限制内，直接返回格式化后的HTML
  if (textContent.length <= maxLength) {
    return formattedHtml
  }
  
  // 智能截断：尝试在句子或单词边界截断
  let truncatedText = textContent.substring(0, maxLength)
  
  // 尝试在最后一个句号、问号、感叹号后截断
  const lastSentenceEnd = Math.max(
    truncatedText.lastIndexOf('。'),
    truncatedText.lastIndexOf('！'),
    truncatedText.lastIndexOf('？'),
    truncatedText.lastIndexOf('.'),
    truncatedText.lastIndexOf('!'),
    truncatedText.lastIndexOf('?')
  )
  
  if (lastSentenceEnd > maxLength * 0.7) {
    truncatedText = truncatedText.substring(0, lastSentenceEnd + 1)
  } else {
    // 否则在最后一个空格或标点后截断
    const lastSpace = truncatedText.lastIndexOf(' ')
    const lastPunct = Math.max(
      truncatedText.lastIndexOf('，'),
      truncatedText.lastIndexOf(','),
      truncatedText.lastIndexOf('；'),
      truncatedText.lastIndexOf(';')
    )
    const cutPoint = Math.max(lastSpace, lastPunct)
    if (cutPoint > maxLength * 0.7) {
      truncatedText = truncatedText.substring(0, cutPoint + 1)
    }
    truncatedText += '...'
  }
  
  // 返回截断后的文本（保持基本的Markdown格式，但简化显示）
  return `<p>${truncatedText.replace(/\n/g, ' ')}</p>`
}

// 格式化Markdown（完整版本，复用AiAssistant的formatMessage逻辑）
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

  // 斜体（*...*，避免与粗体冲突）
  html = html.replace(/\*([^*<]+)\*/g, (match, text) => {
    if (match.includes('<strong>') || match.includes('<code>')) {
      return match
    }
    return `<em>${text}</em>`
  })

  // 水平线（--- 或 ***）
  html = html.replace(/^[-*]{3,}$/gm, '<hr>')

  // 处理表格（必须在列表处理之前）
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
      continue
    } else {
      if (inTable && tableLines.length > 0) {
        const tableHtml = parseTable(tableLines)
        for (let j = tableStartIndex; j < i; j++) {
          allLines[j] = ''
        }
        allLines[tableStartIndex] = tableHtml
        tableLines.length = 0
        inTable = false
      }
    }
  }
  
  if (inTable && tableLines.length > 0) {
    const tableHtml = parseTable(tableLines)
    for (let j = tableStartIndex; j < allLines.length; j++) {
      allLines[j] = ''
    }
    allLines[tableStartIndex] = tableHtml
  }
  
  html = allLines.join('\n')
  
  function parseTable(lines) {
    if (lines.length === 0) return ''
    
    const headerLine = lines[0]
    const headers = headerLine.split('|')
      .map(h => h.trim())
      .filter(h => h && !h.match(/^[\s\-:]+$/))
    
    if (headers.length === 0) return ''
    
    let tableHtml = '<table><thead><tr>'
    headers.forEach(header => {
      tableHtml += `<th>${header}</th>`
    })
    tableHtml += '</tr></thead><tbody>'
    
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim()
      if (/^[\|\s\-:]+$/.test(line)) continue
      
      const cells = line.split('|')
        .map(c => c.trim())
        .filter(c => c)
      
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

  // 无序列表和有序列表处理
  const lines = html.split('\n')
  const processed = []
  let inList = false
  let listItems = []

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]
    const trimmed = line.trim()
    
    const listMatch = trimmed.match(/^[-*]\s+(.+)$/)
    if (listMatch) {
      if (!inList) inList = true
      listItems.push(`<li>${listMatch[1]}</li>`)
      continue
    }

    const orderedMatch = trimmed.match(/^\d+\.\s+(.+)$/)
    if (orderedMatch) {
      if (!inList) inList = true
      listItems.push(`<li>${orderedMatch[1]}</li>`)
      continue
    }

    if (inList && listItems.length > 0) {
      processed.push(`<ul>${listItems.join('')}</ul>`)
      listItems = []
      inList = false
    }

    if (!trimmed) {
      processed.push('')
      continue
    }

    if (/^<(h[1-6]|p|pre|hr|blockquote|table)/.test(trimmed)) {
      processed.push(trimmed)
    } else {
      processed.push(trimmed)
    }
  }

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

  // 处理段落
  const finalLines = html.split('\n')
  const finalProcessed = []
  let currentPara = []

  for (let i = 0; i < finalLines.length; i++) {
    const line = finalLines[i]

    if (!line.trim()) {
      if (currentPara.length > 0) {
        const paraText = currentPara.join(' ')
        if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(paraText)) {
          finalProcessed.push(paraText)
        } else {
          finalProcessed.push(`<p>${paraText}</p>`)
        }
        currentPara = []
      }
      continue
    }

    if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(line)) {
      if (currentPara.length > 0) {
        const paraText = currentPara.join(' ')
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

  if (currentPara.length > 0) {
    const paraText = currentPara.join(' ')
    if (/^<(h[1-6]|pre|ul|ol|hr|blockquote|table)/.test(paraText)) {
      finalProcessed.push(paraText)
    } else {
      finalProcessed.push(`<p>${paraText}</p>`)
    }
  }

  html = finalProcessed.join('')

  return html
}

function formatMarkdown(content) {
  return formatMessage(content)
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.post-center {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(248, 248, 250, 0.5);
}

.post-center-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  flex-shrink: 0;
}

.back-button {
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  color: #1d1d1f;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.back-button:hover {
  background: rgba(0, 0, 0, 0.08);
  transform: translateX(-2px);
}

.post-center-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
}

.post-center-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.loading-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 12px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(0, 122, 255, 0.2);
  border-top-color: #007AFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-text {
  font-size: 16px;
  color: #8e8e93;
  margin: 0;
}

.empty-hint {
  font-size: 14px;
  color: #8e8e93;
  margin: 0;
  opacity: 0.7;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  align-items: start;
}

.post-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 180px;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: rgba(0, 122, 255, 0.2);
}

.post-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-date {
  font-size: 12px;
  color: #8e8e93;
}

.post-delete {
  width: 24px;
  height: 24px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  color: #8e8e93;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.post-delete:hover {
  background: rgba(255, 59, 48, 0.1);
  color: #FF3B30;
  transform: scale(1.1);
}

.post-question,
.post-answer {
  flex: 1;
}

.post-label {
  font-size: 11px;
  font-weight: 600;
  color: #8e8e93;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.post-text {
  font-size: 14px;
  line-height: 1.6;
  color: #1d1d1f;
  word-break: break-word;
}

.post-text :deep(code) {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.9em;
}

.post-text :deep(pre) {
  background: rgba(0, 0, 0, 0.05);
  padding: 8px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 4px 0;
}

.post-text :deep(pre code) {
  background: transparent;
  padding: 0;
}

.post-text :deep(p) {
  margin: 0.5em 0;
}

.post-text :deep(strong) {
  font-weight: 600;
  color: #1d1d1f;
}

.post-text :deep(em) {
  font-style: italic;
}

.post-text :deep(a) {
  color: #007AFF;
  text-decoration: none;
}

.post-text :deep(a:hover) {
  text-decoration: underline;
}

.post-text :deep(ul), .post-text :deep(ol) {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.post-text :deep(li) {
  margin: 0.25em 0;
}

.post-text :deep(h1), .post-text :deep(h2), .post-text :deep(h3),
.post-text :deep(h4), .post-text :deep(h5), .post-text :deep(h6) {
  margin: 0.5em 0;
  font-weight: 600;
  line-height: 1.3;
}

.post-text :deep(h1) { font-size: 1.3em; }
.post-text :deep(h2) { font-size: 1.15em; }
.post-text :deep(h3) { font-size: 1.05em; }

.post-text :deep(hr) {
  border: none;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  margin: 0.75em 0;
}

.post-text :deep(blockquote) {
  border-left: 3px solid rgba(0, 122, 255, 0.3);
  padding-left: 0.75em;
  margin: 0.5em 0;
  color: #666;
  font-style: italic;
}

.post-answer-content {
  max-height: 200px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 6;
  -webkit-box-orient: vertical;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  padding-top: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  font-size: 12px;
  color: #8e8e93;
}

.post-like-icon {
  font-size: 14px;
}

.post-detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.post-detail-modal {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 700px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.post-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.post-detail-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
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
  transition: all 0.2s;
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.post-detail-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.post-detail-section {
  margin-bottom: 24px;
}

.post-detail-label {
  font-size: 13px;
  font-weight: 600;
  color: #007AFF;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.post-detail-text {
  font-size: 15px;
  line-height: 1.8;
  color: #1d1d1f;
  word-break: break-word;
}

.post-detail-text :deep(code) {
  background: rgba(0, 0, 0, 0.08);
  padding: 3px 8px;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.92em;
}

.post-detail-text :deep(pre) {
  background: rgba(0, 0, 0, 0.06);
  padding: 16px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 1em 0;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.post-detail-text :deep(pre code) {
  background: transparent;
  padding: 0;
}

.post-detail-text :deep(strong) {
  font-weight: 600;
  color: #1d1d1f;
}

.post-detail-text :deep(em) {
  font-style: italic;
}

.post-detail-text :deep(a) {
  color: #007AFF;
  text-decoration: none;
}

.post-detail-text :deep(a:hover) {
  text-decoration: underline;
}

.post-detail-text :deep(h1) { font-size: 1.8em; margin: 16px 0 8px 0; }
.post-detail-text :deep(h2) { font-size: 1.5em; margin: 14px 0 6px 0; }
.post-detail-text :deep(h3) { font-size: 1.2em; margin: 12px 0 6px 0; }
.post-detail-text :deep(h4) { font-size: 1.1em; margin: 10px 0 5px 0; }
.post-detail-text :deep(h5) { font-size: 1.05em; margin: 8px 0 4px 0; }
.post-detail-text :deep(h6) { font-size: 1em; margin: 6px 0 3px 0; }

.post-detail-text :deep(ul),
.post-detail-text :deep(ol) {
  margin: 8px 0;
  padding-left: 24px;
}

.post-detail-text :deep(li) {
  margin: 0.4em 0;
  line-height: 1.6;
}

.post-detail-text :deep(p) {
  margin: 0.75em 0;
}

.post-detail-text :deep(hr) {
  border: none;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  margin: 1.5em 0;
}

.post-detail-text :deep(blockquote) {
  border-left: 4px solid rgba(0, 122, 255, 0.3);
  padding-left: 1em;
  margin: 1em 0;
  color: #666;
  font-style: italic;
}

.post-detail-answer {
  margin-top: 8px;
}

.post-text :deep(table),
.post-detail-text :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 0.9em;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.post-text :deep(table thead),
.post-detail-text :deep(table thead) {
  background: rgba(0, 122, 255, 0.08);
}

.post-text :deep(table th),
.post-detail-text :deep(table th) {
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  color: #1d1d1f;
  border-bottom: 2px solid rgba(0, 122, 255, 0.2);
  font-size: 0.95em;
}

.post-text :deep(table td),
.post-detail-text :deep(table td) {
  padding: 10px 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  color: #1d1d1f;
  line-height: 1.5;
}

.post-text :deep(table tr:last-child td),
.post-detail-text :deep(table tr:last-child td) {
  border-bottom: none;
}

.post-text :deep(table tbody tr:hover),
.post-detail-text :deep(table tbody tr:hover) {
  background: rgba(0, 122, 255, 0.03);
}

.post-text :deep(table tbody tr:nth-child(even)),
.post-detail-text :deep(table tbody tr:nth-child(even)) {
  background: rgba(0, 0, 0, 0.02);
}

.post-text :deep(table tbody tr:nth-child(even):hover),
.post-detail-text :deep(table tbody tr:nth-child(even):hover) {
  background: rgba(0, 122, 255, 0.05);
}

.post-detail-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.post-detail-date {
  font-size: 12px;
  color: #8e8e93;
}

.post-detail-delete {
  padding: 8px 16px;
  background: rgba(255, 59, 48, 0.1);
  border: 1px solid rgba(255, 59, 48, 0.2);
  border-radius: 8px;
  color: #FF3B30;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.post-detail-delete:hover {
  background: rgba(255, 59, 48, 0.15);
  transform: translateY(-1px);
}
</style>

