"""
L4-SEO智能体 - 策略库模块
SEO优化策略知识库
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import yaml

@dataclass
class Strategy:
    """SEO优化策略"""
    strategy_id: str
    name: str
    description: str
    category: str  # performance, content, technical, ai_citation
    subcategory: str
    implementation: str
    expected_impact: Dict[str, float]  # 预期影响的指标和程度
    success_rate: float
    effort_level: str  # low, medium, high
    risk_level: str  # low, medium, high
    prerequisites: List[str]
    related_strategies: List[str]
    created_at: str
    last_used: str
    usage_count: int
    average_effectiveness: float

@dataclass
class StrategyExecution:
    """策略执行记录"""
    execution_id: str
    strategy_id: str
    timestamp: str
    website_url: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]
    effectiveness_score: float
    learned_lessons: List[str]

class StrategyLibrary:
    """SEO优化策略库"""
    
    def __init__(self):
        self.workspace = Path("/Users/qinzheng/.openclaw/workspace")
        self.library_file = self.workspace / "strategy_library.json"
        self.executions_file = self.workspace / "strategy_executions.json"
        
        # 初始化策略库
        self.strategies = self._load_strategies()
        self.executions = self._load_executions()
        
        # 如果策略库为空，加载默认策略
        if not self.strategies:
            self._load_default_strategies()
    
    def _load_strategies(self) -> Dict[str, Strategy]:
        """加载策略库"""
        strategies = {}
        
        if self.library_file.exists():
            try:
                with open(self.library_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for strategy_id, strategy_data in data.items():
                    strategies[strategy_id] = Strategy(**strategy_data)
                    
            except Exception as e:
                print(f"⚠️ 加载策略库失败: {str(e)}")
        
        return strategies
    
    def _load_executions(self) -> Dict[str, List[StrategyExecution]]:
        """加载执行记录"""
        executions = {}
        
        if self.executions_file.exists():
            try:
                with open(self.executions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for strategy_id, exec_list in data.items():
                    executions[strategy_id] = [
                        StrategyExecution(**exec_data) for exec_data in exec_list
                    ]
                    
            except Exception as e:
                print(f"⚠️ 加载执行记录失败: {str(e)}")
        
        return executions
    
    def _load_default_strategies(self):
        """加载默认策略"""
        print("   📚 加载默认SEO优化策略...")
        
        default_strategies = self._create_default_strategies()
        
        for strategy in default_strategies:
            self.strategies[strategy.strategy_id] = strategy
        
        self._save_strategies()
        print(f"   ✅ 加载{len(default_strategies)}个默认策略")
    
    def _create_default_strategies(self) -> List[Strategy]:
        """创建默认策略"""
        now = datetime.now().isoformat()
        
        return [
            # 性能优化策略
            Strategy(
                strategy_id="perf_001",
                name="优化LCP（最大内容绘制）",
                description="通过优化关键资源加载来改善LCP指标",
                category="performance",
                subcategory="core_web_vitals",
                implementation="1. 优化关键图片尺寸和格式\n2. 使用WebP格式图片\n3. 实现懒加载\n4. 预加载关键资源\n5. 使用CDN加速",
                expected_impact={"lcp": 0.3, "overall_performance": 0.25},
                success_rate=0.85,
                effort_level="medium",
                risk_level="low",
                prerequisites=["图片优化工具", "CDN服务"],
                related_strategies=["perf_002", "perf_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            Strategy(
                strategy_id="perf_002",
                name="减少CLS（累积布局偏移）",
                description="通过稳定布局防止页面元素意外移动",
                category="performance",
                subcategory="core_web_vitals",
                implementation="1. 为图片和视频指定尺寸\n2. 预留广告位空间\n3. 避免动态插入内容\n4. 使用CSS transform代替top/left\n5. 预加载字体",
                expected_impact={"cls": 0.4, "user_experience": 0.3},
                success_rate=0.9,
                effort_level="low",
                risk_level="low",
                prerequisites=["CSS知识", "布局分析工具"],
                related_strategies=["perf_001", "perf_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            # 内容优化策略
            Strategy(
                strategy_id="content_001",
                name="优化标题标签",
                description="改进页面标题以提高点击率和SEO效果",
                category="content",
                subcategory="title_optimization",
                implementation="1. 确保每个页面有唯一H1标签\n2. 标题长度保持在30-70字符\n3. 包含主要关键词\n4. 添加品牌名称\n5. 使用情感词提高点击率",
                expected_impact={"click_through_rate": 0.2, "ranking": 0.15},
                success_rate=0.8,
                effort_level="low",
                risk_level="low",
                prerequisites=["关键词研究", "标题分析工具"],
                related_strategies=["content_002", "content_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            Strategy(
                strategy_id="content_002",
                name="优化元描述",
                description="改进元描述以提高搜索结果的点击率",
                category="content",
                subcategory="meta_optimization",
                implementation="1. 描述长度120-160字符\n2. 包含主要关键词\n3. 添加行动号召\n4. 突出独特价值主张\n5. 避免重复描述",
                expected_impact={"click_through_rate": 0.15, "user_engagement": 0.1},
                success_rate=0.75,
                effort_level="low",
                risk_level="low",
                prerequisites=["内容分析", "竞争对手分析"],
                related_strategies=["content_001", "content_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            # 技术SEO策略
            Strategy(
                strategy_id="tech_001",
                name="优化图片ALT文本",
                description="为所有图片添加描述性ALT文本以提高可访问性和SEO",
                category="technical",
                subcategory="image_optimization",
                implementation="1. 检查所有图片是否有ALT文本\n2. 为装饰性图片添加空ALT\n3. 为内容性图片添加描述性ALT\n4. 包含相关关键词\n5. 保持ALT文本简洁",
                expected_impact={"accessibility": 0.4, "image_search": 0.25},
                success_rate=0.95,
                effort_level="medium",
                risk_level="low",
                prerequisites=["图片清单", "ALT文本分析工具"],
                related_strategies=["tech_002", "tech_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            Strategy(
                strategy_id="tech_002",
                name="改进内部链接结构",
                description="优化网站内部链接以提高爬虫效率和用户体验",
                category="technical",
                subcategory="link_optimization",
                implementation="1. 确保每个页面有至少一个内部链接\n2. 使用描述性锚文本\n3. 创建清晰的导航结构\n4. 添加面包屑导航\n5. 建立相关内容链接",
                expected_impact={"crawl_efficiency": 0.3, "page_authority": 0.2},
                success_rate=0.85,
                effort_level="medium",
                risk_level="low",
                prerequisites=["网站地图", "链接分析工具"],
                related_strategies=["tech_001", "tech_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            # AI引用优化策略
            Strategy(
                strategy_id="ai_001",
                name="增强结构化数据",
                description="添加丰富的结构化数据以帮助AI系统理解内容",
                category="ai_citation",
                subcategory="structured_data",
                implementation="1. 实现Schema.org标记\n2. 添加FAQ结构化数据\n3. 实现HowTo结构化数据\n4. 添加产品/服务标记\n5. 验证结构化数据",
                expected_impact={"ai_citation": 0.35, "rich_results": 0.4},
                success_rate=0.8,
                effort_level="high",
                risk_level="medium",
                prerequisites=["Schema.org知识", "结构化数据测试工具"],
                related_strategies=["ai_002", "ai_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            Strategy(
                strategy_id="ai_002",
                name="优化内容语义丰富度",
                description="提高内容的语义丰富度以增加AI引用概率",
                category="ai_citation",
                subcategory="semantic_optimization",
                implementation="1. 使用同义词和相关术语\n2. 添加定义和解释\n3. 包含数据和统计\n4. 使用列表和表格\n5. 添加引用和来源",
                expected_impact={"semantic_richness": 0.3, "ai_citation": 0.25},
                success_rate=0.7,
                effort_level="medium",
                risk_level="low",
                prerequisites=["语义分析工具", "内容编辑能力"],
                related_strategies=["ai_001", "ai_003"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            ),
            Strategy(
                strategy_id="ai_003",
                name="创建AI友好内容格式",
                description="格式化内容以便AI系统更容易提取和引用",
                category="ai_citation",
                subcategory="content_formatting",
                implementation="1. 使用清晰的标题层级\n2. 添加摘要和要点\n3. 使用定义列表\n4. 添加时间线和流程图\n5. 使用代码块展示数据",
                expected_impact={"ai_extraction": 0.4, "content_clarity": 0.35},
                success_rate=0.75,
                effort_level="medium",
                risk_level="low",
                prerequisites=["内容格式化工具", "AI内容分析"],
                related_strategies=["ai_001", "ai_002"],
                created_at=now,
                last_used=now,
                usage_count=0,
                average_effectiveness=0.0
            )
        ]
    
    def get_strategies_for_problems(self, problems: List[Dict]) -> List[Dict]:
        """根据问题获取相关策略"""
        print("   🔍 匹配策略到问题...")
        
        matched_strategies = []
        problem_categories = set()
        
        # 提取问题类别
        for problem in problems:
            problem_categories.add(problem.get("category", ""))
        
        # 匹配策略
        for strategy in self.strategies.values():
            if strategy.category in problem_categories:
                # 计算策略与问题的匹配度
                match_score = self._calculate_match_score(strategy, problems)
                
                if match_score > 0.3:  # 匹配度阈值
                    strategy_dict = asdict(strategy)
                    strategy_dict["match_score"] = match_score
                    matched_strategies.append(strategy_dict)
        
        # 按匹配度排序
        matched_strategies.sort(key=lambda s: s.get("match_score", 0), reverse=True)
        
        print(f"   ✅ 匹配到{len(matched_strategies)}个相关策略")
        return matched_strategies
    
    def _calculate_match_score(self, strategy: Strategy, problems: List[Dict]) -> float:
        """计算策略与问题的匹配度"""
        match_score = 0.0
        
        for problem in problems:
            # 类别匹配
            if strategy.category == problem.get("category"):
                match_score += 0.3
            
            # 子类别匹配（如果有）
            problem_desc = problem.get("description", "").lower()
            strategy_desc = strategy.description.lower()
            
            # 关键词匹配
            common_keywords = self._find_common_keywords(problem_desc, strategy_desc)
            match_score += len(common_keywords) * 0.1
            
            # 严重性加权
            severity = problem.get("severity", 0.5)
            match_score *= (1 + severity)
        
        # 考虑策略成功率
        match_score *= strategy.success_rate
        
        # 考虑使用历史
        if strategy.usage_count > 0 and strategy.average_effectiveness > 0:
            match_score *= (1 + strategy.average_effectiveness)
        
        return min(match_score, 1.0)
    
    def _find_common_keywords(self, text1: str, text2: str) -> List[str]:
        """查找共同关键词"""
        # 简单实现：按空格分割并找共同单词
        words1 = set(text1.split())
        words2 = set(text2.split())
        return list(words1.intersection(words2))
    
    def update_based_on_results(self, execution_results: List[Dict], monitoring_results: Dict[str, Any]):
        """基于结果更新策略库"""
        print("   🔄 基于结果更新策略库...")
        
        updates_made = 0
        
        for execution in execution_results:
            strategy_id = execution.get("strategy_id")
            if strategy_id and strategy_id in self.strategies:
                strategy = self.strategies[strategy_id]
                
                # 更新使用次数
                strategy.usage_count += 1
                strategy.last_used = datetime.now().isoformat()
                
                # 计算效果分数
                effectiveness = self._calculate_effectiveness(execution, monitoring_results)
                if effectiveness > 0:
                    # 更新平均效果
                    if strategy.average_effectiveness == 0:
                        strategy.average_effectiveness = effectiveness
                    else:
                        strategy.average_effectiveness = (
                            strategy.average_effectiveness * (strategy.usage_count - 1) + effectiveness
                        ) / strategy.usage_count
                    
                    # 根据效果调整成功率
                    if effectiveness > 0.7:
                        strategy.success_rate = min(1.0, strategy.success_rate * 1.1)
                    elif effectiveness < 0.3:
                        strategy.success_rate = max(0.1, strategy.success_rate * 0.9)
                
                updates_made += 1
        
        if updates_made > 0:
            self._save_strategies()
            print(f"   ✅ 更新{updates_made}个策略")
        
        # 记录执行
        self._record_executions(execution_results, monitoring_results)
    
    def _calculate_effectiveness(self, execution: Dict, monitoring_results: Dict[str, Any]) -> float:
        """计算策略效果"""
        # 简单实现：基于监控结果计算
        # 实际应该根据具体指标变化计算
        
        # 如果有明确的监控数据
        if "effectiveness" in monitoring_results:
            return monitoring_results.get("effectiveness", 0.5)
        
        # 默认效果
        return 0.5
    
    def _record_executions(self, execution_results: List[Dict], monitoring_results: Dict[str, Any]):
        """记录策略执行"""
        try:
            # 加载现有记录
            if self.executions_file.exists():
                with open(self.executions_file, 'r', encoding='utf-8') as f:
                    all_executions = json.load(f)
            else:
                all_executions = {}
            
            # 添加新记录
            for execution in execution_results:
                strategy_id = execution.get("strategy_id")
                if not strategy_id:
                    continue
                
                execution_record = StrategyExecution(
                    execution_id=f"exec_{int(datetime.now().timestamp())}_{hashlib.md5(str(execution).encode()).hexdigest()[:8]}",
                    strategy_id=strategy_id,
                    timestamp=datetime.now().isoformat(),
                    website_url="https://qinzhengzhanghao-oss.github.io/medical-tourism-website/",
                    parameters=execution.get("parameters", {}),
                    result=execution.get("result", {}),
                    effectiveness_score=self._calculate_effectiveness(execution, monitoring_results),
                    learned_lessons=self._extract_lessons(execution, monitoring_results)
                )
                
                if strategy_id not in all_executions:
                    all_executions[strategy_id] = []
                
                all_executions[strategy_id].append(asdict(execution_record))
                
                # 只保留最近20条记录
                if len(all_executions[strategy_id]) > 20:
                    all_executions[strategy_id] = all_executions[strategy_id][-20:]
            
            # 保存记录
            with open(self.executions_file, 'w', encoding='utf-8') as f:
                json.dump(all_executions, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"   ⚠️ 记录策略执行失败: {