<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { api, type Internship, type Project, type TechStack, type ResumePhoto, type JobDescription, type JdBreakdown } from '../api'

const router = useRouter()
const route = useRoute()

// 状态管理 - 从路由参数或默认值获取
const activeSection = ref<'internships' | 'projects' | 'tech-stacks' | 'photos' | 'job-descriptions'>('internships')

// 监听路由变化
watch(() => route.params.subtab, (newSubtab) => {
  if (newSubtab === 'internships' || newSubtab === 'projects' || newSubtab === 'tech-stacks' || newSubtab === 'photos' || newSubtab === 'job-descriptions') {
    activeSection.value = newSubtab as 'internships' | 'projects' | 'tech-stacks' | 'photos' | 'job-descriptions'
    loadSectionData(newSubtab as 'internships' | 'projects' | 'tech-stacks' | 'photos' | 'job-descriptions')
  }
}, { immediate: true })

// 实习经历
const internships = ref<Internship[]>([])
const internshipForm = ref({
  group_title: '',  // 分组标题
  company: '',
  position: '',
  start_date: '',
  end_date: '',
  description: '',
  skills: ''
})
const editingInternshipId = ref<number | null>(null)

// 项目经历
const projects = ref<Project[]>([])
const projectForm = ref({
  name: '',
  description: '',
  tech_stack: '',
  start_date: '',
  end_date: '',
  url: ''
})
const editingProjectId = ref<number | null>(null)

// 技术栈
const techStacks = ref<TechStack[]>([])
const techStackForm = ref({
  category: '',
  name: '',
  level: '',
  description: ''
})
const editingTechStackId = ref<number | null>(null)

// 简历照片
const photos = ref<ResumePhoto[]>([])
const photoForm = ref({
  title: '',
  files: [] as File[]
})
const editingPhotoId = ref<number | null>(null)
const showingPhotoModal = ref(false)
const selectedPhoto = ref<string>('')

// 岗位要求（JD）
const jobDescriptions = ref<JobDescription[]>([])
const jdForm = ref({
  company: '',
  position: '',
  description: '',
  files: [] as File[]
})
const editingJdId = ref<number | null>(null)

// JD拆解
const jdBreakdowns = ref<JdBreakdown[]>([])
const jdBreakdownForm = ref({
  jd_id: 0,
  company: '',
  position: '',
  breakdown_content: ''
})
const editingBreakdownId = ref<number | null>(null)
const showingBreakdownModal = ref(false)
const currentJdForBreakdown = ref<JobDescription | null>(null)

// AI拆解相关
const showingSystemPromptEditor = ref(false)
const systemPrompt = ref('')
const aiAnalyzing = ref(false)

const loading = ref(false)
const error = ref<string | null>(null)

// 计算属性
const groupedInternships = computed(() => {
  const groups: Record<string, Internship[]> = {}
  internships.value.forEach(internship => {
    // 使用 group_title 或 position 作为分组键，如果都没有则归到"其他"组
    const groupKey = internship.group_title || (internship.position || '其他')
    if (!groups[groupKey]) {
      groups[groupKey] = []
    }
    groups[groupKey].push(internship)
  })
  return groups
})

const groupedTechStacks = computed(() => {
  const groups: Record<string, TechStack[]> = {}
  techStacks.value.forEach(tech => {
    if (!groups[tech.category]) {
      groups[tech.category] = []
    }
    groups[tech.category].push(tech)
  })
  return groups
})

// Markdown 渲染函数（简单版）
function renderMarkdown(text: string): string {
  if (!text) return ''
  
  let html = text
  
  // 处理标题
  html = html.replace(/^(#{1,6})\s+(.+)$/gm, (match, hashes, title) => {
    const level = hashes.length
    return `<h${level}>${title}</h${level}>`
  })
  
  // 处理列表项
  html = html.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>')
  
  // 处理粗体
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  
  // 处理斜体
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
  
  // 处理换行 - 将单行换行转换为 br，空行转换为段落
  const lines = html.split('\n')
  const processed: string[] = []
  let currentPara = ''
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const trimmed = line.trim()
    
    // 如果是空行，结束当前段落
    if (!trimmed) {
      if (currentPara) {
        if (currentPara.includes('<li>')) {
          processed.push(currentPara)
        } else {
          processed.push(`<p>${currentPara}</p>`)
        }
        currentPara = ''
      }
      continue
    }
    
    // 如果是列表项，单独处理
    if (trimmed.startsWith('<li>')) {
      if (currentPara) {
        processed.push(`<p>${currentPara}</p>`)
        currentPara = ''
      }
      processed.push(trimmed)
    } else {
      // 添加到当前段落
      if (currentPara) {
        currentPara += '<br>' + trimmed
      } else {
        currentPara = trimmed
      }
    }
  }
  
  // 处理最后的段落
  if (currentPara) {
    if (currentPara.includes('<li>')) {
      processed.push(currentPara)
    } else {
      processed.push(`<p>${currentPara}</p>`)
    }
  }
  
  html = processed.join('')
  
  return html
}

// 实习经历相关方法
async function loadInternships() {
  try {
    loading.value = true
    internships.value = await api.getInternships()
  } catch (e: any) {
    error.value = e?.message || '加载实习经历失败'
  } finally {
    loading.value = false
  }
}

async function submitInternship() {
  try {
    const text = internshipForm.value.company
    const title = internshipForm.value.position || ''  // 子标题可以为空
    const groupTitle = internshipForm.value.group_title || ''
    
    // 简单拆分第一行的公司、职位、时间
    const firstLine = text.split('\n')[0].trim()
    const parts = firstLine.split(/\s{4,}/).filter(p => p.trim()) // 用多个空格分割
    
    let company = ''
    let position = ''
    let timeRange = ''
    
    if (parts.length >= 1) company = parts[0].trim()
    if (parts.length >= 2) position = parts[1].trim()
    if (parts.length >= 3) timeRange = parts[2].trim()
    
    // 如果分割失败，取前100字符作为公司名
    if (!company && text.length > 0) {
      company = text.slice(0, Math.min(100, text.length)).replace(/\n.*/, '')
    }
    
    // 如果没有职位，使用空字符串
    if (!position) position = ''
    
    // 时间处理
    let startDate = ''
    let endDate = ''
    if (timeRange) {
      const timeParts = timeRange.split(' - ').map(p => p.trim())
      startDate = timeParts[0] || ''
      endDate = timeParts[1] || ''
    }
    
    // 描述为整个文本内容
    const description = text
    
    const data = {
      group_title: groupTitle,  // 分组标题
      company: company.slice(0, 500),
      position: title.slice(0, 500), // 使用用户输入的标题，可以为空
      start_date: startDate || '',
      end_date: endDate || undefined,
      description: description,
      skills: ''
    }
    
    if (editingInternshipId.value) {
      const updated = await api.updateInternship(editingInternshipId.value, data)
      const index = internships.value.findIndex(i => i.id === editingInternshipId.value)
      if (index >= 0) internships.value[index] = updated
    } else {
      const created = await api.createInternship(data)
      internships.value.unshift(created)
    }
    resetInternshipForm()
    alert('提交成功！')
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editInternship(internship: Internship) {
  editingInternshipId.value = internship.id
  // 显示分组标题
  internshipForm.value.group_title = internship.group_title || ''
  // 显示标题
  internshipForm.value.position = internship.position
  // 将描述内容作为主要内容显示在文本框
  internshipForm.value.company = internship.description || `${internship.company}\n${internship.position}\n${internship.start_date} - ${internship.end_date || '至今'}`
}

function resetInternshipForm() {
  editingInternshipId.value = null
  internshipForm.value = {
    group_title: '',
    company: '',
    position: '',
    start_date: '',
    end_date: '',
    description: '',
    skills: ''
  }
}

async function deleteInternship(id: number) {
  if (!confirm('确定删除该实习经历？')) return
  try {
    await api.deleteInternship(id)
    internships.value = internships.value.filter(i => i.id !== id)
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

// 项目经历相关方法
async function loadProjects() {
  try {
    loading.value = true
    projects.value = await api.getProjects()
  } catch (e: any) {
    error.value = e?.message || '加载项目经历失败'
  } finally {
    loading.value = false
  }
}

async function submitProject() {
  try {
    // 用户输入的标题和内容
    const title = projectForm.value.name || ''
    const content = projectForm.value.description || ''
    
    // 直接使用用户输入，不做任何提取逻辑
    const data = {
      name: title,
      description: content,
      tech_stack: '',
      start_date: '',
      end_date: '',
      url: ''
    }
    
    if (editingProjectId.value) {
      const updated = await api.updateProject(editingProjectId.value, data)
      const index = projects.value.findIndex(p => p.id === editingProjectId.value)
      if (index >= 0) projects.value[index] = updated
    } else {
      const created = await api.createProject(data)
      projects.value.unshift(created)
    }
    resetProjectForm()
    alert('提交成功！')
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editProject(project: Project) {
  editingProjectId.value = project.id
  projectForm.value = { ...project }
}

function resetProjectForm() {
  editingProjectId.value = null
  projectForm.value = {
    name: '',
    description: '',
    tech_stack: '',
    start_date: '',
    end_date: '',
    url: ''
  }
}

async function deleteProject(id: number) {
  if (!confirm('确定删除该项目经历？')) return
  try {
    await api.deleteProject(id)
    projects.value = projects.value.filter(p => p.id !== id)
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

// 技术栈相关方法
async function loadTechStacks() {
  try {
    loading.value = true
    techStacks.value = await api.getTechStacks()
  } catch (e: any) {
    error.value = e?.message || '加载技术栈失败'
  } finally {
    loading.value = false
  }
}

async function submitTechStack() {
  try {
    const title = techStackForm.value.category || ''  // 标题
    const content = techStackForm.value.description || ''  // 内容
    
    const data = {
      category: title,
      name: '',
      level: '',
      description: content
    }
    
    if (editingTechStackId.value) {
      const updated = await api.updateTechStack(editingTechStackId.value, data)
      const index = techStacks.value.findIndex(t => t.id === editingTechStackId.value)
      if (index >= 0) techStacks.value[index] = updated
    } else {
      const created = await api.createTechStack(data)
      techStacks.value.unshift(created)
    }
    resetTechStackForm()
    alert('提交成功！')
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editTechStack(techStack: TechStack) {
  editingTechStackId.value = techStack.id
  // 标题存储在 category 字段，内容存储在 description 字段
  techStackForm.value.category = techStack.category || ''  // 标题
  techStackForm.value.description = techStack.description || ''  // 内容
  techStackForm.value.name = ''
  techStackForm.value.level = ''
}

function resetTechStackForm() {
  editingTechStackId.value = null
  techStackForm.value = {
    category: '',
    name: '',
    level: '',
    description: ''
  }
}

async function deleteTechStack(id: number) {
  if (!confirm('确定删除该技术栈？')) return
  try {
    await api.deleteTechStack(id)
    techStacks.value = techStacks.value.filter(t => t.id !== id)
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

// 简历照片相关方法
async function loadPhotos() {
  try {
    loading.value = true
    photos.value = await api.getResumePhotos()
  } catch (e: any) {
    error.value = e?.message || '加载简历照片失败'
  } finally {
    loading.value = false
  }
}

async function submitPhoto() {
  try {
    if (photoForm.value.files.length === 0) {
      alert('请选择要上传的图片')
      return
    }
    if (!photoForm.value.title) {
      alert('请输入标题')
      return
    }

    // 先上传所有图片
    const formData = new FormData()
    photoForm.value.files.forEach(file => {
      formData.append('files', file)
    })
    const uploadResult = await api.uploadPhoto(formData)
    
    // 将多个文件名用逗号连接
    const imagePaths = uploadResult.filenames.join(',')
    const data = {
      title: photoForm.value.title,
      image_paths: imagePaths
    }
    
    if (editingPhotoId.value) {
      const updated = await api.updateResumePhoto(editingPhotoId.value, data)
      const index = photos.value.findIndex(p => p.id === editingPhotoId.value)
      if (index >= 0) photos.value[index] = updated
    } else {
      const created = await api.createResumePhoto(data)
      photos.value.unshift(created)
    }
    resetPhotoForm()
    alert('提交成功！')
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editPhoto(photo: ResumePhoto) {
  editingPhotoId.value = photo.id
  photoForm.value.title = photo.title
  photoForm.value.files = []  // 编辑时不重新上传文件
}

function resetPhotoForm() {
  editingPhotoId.value = null
  photoForm.value = {
    title: '',
    files: []
  }
}

async function deletePhoto(id: number) {
  if (!confirm('确定删除这张简历照片？')) return
  try {
    await api.deleteResumePhoto(id)
    photos.value = photos.value.filter(p => p.id !== id)
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

function showPhotoModal(imagePaths: string) {
  // imagePaths 是逗号分隔的多个路径，取第一个
  const firstPath = imagePaths.split(',')[0]
  selectedPhoto.value = `/api/uploads/${firstPath}`
  showingPhotoModal.value = true
}

function closePhotoModal() {
  showingPhotoModal.value = false
  selectedPhoto.value = ''
}

// 岗位要求（JD）相关方法
async function loadJobDescriptions() {
  try {
    loading.value = true
    jobDescriptions.value = await api.getJobDescriptions()
  } catch (e: any) {
    error.value = e?.message || '加载岗位要求失败'
  } finally {
    loading.value = false
  }
}

async function submitJd() {
  try {
    if (!jdForm.value.company) {
      alert('请输入公司名称')
      return
    }
    if (!jdForm.value.position) {
      alert('请输入岗位名称')
      return
    }

    let imagePaths = ''
    // 如果有上传图片，先上传
    if (jdForm.value.files.length > 0) {
      const formData = new FormData()
      jdForm.value.files.forEach(file => {
        formData.append('files', file)
      })
      const uploadResult = await api.uploadJdImage(formData)
      imagePaths = uploadResult.filenames.join(',')
    }
    
    const data = {
      company: jdForm.value.company,
      position: jdForm.value.position,
      description: jdForm.value.description || undefined,
      image_paths: imagePaths || undefined
    }
    
    if (editingJdId.value) {
      const updated = await api.updateJobDescription(editingJdId.value, data)
      const index = jobDescriptions.value.findIndex(j => j.id === editingJdId.value)
      if (index >= 0) jobDescriptions.value[index] = updated
    } else {
      const created = await api.createJobDescription(data)
      jobDescriptions.value.unshift(created)
    }
    resetJdForm()
    alert('提交成功！')
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editJd(jd: JobDescription) {
  editingJdId.value = jd.id
  jdForm.value.company = jd.company
  jdForm.value.position = jd.position
  jdForm.value.description = jd.description || ''
  jdForm.value.files = []  // 编辑时不重新上传文件
}

function resetJdForm() {
  editingJdId.value = null
  jdForm.value = {
    company: '',
    position: '',
    description: '',
    files: []
  }
}

async function deleteJd(id: number) {
  if (!confirm('确定删除这个岗位要求？')) return
  try {
    await api.deleteJobDescription(id)
    jobDescriptions.value = jobDescriptions.value.filter(j => j.id !== id)
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

// JD拆解相关方法
async function loadBreakdowns(jdId: number) {
  try {
    loading.value = true
    jdBreakdowns.value = await api.getJdBreakdownsByJd(jdId)
  } catch (e: any) {
    error.value = e?.message || '加载拆解失败'
  } finally {
    loading.value = false
  }
}

function showBreakdownModal(jd: JobDescription) {
  currentJdForBreakdown.value = jd
  jdBreakdownForm.value.jd_id = jd.id
  jdBreakdownForm.value.company = jd.company
  jdBreakdownForm.value.position = jd.position
  jdBreakdownForm.value.breakdown_content = ''
  showingBreakdownModal.value = true
  loadBreakdowns(jd.id)
}

function closeBreakdownModal() {
  showingBreakdownModal.value = false
  currentJdForBreakdown.value = null
  jdBreakdownForm.value = {
    jd_id: 0,
    company: '',
    position: '',
    breakdown_content: ''
  }
  editingBreakdownId.value = null
}

async function submitBreakdown() {
  try {
    if (!jdBreakdownForm.value.breakdown_content) {
      alert('请输入拆解内容')
      return
    }

    const data = {
      jd_id: jdBreakdownForm.value.jd_id,
      company: jdBreakdownForm.value.company,
      position: jdBreakdownForm.value.position,
      breakdown_content: jdBreakdownForm.value.breakdown_content
    }
    
    if (editingBreakdownId.value) {
      const updated = await api.updateJdBreakdown(editingBreakdownId.value, data)
      const index = jdBreakdowns.value.findIndex(b => b.id === editingBreakdownId.value)
      if (index >= 0) jdBreakdowns.value[index] = updated
    } else {
      const created = await api.createJdBreakdown(data)
      jdBreakdowns.value.unshift(created)
    }
    resetBreakdownForm()
    alert('提交成功！')
  } catch (e: any) {
    alert(e?.message || '提交失败')
  }
}

function editBreakdown(breakdown: JdBreakdown) {
  editingBreakdownId.value = breakdown.id
  jdBreakdownForm.value.breakdown_content = breakdown.breakdown_content
}

function resetBreakdownForm() {
  editingBreakdownId.value = null
  if (currentJdForBreakdown.value) {
    jdBreakdownForm.value.company = currentJdForBreakdown.value.company
    jdBreakdownForm.value.position = currentJdForBreakdown.value.position
    jdBreakdownForm.value.breakdown_content = ''
  }
}

async function deleteBreakdown(id: number) {
  if (!confirm('确定删除这个拆解？')) return
  try {
    await api.deleteJdBreakdown(id)
    jdBreakdowns.value = jdBreakdowns.value.filter(b => b.id !== id)
  } catch (e: any) {
    alert(e?.message || '删除失败')
  }
}

// AI拆解功能
async function analyzeJdWithAI() {
  if (!currentJdForBreakdown.value) return
  
  try {
    // 检查JD是否有描述
    if (!currentJdForBreakdown.value.description) {
      alert('该JD没有文字描述，无法使用AI解析。请先添加文字描述。')
      return
    }
    
    aiAnalyzing.value = true
    
    // 清空表单内容，准备实时显示
    jdBreakdownForm.value.breakdown_content = ''
    
    // 调用流式AI拆解API
    await api.analyzeJdStream(
      currentJdForBreakdown.value.id,
      systemPrompt.value || undefined,
      // onChunk: 实时接收内容块
      (chunk: string) => {
        jdBreakdownForm.value.breakdown_content += chunk
      },
      // onDone: 完成后添加到列表
      (breakdownId: number) => {
        // 重新加载拆解列表
        loadBreakdowns(currentJdForBreakdown.value!.id)
        
        // 关闭系统提示词编辑器
        showingSystemPromptEditor.value = false
        
        alert('AI拆解完成！')
      },
      // onError: 错误处理
      (error: string) => {
        alert(error)
      }
    )
  } catch (e: any) {
    alert(e?.message || 'AI拆解失败')
  } finally {
    aiAnalyzing.value = false
  }
}

function toggleSystemPromptEditor() {
  showingSystemPromptEditor.value = !showingSystemPromptEditor.value
  if (!showingSystemPromptEditor.value) {
    // 关闭时清空提示词
    systemPrompt.value = ''
  }
}

// 加载不同子页面的数据
async function loadSectionData(section: 'internships' | 'projects' | 'tech-stacks' | 'photos' | 'job-descriptions') {
  switch (section) {
    case 'internships':
      await loadInternships()
      break
    case 'projects':
      await loadProjects()
      break
    case 'tech-stacks':
      await loadTechStacks()
      break
    case 'photos':
      await loadPhotos()
      break
    case 'job-descriptions':
      await loadJobDescriptions()
      break
  }
}

// 切换标签页时加载对应数据并更新路由
async function switchSection(section: 'internships' | 'projects' | 'tech-stacks' | 'photos' | 'job-descriptions') {
  activeSection.value = section
  
  // 更新路由
  const currentPath = route.path
  const pathParts = currentPath.split('/')
  const basePath = pathParts[1] // 当前的主标签页（如 'prompts', 'resume'）
  
  // 更新为 /basePath/section 格式
  router.push(`/${basePath}/${section}`)
  
  // 加载数据
  await loadSectionData(section)
}

onMounted(async () => {
  await api.ready()
  
  // 从路由获取初始子页面
  const subtab = route.params.subtab as string
  if (subtab === 'internships' || subtab === 'projects' || subtab === 'tech-stacks') {
    activeSection.value = subtab as 'internships' | 'projects' | 'tech-stacks'
    await loadSectionData(activeSection.value)
  } else {
    // 默认加载实习经历
    await loadInternships()
  }
})
</script>

<template>
  <div class="page">
    <!-- 内部导航栏 -->
    <div class="internal-nav">
      <nav class="tabs">
        <button 
          :class="{ active: activeSection === 'internships' }" 
          @click="switchSection('internships')"
        >
          💼 实习经历
        </button>
        <button 
          :class="{ active: activeSection === 'projects' }" 
          @click="switchSection('projects')"
        >
          🚀 项目经历
        </button>
        <button 
          :class="{ active: activeSection === 'tech-stacks' }" 
          @click="switchSection('tech-stacks')"
        >
          🛠️ 技术栈
        </button>
        <button 
          :class="{ active: activeSection === 'photos' }" 
          @click="switchSection('photos')"
        >
          📷 简历照片
        </button>
        <button 
          :class="{ active: activeSection === 'job-descriptions' }" 
          @click="switchSection('job-descriptions')"
        >
          💼 岗位要求
        </button>
      </nav>
    </div>

    <main class="main">
      <!-- 实习经历 -->
      <section v-show="activeSection === 'internships'" class="panel">
        <div class="section-header">
          <h2>💼 实习经历管理</h2>
          <p>记录您的实习工作经历，展示实践能力</p>
        </div>

        <div class="content-grid">
          <!-- 列表区域 -->
          <div class="list-section">
            <div class="list-header">
              <h3>实习经历列表</h3>
              <span class="count">{{ internships.length }} 条记录</span>
            </div>
            
            <div v-if="loading" class="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="internships.length === 0" class="empty">
              <div class="empty-icon">💼</div>
              <p>暂无实习经历</p>
              <small>点击右侧"新增"按钮开始添加</small>
            </div>
            <div v-else class="internship-groups">
              <template v-for="(items, groupKey) in groupedInternships" :key="groupKey">
                <!-- 分组标题 -->
                <div class="group-header">
                  <h4>{{ groupKey }}</h4>
                </div>
                <!-- 该组的所有列表项 -->
                <div 
                  v-for="internship in items" 
                  :key="internship.id" 
                  class="list-item"
                >
                <div v-if="internship.position" class="item-header">
                  <div class="item-title">{{ internship.position }}</div>
                </div>
                <div v-if="internship.description" class="item-description markdown">
                    <div v-html="renderMarkdown(internship.description)"></div>
                  </div>
                  <div class="item-actions">
                    <button class="btn-edit" @click="editInternship(internship)">编辑</button>
                    <button class="btn-delete" @click="deleteInternship(internship.id)">删除</button>
                  </div>
                </div>
              </template>
            </div>
          </div>

          <!-- 表单区域 -->
          <div class="form-section">
            <div class="form-header">
              <h3>{{ editingInternshipId ? '编辑实习经历' : '新增实习经历' }}</h3>
            </div>
            
            <form @submit.prevent="submitInternship" class="form">
              <div class="form-group">
                <label>分组标题</label>
                <input 
                  v-model="internshipForm.group_title" 
                  placeholder="请输入分组标题，如：小米科技实习（同一标题可包含多段描述）"
                />
                <small class="form-hint">💡 同一标题下的多个描述会分组展示</small>
              </div>

              <div class="form-group">
                <label>子标题（可选）</label>
                <input 
                  v-model="internshipForm.position" 
                  placeholder="请输入子标题，如：小米科技实习经历"
                />
                <small class="form-hint">💡 为这段经历起个简洁的标题（可选填）</small>
              </div>

              <div class="form-group">
                <label>录入内容 *</label>
                <textarea 
                  v-model="internshipForm.company" 
                  required 
                  rows="8" 
                  placeholder="请直接输入实习经历内容，例如：&#10;公司：腾讯&#10;职位：前端开发工程师&#10;时间：2023.06 - 2023.09&#10;描述：负责公司前端项目开发，使用React框架...&#10;技能：React, TypeScript, Vue"
                ></textarea>
                <small class="form-hint">💡 提示：直接粘贴或输入完整的实习经历内容即可</small>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn-primary">
                  {{ editingInternshipId ? '保存修改' : '新增记录' }}
                </button>
                <button type="button" class="btn-secondary" @click="resetInternshipForm">
                  清空
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- 项目经历 -->
      <section v-show="activeSection === 'projects'" class="panel">
        <div class="section-header">
          <h2>🚀 项目经历管理</h2>
          <p>记录您的项目经验，展示技术能力</p>
        </div>

        <div class="content-grid">
          <!-- 列表区域 -->
          <div class="list-section">
            <div class="list-header">
              <h3>项目经历列表</h3>
              <span class="count">{{ projects.length }} 条记录</span>
            </div>
            
            <div v-if="loading" class="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="projects.length === 0" class="empty">
              <div class="empty-icon">🚀</div>
              <p>暂无项目经历</p>
              <small>点击右侧"新增"按钮开始添加</small>
            </div>
            <div v-else class="list">
              <div 
                v-for="project in projects" 
                :key="project.id" 
                class="list-item"
              >
                <div class="item-header">
                  <div class="item-title">{{ project.name }}</div>
                  <div v-if="project.url" class="item-url">
                    <a :href="project.url" target="_blank" class="link">🔗 查看项目</a>
                  </div>
                </div>
                <div v-if="project.description" class="item-description markdown">
                  <div v-html="renderMarkdown(project.description)"></div>
                </div>
                <div class="item-actions">
                  <button class="btn-edit" @click="editProject(project)">编辑</button>
                  <button class="btn-delete" @click="deleteProject(project.id)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 表单区域 -->
          <div class="form-section">
            <div class="form-header">
              <h3>{{ editingProjectId ? '编辑项目经历' : '新增项目经历' }}</h3>
            </div>
            
            <form @submit.prevent="submitProject" class="form">
              <div class="form-group">
                <label>标题 *</label>
                <input 
                  v-model="projectForm.name" 
                  required 
                  placeholder="请输入项目标题"
                />
                <small class="form-hint">💡 为这段项目经历起个简洁的标题</small>
              </div>

              <div class="form-group">
                <label>录入内容 *</label>
                <textarea 
                  v-model="projectForm.description" 
                  required 
                  rows="8" 
                  placeholder="请直接输入项目经历内容，例如：&#10;项目名称：电商平台&#10;项目描述：一个在线购物平台，包含商品浏览、购物车、支付等功能...&#10;技术栈：Vue.js, Node.js, MongoDB, Redis&#10;时间：2023.01 - 2023.06&#10;项目链接：https://github.com/username/project"
                ></textarea>
                <small class="form-hint">💡 提示：直接粘贴或输入完整的项目经历内容即可</small>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn-primary">
                  {{ editingProjectId ? '保存修改' : '新增记录' }}
                </button>
                <button type="button" class="btn-secondary" @click="resetProjectForm">
                  清空
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- 技术栈 -->
      <section v-show="activeSection === 'tech-stacks'" class="panel">
        <div class="section-header">
          <h2>🛠️ 技术栈管理</h2>
          <p>管理您的技术技能，按分类展示</p>
        </div>

        <div class="content-grid">
          <!-- 列表区域 -->
          <div class="list-section">
            <div class="list-header">
              <h3>技术栈列表</h3>
              <span class="count">{{ techStacks.length }} 项技能</span>
            </div>
            
            <div v-if="loading" class="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="techStacks.length === 0" class="empty">
              <div class="empty-icon">🛠️</div>
              <p>暂无技术栈</p>
              <small>点击右侧"新增"按钮开始添加</small>
            </div>
            <div v-else class="list">
              <div 
                v-for="tech in techStacks" 
                :key="tech.id" 
                class="list-item"
              >
                <div v-if="tech.category" class="item-header">
                  <div class="item-title">{{ tech.category }}</div>
                </div>
                <div v-if="tech.description" class="item-description markdown">
                  <div v-html="renderMarkdown(tech.description)"></div>
                </div>
                <div class="item-actions">
                  <button class="btn-edit" @click="editTechStack(tech)">编辑</button>
                  <button class="btn-delete" @click="deleteTechStack(tech.id)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 表单区域 -->
          <div class="form-section">
            <div class="form-header">
              <h3>{{ editingTechStackId ? '编辑技术栈' : '新增技术栈' }}</h3>
            </div>
            
            <form @submit.prevent="submitTechStack" class="form">
              <div class="form-group">
                <label>标题 *</label>
                <input
                  v-model="techStackForm.category"
                  required
                  placeholder="请输入标题，如：前端技术"
                />
                <small class="form-hint">💡 为这个技术栈起个简洁的标题</small>
              </div>

              <div class="form-group">
                <label>录入内容 *</label>
                <textarea 
                  v-model="techStackForm.description" 
                  required 
                  rows="8" 
                  placeholder="请直接输入技术栈内容，例如：&#10;- React: 熟练&#10;- Vue: 掌握&#10;- TypeScript: 精通..."
                ></textarea>
                <small class="form-hint">💡 提示：直接粘贴或输入完整的技术栈内容即可（支持 Markdown）</small>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn-primary">
                  {{ editingTechStackId ? '保存修改' : '新增记录' }}
                </button>
                <button type="button" class="btn-secondary" @click="resetTechStackForm">
                  清空
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- 简历照片 -->
      <section v-show="activeSection === 'photos'" class="panel">
        <div class="section-header">
          <h2>📷 简历照片管理</h2>
          <p>上传和管理您的简历照片，点击可放大查看</p>
        </div>

        <div class="content-grid">
          <!-- 列表区域 -->
          <div class="list-section">
            <div class="list-header">
              <h3>照片列表</h3>
              <span class="count">{{ photos.length }} 张</span>
            </div>
            
            <div v-if="loading" class="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="photos.length === 0" class="empty">
              <div class="empty-icon">📷</div>
              <p>暂无简历照片</p>
              <small>点击右侧"新增"按钮开始上传</small>
            </div>
            <div v-else class="photo-list">
              <div 
                v-for="photo in photos" 
                :key="photo.id" 
                class="photo-item"
              >
                <div class="photo-header">
                  <h4>{{ photo.title }}</h4>
                </div>
                <div class="photo-images">
                  <template v-if="photo.image_paths">
                    <div 
                      v-for="(imagePath, index) in photo.image_paths.split(',')" 
                      :key="index"
                      class="photo-image"
                      @click="showPhotoModal(photo.image_paths || '')"
                    >
                      <img :src="`/api/uploads/${imagePath}`" :alt="photo.title" />
                    </div>
                  </template>
                </div>
                <div class="photo-actions">
                  <button class="btn-edit" @click="editPhoto(photo)">编辑</button>
                  <button class="btn-delete" @click="deletePhoto(photo.id)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 表单区域 -->
          <div class="form-section">
            <div class="form-header">
              <h3>{{ editingPhotoId ? '编辑照片信息' : '新增简历照片' }}</h3>
            </div>
            
            <form @submit.prevent="submitPhoto" class="form">
              <div class="form-group">
                <label>标题 *</label>
                <input
                  v-model="photoForm.title"
                  required
                  placeholder="请输入照片标题，如：个人简历2024"
                />
                <small class="form-hint">💡 为这张照片起个简洁的标题</small>
              </div>

              <div class="form-group">
                <label>选择图片 *</label>
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  @change="(e: Event) => {
                    const target = e.target as HTMLInputElement;
                    if (target.files) {
                      photoForm.files = Array.from(target.files);
                    }
                  }"
                  :required="!editingPhotoId"
                />
                <small class="form-hint">💡 支持 JPG、PNG 等常见图片格式，可同时选择多张图片</small>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn-primary">
                  {{ editingPhotoId ? '保存修改' : '上传照片' }}
                </button>
                <button type="button" class="btn-secondary" @click="resetPhotoForm">
                  清空
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      <!-- 岗位要求 -->
      <section v-show="activeSection === 'job-descriptions'" class="panel">
        <div class="section-header">
          <h2>💼 岗位要求管理</h2>
          <p>管理岗位要求（JD），支持上传图片或输入文字描述</p>
        </div>

        <div class="content-grid">
          <!-- 列表区域 -->
          <div class="list-section">
            <div class="list-header">
              <h3>岗位要求列表</h3>
              <span class="count">{{ jobDescriptions.length }} 条</span>
            </div>
            
            <div v-if="loading" class="loading">加载中...</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="jobDescriptions.length === 0" class="empty">
              <div class="empty-icon">💼</div>
              <p>暂无岗位要求</p>
              <small>点击右侧"新增"按钮开始添加</small>
            </div>
            <div v-else class="list">
              <div 
                v-for="jd in jobDescriptions" 
                :key="jd.id" 
                class="list-item"
              >
                <div class="item-header">
                  <div class="item-title">{{ jd.company }} - {{ jd.position }}</div>
                </div>
                
                <!-- 显示文字描述（Markdown 渲染） -->
                <div v-if="jd.description" class="item-description markdown">
                  <div v-html="renderMarkdown(jd.description)"></div>
                </div>
                
                <!-- 显示图片 -->
                <div v-if="jd.image_paths" class="jd-images">
                  <div 
                    v-for="(imagePath, index) in jd.image_paths.split(',')" 
                    :key="index"
                    class="jd-image"
                    @click="showPhotoModal(jd.image_paths || '')"
                  >
                    <img :src="`/api/uploads/${imagePath}`" :alt="jd.company + ' - ' + jd.position" />
                  </div>
                </div>
                
                <div class="item-actions">
                  <button class="btn-primary" @click="showBreakdownModal(jd)">🔍 拆解</button>
                  <button class="btn-edit" @click="editJd(jd)">编辑</button>
                  <button class="btn-delete" @click="deleteJd(jd.id)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 表单区域 -->
          <div class="form-section">
            <div class="form-header">
              <h3>{{ editingJdId ? '编辑岗位要求' : '新增岗位要求' }}</h3>
            </div>
            
            <form @submit.prevent="submitJd" class="form">
              <div class="form-group">
                <label>公司名称 *</label>
                <input
                  v-model="jdForm.company"
                  required
                  placeholder="请输入公司名称"
                />
              </div>

              <div class="form-group">
                <label>岗位名称 *</label>
                <input
                  v-model="jdForm.position"
                  required
                  placeholder="请输入岗位名称"
                />
              </div>

              <div class="form-group">
                <label>文字描述</label>
                <textarea 
                  v-model="jdForm.description" 
                  rows="6" 
                  placeholder="请输入岗位要求的文字描述（可选）"
                ></textarea>
                <small class="form-hint">💡 可以输入纯文字描述，也可以上传图片</small>
              </div>

              <div class="form-group">
                <label>JD图片（可选）</label>
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  @change="(e: Event) => {
                    const target = e.target as HTMLInputElement;
                    if (target.files) {
                      jdForm.files = Array.from(target.files);
                    }
                  }"
                />
                <small class="form-hint">💡 支持上传多张 JD 图片，也支持只上传图片不填文字</small>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn-primary">
                  {{ editingJdId ? '保存修改' : '提交' }}
                </button>
                <button type="button" class="btn-secondary" @click="resetJdForm">
                  清空
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>
    </main>
  </div>

  <!-- 图片查看模态框 -->
  <Teleport to="body">
    <div v-if="showingPhotoModal" class="photo-modal" @click="closePhotoModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closePhotoModal">×</button>
        <img :src="selectedPhoto" alt="简历照片" />
      </div>
    </div>
  </Teleport>

  <!-- JD拆解管理模态框 -->
  <Teleport to="body">
    <div v-if="showingBreakdownModal" class="breakdown-modal" @click="closeBreakdownModal">
      <div class="breakdown-modal-content" @click.stop>
        <div class="breakdown-header">
          <h2>{{ currentJdForBreakdown?.company }} - {{ currentJdForBreakdown?.position }} 拆解</h2>
          <button class="modal-close" @click="closeBreakdownModal">×</button>
        </div>
        
        <div class="breakdown-body">
          <!-- 拆解列表 -->
          <div class="breakdown-list">
            <div class="breakdown-list-header">
              <h3>已有拆解（{{ jdBreakdowns.length }} 条）</h3>
              <button 
                class="btn-primary" 
                @click="toggleSystemPromptEditor"
                :disabled="aiAnalyzing"
              >
                {{ showingSystemPromptEditor ? '取消' : '🤖 使用AI拆解' }}
              </button>
            </div>
            
            <!-- 系统提示词编辑器 -->
            <div v-if="showingSystemPromptEditor" class="system-prompt-editor">
              <h4>系统提示词配置（可选）</h4>
              <textarea 
                v-model="systemPrompt" 
                rows="8"
                placeholder="输入自定义系统提示词，用于指导AI如何拆解JD。留空则使用默认提示词。"
              ></textarea>
              <div class="system-prompt-actions">
                <button 
                  class="btn-primary" 
                  @click="analyzeJdWithAI"
                  :disabled="aiAnalyzing"
                >
                  {{ aiAnalyzing ? '分析中...' : '开始AI拆解' }}
                </button>
              </div>
            </div>
            
            <div v-if="jdBreakdowns.length === 0 && !showingSystemPromptEditor" class="empty">
              <p>暂无拆解内容</p>
            </div>
            <div v-else-if="jdBreakdowns.length > 0" class="breakdown-items">
              <div 
                v-for="breakdown in jdBreakdowns" 
                :key="breakdown.id"
                class="breakdown-item"
              >
                <div class="breakdown-content markdown" v-html="renderMarkdown(breakdown.breakdown_content)"></div>
                <div class="breakdown-actions">
                  <button class="btn-small" @click="editBreakdown(breakdown)">编辑</button>
                  <button class="btn-small btn-delete" @click="deleteBreakdown(breakdown.id)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 新增/编辑拆解表单 -->
          <div class="breakdown-form">
            <h3>{{ editingBreakdownId ? '编辑拆解' : '新增拆解' }}</h3>
            <form @submit.prevent="submitBreakdown">
              <div class="form-group">
                <label>拆解内容 *</label>
                <textarea 
                  v-model="jdBreakdownForm.breakdown_content" 
                  required
                  rows="10" 
                  placeholder="请输入拆解内容（支持 Markdown 格式）"
                ></textarea>
                <small class="form-hint">💡 支持 Markdown 格式，用于结构化展示JD拆解</small>
              </div>
              <div class="form-actions">
                <button type="submit" class="btn-primary">
                  {{ editingBreakdownId ? '保存修改' : '提交' }}
                </button>
                <button type="button" class="btn-secondary" @click="resetBreakdownForm">
                  重置
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
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

/* 区域头部 */
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

/* 内容网格布局 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  align-items: start;
}

/* 列表区域 */
.list-section {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.list-header h3 {
  color: #1e293b;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.count {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* 空状态 */
.empty {
  text-align: center;
  padding: 40px 20px;
  color: #64748b;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty p {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 500;
}

.empty small {
  font-size: 14px;
  opacity: 0.8;
}

/* 加载和错误状态 */
.loading, .error {
  text-align: center;
  padding: 40px 20px;
  font-size: 16px;
}

.error {
  color: #ef4444;
}

/* 列表项 */
.list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.list-item {
  width: 100%;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.list-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.item-company {
  color: #64748b;
  font-size: 14px;
}

.item-url {
  margin-left: 12px;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-size: 12px;
}

.link:hover {
  text-decoration: underline;
}

.item-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 14px;
}

.date {
  color: #64748b;
}

.skills, .tech-stack {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
}

.item-description {
  color: #475569;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
}

.item-description.markdown {
  white-space: pre-wrap;
  line-height: 1.5;
}

.item-description.markdown p {
  margin: 2px 0;
  line-height: 1.4;
  padding: 0;
}

.item-description.markdown h1,
.item-description.markdown h2,
.item-description.markdown h3,
.item-description.markdown h4,
.item-description.markdown h5,
.item-description.markdown h6 {
  color: #1e293b;
  margin: 8px 0 4px;
  font-weight: 600;
}

.item-description.markdown h1 { font-size: 20px; }
.item-description.markdown h2 { font-size: 18px; }
.item-description.markdown h3 { font-size: 16px; }

.item-description.markdown ul {
  margin: 8px 0;
  padding-left: 20px;
  list-style-type: disc;
}

.item-description.markdown li {
  margin: 3px 0;
  line-height: 1.5;
}

.item-description.markdown strong {
  color: #1e293b;
  font-weight: 600;
}

.item-description.markdown em {
  font-style: italic;
}

/* 分组展示样式 */
.internship-groups {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.group-header {
  width: 100%;
  margin-bottom: 4px;
  margin-top: 8px;
}

.group-header h4 {
  color: #1e293b;
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(102, 126, 234, 0.3);
  width: 100%;
}

.item-actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-edit {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.btn-edit:hover {
  background: rgba(102, 126, 234, 0.2);
}

.btn-delete {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* 技术栈分组 */
.tech-stack-groups {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tech-group {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.group-header h4 {
  color: #1e293b;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.group-count {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
}

.group-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.tech-item {
  background: rgba(248, 250, 252, 0.8);
  border-radius: 8px;
  padding: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.tech-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.tech-name {
  font-weight: 500;
  color: #1e293b;
  font-size: 14px;
}

.tech-level {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.tech-description {
  color: #64748b;
  font-size: 12px;
  line-height: 1.4;
  margin-bottom: 8px;
}

.tech-actions {
  display: flex;
  gap: 4px;
}

/* 表单区域 */
.form-section {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 20px;
}

.form-header {
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.form-header h3 {
  color: #1e293b;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

label {
  font-size: 13px;
  color: #374151;
  font-weight: 500;
}

input, textarea, select {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  background: #fff;
  color: #111;
  transition: all 0.2s ease;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

input::placeholder, textarea::placeholder {
  color: #9ca3af;
}

.form-hint {
  display: block;
  margin-top: 8px;
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn-primary, .btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  flex: 1;
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

/* 响应式设计 */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .form-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .main {
    padding: 0 16px 16px;
  }
  
  .topbar {
    padding: 12px 16px;
    margin-bottom: 16px;
  }
  
  .tabs {
    gap: 4px;
  }
  
  .tabs button {
    padding: 6px 12px;
    font-size: 13px;
  }
  
  .section-header {
    padding: 16px;
    margin-bottom: 20px;
  }
  
  .section-header h2 {
    font-size: 20px;
  }
  
  .list-section, .form-section {
    padding: 16px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .group-items {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .brand {
    font-size: 16px;
  }
  
  .tabs button {
    padding: 6px 8px;
  }
  
  .item-header {
    flex-direction: column;
    gap: 4px;
  }
  
  .item-meta {
    flex-direction: column;
    gap: 4px;
  }
}

/* 照片列表 */
.photo-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.photo-item {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.photo-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.photo-header {
  margin-bottom: 12px;
}

.photo-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.photo-images {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.photo-image {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: border-color 0.2s;
}

.photo-image:hover {
  border-color: #3b82f6;
}

.photo-image img {
  width: 100%;
  height: auto;
  display: block;
}

.photo-actions {
  display: flex;
  gap: 8px;
}

/* 图片查看模态框 */
.photo-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  cursor: pointer;
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  cursor: default;
}

.modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 40px;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  line-height: 40px;
  transition: opacity 0.2s;
}

.modal-close:hover {
  opacity: 0.7;
}

.modal-content img {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
}

/* JD 图片列表 */
.jd-images {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.jd-image {
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  transition: border-color 0.2s;
}

.jd-image:hover {
  border-color: #3b82f6;
}

.jd-image img {
  width: 100%;
  height: auto;
  display: block;
}

/* JD拆解模态框 */
.breakdown-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.breakdown-modal-content {
  background: white;
  border-radius: 16px;
  max-width: 1200px;
  max-height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.breakdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.breakdown-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
}

.breakdown-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.breakdown-list {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
}

.breakdown-list h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.breakdown-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.breakdown-item {
  background: white;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e2e8f0;
}

.breakdown-content {
  margin-bottom: 12px;
  color: #334155;
  line-height: 1.6;
  font-size: 14px;
}

.breakdown-actions {
  display: flex;
  gap: 8px;
}

.btn-small {
  padding: 4px 12px;
  font-size: 12px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-small:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.btn-small.btn-delete {
  color: #ef4444;
  border-color: #ef4444;
}

.btn-small.btn-delete:hover {
  background: #fee2e2;
}

.breakdown-form {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
}

.breakdown-form h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.breakdown-form .form-group {
  margin-bottom: 16px;
}

.breakdown-form .form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #334155;
}

.breakdown-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
}

@media (max-width: 1024px) {
  .breakdown-body {
    grid-template-columns: 1fr;
  }
}

/* 拆解列表头部 */
.breakdown-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.breakdown-list-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

/* 系统提示词编辑器 */
.system-prompt-editor {
  background: white;
  border: 2px solid #667eea;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.system-prompt-editor h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.system-prompt-editor textarea {
  width: 100%;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  font-family: monospace;
  margin-bottom: 12px;
  resize: vertical;
  line-height: 1.5;
}

.system-prompt-actions {
  display: flex;
  justify-content: flex-end;
}

.system-prompt-actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
