import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/prompts'
  },
  {
    path: '/:tab/:subtab?',
    name: 'TabPage',
    meta: {
      title: '智能工作台'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 监听路由变化，更新页面标题
router.beforeEach((to, from, next) => {
  const tabName = to.params.tab
  const tabMap = {
    'prompts': '💡 Prompt管理',
    'resume': '📄 简历管理',
    'okr': '🎯 OKR管理',
    'algo': '🧩 刷题',
    'analytics': '📊 数据分析',
    'settings': '⚙️ 系统设置',
    'tools': '🔧 工具箱',
    'docs': '📚 文档中心',
    'templates': '📋 模板库',
    'collaboration': '👥 协作空间',
    'ai-assistant': '🤖 AI助手',
    'workflow': '🔄 工作流',
    'export': '📤 导出工具',
    'backup': '💾 备份恢复',
    'interview': '🎤 面试题库 Interview',
    'opinion': '💭 观点记录',
    'story': '📖 故事会',
    'timeline': '📋 记录线'
  }
  
  const title = tabMap[tabName] || '智能工作台'
  document.title = title
  
  next()
})

export default router
