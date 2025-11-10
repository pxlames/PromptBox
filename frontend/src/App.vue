<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PromptManager from './components/PromptManager.vue'
import ResumeManager from './components/ResumeManager.vue'
import OKRManager from './components/OKRManager.vue'
import AlgoPractice from './components/AlgoPractice.vue'
import InterviewBank from './components/InterviewBank.vue'
import OpinionBank from './components/OpinionBank.vue'
import StoryBank from './components/StoryBank.vue'
import TimelineRecord from './components/TimelineRecord.vue'
import AiAssistant from './components/AiAssistant.vue'

const router = useRouter()
const route = useRoute()

// 标签页配置
const tabs = [
  { id: 'prompts', name: 'Prompt管理', icon: '💡', component: PromptManager },
  { id: 'resume', name: '简历管理', icon: '📄', component: ResumeManager },
  { id: 'okr', name: 'OKR管理', icon: '🎯', component: OKRManager },
  { id: 'algo', name: '刷题', icon: '🧩', component: AlgoPractice },
  { id: 'interview', name: '面试题库 Interview', icon: '🎤', component: InterviewBank },
  { id: 'opinion', name: '观点记录', icon: '💭', component: OpinionBank },
  { id: 'story', name: '故事会', icon: '📖', component: StoryBank },
  { id: 'timeline', name: '记录线', icon: '📋', component: TimelineRecord },
  // 预留更多标签页位置
  { id: 'analytics', name: '数据分析', icon: '📊', component: null },
  { id: 'settings', name: '系统设置', icon: '⚙️', component: null },
  { id: 'tools', name: '工具箱', icon: '🔧', component: null },
  { id: 'docs', name: '文档中心', icon: '📚', component: null },
  { id: 'templates', name: '模板库', icon: '📋', component: null },
  { id: 'collaboration', name: '协作空间', icon: '👥', component: null },
  { id: 'ai-assistant', name: 'AI助手', icon: '🤖', component: null },
  { id: 'workflow', name: '工作流', icon: '🔄', component: null },
  { id: 'export', name: '导出工具', icon: '📤', component: null },
  { id: 'backup', name: '备份恢复', icon: '💾', component: null }
]

// 从路由获取当前标签页
const activeTab = computed(() => {
  const tabFromRoute = route.params.tab || 'prompts'
  return tabFromRoute
})

const currentTab = computed(() => tabs.find(tab => tab.id === activeTab.value))

// 监听路由变化，更新活动标签
watch(() => route.params.tab, (newTab) => {
  if (newTab) {
    // 路由变化时，组件会自动更新
  }
}, { immediate: true })

function switchTab(tabId) {
  // 更新路由
  router.push(`/${tabId}`)
}
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-content">
        <div class="brand">
          <div class="brand-icon">🚀</div>
          <div class="brand-text">智能工作台</div>
        </div>
        
        <nav class="tab-navigation">
          <div class="tab-list">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              :class="['tab-button', { active: activeTab.value === tab.id, disabled: !tab.component }]"
              @click="tab.component ? switchTab(tab.id) : null"
              :title="tab.component ? tab.name : `${tab.name} (即将推出)`"
            >
              <span class="tab-icon">{{ tab.icon }}</span>
              <span class="tab-name">{{ tab.name }}</span>
            </button>
          </div>
        </nav>
        
        <div class="header-actions">
          <button class="action-button" title="搜索">
            <span>🔍</span>
          </button>
          <button class="action-button" title="通知">
            <span>🔔</span>
          </button>
          <button class="action-button" title="用户设置">
            <span>👤</span>
          </button>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="app-main">
      <div class="content-wrapper">
        <component 
          :is="currentTab?.component" 
          v-if="currentTab?.component"
          :key="activeTab"
        />
        <div v-else class="coming-soon">
          <div class="coming-soon-content">
            <div class="coming-soon-icon">{{ currentTab?.icon }}</div>
            <h2>{{ currentTab?.name }}</h2>
            <p>该功能正在开发中，敬请期待...</p>
            <div class="progress-indicator">
              <div class="progress-bar">
                <div class="progress-fill"></div>
              </div>
              <span class="progress-text">开发进度: 25%</span>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- AI助手组件 -->
    <AiAssistant />
  </div>
</template>

<style scoped>
.app-container {
  display: grid;
  grid-template-rows: 64px 1fr;
  height: 100dvh;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 顶部导航栏 */
.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
}

.header-content {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 20px;
  height: 100%;
  padding: 0 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 18px;
  color: #1e293b;
  white-space: nowrap;
  flex-shrink: 0;
}

.brand-icon {
  font-size: 24px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.brand-text {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 标签页导航 */
.tab-navigation {
  display: flex;
  justify-content: center;
  min-width: 0;
  overflow: hidden;
}

.tab-list {
  display: flex;
  gap: 4px;
  background: rgba(0, 0, 0, 0.05);
  padding: 4px;
  border-radius: 12px;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.tab-list::-webkit-scrollbar {
  display: none;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  position: relative;
}

.tab-button:hover:not(.disabled) {
  background: rgba(255, 255, 255, 0.7);
  color: #334155;
  transform: translateY(-1px);
}

.tab-button.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transform: translateY(-1px);
}

.tab-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tab-icon {
  font-size: 16px;
}

.tab-name {
  font-weight: 500;
}

/* 头部操作按钮 */
.header-actions {
  display: flex;
  gap: 8px;
}

.action-button {
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.action-button:hover {
  background: rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

/* 主内容区域 */
.app-main {
  background: #f8fafc;
  overflow: hidden;
}

.content-wrapper {
  height: 100%;
  overflow: auto;
}

/* 即将推出页面 */
.coming-soon {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.coming-soon-content {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 400px;
}

.coming-soon-icon {
  font-size: 64px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.coming-soon-content h2 {
  color: #1e293b;
  margin-bottom: 12px;
  font-size: 24px;
  font-weight: 600;
}

.coming-soon-content p {
  color: #64748b;
  margin-bottom: 24px;
  font-size: 16px;
}

.progress-indicator {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  width: 25%;
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  animation: progress 2s ease-in-out infinite;
}

@keyframes progress {
  0% { width: 25%; }
  50% { width: 30%; }
  100% { width: 25%; }
}

.progress-text {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .tab-name {
    display: none;
  }
  
  .tab-button {
    padding: 8px 12px;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
    gap: 12px;
  }
  
  .tab-navigation {
    min-width: 0;
  }
  
  .brand-text {
    display: none;
  }
  
  .header-actions {
    gap: 4px;
    flex-shrink: 0;
  }
  
  .action-button {
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 480px) {
  .header-content {
    padding: 0 12px;
    gap: 8px;
  }
  
  .tab-list {
    gap: 2px;
    padding: 2px;
  }
  
  .tab-button {
    padding: 6px 8px;
  }
  
  .tab-icon {
    font-size: 14px;
  }
  
  .action-button {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }
}
</style>
