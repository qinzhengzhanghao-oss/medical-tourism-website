"""
L4-SEO智能体 - AI引用优化器模块
提升页面被AI系统引用概率
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import requests

@dataclass
class AICitationAnalysis:
    """AI引用分析结果"""
    timestamp: str
    website_url: str
    ai_friendliness_score: float  # 0-1
    citation_potential: float  # 0-1
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    structured_data_coverage: float
    semantic_richness: float
    content_clarity: float

@dataclass
class AICitationOptimization:
    """AI引用优化建议"""
    optimization_id: str
    name: str
    description: str
    target_element: str
    implementation: str
    expected_impact: float
    priority: int
    effort_level: str

class AICitationOptimizer:
    """AI引用优化器"""
    
    def __init__(self):
        self.workspace = Path("/Users/qinzheng/.openclaw/workspace")
        self.analysis_file = self.workspace / "ai_citation_analysis.json"
        
        # AI引用特征
        self.ai_preferences = {
            "structured_data": ["schema.org", "json-ld", "microdata", "rdfa"],
            "content_characteristics": ["clear_headings", "definitions", "examples", "data_points", "references"],
            "formatting": ["lists", "tables", "diagrams", "code_blocks", "timelines"],
            "semantic_elements": ["article", "section", "header", "footer", "nav", "aside"]
        }
    
    def analyze_current_state(self, website_url: str) -> Dict[str, Any]:
        """分析当前AI引用状态"""
        print("   🔍 分析AI引用现状...")
        
        # 收集分析数据
        analysis_data = self._collect_analysis_data(website_url)
        
        # 计算各项分数
        structured_data_score = self._analyze_structured_data(analysis_data)
        semantic_richness_score = self._analyze_semantic_richness(analysis_data)
        content_clarity_score = self._analyze_content_clarity(analysis_data)
        
        # 计算总体AI友好度
        ai_friendliness = (
            structured_data_score * 0.4 +
            semantic_richness_score * 0.35 +
            content_clarity_score * 0.25
        )
        
        # 计算引用潜力
        citation_potential = self._calculate_citation_potential(
            structured_data_score, semantic_richness_score, content_clarity_score
        )
        
        # 识别优缺点
        strengths, weaknesses = self._identify_strengths_weaknesses(
            structured_data_score, semantic_richness_score, content_clarity_score
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(strengths, weaknesses)
        
        analysis = AICitationAnalysis(
            timestamp=datetime.now().isoformat(),
            website_url=website_url,
            ai_friendliness_score=round(ai_friendliness, 2),
            citation_potential=round(citation_potential, 2),
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            structured_data_coverage=round(structured_data_score, 2),
            semantic_richness=round(semantic_richness_score, 2),
            content_clarity=round(content_clarity_score, 2)
        )
        
        # 保存分析结果
        self._save_analysis(analysis)
        
        print(f"   ✅ AI引用分析完成，友好度: {ai_friendliness:.2%}")
        return asdict(analysis)
    
    def _collect_analysis_data(self, website_url: str) -> Dict[str, Any]:
        """收集分析数据"""
        # 注意：这里应该实际获取网站内容
        # 由于安全限制，我们使用模拟数据
        
        return {
            "has_structured_data": True,
            "structured_data_types": ["Organization", "WebSite", "BreadcrumbList"],
            "heading_structure": ["h1", "h2", "h2", "h3", "h3", "h2"],
            "content_elements": {
                "lists": 8,
                "tables": 2,
                "images_with_alt": 15,
                "code_blocks": 0,
                "definitions": 3,
                "examples": 5,
                "references": 2
            },
            "semantic_tags": ["header", "nav", "main", "section", "article", "footer"],
            "content_length": 2500,  # 字符数
            "readability_score": 65,  # 可读性分数
            "keyword_density": 2.5,  # 关键词密度
            "internal_links": 12,
            "external_links": 8
        }
    
    def _analyze_structured_data(self, data: Dict[str, Any]) -> float:
        """分析结构化数据"""
        score = 0.0
        
        if data.get("has_structured_data", False):
            score += 0.3
        
        # 检查结构化数据类型
        types = data.get("structured_data_types", [])
        essential_types = ["Organization", "WebSite", "BreadcrumbList"]
        
        for essential_type in essential_types:
            if essential_type in types:
                score += 0.1
        
        # 额外类型加分
        additional_types = ["FAQPage", "HowTo", "Product", "Service", "Event"]
        for add_type in additional_types:
            if add_type in types:
                score += 0.05
        
        return min(score, 1.0)
    
    def _analyze_semantic_richness(self, data: Dict[str, Any]) -> float:
        """分析语义丰富度"""
        score = 0.0
        
        # 标题结构
        headings = data.get("heading_structure", [])
        if len(headings) >= 3:
            score += 0.2
        
        # 检查标题层级合理性
        if self._check_heading_hierarchy(headings):
            score += 0.1
        
        # 语义标签
        semantic_tags = data.get("semantic_tags", [])
        essential_tags = ["header", "main", "footer"]
        
        for tag in essential_tags:
            if tag in semantic_tags:
                score += 0.05
        
        # 内容元素
        content_elements = data.get("content_elements", {})
        
        # 列表
        if content_elements.get("lists", 0) >= 3:
            score += 0.1
        
        # 定义和例子
        if content_elements.get("definitions", 0) >= 2:
            score += 0.1
        if content_elements.get("examples", 0) >= 3:
            score += 0.1
        
        # 引用
        if content_elements.get("references", 0) >= 1:
            score += 0.05
        
        return min(score, 1.0)
    
    def _check_heading_hierarchy(self, headings: List[str]) -> bool:
        """检查标题层级合理性"""
        if not headings:
            return False
        
        # 简单检查：确保h1只有一个，标题层级合理
        h1_count = headings.count("h1")
        if h1_count != 1:
            return False
        
        # 检查层级顺序（简化）
        current_level = 1
        for heading in headings:
            level = int(heading[1]) if len(heading) > 1 else 1
            if level > current_level + 1:  # 不能跳过层级
                return False
            current_level = level
        
        return True
    
    def _analyze_content_clarity(self, data: Dict[str, Any]) -> float:
        """分析内容清晰度"""
        score = 0.0
        
        # 内容长度
        content_length = data.get("content_length", 0)
        if 1500 <= content_length <= 5000:  # 理想长度
            score += 0.3
        elif 800 <= content_length <= 8000:  # 可接受范围
            score += 0.2
        else:
            score += 0.1
        
        # 可读性
        readability = data.get("readability_score", 0)
        if readability >= 60:  # 良好可读性
            score += 0.3
        elif readability >= 40:  # 一般可读性
            score += 0.2
        else:
            score += 0.1
        
        # 关键词密度
        keyword_density = data.get("keyword_density", 0)
        if 1.0 <= keyword_density <= 3.0:  # 理想范围
            score += 0.2
        else:
            score += 0.1
        
        # 链接结构
        internal_links = data.get("internal_links", 0)
        external_links = data.get("external_links", 0)
        
        if internal_links >= 5:
            score += 0.1
        if external_links >= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_citation_potential(self, structured_score: float, 
                                     semantic_score: float, clarity_score: float) -> float:
        """计算引用潜力"""
        # 引用潜力公式
        citation_potential = (
            structured_score * 0.5 +  # 结构化数据最重要
            semantic_score * 0.3 +    # 语义丰富度次之
            clarity_score * 0.2       # 内容清晰度
        )
        
        # 调整因子
        if structured_score > 0.7:
            citation_potential *= 1.2
        if semantic_score > 0.6:
            citation_potential *= 1.1
        
        return min(citation_potential, 1.0)
    
    def _identify_strengths_weaknesses(self, structured_score: float,
                                      semantic_score: float, clarity_score: float) -> tuple:
        """识别优缺点"""
        strengths = []
        weaknesses = []
        
        # 结构化数据
        if structured_score > 0.7:
            strengths.append("良好的结构化数据覆盖")
        elif structured_score < 0.3:
            weaknesses.append("缺乏结构化数据")
        else:
            weaknesses.append("结构化数据需要增强")
        
        # 语义丰富度
        if semantic_score > 0.7:
            strengths.append("丰富的语义内容")
        elif semantic_score < 0.3:
            weaknesses.append("语义内容不足")
        else:
            weaknesses.append("语义丰富度可提升")
        
        # 内容清晰度
        if clarity_score > 0.7:
            strengths.append("清晰易读的内容")
        elif clarity_score < 0.3:
            weaknesses.append("内容可读性需要改进")
        
        # 如果没有识别到优缺点，添加通用建议
        if not strengths:
            strengths.append("具备基础AI友好特征")
        if not weaknesses:
            weaknesses.append("有进一步提升AI引用概率的空间")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, strengths: List[str], weaknesses: List[str]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 基于弱点生成建议
        weakness_map = {
            "缺乏结构化数据": "实现Schema.org结构化数据标记",
            "结构化数据需要增强": "添加更多类型的结构化数据（如FAQ、HowTo）",
            "语义内容不足": "增加定义、例子和相关术语解释",
            "语义丰富度可提升": "使用更多语义HTML标签和内容元素",
            "内容可读性需要改进": "优化内容结构和语言表达",
            "有进一步提升AI引用概率的空间": "实施综合AI引用优化策略"
        }
        
        for weakness in weaknesses:
            if weakness in weakness_map:
                recommendations.append(weakness_map[weakness])
        
        # 添加通用建议
        general_recommendations = [
            "添加FAQ结构化数据以回答常见问题",
            "使用HowTo结构化数据展示操作步骤",
            "增加数据点和统计信息",
            "添加引用和来源信息",
            "使用列表和表格组织信息",
            "优化图片ALT文本包含关键词"
        ]
        
        # 添加2-3个通用建议
        recommendations.extend(general_recommendations[:3])
        
        return recommendations
    
    def optimize_for_ai(self, weaknesses: List[str]) -> List[Dict[str, Any]]:
        """生成AI引用优化方案"""
        print("   🛠️ 生成AI引用优化方案...")
        
        optimizations = []
        
        # 根据弱点生成具体优化
        for weakness in weaknesses:
            if "结构化数据" in weakness:
                optimizations.extend(self._create_structured_data_optimizations())
            elif "语义" in weakness:
                optimizations.extend(self._create_semantic_optimizations())
            elif "内容" in weakness or "可读性" in weakness:
                optimizations.extend(self._create_content_optimizations())
        
        # 添加通用优化
        if not optimizations:
            optimizations.extend(self._create_general_optimizations())
        
        # 限制数量并排序
        optimizations = optimizations[:10]  # 最多10个优化
        optimizations.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        print(f"   ✅ 生成{len(optimizations)}个AI引用优化方案")
        return optimizations
    
    def _create_structured_data_optimizations(self) -> List[Dict[str, Any]]:
        """创建结构化数据优化"""
        return [
            {
                "optimization_id": "ai_sd_001",
                "name": "实现FAQ结构化数据",
                "description": "添加FAQPage结构化数据以回答常见问题",
                "target_element": "FAQ部分",
                "implementation": "1. 识别常见问题\n2. 创建FAQ页面\n3. 添加FAQPage Schema标记\n4. 验证结构化数据",
                "expected_impact": 0.4,
                "priority": 9,
                "effort_level": "medium"
            },
            {
                "optimization_id": "ai_sd_002",
                "name": "添加HowTo结构化数据",
                "description": "使用HowTo Schema展示服务流程",
                "target_element": "服务流程说明",
                "implementation": "1. 分解服务步骤\n2. 添加步骤说明和图片\n3. 实现HowTo Schema\n4. 测试搜索结果展示",
                "expected_impact": 0.35,
                "priority": 8,
                "effort_level": "medium"
            },
            {
                "optimization_id": "ai_sd_003",
                "name": "增强Organization标记",
                "description": "完善组织信息结构化数据",
                "target_element": "页眉/页脚",
                "implementation": "1. 添加完整组织信息\n2. 包含联系方式\n3. 添加社交媒体链接\n4. 实现Organization Schema",
                "expected_impact": 0.3,
                "priority": 7,
                "effort_level": "low"
            }
        ]
    
    def _create_semantic_optimizations(self) -> List[Dict[str, Any]]:
        """创建语义优化"""
        return [
            {
                "optimization_id": "ai_sem_001",
                "name": "优化标题层级结构",
                "description": "改进标题标签的层级关系",
                "target_element": "所有标题标签",
                "implementation": "1. 确保每个页面只有一个H1\n2. 合理使用H2-H6\n3. 避免跳过标题层级\n4. 使用描述性标题文本",
                "expected_impact": 0.3,
                "priority": 8,
                "effort_level": "low"
            },
            {
                "optimization_id": "ai_sem_002",
                "name": "增加定义和解释",
                "description": "为专业术语添加定义和解释",
                "target_element": "专业术语内容",
                "implementation": "1. 识别专业术语\n2. 添加术语定义\n3. 使用<dfn>标签\n4. 提供简单解释",
                "expected_impact": 0.35,
                "priority": 7,
                "effort_level": "medium"
            },
            {
                "optimization_id": "ai_sem_003",
                "name": "使用语义HTML标签",
                "description": "用语义标签替换通用div标签",
                "target_element": "页面布局",
                "implementation": "1. 识别可语义化的区域\n2. 使用<article>、<section>\n3. 添加<header>、<footer>\n4. 使用<nav>导航",
                "expected_impact": 0.25,
                "priority": 6,
                "effort_level": "medium"
            }
        ]
    
    def _create_content_optimizations(self) -> List[Dict[str, Any]]:
        """创建内容优化"""
        return [
            {
                "optimization_id": "ai_con_001",
                "name": "添加数据点和统计",
                "description": "在内容中添加具体数据和统计信息",
                "target_element": "内容段落",
                "implementation": "1. 收集相关统计数据\n2. 以表格或列表展示\n3. 添加数据来源\n4. 解释数据意义",
                "expected_impact": 0.4,
                "priority": 9,
                "effort_level": "medium"
            },
            {
                "optimization_id": "ai_con_002",
                "name": "优化内容可读性",
                "description": "改进内容结构和语言表达",
                "target_element": "所有文本内容",
                "implementation": "1. 使用短段落\n2. 添加小标题\n3. 使用项目符号\n4. 简化复杂句子",
                "expected_impact": 0.