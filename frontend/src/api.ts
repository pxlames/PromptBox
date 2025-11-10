let BASE_URL: string = 'http://127.0.0.1:8000';
let resolveReady: (() => void) | null = null;
// 当配置读取完成后 resolve，用于首屏请求等待配置
const configReady: Promise<void> = new Promise((resolve) => { resolveReady = resolve; });

// runtime config via /public/config.json
// if the file exists, override BASE_URL at runtime
fetch('/config.json').then(async (r) => {
  try {
    if (r.ok) {
      const cfg = await r.json();
      if (cfg && typeof cfg.apiBase === 'string' && cfg.apiBase.trim()) {
        BASE_URL = cfg.apiBase.trim();
      }
    }
  } catch {}
  finally { if (resolveReady) resolveReady(); }
}).catch(() => { if (resolveReady) resolveReady(); });

export type Prompt = {
  id: number;
  title: string;
  content: string;
  tags?: string;
  created_at: string;
  updated_at: string;
};

export type PromptCreate = Omit<Prompt, 'id' | 'created_at' | 'updated_at'>;
export type PromptUpdate = Partial<PromptCreate>;

// 简历相关类型定义
export type Internship = {
  id: number;
  group_title?: string;  // 分组标题
  company: string;
  position: string;
  start_date: string;
  end_date?: string;
  description?: string;
  skills?: string;
  created_at: string;
  updated_at: string;
};

export type InternshipCreate = Omit<Internship, 'id' | 'created_at' | 'updated_at'>;
export type InternshipUpdate = Partial<InternshipCreate>;

export type Project = {
  id: number;
  name: string;
  description: string;
  tech_stack?: string;
  start_date?: string;
  end_date?: string;
  url?: string;
  created_at: string;
  updated_at: string;
};

export type ProjectCreate = Omit<Project, 'id' | 'created_at' | 'updated_at'>;
export type ProjectUpdate = Partial<ProjectCreate>;

export type TechStack = {
  id: number;
  category: string;
  name: string;
  level: string;
  description?: string;
  created_at: string;
  updated_at: string;
};

export type TechStackCreate = Omit<TechStack, 'id' | 'created_at' | 'updated_at'>;
export type TechStackUpdate = Partial<TechStackCreate>;

export type ResumePhoto = {
  id: number;
  title: string;
  image_paths?: string;  // 多个图片路径，用逗号分隔
  created_at: string;
  updated_at: string;
};

export type ResumePhotoCreate = Omit<ResumePhoto, 'id' | 'created_at' | 'updated_at'>;
export type ResumePhotoUpdate = Partial<ResumePhotoCreate>;

export type JobDescription = {
  id: number;
  company: string;
  position: string;
  image_paths?: string;  // JD图片路径，用逗号分隔
  description?: string;  // 文字描述
  created_at: string;
  updated_at: string;
};

export type JobDescriptionCreate = Omit<JobDescription, 'id' | 'created_at' | 'updated_at'>;
export type JobDescriptionUpdate = Partial<JobDescriptionCreate>;

export type JdBreakdown = {
  id: number;
  jd_id: number;
  company: string;
  position: string;
  breakdown_content: string;  // 拆解内容（Markdown格式）
  created_at: string;
  updated_at: string;
};

export type JdBreakdownCreate = Omit<JdBreakdown, 'id' | 'created_at' | 'updated_at'>;
export type JdBreakdownUpdate = Partial<JdBreakdownCreate>;

// OKR相关类型定义
export type OKR = {
  id: number;
  objective: string;
  completed: boolean;
  due_date?: string;
  created_at: string;
  updated_at: string;
};

export type OKRCreate = Omit<OKR, 'id' | 'completed' | 'created_at' | 'updated_at'>;
export type OKRUpdate = Partial<OKRCreate> & { completed?: boolean };

// Task相关类型定义
export type Task = {
  id: number;
  okr_id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
};

export type TaskCreate = Omit<Task, 'id' | 'completed' | 'created_at' | 'updated_at'>;
export type TaskUpdate = Partial<TaskCreate> & { completed?: boolean };

// 面试题库相关类型定义
export type InterviewCategory = {
  id: number;
  name: string;
  order: number;
  created_at: string;
  updated_at: string;
};

export type InterviewCategoryCreate = Omit<InterviewCategory, 'id' | 'created_at' | 'updated_at'>;
export type InterviewCategoryUpdate = Partial<InterviewCategoryCreate>;

export type InterviewAnswer = {
  id: number;
  question_id: number;
  content: string;
  created_at: string;
  updated_at: string;
};

export type InterviewAnswerCreate = Omit<InterviewAnswer, 'id' | 'created_at' | 'updated_at'>;
export type InterviewAnswerUpdate = Partial<Omit<InterviewAnswer, 'id' | 'question_id' | 'created_at' | 'updated_at'>>;

export type InterviewQuestion = {
  id: number;
  description: string;
  category_id: number | null;
  company: string;
  tags: string;
  difficulty: '简单' | '中等' | '困难';
  round: string;
  answers: InterviewAnswer[];
  created_at: string;
  updated_at: string;
};

export type InterviewQuestionCreate = Omit<InterviewQuestion, 'id' | 'answers' | 'created_at' | 'updated_at'>;
export type InterviewQuestionUpdate = Partial<Omit<InterviewQuestion, 'id' | 'answers' | 'created_at' | 'updated_at'>>;

// 观点记录相关类型定义
export type OpinionCategory = {
  id: number;
  name: string;
  order: number;
  created_at: string;
  updated_at: string;
};

export type OpinionCategoryCreate = Omit<OpinionCategory, 'id' | 'created_at' | 'updated_at'>;
export type OpinionCategoryUpdate = Partial<OpinionCategoryCreate>;

export type Opinion = {
  id: number;
  description: string;
  category_id: number | null;
  created_at: string;
  updated_at: string;
};

export type OpinionCreate = Omit<Opinion, 'id' | 'created_at' | 'updated_at'>;
export type OpinionUpdate = Partial<OpinionCreate>;

// 故事会相关类型定义
export type StoryCategory = {
  id: number;
  name: string;
  order: number;
  created_at: string;
  updated_at: string;
};

export type StoryCategoryCreate = Omit<StoryCategory, 'id' | 'created_at' | 'updated_at'>;
export type StoryCategoryUpdate = Partial<StoryCategoryCreate>;

export type Story = {
  id: number;
  title: string;
  content: string;
  category_id: number | null;
  image_paths: string | null;  // 图片路径，用逗号分隔
  essence: string | null;  // 透过故事看到的本质
  created_at: string;
  updated_at: string;
};

export type StoryCreate = Omit<Story, 'id' | 'created_at' | 'updated_at'>;
export type StoryUpdate = Partial<StoryCreate>;

// 刷题相关类型定义
export type AlgoCategory = {
  id: number;
  name: string;
  order: number;
  created_at: string;
  updated_at: string;
};

export type AlgoCategoryCreate = Omit<AlgoCategory, 'id' | 'created_at' | 'updated_at'>;
export type AlgoCategoryUpdate = Partial<AlgoCategoryCreate>;

export type AlgoProblem = {
  id: number;
  title: string;
  category_id: number | null;
  difficulty: '简单' | '中等' | '困难';
  companies: string;
  tags: string;
  status: '未开始' | '已掌握' | '再复习';
  link: string;
  description: string | null;
  solution: string | null;
  created_at: string;
  updated_at: string;
};

export type AlgoProblemCreate = Omit<AlgoProblem, 'id' | 'created_at' | 'updated_at'>;
export type AlgoProblemUpdate = Partial<AlgoProblemCreate>;

// 题解相关类型定义
export type AlgoSolution = {
  id: number;
  problem_id: number;
  title: string;
  content: string;
  language: string;
  complexity_time: string;
  complexity_space: string;
  order: number;
  created_at: string;
  updated_at: string;
};

export type AlgoSolutionCreate = Omit<AlgoSolution, 'id' | 'created_at' | 'updated_at'>;
export type AlgoSolutionUpdate = Partial<Omit<AlgoSolution, 'id' | 'problem_id' | 'created_at' | 'updated_at'>>;

// 时间线记录相关类型定义
export type TimelineTopic = {
  id: number;
  title: string;
  order: number;
  created_at: string;
  updated_at: string;
};

export type TimelineTopicCreate = Omit<TimelineTopic, 'id' | 'created_at' | 'updated_at'>;
export type TimelineTopicUpdate = Partial<TimelineTopicCreate>;

export type TimelineEntry = {
  id: number;
  topic_id: number;
  subtitle: string;
  conclusion: string | null;
  content: string | null;
  image_paths: string | null;  // 图片路径，用逗号分隔
  order: number;
  created_at: string;
  updated_at: string;
};

export type TimelineEntryCreate = Omit<TimelineEntry, 'id' | 'created_at' | 'updated_at'>;
export type TimelineEntryUpdate = Partial<Omit<TimelineEntry, 'id' | 'topic_id' | 'created_at' | 'updated_at'>>;

export type TimelineSubEntry = {
  id: number;
  entry_id: number;
  subtitle: string;
  conclusion: string | null;
  content: string | null;
  image_paths: string | null;  // 图片路径，用逗号分隔
  order: number;
  created_at: string;
  updated_at: string;
};

export type TimelineSubEntryCreate = Omit<TimelineSubEntry, 'id' | 'created_at' | 'updated_at'>;
export type TimelineSubEntryUpdate = Partial<Omit<TimelineSubEntry, 'id' | 'entry_id' | 'created_at' | 'updated_at'>>;

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  // 使用相对路径，通过 Vite 代理访问后端
  // 这样可以避免跨域问题，特别是在局域网访问时
  try {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  if (res.status === 204) return undefined as unknown as T;
  return (await res.json()) as T;
  } catch (error) {
    // 包装fetch错误，提供更友好的错误信息
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('网络请求失败，请检查后端服务是否运行');
    }
    throw error;
  }
}

export const api = {
  ready: () => configReady,
  
  // Prompt API
  list: (params?: { skip?: number; limit?: number; q?: string | null; sort?: string | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.q) query.set('q', params.q);
    if (params?.sort) query.set('sort', params.sort);
    const qs = query.toString();
    return http<Prompt[]>(`/prompts/${qs ? `?${qs}` : ''}`);
  },
  count: (q?: string | null) => {
    const query = new URLSearchParams();
    if (q) query.set('q', q);
    const qs = query.toString();
    return http<{ total: number }>(`/prompts/count${qs ? `?${qs}` : ''}`);
  },
  get: (id: number) => http<Prompt>(`/prompts/${id}`),
  create: (data: PromptCreate) => http<Prompt>('/prompts/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: PromptUpdate) => http<Prompt>(`/prompts/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  remove: (id: number) => http<void>(`/prompts/${id}`, { method: 'DELETE' }),

  // Internship API
  getInternships: () => http<Internship[]>('/resume/internships/'),
  getInternship: (id: number) => http<Internship>(`/resume/internships/${id}`),
  createInternship: (data: InternshipCreate) => http<Internship>('/resume/internships/', { method: 'POST', body: JSON.stringify(data) }),
  updateInternship: (id: number, data: InternshipUpdate) => http<Internship>(`/resume/internships/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteInternship: (id: number) => http<void>(`/resume/internships/${id}`, { method: 'DELETE' }),

  // Project API
  getProjects: () => http<Project[]>('/resume/projects/'),
  getProject: (id: number) => http<Project>(`/resume/projects/${id}`),
  createProject: (data: ProjectCreate) => http<Project>('/resume/projects/', { method: 'POST', body: JSON.stringify(data) }),
  updateProject: (id: number, data: ProjectUpdate) => http<Project>(`/resume/projects/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteProject: (id: number) => http<void>(`/resume/projects/${id}`, { method: 'DELETE' }),

  // TechStack API
  getTechStacks: () => http<TechStack[]>('/resume/tech-stacks/'),
  getTechStack: (id: number) => http<TechStack>(`/resume/tech-stacks/${id}`),
  createTechStack: (data: TechStackCreate) => http<TechStack>('/resume/tech-stacks/', { method: 'POST', body: JSON.stringify(data) }),
  updateTechStack: (id: number, data: TechStackUpdate) => http<TechStack>(`/resume/tech-stacks/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteTechStack: (id: number) => http<void>(`/resume/tech-stacks/${id}`, { method: 'DELETE' }),

  // ResumePhoto API
  getResumePhotos: () => http<ResumePhoto[]>('/resume/photos/'),
  getResumePhoto: (id: number) => http<ResumePhoto>(`/resume/photos/${id}`),
  createResumePhoto: (data: ResumePhotoCreate) => http<ResumePhoto>('/resume/photos/', { method: 'POST', body: JSON.stringify(data) }),
  updateResumePhoto: (id: number, data: ResumePhotoUpdate) => http<ResumePhoto>(`/resume/photos/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteResumePhoto: (id: number) => http<void>(`/resume/photos/${id}`, { method: 'DELETE' }),
  uploadPhoto: async (formData: FormData) => {
    // 上传图片时不设置 Content-Type，让浏览器自动设置 boundary
    const res = await fetch(`/api/resume/photos/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    return (await res.json()) as { filenames: string[] };
  },

  // JobDescription API
  getJobDescriptions: () => http<JobDescription[]>('/resume/job-descriptions/'),
  getJobDescription: (id: number) => http<JobDescription>(`/resume/job-descriptions/${id}`),
  createJobDescription: (data: JobDescriptionCreate) => http<JobDescription>('/resume/job-descriptions/', { method: 'POST', body: JSON.stringify(data) }),
  updateJobDescription: (id: number, data: JobDescriptionUpdate) => http<JobDescription>(`/resume/job-descriptions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteJobDescription: (id: number) => http<void>(`/resume/job-descriptions/${id}`, { method: 'DELETE' }),
  uploadJdImage: async (formData: FormData) => {
    const res = await fetch(`/api/resume/job-descriptions/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    return (await res.json()) as { filenames: string[] };
  },

  // JdBreakdown API
  getJdBreakdowns: () => http<JdBreakdown[]>('/resume/jd-breakdowns/'),
  getJdBreakdownsByJd: (jdId: number) => http<JdBreakdown[]>(`/resume/jd-breakdowns/jd/${jdId}`),
  getJdBreakdown: (id: number) => http<JdBreakdown>(`/resume/jd-breakdowns/${id}`),
  createJdBreakdown: (data: JdBreakdownCreate) => http<JdBreakdown>('/resume/jd-breakdowns/', { method: 'POST', body: JSON.stringify(data) }),
  updateJdBreakdown: (id: number, data: JdBreakdownUpdate) => http<JdBreakdown>(`/resume/jd-breakdowns/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteJdBreakdown: (id: number) => http<void>(`/resume/jd-breakdowns/${id}`, { method: 'DELETE' }),
  analyzeJd: (jdId: number, systemPrompt?: string) => {
    return http<JdBreakdown>('/resume/jd-breakdowns/analyze', {
      method: 'POST',
      body: JSON.stringify({ jd_id: jdId, system_prompt: systemPrompt || null })
    });
  },
  analyzeJdStream: async (
    jdId: number, 
    systemPrompt: string | undefined,
    onChunk: (chunk: string) => void,
    onDone: (breakdownId: number) => void,
    onError: (error: string) => void
  ) => {
    try {
      const response = await fetch(`/api/resume/jd-breakdowns/analyze-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ jd_id: jdId, system_prompt: systemPrompt || null })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || response.statusText);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        for (let i = 0; i < lines.length - 1; i++) {
          const line = lines[i].trim();
          
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            
            if (dataStr === '[DONE]') {
              continue;
            }

            try {
              const data = JSON.parse(dataStr);
              
              if (data.error) {
                onError(data.error);
                return;
              }
              
              if (data.done && data.breakdown_id) {
                onDone(data.breakdown_id);
                return;
              }
              
              if (data.content) {
                onChunk(data.content);
              }
            } catch (e) {
              // 忽略JSON解析错误
              console.warn('Failed to parse SSE data:', dataStr);
            }
          }
        }
        
        buffer = lines[lines.length - 1];
      }
    } catch (e: any) {
      onError(e?.message || '流式请求失败');
    }
  },

  // OKR API
  getOkrs: () => http<OKR[]>('/okr/okrs/'),
  getOkr: (id: number) => http<OKR>(`/okr/okrs/${id}`),
  createOkr: (data: OKRCreate) => http<OKR>('/okr/okrs/', { method: 'POST', body: JSON.stringify(data) }),
  updateOkr: (id: number, data: OKRUpdate) => http<OKR>(`/okr/okrs/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  toggleOkr: (id: number, completed: boolean) => http<OKR>(`/okr/okrs/${id}/toggle`, { method: 'POST', body: JSON.stringify({ completed }) }),
  deleteOkr: (id: number) => http<void>(`/okr/okrs/${id}`, { method: 'DELETE' }),

  // Task API
  getTasksByOkr: (okrId: number) => http<Task[]>(`/okr/okrs/${okrId}/tasks/`),
  getTask: (id: number) => http<Task>(`/okr/tasks/${id}`),
  createTask: (data: TaskCreate) => http<Task>('/okr/tasks/', { method: 'POST', body: JSON.stringify(data) }),
  updateTask: (id: number, data: TaskUpdate) => http<Task>(`/okr/tasks/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  toggleTask: (id: number, completed: boolean) => http<Task>(`/okr/tasks/${id}/toggle`, { method: 'POST', body: JSON.stringify({ completed }) }),
  deleteTask: (id: number) => http<void>(`/okr/tasks/${id}`, { method: 'DELETE' }),

  // Interview API
  // Category API
  getInterviewCategories: () => http<InterviewCategory[]>('/interview/categories/'),
  getInterviewCategory: (id: number) => http<InterviewCategory>(`/interview/categories/${id}`),
  createInterviewCategory: (data: InterviewCategoryCreate) => http<InterviewCategory>('/interview/categories/', { method: 'POST', body: JSON.stringify(data) }),
  updateInterviewCategory: (id: number, data: InterviewCategoryUpdate) => http<InterviewCategory>(`/interview/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteInterviewCategory: (id: number) => http<void>(`/interview/categories/${id}`, { method: 'DELETE' }),

  // Question API
  getInterviewQuestions: (params?: { skip?: number; limit?: number; category_id?: number | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.category_id != null) query.set('category_id', String(params.category_id));
    const qs = query.toString();
    return http<InterviewQuestion[]>(`/interview/questions/${qs ? `?${qs}` : ''}`);
  },
  getInterviewQuestion: (id: number) => http<InterviewQuestion>(`/interview/questions/${id}`),
  createInterviewQuestion: (data: InterviewQuestionCreate) => http<InterviewQuestion>('/interview/questions/', { method: 'POST', body: JSON.stringify(data) }),
  updateInterviewQuestion: (id: number, data: InterviewQuestionUpdate) => http<InterviewQuestion>(`/interview/questions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteInterviewQuestion: (id: number) => http<void>(`/interview/questions/${id}`, { method: 'DELETE' }),

  // Answer API
  getInterviewAnswersByQuestion: (questionId: number) => http<InterviewAnswer[]>(`/interview/questions/${questionId}/answers/`),
  getInterviewAnswer: (id: number) => http<InterviewAnswer>(`/interview/answers/${id}`),
  createInterviewAnswer: (data: InterviewAnswerCreate) => http<InterviewAnswer>('/interview/answers/', { method: 'POST', body: JSON.stringify(data) }),
  updateInterviewAnswer: (id: number, data: InterviewAnswerUpdate) => http<InterviewAnswer>(`/interview/answers/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteInterviewAnswer: (id: number) => http<void>(`/interview/answers/${id}`, { method: 'DELETE' }),

  // Opinion API
  // Category API
  getOpinionCategories: () => http<OpinionCategory[]>('/opinion/categories/'),
  getOpinionCategory: (id: number) => http<OpinionCategory>(`/opinion/categories/${id}`),
  createOpinionCategory: (data: OpinionCategoryCreate) => http<OpinionCategory>('/opinion/categories/', { method: 'POST', body: JSON.stringify(data) }),
  updateOpinionCategory: (id: number, data: OpinionCategoryUpdate) => http<OpinionCategory>(`/opinion/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteOpinionCategory: (id: number) => http<void>(`/opinion/categories/${id}`, { method: 'DELETE' }),

  // Opinion API
  getOpinions: (params?: { skip?: number; limit?: number; category_id?: number | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.category_id != null) query.set('category_id', String(params.category_id));
    const qs = query.toString();
    return http<Opinion[]>(`/opinion/opinions/${qs ? `?${qs}` : ''}`);
  },
  getOpinion: (id: number) => http<Opinion>(`/opinion/opinions/${id}`),
  createOpinion: (data: OpinionCreate) => http<Opinion>('/opinion/opinions/', { method: 'POST', body: JSON.stringify(data) }),
  updateOpinion: (id: number, data: OpinionUpdate) => http<Opinion>(`/opinion/opinions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteOpinion: (id: number) => http<void>(`/opinion/opinions/${id}`, { method: 'DELETE' }),

  // Story API
  // Category API
  getStoryCategories: () => http<StoryCategory[]>('/story/categories/'),
  getStoryCategory: (id: number) => http<StoryCategory>(`/story/categories/${id}`),
  createStoryCategory: (data: StoryCategoryCreate) => http<StoryCategory>('/story/categories/', { method: 'POST', body: JSON.stringify(data) }),
  updateStoryCategory: (id: number, data: StoryCategoryUpdate) => http<StoryCategory>(`/story/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteStoryCategory: (id: number) => http<void>(`/story/categories/${id}`, { method: 'DELETE' }),

  // Story API
  getStories: (params?: { skip?: number; limit?: number; category_id?: number | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.category_id != null) query.set('category_id', String(params.category_id));
    const qs = query.toString();
    return http<Story[]>(`/story/stories/${qs ? `?${qs}` : ''}`);
  },
  getStory: (id: number) => http<Story>(`/story/stories/${id}`),
  createStory: (data: StoryCreate) => http<Story>('/story/stories/', { method: 'POST', body: JSON.stringify(data) }),
  updateStory: (id: number, data: StoryUpdate) => http<Story>(`/story/stories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteStory: (id: number) => http<void>(`/story/stories/${id}`, { method: 'DELETE' }),

  // Story Image Upload API
  uploadStoryImages: async (files: File[]): Promise<{ filenames: string[] }> => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    const res = await fetch(`/api/story/upload-images`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    return await res.json();
  },

  // AI Assistant API
  chat: async (messages: Array<{ role: string; content: string; image_urls?: string[] }>, stream: boolean = false, options?: { reasoning_effort?: string; temperature?: number; max_tokens?: number }) => {
    if (stream) {
      throw new Error('Use chatStream for streaming responses');
    }
    return http<{ content: string; reasoning_content: string }>('/assistant/chat', {
      method: 'POST',
      body: JSON.stringify({
        messages,
        stream: false,
        reasoning_effort: options?.reasoning_effort || 'medium',
        temperature: options?.temperature ?? 0.7,
        max_tokens: options?.max_tokens || null
      })
    });
  },
  chatStream: async (
    messages: Array<{ role: string; content: string; image_urls?: string[] }>,
    onChunk: (chunk: string) => void,
    onDone: () => void,
    onError: (error: string) => void,
    options?: { reasoning_effort?: string; temperature?: number; max_tokens?: number }
  ) => {
    try {
      const response = await fetch(`/api/assistant/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages,
          reasoning_effort: options?.reasoning_effort || 'medium',
          temperature: options?.temperature ?? 0.7,
          max_tokens: options?.max_tokens || null
        })
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || response.statusText);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        for (let i = 0; i < lines.length - 1; i++) {
          const line = lines[i].trim();
          
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            
            if (dataStr === '[DONE]') {
              continue;
            }

            try {
              const data = JSON.parse(dataStr);
              
              if (data.error) {
                onError(data.error);
                return;
              }
              
              if (data.done) {
                onDone();
                return;
              }
              
              if (data.content) {
                onChunk(data.content);
              }
            } catch (e) {
              // 忽略JSON解析错误
              console.warn('Failed to parse SSE data:', dataStr);
            }
          }
        }
        
        buffer = lines[lines.length - 1];
      }
    } catch (e: any) {
      onError(e?.message || '流式请求失败');
    }
  },
  uploadAssistantImage: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const res = await fetch(`/api/assistant/upload-image`, {
      method: 'POST',
      body: formData,
    });
    
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    
    return (await res.json()) as { filename: string; url: string };
  },

  // Chat History API
  saveChatHistory: (title: string | null, messages: Array<{ role: string; content: string; image_urls?: string[] }>) => {
    return http<{ id: number; title: string | null; created_at: string; updated_at: string }>('/assistant/history', {
      method: 'POST',
      body: JSON.stringify({ title, messages })
    });
  },
  getChatHistories: (params?: { skip?: number; limit?: number; q?: string | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.q) query.set('q', params.q);
    const qs = query.toString();
    return http<Array<{ id: number; title: string | null; created_at: string; updated_at: string }>>(`/assistant/history${qs ? `?${qs}` : ''}`);
  },
  getChatHistory: (id: number) => {
    return http<{ id: number; title: string | null; messages: Array<{ role: string; content: string; image_urls?: string[] }>; created_at: string; updated_at: string }>(`/assistant/history/${id}`);
  },
  updateChatHistory: (id: number, title: string | null, messages: Array<{ role: string; content: string; image_urls?: string[] }>) => {
    return http<{ id: number; title: string | null; created_at: string; updated_at: string }>(`/assistant/history/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title, messages })
    });
  },
  deleteChatHistory: (id: number) => {
    return http<{ success: boolean }>(`/assistant/history/${id}`, { method: 'DELETE' });
  },

  // Random Opinion API (筛子功能)
  getRandomOpinion: (categoryId?: number | null) => {
    const query = new URLSearchParams();
    if (categoryId != null) query.set('category_id', String(categoryId));
    const qs = query.toString();
    return http<{ id: number; description: string; category_id: number | null }>(`/assistant/random-opinion${qs ? `?${qs}` : ''}`);
  },

  // Like Record API (点赞功能)
  createLikeRecord: (question: string, answer: string) => {
    return http<{ id: number; question: string; answer: string; created_at: string }>('/assistant/likes/', {
      method: 'POST',
      body: JSON.stringify({ question, answer })
    });
  },
  getLikeRecords: (params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    const qs = query.toString();
    const url = `/assistant/likes/${qs ? `?${qs}` : ''}`;
    return http<Array<{ id: number; question: string; answer: string; created_at: string }>>(url);
  },
  getLikeRecord: (id: number) => {
    return http<{ id: number; question: string; answer: string; created_at: string }>(`/assistant/likes/${id}`);
  },
  deleteLikeRecord: (id: number) => {
    return http<{ success: boolean }>(`/assistant/likes/${id}`, { method: 'DELETE' });
  },

  // Algorithm Practice API
  // Categories
  getAlgoCategories: () => {
    return http<Array<{ id: number; name: string; order: number; created_at: string; updated_at: string }>>('/algo/categories/');
  },
  getAlgoCategory: (id: number) => {
    return http<{ id: number; name: string; order: number; created_at: string; updated_at: string }>(`/algo/categories/${id}`);
  },
  createAlgoCategory: (data: { name: string; order?: number }) => {
    return http<{ id: number; name: string; order: number; created_at: string; updated_at: string }>('/algo/categories/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },
  updateAlgoCategory: (id: number, data: { name?: string; order?: number }) => {
    return http<{ id: number; name: string; order: number; created_at: string; updated_at: string }>(`/algo/categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },
  deleteAlgoCategory: (id: number) => {
    return http<void>(`/algo/categories/${id}`, { method: 'DELETE' });
  },
  // Problems
  getAlgoProblems: (params?: { skip?: number; limit?: number; category_id?: number | null; difficulty?: string | null; status?: string | null; keyword?: string | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.category_id != null) query.set('category_id', String(params.category_id));
    if (params?.difficulty) query.set('difficulty', params.difficulty);
    if (params?.status) query.set('status', params.status);
    if (params?.keyword) query.set('keyword', params.keyword);
    const qs = query.toString();
    return http<AlgoProblem[]>(`/algo/problems/${qs ? `?${qs}` : ''}`);
  },
  getAlgoProblem: (id: number) => {
    return http<AlgoProblem>(`/algo/problems/${id}`);
  },
  createAlgoProblem: (data: AlgoProblemCreate) => {
    return http<AlgoProblem>('/algo/problems/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },
  updateAlgoProblem: (id: number, data: AlgoProblemUpdate) => {
    return http<AlgoProblem>(`/algo/problems/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },
  deleteAlgoProblem: (id: number) => {
    return http<void>(`/algo/problems/${id}`, { method: 'DELETE' });
  },

  // AlgoSolution API
  getAlgoSolutions: (problemId: number, params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    const qs = query.toString();
    return http<AlgoSolution[]>(`/algo/problems/${problemId}/solutions/${qs ? `?${qs}` : ''}`);
  },
  getAlgoSolution: (id: number) => http<AlgoSolution>(`/algo/solutions/${id}`),
  createAlgoSolution: (data: AlgoSolutionCreate) => http<AlgoSolution>('/algo/solutions/', { method: 'POST', body: JSON.stringify(data) }),
  updateAlgoSolution: (id: number, data: AlgoSolutionUpdate) => http<AlgoSolution>(`/algo/solutions/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteAlgoSolution: (id: number) => http<void>(`/algo/solutions/${id}`, { method: 'DELETE' }),

  // Timeline API
  // Topic API
  getTimelineTopics: (params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    const qs = query.toString();
    return http<TimelineTopic[]>(`/timeline/topics/${qs ? `?${qs}` : ''}`);
  },
  getTimelineTopic: (id: number) => http<TimelineTopic>(`/timeline/topics/${id}`),
  createTimelineTopic: (data: TimelineTopicCreate) => http<TimelineTopic>('/timeline/topics/', { method: 'POST', body: JSON.stringify(data) }),
  updateTimelineTopic: (id: number, data: TimelineTopicUpdate) => http<TimelineTopic>(`/timeline/topics/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteTimelineTopic: (id: number) => http<void>(`/timeline/topics/${id}`, { method: 'DELETE' }),

  // Entry API
  getTimelineEntries: (topicId: number, params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    query.set('topic_id', String(topicId));
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    const qs = query.toString();
    return http<TimelineEntry[]>(`/timeline/entries/${qs ? `?${qs}` : ''}`);
  },
  getTimelineEntry: (id: number) => http<TimelineEntry>(`/timeline/entries/${id}`),
  createTimelineEntry: (data: TimelineEntryCreate) => http<TimelineEntry>('/timeline/entries/', { method: 'POST', body: JSON.stringify(data) }),
  updateTimelineEntry: (id: number, data: TimelineEntryUpdate) => http<TimelineEntry>(`/timeline/entries/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteTimelineEntry: (id: number) => http<void>(`/timeline/entries/${id}`, { method: 'DELETE' }),

  // TimelineSubEntry API
  getTimelineSubEntries: (entryId: number, params?: { skip?: number; limit?: number }) => {
    const query = new URLSearchParams();
    query.set('entry_id', String(entryId));
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    const qs = query.toString();
    return http<TimelineSubEntry[]>(`/timeline/sub-entries/${qs ? `?${qs}` : ''}`);
  },
  getTimelineSubEntry: (id: number) => http<TimelineSubEntry>(`/timeline/sub-entries/${id}`),
  createTimelineSubEntry: (data: TimelineSubEntryCreate) => http<TimelineSubEntry>('/timeline/sub-entries/', { method: 'POST', body: JSON.stringify(data) }),
  updateTimelineSubEntry: (id: number, data: TimelineSubEntryUpdate) => http<TimelineSubEntry>(`/timeline/sub-entries/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteTimelineSubEntry: (id: number) => http<void>(`/timeline/sub-entries/${id}`, { method: 'DELETE' }),

  // Timeline Image Upload API
  uploadTimelineImages: async (files: File[]): Promise<{ filenames: string[] }> => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    const res = await fetch(`/api/timeline/upload-images`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    return await res.json();
  },
};
