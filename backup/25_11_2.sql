-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: prompt
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `internships`
--

DROP TABLE IF EXISTS `internships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_title` varchar(500) DEFAULT NULL,
  `company` varchar(500) NOT NULL,
  `position` varchar(500) NOT NULL,
  `start_date` varchar(50) NOT NULL,
  `end_date` varchar(50) DEFAULT NULL,
  `description` text,
  `skills` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_internships_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internships`
--

LOCK TABLES `internships` WRITE;
/*!40000 ALTER TABLE `internships` DISABLE KEYS */;
INSERT INTO `internships` VALUES (1,'小米科技有限责任公司                                             大语言模型算法工程师日常实习生 ','小米科技有限责任公司',' ','2025年4月','2025年8月22日','小米科技有限责任公司                                             大语言模型算法工程师日常实习生                                        2025年4月 - 2025年8月22日\n主导大模型技术在整车业务场景的研究与落地，聚焦智能体应用平台的维护与二次开发，结合 RAG、Agent、多模态、Text2SQL 等技术，赋能整车业务智能化升级。\n能力总结：\n大模型基座构建与应用: 具备私有化部署（如 DeepSeek-R1, Bge-m3）与高效运维经验，构建支持文本生成、语义理解、意图识别的高可用大模型基础服务。\n多模态交互系统开发: 整合语音识别 (SenseVoice, Whisper)、语音合成 (Spark-TTS, CosyVoice) 及音色识别 (Pyannote) 技术，成功构建支持会议转录、说话人分离、音色克隆的端到端多模态交互系统。\n垂域知识增强能力: 自研RAG+检索增强框架 ，准确率达95%+，支持多业务场景下的知识问答与语义匹配，显著提升知识库类应用的准确性和响应效率。\n定制化集成开发: 基于智能体平台进行深度定制开发，完成多Agent协同架构设计（遵循A2A协议），融合任务拆解、意图识别、工具调用（遵循MCP协议）及可视化模块，实现从自然语言到业务洞察的自动化流程。\n垂类项目成果：\n1. 天瞳智能取数助手 (Text2SQL + Text2API)\n核心技术:  主导设计了一套从自然语言到可视化图表的端到端多Agent协同架构，融合多Agent协同调度、意图识别、API自动调用、Text2SQL解析与图表自动可视化模块，并构建了汽车领域专有SQL规则库，提升Text2SQL的准确度。\n项目成果:  在deepseek-14B模型上，实现30秒内完成自然语言到数据图表转换，问答准确率90%+，显著提升整车数据分析效率。\n2. 企标信号智能解说员 (Agent + RAG)\n核心技术:  基于Agent+RAG技术，开发面向整车工程师的信号知识问答系统。主要工作包括：编写自动化知识库上传脚本，并构建融合查询改写与多维检索的增强型RAG框架，最终打通2000+个企标信号与业务场景。\n项目成果：问答准确率98%+，帮助非专业域工程师快速理解实车信号数据，效率提升20倍。\n3. 汽车领域智能会议生态工具（STT + TTS）\n核心技术:  主导研发覆盖“会议纪要”与“同声翻译”的多模态会议系统。核心工作包括私有化部署STT(SenseVoice)、TTS(Spark-TTS)及音色识别(pyannote)等核心引擎；开发基于GPU使用率的智能调度服务，将长音频转录效率最大化；研发支持随时打断、快速响应的语音交互助手，赋能实时同声翻译。\n项目成果:  3小时会议在6分钟内即可生成结构化纪要，准确率达95%，已在公司内部推广。\n4.智能体开发平台运维与开发\n核心技术与项目成果:  \n平台核心运维：负责大模型基座(DeepSeek, Bge-m3)的部署、维护与参数优化，并承担应用平台的深度定制。\n自动化与CI/CD：开发Bash自动化运维脚本(开启定时备份、修改环境变量、构建运行服务等)，并集成至CI/CD流程，提升部署与运维效率。\n高可用建设：开发自动化探活程序，实现平台异常与恢复的实时通知；设计并实现容器数据的持久化与实时备份机制；确保容器在异常时能够自动化重启，并支持断电后自动恢复，提升服务高可用。','','2025-10-26 15:13:27','2025-10-26 15:23:36'),(2,'成都迪孚数据处理有限责任公司                                  大模型应用开发工程师-项目负责人  ','成都迪孚数据处理有限责任公司','','2024年12月','2025年3月','成都迪孚数据处理有限责任公司                                  大模型应用开发工程师-项目负责人                                  2024年12月 - 2025年3月\n工作描述：负责搭建成都天府新区基于大模型的税务智能分析系统，赋能税务部门实现高效且精准的税务审核、税务知识库问答。\n系统架构：基于LangChain框架，本地化部署DeepSeek-32B/70B 和 Janus-7B/Qwen2.5-VL-7B 多模态大模型，结合提示词工程、思维链和RAG框架，提升模型在税务场景下的理解与推理能力。\n负责功能：1）风险应对报告合规性智能复核系统，实现对Word、Excel、PDF、图片等多种格式文档的自动化审核，识别日期格式错误上下文逻辑矛盾、税务数据计算偏差等异常。\n        2）全国税务政策分析报告生成系统，通过爬取政府网站的政策报告建立本地知识库，通过由粗到细的多轮生成方案，最终生成的分析报告字数可达15万+。\n        3）税务专业问答助手，建立知识库，包括相似案例、申报流程说明，可以为用户提供操作指南。','','2025-10-26 15:15:03','2025-10-26 15:29:00'),(3,'南京维伍网络科技有限公司                                                            前后端开发实习生      ','南京维伍网络科技有限公司','精简整理','2023年6月','2023年9月','南京维伍网络科技有限公司                                                            前后端开发实习生                                               2023年6月 - 2023年9月\n官方：https://cn.d5render.com、支付功能：https://www.d5render.cn/pricing \n工作描述：D5渲染器 是一款实时光线追踪渲染器软件，作为国产实时渲染器领跑者。在20版本发布时，主要负责搭建用户中心微服务、从单一购买升级为国内外订阅支付会员系统。\n亮点：       独立从0到1开发国内（支付宝）、国外（空中云汇）按月/按年订阅支付功能。系统能够稳健应对网络安全、定时任务失效等严重问题，稳定服务于全球160个国家用户订阅支付。\n涉及技术栈：SpringCloud微服务架构组件、Serverless部署引擎、基于Jenkins的CI/CD、xxl-job定时任务框架。','','2025-10-26 15:18:32','2025-10-26 16:26:39'),(4,'yocoto','易凯通医疗管理后台、易康护小程序后台','','',NULL,'易凯通医疗管理后台、易康护小程序后台\n2020年08月  - 2021年07月\n项⽬描述： 打造一款在公共场所提供医疗急救服务的设备，目前团队开发的医疗物品售卖货柜1.0 和 医疗急救柜2.0 已在校园运营。\n负责模块：\n易凯通医疗管理后台：负责运营数据可视化、货柜管理、商品管理功能模块。\n易康护⼩程序后台：负责货物⽀付功能、⼀件呼救功能、查找附近的急救物品功能。\n涉及知识：SpringBoot框架、采⽤SpingSecurity+JWT作为⽹关、MQTT通信、Mysql、Redis、Websocket通信、微信⽀付。\n项目收获：能在团队的指导下独立完成后端某个模块的设计、开发工作，基本了解网站的整个开发规范及流程，专业技术能力在实践中得到提升。','','2025-10-26 15:19:32','2025-10-26 15:28:54'),(6,'南京维伍网络科技有限公司                                                            前后端开发实习生      ','D5 渲染器','实习完重构整理','','','D5 渲染器\n担任角色：后端开发实习生 公司：南京维伍网络科技有限公司\n2021年07月  - 2021年12月\n项⽬描述： ⼀款三维实时渲染客户端软件, 在项目中负责搭建用户中心微服务和开发订阅支付功能。https://cn.d5render.com/\n负责模块\n重新设计用户登录注册逻辑。\n设计开发国内(⽀付宝)、国外(空中云汇) 按⽉、按年软件订阅支付功能。\n由于⽀付⼯作审核需要, 负责基于uni-app开发⼀款D5 Render官⽅App,包括软件介绍和⽤户信息板块。\n涉及技术： 阿里云Serverless应用引擎、Jenkins、Docker、定时任务框架xxl-job。\n项目收获：自主开发能力、逻辑思维能力、阅读英文技术文档能力、团队协调配合能力得到极大提高，对未来的方向更加清晰，对应对未来的挑战充满信心和勇气。','','2025-10-26 15:30:01','2025-10-26 16:27:08'),(7,'南京维伍网络科技有限公司                                                            前后端开发实习生      ','D5 渲染器   后端Java工程师','实习完整理','','','D5 渲染器   后端Java工程师    2021.7 - 2021.10\n项目描述: 一款三维实时渲染客户端软件, 在其中负责整个生态的后台服务 https://cn.d5render.com/\nD5 web官方网站, 独立设计开发国内(支付宝)、国外(空中云汇) 按月、按年订阅系统.\nD5 user, 重构整个用户中心登陆、注册逻辑.\nD5 render, 负责客户端所需的接口.\n由于支付工作审核需要, 基于uni-app开发一款D5 Render官方App,包括软件介绍和用户中心\n 整个模块上线后运行稳健, 订阅系统精确扣费续时, 支撑着全球用户订购使用.\n技术栈: Spring Cloud Alibaba、阿里云Serveless服务、Docker、Jenkins、xxl-job……','','2025-10-26 16:25:24','2025-10-26 16:26:23'),(8,'南京维伍网络科技有限公司                                                            前后端开发实习生      ','实习时间：2021.7 - 2021-10','实习完精简整理','Java开发实习生','','实习时间：2021.7 - 2021-10        工作单位：南京维伍网络科技有限公司    Java开发实习生\n工作内容：\n参与公司后端系统重构工作,从原先单体应用像微服务架构演变.\n负责用户中心服务、官网订阅支付整个模块.','','2025-10-26 16:27:35','2025-10-26 16:27:35'),(9,'yocoto','易凯通管理平台、易凯通YOCOTO康护小程序平台','实习完整理','2020.9','至今','易凯通管理平台、易凯通YOCOTO康护小程序平台        后端工程师        2020.9 - 至今\n项目描述： 用于打造健康医疗急救系统，货柜已在校园投产运营\n易凯通管理平台：包括运营数据可视化、货柜管理、商品管理、文章视频管理等模块\n易凯通YOCOTO康护小程序平台：货物支付功能、一件呼救功能、查找附近的急救物品等模块\n技术栈：SpringBoot搭建、采用SpingSecurity+JWT作为网关、MQTT通信、Mysql、Redis、Websocket…\n第三方服务：微信登录、微信支付、阿里云OSS对象存储、墨迹天气等','','2025-10-26 16:28:15','2025-10-26 16:28:15');
/*!40000 ALTER TABLE `internships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_answers`
--

DROP TABLE IF EXISTS `interview_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interview_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_interview_answers_question_id` (`question_id`),
  KEY `ix_interview_answers_id` (`id`),
  CONSTRAINT `interview_answers_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `interview_questions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_answers`
--

LOCK TABLES `interview_answers` WRITE;
/*!40000 ALTER TABLE `interview_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `interview_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_categories`
--

DROP TABLE IF EXISTS `interview_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interview_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `order` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_interview_categories_name` (`name`),
  KEY `ix_interview_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_categories`
--

LOCK TABLES `interview_categories` WRITE;
/*!40000 ALTER TABLE `interview_categories` DISABLE KEYS */;
INSERT INTO `interview_categories` VALUES (1,'深度学习',1,'2025-10-31 16:58:54','2025-10-31 16:58:54'),(2,'大模型',2,'2025-10-31 17:00:10','2025-10-31 17:00:10');
/*!40000 ALTER TABLE `interview_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview_questions`
--

DROP TABLE IF EXISTS `interview_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interview_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `category_id` int DEFAULT NULL,
  `company` varchar(200) DEFAULT NULL,
  `tags` varchar(500) DEFAULT NULL,
  `difficulty` varchar(20) NOT NULL,
  `round` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_interview_questions_id` (`id`),
  KEY `ix_interview_questions_category_id` (`category_id`),
  CONSTRAINT `interview_questions_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `interview_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview_questions`
--

LOCK TABLES `interview_questions` WRITE;
/*!40000 ALTER TABLE `interview_questions` DISABLE KEYS */;
INSERT INTO `interview_questions` VALUES (1,'你了解知识图谱吗',1,'','','中等','','2025-10-31 16:59:02','2025-10-31 16:59:02'),(2,'你了解目标检测吗',1,'','','中等','','2025-10-31 16:59:12','2025-10-31 16:59:12'),(3,'你了解Yolo算法吗',1,'','','中等','','2025-10-31 16:59:17','2025-10-31 16:59:17'),(4,'你了解图像滤波算法吗',1,'','','中等','','2025-10-31 16:59:22','2025-10-31 16:59:22'),(5,'你了解大模型技术吗',1,'','','中等','','2025-10-31 16:59:31','2025-10-31 16:59:31'),(6,'RAG向量检索算法有哪些',2,'','','中等','','2025-10-31 17:00:34','2025-10-31 17:00:34');
/*!40000 ALTER TABLE `interview_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jd_breakdowns`
--

DROP TABLE IF EXISTS `jd_breakdowns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jd_breakdowns` (
  `id` int NOT NULL AUTO_INCREMENT,
  `jd_id` int NOT NULL,
  `company` varchar(500) NOT NULL,
  `position` varchar(500) NOT NULL,
  `breakdown_content` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_jd_breakdowns_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jd_breakdowns`
--

LOCK TABLES `jd_breakdowns` WRITE;
/*!40000 ALTER TABLE `jd_breakdowns` DISABLE KEYS */;
INSERT INTO `jd_breakdowns` VALUES (2,3,'阶跃星辰','大模型算法工程师【实习】','以下是对该岗位JD的详细分析：\n\n## 岗位职责分析\n**核心职责：**\n1. **算法需求理解与方案设计** - 在真实产品中理解算法需求，进行问题拆解和解决方案设计\n2. **模型评测与优化** - 建立评测体系，通过提示词工程和模型训练算法进行快速调优\n3. **智能体系统构建** - 设计并构建智能体/toolcall方案，弥补单一模型的能力局限\n\n**重要性和优先级：**\n- **高优先级**：算法方案设计和模型优化调优，直接影响产品效果\n- **中等优先级**：智能体系统构建，属于能力扩展和系统完善\n\n**关键能力要求：**\n- 产品思维和需求理解能力\n- 算法设计和优化能力\n- 系统架构设计能力\n- 实验分析和问题解决能力\n\n## 岗位要求分析\n**技能要求：**\n- **编程语言**：熟练掌握Python\n- **算法基础**：扎实的算法基础，熟悉大语言模型/多模态模型算法架构\n- **核心技术**：熟悉instructGPT、LLaMA等主流架构\n- **对齐技术**：熟悉SFT、DPO、PPO、Self-Rewarding、Self-Critic等Alignment方法\n\n**学历和经验要求：**\n- 未明确要求具体学历，但强调计算机/数学基础和算法基础\n- 需要具备实际项目经验，特别是在真实产品环境中的经验\n\n**软技能要求：**\n- 创新思维和问题解决能力\n- 良好的沟通能力\n- 团队协作能力\n- 实验分析能力\n\n## 加分项分析\n**额外加分项目：**\n- 相关领域论文发表\n- 竞赛获奖经历\n- 丰富的项目经历\n\n**匹配度提升评估：**\n- **高价值**：论文发表和丰富项目经历，直接证明技术深度和实践能力\n- **中等价值**：竞赛获奖，体现算法能力和竞争意识\n\n## 岗位评估\n**岗位难度评估：** ⭐⭐⭐⭐⭐（5星）\n- 要求深入理解大语言模型和Alignment技术，技术门槛较高\n- 需要在真实产品环境中解决问题，对实践能力要求高\n\n**待遇可能的行业水平：**\n- 预计年薪范围：40-80万（根据经验和能力）\n- 属于AI算法工程师中的高阶岗位\n\n**适合的候选人类别：**\n- 有2-5年大模型相关经验的算法工程师\n- 对Alignment技术有深入研究的技术专家\n- 具备产品思维和工程实践能力的AI研究员\n\n## 匹配建议\n**简历准备建议：**\n1. **突出项目经历**：详细描述参与的大模型相关项目，特别是产品化项目\n2. **技术深度展示**：重点体现对LLaMA、instructGPT等架构的理解\n3. **Alignment技术经验**：明确列出SFT、DPO等技术的实际应用经验\n\n**需要强调的技能：**\n- Python编程能力和代码规范\n- 大模型架构理解深度\n- Alignment技术的实践应用\n- 实验分析和优化能力\n\n**可能的面试重点：**\n1. **技术深度**：对大模型架构和Alignment原理的理解\n2. **实践能力**：在真实项目中的问题解决经验\n3. **系统设计**：智能体系统架构设计能力\n4. **创新思维**：对新方法和技术的理解和应用\n\n**建议准备方向：**\n- 复习大模型主流架构的技术细节\n- 准备Alignment技术的实际应用案例\n- 梳理项目经历中的技术难点和解决方案\n- 练习系统设计和技术方案阐述能力','2025-10-29 15:12:02','2025-10-29 15:12:02'),(3,3,'阶跃星辰','大模型算法工程师【实习】','## 岗位讲解\n\n### 岗位定位\n这是一个**AI算法工程师-大模型方向**的岗位。该岗位在公司中扮演技术核心角色，负责将前沿的大语言模型技术落地到实际产品中，通过算法优化提升产品智能化水平。\n\n### 工作内容\n- **需求分析**：深入理解产品需求，将业务问题转化为可解决的算法问题\n- **模型优化**：通过提示词工程、模型训练等方式持续提升模型性能\n- **系统集成**：设计智能体和工具调用方案，构建完整的AI应用系统\n- **质量评估**：建立评测体系，量化评估模型效果并持续迭代\n\n### 工作意义\n这是AI领域当前最热门的方向之一，直接参与大模型产品的研发和优化。未来可以向AI算法专家、技术负责人等方向发展，职业天花板高。\n\n### 适合人群\n- 技术背景：计算机/数学基础扎实，熟悉Python和深度学习\n- 性格特点：逻辑思维强，善于分析问题，有创新意识，团队协作好\n- 学习能力：能够快速跟进AI领域最新技术发展\n\n## 岗位职责分析\n\n### 核心职责\n1. **算法需求分析与方案设计**\n   - 将产品需求转化为具体算法问题\n   - 设计可行的技术解决方案\n\n2. **模型调优与评测**\n   - 建立模型评估标准和方法\n   - 通过提示词工程和训练算法优化模型\n\n3. **智能体系统构建**\n   - 设计智能体架构和工具调用机制\n   - 整合多种技术方案提升系统能力\n\n### 职责优先级\n- **最高优先级**：模型调优与评测（直接决定产品效果）\n- **次重要**：算法需求分析（影响技术方案正确性）\n- **基础要求**：智能体系统构建（需要前两者支撑）\n\n### 能力要求\n- 技术转化能力：业务需求→技术方案\n- 算法优化能力：模型调优、效果提升\n- 系统设计能力：架构设计、模块整合\n- 实验分析能力：数据驱动、效果评估\n\n## 岗位要求分析\n\n### 硬技能要求\n**编程语言**\n- **必需**：Python（熟练掌握，良好编程习惯）\n- **加分**：C++、Rust（高性能计算场景）\n\n**框架和工具**\n- **深度学习框架**：PyTorch（必需）、TensorFlow\n- **大模型工具**：Hugging Face、vLLM、LangChain\n- **实验管理**：MLflow、Weights & Biases\n\n**技术栈深度要求**\n- **大模型架构**：instructGPT、LLaMA等主流架构（深入理解）\n- **对齐算法**：SFT、DPO、PPO、Self-Rewarding、Self-Critic（熟练掌握）\n- **多模态模型**：理解视觉-语言联合建模原理\n\n### 软技能要求\n- **沟通协作**：与产品、工程团队高效合作\n- **问题解决**：复杂算法问题的分析解决能力\n- **创新思维**：提出新的技术方案和优化思路\n- **学习能力**：快速掌握AI领域最新技术\n\n### 学历和经验要求\n- **学历**：计算机/数学相关专业本科及以上（硕士优先）\n- **经验**：1-3年AI算法相关经验（应届生需有突出项目）\n- **项目经验**：大模型相关项目经历（必需）\n\n## 需要学习什么\n\n### 必须掌握的技能（优先级：高）\n\n**1. Python深度学习编程**\n- **为什么需要**：所有算法实现的基础工具\n- **掌握程度**：熟练使用PyTorch，理解自动求导、模型训练流程\n- **学习资源**：\n  - 《Python深度学习》（François Chollet）\n  - PyTorch官方教程\n  - Kaggle深度学习课程\n\n**2. 大模型核心算法**\n- **为什么需要**：岗位要求明确提到instructGPT、LLaMA架构\n- **掌握程度**：理解Transformer架构，掌握预训练、微调流程\n- **学习资源**：\n  - 《自然语言处理实战》（Hobson Lane）\n  - Hugging Face Transformers课程\n  - 论文精读：Attention is All You Need、LLaMA论文\n\n**3. 对齐算法技术**\n- **为什么需要**：职责中模型调优的核心技术\n- **掌握程度**：掌握SFT、DPO、PPO原理和实现\n- **学习资源**：\n  - 论文：Training language models to follow instructions、Direct Preference Optimization\n  - 开源项目：TRL、DeepSpeed-Chat\n  - 博客：Lil\'Log、Sebastian Raschka博客\n\n### 建议学习的技能（优先级：中）\n\n**1. 提示词工程**\n- **学习理由**：快速提升模型效果的重要手段\n- **快速上手**：学习Prompt Engineering Guide，实践CoT、Few-shot等技术\n\n**2. 智能体系统设计**\n- **学习理由**：构建完整AI应用的关键能力\n- **快速上手**：学习LangChain、AutoGPT等框架，构建简单智能体\n\n**3. 实验分析方法**\n- **学习理由**：科学评估模型效果的基础\n- **快速上手**：学习AB测试、统计显著性检验方法\n\n### 加分技能（优先级：低）\n\n- **多模态模型**：CLIP、BLIP等模型原理\n- **模型压缩**：量化、剪枝、蒸馏技术\n- **高性能计算**：CUDA编程、模型并行\n\n### 学习路径建议\n\n**第一阶段（1-2个月）：基础巩固**\n1. 深度学习基础（PyTorch熟练使用）\n2. Transformer架构深入理解\n3. 完成一个文本分类或生成项目\n\n**第二阶段（2-3个月）：核心技术**\n1. 大模型预训练和微调实践\n2. 对齐算法代码实现\n3. 构建完整的对话系统项目\n\n**第三阶段（持续）：深度优化**\n1. 参与开源项目或竞赛\n2. 论文复现和算法改进\n3. 技术博客写作和分享\n\n## 岗位评估\n\n### 岗位难度：⭐⭐⭐⭐⭐（5星）\n- **技术深度**：需要深入理解大模型最新技术\n- **实践要求**：强调真实项目中的算法落地能力\n- **创新要求**：需要持续的技术创新和优化\n\n### 匹配难度\n- **技术差距**：缺少大模型实战经验需要3-6个月系统学习\n- **项目经验**：需要完成1-2个完整的大模型项目\n- **理论深度**：需要补足对齐算法等理论知识\n\n### 待遇水平\n- **初级**：25-40k/月（1-3年经验）\n- **中级**：40-60k/月（3-5年经验）\n- **高级**：60k+/月（5年以上经验）\n\n### 发展前景\n- **短期**：AI算法工程师、大模型研发工程师\n- **中期**：技术专家、算法团队负责人\n- **长期**：AI架构师、技术总监\n\n## 匹配建议\n\n### 简历准备\n- **技能突出**：将大模型技术、对齐算法放在技能栏首位\n- **项目描述**：使用STAR法则描述项目，突出技术难点和解决方案\n- **弥补不足**：通过开源项目贡献、技术博客展示学习能力\n\n### 面试准备\n**技术问题可能包括：**\n- Transformer架构细节和优化\n- 各种对齐算法的对比和适用场景\n- 实际业务问题的算法解决方案设计\n- 模型效果评估和优化方法\n\n**需要准备的内容：**\n- 算法原理白板推导\n- 代码实现能力展示\n- 项目经验深度讲解\n\n## 行动清单\n\n### 立即开始（第1周）\n1. **技术栈梳理**：评估当前技能与大模型要求的差距\n2. **学习计划**：制定3个月的系统学习计划\n3. **环境搭建**：配置PyTorch、Hugging Face开发环境\n\n### 短期目标（1-2个月）\n1. **基础项目**：完成基于Hugging Face的文本生成项目\n2. **算法理解**：掌握SFT、DPO等对齐算法原理\n3. **代码实践**：复现简单的对齐算法代码\n\n### 中期目标（2-4个月）\n1. **完整项目**：构建端到端的对话系统\n2. **性能优化**：实践模型调优和提示词工程\n3. **知识输出**：撰写技术博客或参与开源项目\n\n### 验证方式\n- **代码能力**：GitHub项目获得star或fork\n- **理论知识**：通过技术面试问题测试\n- **实践能力**：完成具有完整文档的项目\n\n**建议时间投入**：每天3-4小时系统学习，周末进行项目实践','2025-10-29 15:58:00','2025-10-29 15:58:00'),(5,3,'阶跃星辰','大模型算法工程师【实习】','## 逐句解释\n\n### 第1段：岗位职责\n\n**原句**：在真实产品项目中理解算法需求，拆解问题，并设计对应的解决方案；\n\n**详细解释**：\n- 这句话要求候选人能够将理论知识应用到实际产品开发中，理解业务场景对算法的具体需求\n- 需要具备问题分析和拆解能力，能够将复杂的实际问题分解为可执行的算法任务\n- 要求具备解决方案设计能力，能够针对具体问题设计合适的算法方案\n- 隐含要求候选人需要有实际项目经验，不能只停留在理论层面\n\n**原句**：建立评测体系，通过提示词、模型训练算法进行快速调优；\n\n**详细解释**：\n- 这句话要求候选人具备算法效果评估能力，能够建立科学的评价指标和测试体系\n- 需要掌握提示词工程技巧，能够通过优化提示词来提升模型表现\n- 要求熟悉模型训练调优方法，能够快速迭代优化模型性能\n- 隐含要求候选人需要具备工程实践能力，能够高效完成模型优化工作\n\n**原句**：设计并构建智能体 /toolcall 方案，补足单模型能力。\n\n**详细解释**：\n- 这句话要求候选人具备智能体系统设计能力，能够构建多组件协作的AI系统\n- 需要掌握工具调用（toolcall）技术，让AI模型能够使用外部工具和API\n- 要求能够设计系统方案来弥补单一模型的局限性，实现更复杂的功能\n- 隐含要求候选人需要具备系统架构思维，能够整合多种技术方案\n\n### 第2段：岗位要求\n\n**原句**：具有良好的计算机 / 数学基础，熟练掌握 Python，有良好的编程习惯和代码风格；\n\n**详细解释**：\n- 这句话要求候选人具备扎实的计算机科学和数学理论知识基础\n- 需要精通Python编程语言，这是AI领域最主流的开发语言\n- 强调代码质量和可维护性，要求编写规范、清晰的代码\n- 隐含要求候选人不仅要有技术能力，还要有工程化思维\n\n**原句**：具备扎实的算法基础，熟悉大语言 / 多模态模型的算法架构，包括 instructGPT，LLaMA 等主流架构算法；\n\n**详细解释**：\n- 这句话要求候选人深入理解深度学习和大模型的核心算法原理\n- 需要熟悉主流大语言模型和多模态模型的架构设计\n- 特别提到instructGPT和LLaMA，说明公司可能正在使用或基于这些模型开发\n- 隐含要求候选人要紧跟技术发展，了解行业主流技术方案\n\n**原句**：熟悉 Alignment 领域的常用方法，包括但不限于 SFT、DPO、PPO、Self-Rewarding 和 Self-Critic 等；\n\n**详细解释**：\n- 这句话要求候选人熟悉模型对齐（Alignment）技术，这是让AI模型更符合人类价值观的关键技术\n- 需要掌握监督微调（SFT）、直接偏好优化（DPO）、近端策略优化（PPO）等具体方法\n- 要求了解前沿的自奖励（Self-Rewarding）和自评判（Self-Critic）技术\n- 隐含要求候选人需要在模型调优和价值观对齐方面有实践经验\n\n**原句**：具备卓越的实验分析与问题解决能力，有创新思维，能够良好沟通，与团队成员高效协作。\n\n**详细解释**：\n- 这句话要求候选人具备强大的实验设计和结果分析能力\n- 需要优秀的问题解决能力和创新思维，能够提出新的解决方案\n- 强调沟通协作能力，说明这是团队合作项目\n- 隐含要求候选人需要具备软技能，能够在团队环境中有效工作\n\n### 第3段：加分项\n\n**原句**：在上述相关领域有论文发表，有竞赛获奖经历，有丰富的项目经历。\n\n**详细解释**：\n- 这句话希望候选人在AI领域有学术研究成果，论文发表是重要加分项\n- 竞赛获奖经历可以证明候选人的技术实力和竞争能力\n- 丰富的项目经历表明候选人具备实践经验，能够快速上手\n- 隐含要求候选人不仅满足基本要求，还要有突出的成就和经历\n\n## 总结归纳\n\n### 核心技能要求\n1. **技术基础**：扎实的计算机/数学基础，精通Python编程\n2. **算法能力**：深入理解大语言模型、多模态模型算法架构\n3. **专业领域**：熟悉模型对齐技术（SFT、DPO、PPO等）\n4. **工程实践**：具备实际项目开发、模型调优、系统构建能力\n\n### 关键能力\n1. **问题解决能力**：从需求理解到方案设计的全流程能力\n2. **实验分析能力**：建立评测体系，进行模型调优和效果评估\n3. **系统设计能力**：智能体系统、工具调用方案设计\n4. **创新思维**：提出新的解决方案和技术思路\n\n### 隐含额外要求\n1. **学术背景**：有论文发表或竞赛经历者优先\n2. **实践经验**：丰富的真实项目经验，能够快速产出成果\n3. **团队协作**：良好的沟通能力和团队合作精神\n4. **技术视野**：了解行业主流技术和前沿发展方向','2025-10-29 16:08:55','2025-10-29 16:08:55'),(7,6,'遂原科技','AI 框架开发工程师','我将按照要求逐句分析这份JD，使用Markdown格式进行详细解释。\n\n## 逐句解释\n\n### 第1段：标签\n\n**原句**：标签：CUDA、机器学习、MATLAB、GPU、模型加速 / 性能优化\n\n**详细解释**：\n- **CUDA**：要求候选人具备NVIDIA GPU并行计算编程能力，能够使用CUDA进行GPU程序开发\n- **机器学习**：需要掌握机器学习相关理论和实践\n- **MATLAB**：可能需要使用MATLAB进行算法原型验证或数值计算\n- **GPU**：强调GPU计算相关经验，包括GPU架构理解和GPU编程\n- **模型加速/性能优化**：核心工作方向，专注于AI模型的性能提升和加速技术\n\n### 第2段：岗位职责概述\n\n**原句**：负责云端 AI 芯片 AI 框架，SDK 和算子编程模型的开发和集成，具体包括以下一到多项：\n\n**详细解释**：\n- 这是一个系统级开发岗位，涉及AI框架、SDK和算子编程模型三个层次\n- \"云端AI芯片\"表明工作针对服务器端AI加速芯片，不是移动端或边缘端\n- \"开发和集成\"意味着既要做底层开发，也要做系统集成工作\n- \"一到多项\"说明可以根据候选人专长分配不同方向的工作\n\n### 第3段：职责项1\n\n**原句**：扩展 Tensorflow/Caffe/PyTorch 等 AI 框架的后端，实现对新云端 AI 计算设备的支持；\n\n**详细解释**：\n- 需要深入理解主流AI框架的架构，特别是后端执行机制\n- 要求具备将新硬件（云端AI计算设备）集成到现有AI框架中的能力\n- 实际工作可能涉及编写设备插件、运行时库或编译器后端\n- 隐含要求：熟悉AI框架的扩展机制和硬件抽象层\n\n### 第4段：职责项2\n\n**原句**：分析和优化 AI 框架的性能；\n\n**详细解释**：\n- 需要具备性能分析和调优能力，能够识别性能瓶颈\n- 要求掌握性能分析工具的使用（如profiler、tracer等）\n- 实际工作：性能测试、瓶颈分析、优化方案实施\n- 隐含要求：对计算机体系结构有深入理解，能够从系统角度分析性能\n\n### 第5段：职责项3\n\n**原句**：针对云端 AI 计算设备，设计和调优 AI 框架图级别调度和融合等算法优化；\n\n**详细解释**：\n- 涉及计算图优化技术，包括算子融合、调度策略等\n- 需要掌握图算法和编译器优化技术\n- 实际工作：设计图优化pass，实现计算图到硬件的高效映射\n- 隐含要求：熟悉编译器原理和计算图优化理论\n\n### 第6段：职责项4\n\n**原句**：AI 框架 AOT/JIT 编译功能支持，动态图和静态图的支持；\n\n**详细解释**：\n- AOT（Ahead-of-Time）和JIT（Just-in-Time）是两种重要的编译模式\n- 需要支持动态图和静态图两种执行模式\n- 实际工作：编译器开发、运行时系统开发\n- 隐含要求：熟悉编译器设计和运行时系统原理\n\n### 第7段：职责项5\n\n**原句**：模型量化 / 模型压缩的 AI 框架级别支持\n\n**详细解释**：\n- 需要实现模型量化（如INT8、FP16）和压缩（如剪枝、蒸馏）的框架支持\n- 要求熟悉模型优化技术及其在框架中的集成方式\n- 实际工作：开发量化工具链、集成压缩算法\n- 隐含要求：了解模型精度与性能的平衡\n\n### 第8段：职责项6\n\n**原句**：算子编程模型支持和自动调优\n\n**详细解释**：\n- 需要设计和实现算子编程模型（如CUDA、OpenCL等）\n- 自动调优要求开发自动性能优化系统\n- 实际工作：算子开发、自动调优算法实现\n- 隐含要求：熟悉自动机器学习（AutoML）和搜索优化算法\n\n### 第9段：职责项7\n\n**原句**：SDK 生态化接口搭建和维护\n\n**详细解释**：\n- 需要构建易用的软件开发工具包\n- 关注生态建设，确保SDK的易用性和兼容性\n- 实际工作：API设计、文档编写、用户支持\n- 隐含要求：具备产品思维和用户视角\n\n### 第10段：基本要求1\n\n**原句**：计算机或软件相关学科本科毕业；\n\n**详细解释**：\n- 学历要求：本科及以上\n- 专业要求：计算机科学、软件工程等相关专业\n- 隐含要求：具备扎实的计算机基础理论知识\n\n### 第11段：基本要求2\n\n**原句**：理解 AI 框架应用及常见的云端 AI 模型；\n\n**详细解释**：\n- 需要熟悉AI框架的使用和原理\n- 了解常见的AI模型（如CNN、RNN、Transformer等）\n- 隐含要求：有实际的AI应用开发经验\n\n### 第12段：基本要求3\n\n**原句**：理解掌握图编译原理，熟悉 AI 框架主要流程；\n\n**详细解释**：\n- 必须掌握编译器原理，特别是图编译器技术\n- 熟悉AI框架从模型定义到执行的全流程\n- 隐含要求：有编译器或AI框架底层开发经验\n\n### 第13段：基本要求4\n\n**原句**：熟练掌握 C/C++，熟悉 Python 编程；\n\n**详细解释**：\n- C/C++是核心开发语言，要求精通\n- Python是脚本和原型开发语言，要求熟练使用\n- 隐含要求：具备系统级编程和快速原型开发能力\n\n### 第14段：基本要求5\n\n**原句**：熟悉软件开发工具和脚本语言（如 git, CMake, Bazel, bash 等）；\n\n**详细解释**：\n- 版本控制：git\n- 构建工具：CMake、Bazel\n- 脚本语言：bash等\n- 隐含要求：具备规范的软件开发习惯和工程能力\n\n### 第15段：基本要求6\n\n**原句**：熟悉软件开发、发布和管理流程（如敏捷开发，缺陷管理，CI/CD 概念等）；\n\n**详细解释**：\n- 开发方法论：敏捷开发\n- 质量管理：缺陷管理\n- 自动化流程：CI/CD\n- 隐含要求：具备团队协作和工程管理意识\n\n### 第16段：加分项1\n\n**原句**：计算机科学或电气工程学硕士毕业或三年以上相关工作经验；\n\n**详细解释**：\n- 优先考虑硕士学历或丰富经验者\n- 相关专业扩展到电气工程（可能涉及硬件相关）\n- 隐含要求：更深入的专业知识或实践经验\n\n### 第17段：加分项2\n\n**原句**：深度学习、机器学习相关工作经验\n\n**详细解释**：\n- 优先考虑有AI算法开发经验者\n- 隐含要求：理解算法原理，能更好地优化框架\n\n### 第18段：加分项3\n\n**原句**：GPU 驱动或应用（CUDA 和 cuDNN 库）开发经验；\n\n**详细解释**：\n- 需要GPU编程经验，特别是CUDA和cuDNN\n- 可能涉及驱动开发，要求底层硬件知识\n- 隐含要求：熟悉GPU架构和并行计算\n\n### 第19段：加分项4\n\n**原句**：MLIR/LLVM 相关开发经验；\n\n**详细解释**：\n- MLIR和LLVM是现代编译器基础设施\n- 需要编译器开发经验\n- 隐含要求：熟悉现代编译器技术和中间表示\n\n### 第20段：加分项5\n\n**原句**：Pytorch，Tensorflow，Mindspore，Paddlepaddle 等任一种或几种框架对接后端硬件经验\n\n**详细解释**：\n- 需要实际的AI框架硬件后端开发经验\n- 熟悉至少一个主流AI框架的架构\n- 隐含要求：有完整的框架-硬件集成经验\n\n### 第21段：加分项6\n\n**原句**：有分布式大模型训练或推理经验者佳\n\n**详细解释**：\n- 需要分布式系统经验\n- 熟悉大模型训练和推理技术\n- 隐含要求：具备大规模系统开发和优化能力\n\n## 总结归纳\n\n### 核心技能要求\n1. **编程语言**：精通C/C++，熟练Python\n2. **AI框架**：熟悉TensorFlow/PyTorch等主流框架架构\n3. **编译器技术**：图编译、MLIR/LLVM、AOT/JIT编译\n4. **硬件知识**：GPU编程（CUDA）、AI芯片架构\n5. **性能优化**：模型加速、算子优化、图级别优化\n\n### 关键能力\n1. **系统架构能力**：AI框架、SDK、算子模型的全栈开发\n2. **性能分析能力**：瓶颈识别、优化方案设计实施\n3. **编译器开发能力**：图优化、代码生成、运行时系统\n4. **工程实践能力**：工具链使用、开发流程规范\n\n### 隐含额外要求\n1. **学术背景**：扎实的计算机科学理论基础\n2. **产品思维**：SDK易用性和生态建设意识\n3. **硬件理解**：从软件角度理解硬件特性并进行优化\n4. **大规模系统经验**：分布式训练、大模型处理能力\n\n这是一个面向AI基础设施开发的高阶技术岗位，要求候选人具备从算法到硬件、从理论到工程的全方位能力。','2025-10-29 22:50:04','2025-10-29 22:50:04');
/*!40000 ALTER TABLE `jd_breakdowns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_descriptions`
--

DROP TABLE IF EXISTS `job_descriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_descriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company` varchar(500) NOT NULL,
  `position` varchar(500) NOT NULL,
  `image_paths` text,
  `description` text,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_job_descriptions_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_descriptions`
--

LOCK TABLES `job_descriptions` WRITE;
/*!40000 ALTER TABLE `job_descriptions` DISABLE KEYS */;
INSERT INTO `job_descriptions` VALUES (1,'百度','大模型应用方向实习生（J92819）',NULL,'**工作职责：**\n-参与多模态大模型的算法方案调研、日常微调、prompt工程，效果优化\n-支持大模型、机器视觉或NLP在各种实际业务中的落地，包括但不限于结构化信息抽取、智慧招采等方向，确保其在真实场景中的有效应用\n-参与大模型的日常评估和开发工作，推动其持续改进和性能提升，提高训练和推理效率\n-与团队成员紧密合作，协同解决开发过程中遇到的问题和技术挑战\n\n**职责要求：**\n-计算机或人工智能相关专业本科及以上学历\n-熟悉计算机视觉和自然语言处理中的至少一个方向，有顶会论文可加分\n-熟练掌握PyTorch等深度学习框架，有较强的编程能力\n-熟悉开源多模态大模型原理，有多模态大模型调优、信息抽取项目经验者优先\n-拥有一定工程能力，熟悉Flask，MySQL，Docker等技术\n-拥有大模型训练推经验，熟悉ms-swift训练套件，SFT、GRPO等训练方式以及VLLM推理部署者优先\n\n\n百度智能云是百度集团“三大增长曲线”之一，是百度 AI to B 业务的承载者，产业智能化领导者。百度智能云战略为“云智一体，深入产业，生态繁荣，AI普惠”。在中国AI公有云服务市场，百度智能云市场份额连续四年排名第一。 AI原生时代，百度智能云全面重构面向大模型的云计算基础设施，百度百舸·AI异构计算平台3.0针对大模型场景专项优化。自文心一言全面开放以来，百度智能云千帆大模型平台上，大模型API日调用量增长10倍，目前文心大模型日调用量已超过5000万次。千帆平台已累计服务超过4万家企业用户，千帆ModelBuilder累计帮助企业用户精调1万个大模型。AI原生应用工作台千帆AppBuilder助力企业高效开发AI原生应用。 百度智能云已服务500万+企业客户与开发者，助力政务、金融、工业、交通等千行百业智能化升级。','2025-10-27 20:35:30','2025-10-27 20:35:30'),(2,'东方算芯','编译器开发',NULL,'标签：编译器开发经验、C++\n工作职责：\n参与自研编译器、调试器及工具开发\n参与自研编程语言生态软件开发\n任职资格：\n掌握 C/C++ 等编程语言\n深入理解编译原理、计算机体系结构\n熟悉 X86、ARM 或 RISC-V 的指令集架构\n熟悉常见的编译器及工具的使用\n对编程语言有见解，做过相关项目的优先\n其他要求：\n211/985 计算机科学或相关专业硕士、本科生，研二或大三优先\n实习期预计 6 个月\n良好的解决问题能力及英文文档阅读能力\n每周至少工作四天','2025-10-28 10:01:28','2025-10-28 10:01:28'),(3,'阶跃星辰','大模型算法工程师【实习】',NULL,'【岗位职责】1. 在真实产品项目中理解算法需求，拆解问题，并设计对应的解决方案；2. 建立评测体系，通过提示词、模型训练算法进行快速调优；3. 设计并构建智能体 /toolcall 方案，补足单模型能力。\n\n【岗位要求】1. 具有良好的计算机 / 数学基础，熟练掌握 Python，有良好的编程习惯和代码风格；2. 具备扎实的算法基础，熟悉大语言 / 多模态模型的算法架构，包括 instructGPT，LLaMA 等主流架构算法；3. 熟悉 Alignment 领域的常用方法，包括但不限于 SFT、DPO、PPO、Self-Rewarding 和 Self-Critic 等；4. 具备卓越的实验分析与问题解决能力，有创新思维，能够良好沟通，与团队成员高效协作。\n\n【加分项】在上述相关领域有论文发表，有竞赛获奖经历，有丰富的项目经历。','2025-10-29 14:54:25','2025-10-29 14:54:41'),(4,'舜宇','机器学习（杭州）',NULL,'职位描述\n工作职责:\n\n1.负责公司产线业务问题分析和建模，能够基于机器学习、深度学习等方法解决痛点问题；\n\n2.基于应用场景，完成算法设计、验证和实现，并在实际产线应用中不断优化现有算法；\n\n3.将数据分析和AI算法应用到生产制造过程中，达成降本增效；\n\n4.基于数据和光学设计软件、渲染软件等工具，构建端到端的仿真链路，构建专业领域的大模型；\n\n5.协助培养团队成员。\n\n\n\n任职要求:\n\n1.计算机、光学工程、数学或统计学等相关专业，具有大数据分析及AI背景，具有3年以上科研/工作经验；\n\n2.熟悉掌握Python/C/Matlab等编程语言，熟悉常用的深度学习框架（如TensorFlow、Pytorch），熟悉常用的CV库及常见的图像检测、识别及分割算法，具备对实际问题进行抽象建模及编程实现的能力，有3年以上工作经验；\n\n3.有光学工程背景，熟练使用Zemax/CodeV等至少一门光学设计软件者优先；\n\n4.对光学镜头、模组的生产加工流程有系统了解者优先；\n\n5.有产线流程效率优化实际项目经验者优先；\n\n6.有大数据分析方向实际项目者优先；\n\n7.对新知识和技术保持好奇心，具备量化的自我驱动学习能力。','2025-10-29 18:07:49','2025-10-29 18:07:49'),(5,'Code Agent 大模型开发工程师','Code Agent 大模型开发工程师',NULL,'工作职责\n负责大型语言模型在代码智能领域的工程化应用，设计、开发和维护类似于 Cursor 或 Claude Code 的 AI 代码代理（Code Agent）系统，包括构建生产级原型和迭代优化。\n实现和优化核心功能，如代码补全、代码生成、代码检索、智能调试以及多代理协作机制，确保系统在实际编程场景中的高效性和可靠性。\n应用强化学习（RL）等先进技术，提升代码生成的准确性、效率和安全性，包括集成 RL 算法到代码代理框架中以处理复杂编程任务。\n构建和优化基于代码反馈的强化学习训练、评估和部署 pipeline，支持持续集成和自动化测试。\n与产品、设计和研究团队协作，推动 AI 编程工具从原型到生产环境的落地，参与性能调优和用户反馈迭代。\n\n职位要求\n本科及以上学历，计算机科学、软件工程、人工智能或相关专业。\n对代码大模型和 AI 编程工具有浓厚兴趣，有 Cursor、Claude Code 或类似 AI 代码助手工具的开发、集成或优化经验者优先（包括 Prompt Engineering、模型微调或代理系统构建）。\n具备出色的逻辑思维能力、问题解决能力和团队协作精神，能够在快节奏环境中独立推动项目。\n\n加分项\n具备前端开发经验，熟悉 TypeScript 及现代前端框架（如 React、Vue 等），能够开发 AI 代码助手的交互界面、插件或 IDE 集成。\n有开源项目贡献经验，或在 GitHub 等平台上维护过 AI 相关仓库。\n熟悉 DevOps 工具（如 Docker、Kubernetes）和云服务（AWS、Azure 等），有部署 AI 模型到生产环境的经验。','2025-10-29 20:29:02','2025-10-29 20:29:02'),(6,'遂原科技','AI 框架开发工程师',NULL,'标签：CUDA、机器学习、MATLAB、GPU、模型加速 / 性能优化\n\n岗位职责：\n负责云端 AI 芯片 AI 框架，SDK 和算子编程模型的开发和集成，具体包括以下一到多项：\n扩展 Tensorflow/Caffe/PyTorch 等 AI 框架的后端，实现对新云端 AI 计算设备的支持；\n分析和优化 AI 框架的性能；\n针对云端 AI 计算设备，设计和调优 AI 框架图级别调度和融合等算法优化；\nAI 框架 AOT/JIT 编译功能支持，动态图和静态图的支持；\n模型量化 / 模型压缩的 AI 框架级别支持\n算子编程模型支持和自动调优\nSDK 生态化接口搭建和维护\n\n职位基本要求：\n计算机或软件相关学科本科毕业；\n理解 AI 框架应用及常见的云端 AI 模型；\n理解掌握图编译原理，熟悉 AI 框架主要流程；\n熟练掌握 C/C++，熟悉 Python 编程；\n熟悉软件开发工具和脚本语言（如 git, CMake, Bazel, bash 等）；\n熟悉软件开发、发布和管理流程（如敏捷开发，缺陷管理，CI/CD 概念等）；\n\n职位要求加分项：\n计算机科学或电气工程学硕士毕业或三年以上相关工作经验；\n深度学习、机器学习相关工作经验\nGPU 驱动或应用（CUDA 和 cuDNN 库）开发经验；\nMLIR/LLVM 相关开发经验；\nPytorch，Tensorflow，Mindspore，Paddlepaddle 等任一种或几种框架对接后端硬件经验\n有分布式大模型训练或推理经验者佳','2025-10-29 20:30:31','2025-10-29 20:30:31'),(7,'理想','电驱动AI智能工程师-上海',NULL,'职位描述\n\n1. 电驱动AI agent智能体开发：主导电驱动AI agent开发，构建全球领先的人工智能AI agent技术和平台，实现电驱动AI agent智能化开发和流程升级、智能预测性维护和诊断、边缘端智能AI模型和功能；\n\n2. 多模态AI模型和功能开发：通过多模态AI大模型的微调、强化学习训练、agent框架等，赋能研发、设计、生产制造领域的AI功能开发和AI agent开发；\n\n3. AI驱动制造升级：开发视觉算法提升电驱动产线效率和质量，构建AI agent优化制造流程，实现产线大数据智能决策闭环；\n\n4. 跨领域技术融合：深度结合电驱动专业机理模型与人工智能方法（如Transformer、神经网络），开发新一代电驱智能算法；\n\n5. 前沿技术攻关：主导如物理信息人工智能网络（PINN）、多模态大模型行为识别等创新项目，推动技术成果专利化与产业化落地。\n\n\n职位要求\n\n1. 硕士及以上学历，计算机、人工智能、车辆、电力电子、机器人等相关专业；\n\n2. 精通大模型前沿理论和先进技术，如大模型微调、强化学习训练，有实际动手经验并获得优异结果；\n\n3. 精通AI agent开发的理念和先进方法，如context engineering、记忆、迭代学习等，有把一个AI agent落地应用在任何项目上的成功经验；\n\n4. 精通深度学习架构，熟练掌握Transformer、CNN、RNN等模型架构，有实际应用经验；\n\n5. 熟悉多模态大模型的相关理论和开发技术，掌握多模态大模型在图片和视频领域的训练方法和agent架构；\n\n6. 熟悉电驱动控制原理、电机和电机控制器知识、控制软件、硬件电路和机械开发、芯片设计等，有与AI结合的开发经历优先；\n\n7. 有顶会或期刊发表电驱动和AI大模型、AI agent领域论文者优先。','2025-10-30 13:05:54','2025-10-30 13:05:54'),(8,'理想','具身智能运控算法工程师（VLA方向）',NULL,'职位描述\n\n1. 基于视觉-语言-动作（Vision-Language-Action, VLA）大模型，探索具身智能高层任务规划与低层运控一体化方案；\n\n2. 设计从多模态感知（视觉、语言、状态）到规划任务的推理框架，完成语义任务规划。\n\n\n职位要求\n\n1. 大模型能力\n\n - 有 VLM（Vision-Language Model）或 VLA 项目经验。\n\n2. 编程与工程能力\n\n - 熟练 Python / C++，掌握 PyTorch / TensorFlow；\n\n - 熟悉 ROS / ROS 2 框架，能进行机器人算法集成与调试。','2025-10-30 13:18:06','2025-10-30 13:18:31'),(9,'理想','【理想+】AIOps研发工程师-北京 （AI架构很有价值）',NULL,'【本岗位的主要工作内容】\n\n1. 负责AIOps前沿算法学习研究以及工程化落地；\n\n2. 负责运维数仓的建设，包括数据清洗、特征工程、数据ETL、数据图谱等；\n\n3. 负责SRE-Copilot的研发，包括multi-agent的架构设计，智能诊断，故障预测等通用Agent的研发落地，运维大模型的训练和微调；\n\n4. 负责AgentCore的平台能力建设，包括Agent Framework，Agent Runtime、沙箱Browser、沙箱Code Interpreter等能力的研发，Agent可观测能力的建设等。\n\n\n职位要求\n\n1. 机器学习与深度学习框架，熟悉常用的机器学习与深度学习框架，包括但不限于：\n\n   - PyTorch、TensorFlow、scikit-learn、XGBoost、LightGBM 等；\n\n   -了解模型训练、评估、微调、部署全流程，具备一定的调参与性能优化能力；\n\n   - 熟悉时间序列预测、异常检测、Root Cause Analysis 等方向优先。\n\n2. 云原生与平台工程相关技术栈，理解云原生理念，具备以下技术栈经验者优先：\n\n    - 容器与调度：Docker、Kubernetes、Helm；\n\n    - 微服务与服务治理：Istio、Envoy、gRPC、Spring Cloud；\n\n    - DevOps工具链：GitLab CI/CD、ArgoCD、Prometheus、Grafana、ELK/EFK。\n\n3. 数据平台与处理工具，有大数据处理和数据平台开发经验者优先，常用技术包括：\n\n   - Kafka、Flink、Spark、Airflow、ClickHouse、Hudi、Delta Lake、Neo4j（图数据库）等；\n\n   - 熟悉运维数据建模、数据血缘追踪、指标体系建设优先。\n\n4. 智能Agent开发经验（加分项）熟悉或有以下框架使用经验者优先：\n\n   - LangChain、Autogen、CrewAI、MetaGPT、Haystack、Semantic Kernel等；\n\n   - 了解多Agent协作范式，具备LLM调用与Tool封装实操经验；\n\n   - 熟悉Memory机制、Agent可观测性、Chain-of-Thought（CoT）、工具调用调度机制优先。\n\n5. 工程开发与系统设计能力：\n\n   - 熟悉微服务架构设计、分布式系统设计原则；\n\n   - 熟练掌握主流后端开发语言，如 Python、Go、Java 中至少一种，具备良好的工程能力。\n\n6. 大语言模型相关经验（加分项），熟悉 LLM微调（如LoRA、QLoRA、PEFT）、RAG检索增强技术；\n\n7. 有阅读论文（如arXiv）或以及参与技术社区（LLM，Agent开源社区）内容的习惯。','2025-10-30 13:29:45','2025-10-30 13:29:45'),(10,'理想','【理想+】AgentOps研发工程师-北京',NULL,'【本岗位的主要工作内容】\n\n1. 负责面向SDLC(软件开发生命周期)方向的Agent 系统的设计、开发和优化、开发和完善基于大语言模型 (LLM) 的智能体系统，提升 Agent 的自主决策和任务执行能力；\n\n2. 负责研发智能助手Agent指令意图理解相关工作(工单指令和值班组分发)，整体提升大模型的多轮对话指令理解能力和性能；\n\n3. 设计并实现 Agent 的工具使用接口，实现与各类外部系统和 API 的集成编排；\n\n4. 负责研发智能助手Agent在检索、推荐、工具调用方面的系统设计实现和优化，探索Agent、RAG、领域模型调优等相关技术在业务场景落地；\n\n5. 具备模型知识、幻觉机制探究，提升模型知识水平、降低模型幻觉率；\n\n6. 建立和完善 Agent 工程化开发实践范式，包括需求理解、评测体系建设、数据收集与反馈闭环机制，推动智能助手的迭代优化与持续提升，实现可观测、可调优、可演进的 Agent 产品能力；\n\n7. 深入调研AI领域相关的前沿技术，跟踪业内大模型领域的最新进展，并寻求将最新技术应用到产品的可能性。\n\n\n职位要求\n\n1. 计算机科学、软件工程、人工智能等相关专业本科及以上学历；具备分布式系统或 AI 架构经验，并且有Agent 实践经验；\n\n2. 精通 Python（或 Go/Java），熟悉 LangChain、AutoGen、LangGraph、Prompt 工程、RAG、微调 (SFT / LoRA)；具备多模型集成与评测经验；\n\n3. 熟练使用 Kubernetes、Docker、Terraform 及 CI/CD；了解 Kubeflow、MLflow、向量数据库 (FAISS/Weaviate) 与 GPU 调度，在大规模推理或训练环境有实践记录；\n\n4. 能独立完成高并发、高可用架构方案设计；具备数据流、缓存、索引与网络调优能力，并能利用监控数据进行容量规划与 SLA/SLO 管理；\n\n5. 了解模型安全、数据安全与合规要求 (GDPR / CCPA / 行业合规)；有建立安全闸口和治理闭环的实战经验；\n\n6. 具备跨部门协调、技术布道与文档写作能力，可将复杂技术方案转化为业务价值并对接用户需求。','2025-10-30 13:34:15','2025-10-30 13:34:15'),(11,'叮咚买菜','预测算法工程师-供应链销量/单量预测方向(J15016)',NULL,'工作职责\n1、生鲜商品销量预测，提前N天给出精准预测结果，降低缺货和损耗；\n2、结合商品本身信息，以及节假日，活动，天气等特征构建鲁棒的时序预测模型；\n3、研究探索业界领先的深度时序预测模型，在零售供应链场景落地；\n4、大数据量下规模化部署预测模型。\n\n任职资格\n1、计算机、数学等相关专业，2026届硕士及以上学历，互联网或零售行业相关工作经验；\n2、掌握常见的深度/机器学习模型及原理，具备大数据训练经验，善于结合数据特性优化网络结构，有深度学习经验尤其是了解应用过深度时序模型的优先；\n3、熟悉Linux基础命令，熟练掌握Python语言，能够熟练使用PyTorch、LightGBM、Pandas等工具独立进行建模实验；\n4、熟练掌握SQL语言，熟悉MySQL、Hive，有Spark大数据处理经验优先；\n5、热爱技术并能主动学习。参与过kaggle M5 forecasting等kaggle比赛以及相关社区活跃者优先。','2025-10-31 16:40:43','2025-10-31 16:40:43'),(12,'叮咚买菜','增长算法工程师-商品运营/用户增长方向(J15019)',NULL,'工作职责\n1、参与和协助零售商品管理，完成商品的数字化，可以通过数据分析完成对商品的评估，并对商品的有效用户画像有效分析，并进一步完成用户增长、商品孵化、人货匹配的Model；\n2、参与和协助智能选品定价，分析弹性，制定多种交叉价格弹性策略，熟悉Uplift Model，有效解决定价带来的替代效应。\n\n任职资格\n1、2026届硕士及以上应届毕业生，计算机、数学等相关专业, 互联网或零售行业实习经历优先；\n2、机器学习要求，掌握常见的机器算法模型及原理，如LR、Model、Boosting、Bagging、PCA，熟悉分类、预测、聚类等常用算法，熟悉工程应用中LGB、XGBoost关键参数，参与过大规模机器学习、强化学习，数据挖掘项目；\n3、运筹优化方向要求，定价与收益管理，随机优化，多目标优化，混合整数规划，元启发式算法；\n4、优秀的分析和解决问题的能力，很强的逻辑能力，动手能力强优先；\n5、熟悉Linux系统，熟练掌握Python语言，能够熟练使用Numpy、Pandas、Scikit-Learn独立进行建模实验；\n6、熟练掌握SQL语言，熟悉MySQL、Hive，有Spark大数据处理经验优先。','2025-10-31 16:42:44','2025-10-31 16:42:44');
/*!40000 ALTER TABLE `job_descriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `okrs`
--

DROP TABLE IF EXISTS `okrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `okrs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `objective` varchar(500) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `due_date` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_okrs_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `okrs`
--

LOCK TABLES `okrs` WRITE;
/*!40000 ALTER TABLE `okrs` DISABLE KEYS */;
INSERT INTO `okrs` VALUES (1,'每天应对手撕、高强度准备手撕',0,'2025-10-30 00:00:00','2025-10-29 19:12:39','2025-10-29 19:13:33'),(2,'AI架构——智能体搭建平台 Dify。架构学习固定1h。',0,'2025-11-04 00:00:00','2025-10-29 19:14:30','2025-10-29 19:14:30'),(3,'完成这一波的面试（百度、智谱、舜宇、小鹏谈薪）',0,'2025-11-02 00:00:00','2025-10-29 19:20:01','2025-10-29 19:37:52');
/*!40000 ALTER TABLE `okrs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opinion_categories`
--

DROP TABLE IF EXISTS `opinion_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opinion_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `order` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_opinion_categories_name` (`name`),
  KEY `ix_opinion_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opinion_categories`
--

LOCK TABLES `opinion_categories` WRITE;
/*!40000 ALTER TABLE `opinion_categories` DISABLE KEYS */;
INSERT INTO `opinion_categories` VALUES (1,'酒桌',1,'2025-11-01 17:49:24','2025-11-01 17:49:24'),(2,'大模型',2,'2025-11-01 17:49:38','2025-11-01 17:49:38'),(3,'人际',3,'2025-11-01 22:14:54','2025-11-01 22:14:54'),(4,'效率',4,'2025-11-01 22:27:44','2025-11-01 22:27:44'),(5,'商业',5,'2025-11-01 23:20:07','2025-11-01 23:20:07');
/*!40000 ALTER TABLE `opinion_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opinions`
--

DROP TABLE IF EXISTS `opinions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opinions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `category_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_opinions_category_id` (`category_id`),
  KEY `ix_opinions_id` (`id`),
  CONSTRAINT `opinions_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `opinion_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opinions`
--

LOCK TABLES `opinions` WRITE;
/*!40000 ALTER TABLE `opinions` DISABLE KEYS */;
INSERT INTO `opinions` VALUES (1,'主动来给你的东西，不要信。但是可以随机应变，玩心眼子。',1,'2025-11-01 17:49:27','2025-11-01 17:49:27'),(2,'现在不管小模型、大模型，这个领域的切换成本不高。',2,'2025-11-01 17:50:00','2025-11-01 17:50:00'),(3,'你赞同与否？一票，中立，拒绝。新中国不需要中立。',1,'2025-11-01 17:50:44','2025-11-01 17:50:44'),(4,'十月桂花香',1,'2025-11-01 19:53:39','2025-11-01 19:53:39'),(5,'那你自己去干',1,'2025-11-01 19:54:27','2025-11-01 19:54:27'),(6,'领导比较喜欢',2,'2025-11-01 19:56:40','2025-11-01 19:56:40'),(7,'认识社交的动物，不要远离环境，这是jack35岁悟到的。不要让别人觉得，你个垃圾，我不跟你这样的人呆一起，这样子他们会感受到，会打压你，戴个耳机。',3,'2025-11-01 22:14:57','2025-11-01 22:14:57'),(8,'看到的环境都在阻碍自己的成长。这是每个人人生的开题，在吵杂的环境、人流吵杂中，找到自己的桃花源，这才是强者。',3,'2025-11-01 22:16:04','2025-11-01 22:16:04'),(9,'日程表，列出来，每天把最重要的先做了，10年下来，养成这个习惯！中间休息可以玩半小时手机，这样子。',4,'2025-11-01 22:28:07','2025-11-01 22:28:07'),(10,'相信自己会变好，这件事非常重要！',4,'2025-11-01 22:39:37','2025-11-01 22:39:37'),(11,'我相信自己会越来越好，越来越幸福。今天人很多，有点紧张，表达不出来。',4,'2025-11-01 22:40:13','2025-11-01 22:40:13'),(12,'穷则独善其身，达则兼济天下。',3,'2025-11-01 22:45:32','2025-11-01 22:45:32'),(13,'精神，祖国。起立！老少皆宜的节目。',3,'2025-11-01 22:50:39','2025-11-01 22:50:39'),(14,'一句话能传承下来，一句话会改变一个人。孔子。',3,'2025-11-01 22:52:05','2025-11-01 22:52:05'),(15,'有一个目标，一直努力，早点晚点就会实现。相信自己。有目标！！一直朝着努力！！！',3,'2025-11-01 22:53:59','2025-11-01 22:53:59'),(16,'懂得感恩！就会解决的很顺利！！！！',3,'2025-11-01 22:54:57','2025-11-01 22:54:57'),(17,'衣食无忧、大富大贵',3,'2025-11-01 22:56:02','2025-11-01 22:56:02'),(18,'人最快的事情，就是对别人有价值！（到了一定年龄，衣食无忧了阶段）',3,'2025-11-01 22:57:22','2025-11-01 22:57:22'),(19,'不要像很多！想干啥就去做！每天很开心，很充实，滚雪球！',4,'2025-11-01 23:05:48','2025-11-01 23:05:48'),(20,'一堆的原生家庭，谁都能找到很多！父母是父母，你是你，你们是两个个体！独立！为自己努力，每天要做什么事情！！！！！父母也会没有的，还是要靠自己生活！',4,'2025-11-01 23:13:23','2025-11-01 23:13:23'),(21,'你不要管别人，就管你自己！！！这是最高效的！！',3,'2025-11-01 23:15:09','2025-11-01 23:15:09'),(22,'做东西一定要昧着良心吗？商业成功不是一定要做坏事，但是做商业成功一定是懂人性的人。',5,'2025-11-01 23:24:07','2025-11-01 23:24:07'),(23,'《聪明的投资者》',5,'2025-11-01 23:24:32','2025-11-01 23:24:32'),(24,'罗伯特·清崎 《穷爸爸富爸爸》的作者，通过书籍来获钱，但是他还是有名的投资者。',5,'2025-11-01 23:25:55','2025-11-01 23:25:55'),(25,'利用自己的明星效应做内容输出付费',5,'2025-11-01 23:28:37','2025-11-01 23:28:37'),(26,'谈恋爱也不是一味的迁就别人，也得让别人得不到，也得让别人垫垫脚勾一勾才能看到！',3,'2025-11-01 23:29:24','2025-11-01 23:29:24'),(27,'《牧羊人的奇幻之旅》！看书，很推荐',5,'2025-11-01 23:29:35','2025-11-01 23:38:41'),(28,'商人，看起来没有什么能力就能做成功。这是因为能够带来很多情绪价值。就是人类是动物，把对面哄开心了，再把事件做好了！',3,'2025-11-01 23:31:31','2025-11-01 23:31:31'),(29,'有的人不值得帮，不应该帮。佛渡有缘人。帮别人也是有成本的，没有把时间用到最应该的人身上。（大冰送羽绒服送给有需要的人，有很多人冒充领。我没办法解决这件事，但是我每年需要坚持做这件事。还有一个故事就是救济的粥里面加了沙子，真正饿的人不会在意傻子的。）！！！！！！！！！！！',3,'2025-11-01 23:34:02','2025-11-01 23:34:02'),(30,'《从0到1》',5,'2025-11-01 23:36:31','2025-11-01 23:36:31'),(31,'思考致富。（也有人说他是心灵鸡汤、毒鸡汤，可以看《秘密》）',5,'2025-11-01 23:37:04','2025-11-01 23:40:06'),(32,'触底反弹！！重生！！要相信相信的力量，相信自己的人生，相信自己能够有很多转机！清零也不会害怕！',4,'2025-11-01 23:44:43','2025-11-01 23:45:02'),(33,'你相信这个东西，他就是在这个胡同里，左边有个墙右边有个墙，撞来撞去，但是朝着自己的目标前进！！你相信他存着，他就存着！！',4,'2025-11-01 23:46:17','2025-11-01 23:46:17'),(34,'深呼吸一下，深度思考一下，冷静一下，应不应该立马去学习，应该的话，所有外界的因素就是你要去克服的对象，这就是锻炼自己的一个契机一个机会。你先观察他们，看他们打游戏的失神的状态！将看别人玩的专注力，转化到自己认真做事的专注当中！！！',4,'2025-11-01 23:51:40','2025-11-01 23:51:40'),(35,'冲突来源于利益。比如纯粹的友谊就没有冲突：军队！',3,'2025-11-01 23:55:26','2025-11-01 23:55:26'),(36,'在脑袋最清醒的时候把重要的事情去做掉！前提重要的事情想明白！这不是一件没法解决的事情！在不清醒的时候就去玩啊闹啊！',3,'2025-11-01 23:57:22','2025-11-01 23:57:22'),(37,'别妄自菲薄',4,'2025-11-01 23:57:27','2025-11-01 23:57:27'),(38,'原来的字节给人感觉努力就行。现在不是嫡系不舔着人家屁也不是。\n\n组织架构成熟后是这样的，有人的地方就有江湖，抱团才能安全持久。',3,'2025-11-02 12:00:54','2025-11-02 12:01:23');
/*!40000 ALTER TABLE `opinions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `tech_stack` varchar(500) DEFAULT NULL,
  `start_date` varchar(50) DEFAULT NULL,
  `end_date` varchar(50) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_projects_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'基于大模型的心脏病术后康复运动序列生成系统                                         竞赛项目    ','基于大模型的心脏病术后康复运动序列生成系统                                         竞赛项目                                             2023年12月 - 2024年8月\n成果展示：《基于多模态AIGC模型的心脏术后康复方案智能生成系统》荣获上海大学2024年中国国际大学生创新大赛银奖（2024年）\n旨在为心脏术后患者提供集“动态监测-处方生成-远程评估”于一体的个性化康复服务。项目依托合作方的十二导联心电衣，并与xx医院合作开展临床入组实验，确保方案的临床有效性与安全性。旨在为心脏术后患者提供集“动态监测-处方生成-远程评估”于一体的个性化康复服务。项目依托合作方的十二导联心电衣，并与xx医院合作开展临床入组实验，确保方案的临床有效性与安全性。\n核心技术贡献：\n1. 个性化运动处方生成\n- 多模态数据融合: 负责心电(ECG)时间序列数据与文本病历的多模态数据处理。借鉴BLIP对齐思想，设计并优化了数据融合与生成流程，为个性化处方生成奠定基础。\n- 生成与安全校正: 应用Transformer大模型生成定制化运动处方，并引入专家知识库与RAG框架进行审核校正，确保方案的安全与有效性。\n2. 康复动作实时评估与闭环优化\n- 技术实现：应用人体姿态估计算法，实时追踪并量化评估患者的运动姿态与动作完成度。\n- 闭环反馈: 将评估结果作为正向反馈，用于动态调整和持续优化后续的运动处方，形成个性化康复闭环。\n','','','','','2025-10-26 15:41:08','2025-10-26 15:41:08'),(2,'医学血管拓扑分割课题  科研项目','医学血管拓扑分割课题                                                                                 科研项目                                               2024年9月 - 2025年3月         成果：《ConformalRefiner: Retinal Vessel Topology Reconstruction via Conformal Risk Control》 IJCRS2025，CCF-C，第一作者，已录用\n项目背景与定位：解决深度学习视网膜血管分割中阈值不确定、拓扑不连续及噪声干扰问题，研发即插即用后处理框架。\n主要思路：\n1. 创新应用共形风险控制（CRC）理论，设计阈值校准模块，以假阴性率为指标，通过校准集求解最优阈值，95% 置信度下覆盖更多模糊          血管，改善固定阈值缺陷。\n2. 基于分形维度理论（1.3-1.4 区间筛选）构建拓扑校准模块，过滤病变噪声，区分血管与病变伪影。\n3. 设计双输入重构网络（TopoRefiner），融合初始分割与拓扑校准结果，引入 TopoLoss 约束，修复血管断裂。\n最终效果：DRIVE、FIVE 数据集验证中，拓扑指标（Cldice、β₀）显著提升，效果优于目前的SOTA方法。','','','','','2025-10-26 15:41:45','2025-10-26 15:41:45');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prompts`
--

DROP TABLE IF EXISTS `prompts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prompts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_prompts_id` (`id`),
  KEY `ix_prompts_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prompts`
--

LOCK TABLES `prompts` WRITE;
/*!40000 ALTER TABLE `prompts` DISABLE KEYS */;
/*!40000 ALTER TABLE `prompts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resume_photos`
--

DROP TABLE IF EXISTS `resume_photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resume_photos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL,
  `image_path` varchar(1000) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_resume_photos_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resume_photos`
--

LOCK TABLES `resume_photos` WRITE;
/*!40000 ALTER TABLE `resume_photos` DISABLE KEYS */;
INSERT INTO `resume_photos` VALUES (2,'大模型实习时的简历','623511c0-c723-4070-b335-e772179f7ad0.png','2025-10-26 16:34:15','2025-10-26 16:34:15');
/*!40000 ALTER TABLE `resume_photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `okr_id` int NOT NULL,
  `title` varchar(500) NOT NULL,
  `description` text,
  `completed` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_tasks_okr_id` (`okr_id`),
  KEY `ix_tasks_id` (`id`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`okr_id`) REFERENCES `okrs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,1,'任务1：Hot 100 都过一遍',NULL,0,'2025-10-29 19:15:38','2025-10-29 19:15:38'),(2,1,'任务2：应对大厂的面试',NULL,0,'2025-10-29 19:15:49','2025-10-29 19:15:49'),(3,2,'提一个pr',NULL,0,'2025-10-29 19:15:58','2025-10-29 19:15:58'),(4,3,'百度二面',NULL,1,'2025-10-29 19:20:16','2025-11-02 10:58:11'),(5,3,'智谱实习 周五上午10点',NULL,1,'2025-10-29 19:20:27','2025-11-02 10:58:10'),(6,3,'舜宇机器学习秋招 1：45-2：00',NULL,1,'2025-10-29 19:20:43','2025-11-02 10:58:09'),(7,3,'小鹏重新谈薪，明天上午，感恩的态度，必须挽回。',NULL,0,'2025-11-02 10:58:03','2025-11-02 10:58:03'),(8,1,'周末必须练一练',NULL,0,'2025-11-02 10:58:31','2025-11-02 10:58:31');
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tech_stacks`
--

DROP TABLE IF EXISTS `tech_stacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tech_stacks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `level` varchar(50) NOT NULL,
  `description` text,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_tech_stacks_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tech_stacks`
--

LOCK TABLES `tech_stacks` WRITE;
/*!40000 ALTER TABLE `tech_stacks` DISABLE KEYS */;
INSERT INTO `tech_stacks` VALUES (1,'大模型算法工程师','','','基础框架：熟练掌握Python、Java编程语⾔，精通FastAPI框架并能独⽴设计、搭建⾼性能后端服务（熟悉RESTful API规范）；具备⽹络爬⾍开发与数据采集经验。\n深度学习：熟练掌握Pytorch深度学习框架；熟悉各类NLP核⼼技术；了解主流的机器学习与不确定性量化⽅法。\n⼤模型相关：\n    核⼼理论: 深⼊理解Transformer、RAG、Agent、多模态对⻬（BLIP思想）、思维链（CoT）等核⼼原理。\n    模型应⽤: 具备DeepSeek、Qwen-VL、SenseVoice、Spark-TTS、Whisper等多种⼤模型的应⽤与私有化部署经验。\n    微调与对⻬: 熟悉SFT、RLHF（PPO、DPO、GRPO）等模型对⻬技术原理；熟悉LoRA、QLoRA等⾼效微调⽅法，具备基于开源框架xtuner、Unsloth等框架进⾏微调能力；了解DeepSpeed分布式训练优化框架。\n    开发框架: 精通LangChain、LangGraph框架，熟练应⽤vLLM、Xinference等推理框架进⾏性能优化。\n数据库：  熟练使⽤MySQL、Redis进⾏业务开发；熟悉向量数据库Chroma、Milvus（⽀撑RAG）与图数据库Neo4j（⽀撑知识图谱）。\n中间件：  熟悉后端业务常⽤的中间件，有RabbitMQ、MQTT等消息队列使⽤经验，具有对接⼤型国内外⽀付系统的实践经验。\n⼯具：    熟练运⽤Linux系统及Shell/Python脚本；精通Git版本控制⼯具；具备Docker容器化开发与运维能⼒，熟悉CI/CD全流程；熟悉Pandas、ECharts等数据处理与可视化⼯具。\n英语：    CET-4，考研英语  78分，具备阅读英⽂技术⽂档与论⽂的能⼒。','2025-10-26 15:48:44','2025-10-27 20:38:36'),(2,'大模型算法工程师-实习阶段','','','基础框架：熟练使⽤Python、Java编程语⾔，了解常⻅的设计模式、软件设计原则。\n深度学习：熟悉常⻅的机器学习模型、深度学习模型、熟悉NLP技术，熟悉Pytorch框架。熟悉主流的不确定性量化⽅法。\n⼤模型相关：了解⼤模型相关原理，了解Deepseak-R1模型，熟悉主流RAG检索增强优化⽅案，熟悉langchain框架、Ollama⼯具、Streamlit库。\n数据库：    熟悉Mysql数据库、Redis数据库、了解EleasticSearch、向量数据库（Chroma）、图数据库（Neo4j）。\n前后端相关：了解Vue框架、熟悉SpringBoot框架、熟悉MVP开发架构、具备SpringCloud微服务开发能⼒。\n中间件：    熟悉中间件SDK对接流程、了解并⽤过RabbitMQ、MQTT消息队列组件，具备对接⼤型国内外⽀付系统能⼒。\n⼯具：        熟悉Git版本控制⼯具，熟悉⼀定的Linux运维技术、Docker技术，独⽴部署过中⼩型Web项⽬。\n英语：        CET-4，考研英⼆78分','2025-10-26 16:23:57','2025-10-26 16:23:57'),(3,'后端开发工程师-本科实习阶段','','','软件水平：\n蓝桥杯软件组省赛二等奖。\n了解前端Html、css、js、three.js 熟悉Vue框架\n熟悉Java语言、JavaWeb技术、数据结构与算法、数据库、计算机网络，具有良好的计算机学科基础素养。\n熟悉MVC架构模式，熟悉SSM、SpringBoot、SpringCloud等框架\n掌握一定的Linux运维技术。\n会写python自动化脚本\n数字媒体方面：\n掌握ps、pr、3dsmax的使用\n了解图形生成算法、图像处理技术。\n英语水平：\n通过CET-4，能读懂英文技术文档。\n团队协作：\n工作中沟通能力、自驱力强。\n具有主人翁意识、产品经理理念。','2025-10-26 16:24:44','2025-10-26 16:24:44');
/*!40000 ALTER TABLE `tech_stacks` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 13:41:45
