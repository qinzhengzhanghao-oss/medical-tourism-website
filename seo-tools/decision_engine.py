"""
L4-SEO智能体 - 决策引擎模块
基于真实数据的L4级决策系统
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import statistics

@dataclass
class Problem:
    """识别的问题"""
    problem_id: str
    category: str  # performance, content, technical, ai_citation
    severity: float  # 0-1
    description: str
    metric_name: str
    current_value: float
    target_value: float
    impact_score: float  # 对SEO/AI引用的影响程度
    confidence: float  # 问题识别置信度

@dataclass
class StrategyRecommendation:
    """策略推荐"""
    strategy_id: str
    problem_id: str
    name: str
    description: str
    implementation: str
    expected_improvement: float  # 预期改进百分比
    confidence_score: float  # 策略置信度
    effort_level: str  # low, medium, high
    risk_level: str  # low, medium, high
    priority: int  # 优先级（1-10）

class DecisionEngine:
    """L4数据驱动决策引擎"""
    
    def __init__(self):
        self.workspace = Path("/Users/qinzheng/.openclaw/workspace")
        self.history_file = self.workspace / "decision_history.json"
        
        # 决策规则库
        self.decision_rules = self._load_decision_rules()
        
        # 初始化历史记录
        self.init_history()
    
    def _load_decision_rules(self) -> Dict[str, Any]:
        """加载决策规则"""
        return {
            "performance": {
                "lcp": {"threshold": 2.5, "severity": 0.8, "impact": 0.9},
                "fid": {"threshold": 100, "severity": 0.7, "impact": 0.8},
                "cls": {"threshold": 0.1, "severity": 0.9, "impact": 0.85}
            },
            "content": {
                "title_length": {"min": 30, "max": 70, "severity": 0.6, "impact": 0.7},
                "description_length": {"min": 120, "max": 160, "severity": 0.5, "impact": 0.6},
                "h1_count": {"min": 1, "max": 1, "severity": 0.8, "impact": 0.9}
            },
            "technical": {
                "image_alt_coverage": {"threshold": 0.9, "severity": 0.4, "impact": 0.5},
                "internal_links": {"threshold": 50, "severity": 0.3, "impact": 0.4},
                "mobile_friendly": {"threshold": 0.8, "severity": 0.9, "impact": 0.95}
            },
            "ai_citation": {
                "semantic_richness": {"threshold": 0.7, "severity": 0.7, "impact": 0.8},
                "structured_data": {"threshold": 0.6, "severity": 0.6, "impact": 0.7},
                "citation_frequency": {"threshold": 0.1, "severity": 0.8, "impact": 0.85}
            }
        }
    
    def init_history(self):
        """初始化历史记录"""
        if not self.history_file.exists():
            history = {
                "created_at": datetime.now().isoformat(),
                "total_decisions": 0,
                "successful_decisions": 0,
                "failed_decisions": 0,
                "decision_history": [],
                "problem_patterns": {},
                "strategy_effectiveness": {}
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
    
    def analyze_data(self, data_collection: Dict[str, Any]) -> Dict[str, Any]:
        """分析数据并识别问题"""
        print("   🔍 开始数据分析...")
        
        data_points = data_collection.get("data_points", [])
        problems = self._identify_problems(data_points)
        
        # 问题分类和优先级排序
        categorized_problems = self._categorize_problems(problems)
        prioritized_problems = self._prioritize_problems(categorized_problems)
        
        # 生成分析报告
        analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "total_data_points": len(data_points),
            "problems_identified": len(problems),
            "problem_categories": self._count_problems_by_category(problems),
            "top_problems": prioritized_problems[:5],
            "data_quality": data_collection.get("data_quality", {}),
            "recommended_focus": self._recommend_focus_area(prioritized_problems)
        }
        
        # 保存分析结果
        self._save_analysis(analysis_report)
        
        print(f"   ✅ 数据分析完成，识别{len(problems)}个问题")
        return analysis_report
    
    def _identify_problems(self, data_points: List[Dict]) -> List[Problem]:
        """识别问题"""
        problems = []
        
        for point in data_points:
            metric_type = point.get("metric_type", "")
            metric_name = point.get("metric_name", "")
            value = point.get("value", 0)
            
            # 根据指标类型应用规则
            if metric_type in self.decision_rules:
                category_rules = self.decision_rules[metric_type]
                
                for rule_key, rule in category_rules.items():
                    if rule_key.lower() in metric_name.lower():
                        problem = self._check_rule_violation(
                            rule_key, rule, value, metric_name, metric_type
                        )
                        if problem:
                            problems.append(problem)
        
        return problems
    
    def _check_rule_violation(self, rule_key: str, rule: Dict, value: float, 
                             metric_name: str, metric_type: str) -> Optional[Problem]:
        """检查规则违反"""
        problem = None
        
        if "threshold" in rule:
            # 阈值检查（大于阈值有问题）
            if value > rule["threshold"]:
                severity = min(1.0, (value - rule["threshold"]) / rule["threshold"] * rule["severity"])
                problem = Problem(
                    problem_id=f"prob_{rule_key}_{int(datetime.now().timestamp())}",
                    category=metric_type,
                    severity=severity,
                    description=f"{metric_name}超出阈值（当前: {value:.2f}, 阈值: {rule['threshold']}）",
                    metric_name=metric_name,
                    current_value=value,
                    target_value=rule["threshold"] * 0.8,  # 目标设为阈值的80%
                    impact_score=rule["impact"],
                    confidence=0.8
                )
        
        elif "min" in rule and "max" in rule:
            # 范围检查
            if value < rule["min"] or value > rule["max"]:
                if value < rule["min"]:
                    deviation = (rule["min"] - value) / rule["min"]
                    target = rule["min"]
                else:
                    deviation = (value - rule["max"]) / rule["max"]
                    target = rule["max"]
                
                severity = min(1.0, deviation * rule["severity"])
                problem = Problem(
                    problem_id=f"prob_{rule_key}_{int(datetime.now().timestamp())}",
                    category=metric_type,
                    severity=severity,
                    description=f"{metric_name}超出范围（当前: {value:.2f}, 范围: {rule['min']}-{rule['max']}）",
                    metric_name=metric_name,
                    current_value=value,
                    target_value=target,
                    impact_score=rule["impact"],
                    confidence=0.7
                )
        
        return problem
    
    def _categorize_problems(self, problems: List[Problem]) -> Dict[str, List[Problem]]:
        """问题分类"""
        categorized = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        for problem in problems:
            # 根据严重性和影响计算优先级分数
            priority_score = problem.severity * problem.impact_score
            
            if priority_score > 0.7:
                categorized["critical"].append(problem)
            elif priority_score > 0.5:
                categorized["high"].append(problem)
            elif priority_score > 0.3:
                categorized["medium"].append(problem)
            else:
                categorized["low"].append(problem)
        
        return categorized
    
    def _prioritize_problems(self, categorized_problems: Dict[str, List[Problem]]) -> List[Problem]:
        """问题优先级排序"""
        all_problems = []
        
        # 按类别顺序添加
        for category in ["critical", "high", "medium", "low"]:
            problems = categorized_problems.get(category, [])
            # 在每个类别内按严重性排序
            problems.sort(key=lambda p: p.severity * p.impact_score, reverse=True)
            all_problems.extend(problems)
        
        return all_problems
    
    def _count_problems_by_category(self, problems: List[Problem]) -> Dict[str, int]:
        """按类别统计问题"""
        categories = {}
        for problem in problems:
            category = problem.category
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _recommend_focus_area(self, problems: List[Problem]) -> str:
        """推荐重点优化领域"""
        if not problems:
            return "数据质量提升"
        
        # 计算各领域的问题严重性总分
        category_scores = {}
        for problem in problems[:10]:  # 只看前10个问题
            score = problem.severity * problem.impact_score
            category_scores[problem.category] = category_scores.get(problem.category, 0) + score
        
        if not category_scores:
            return "数据收集优化"
        
        # 返回分数最高的领域
        focus_area = max(category_scores.items(), key=lambda x: x[1])[0]
        
        # 映射到友好名称
        name_map = {
            "performance": "页面性能",
            "content": "内容质量",
            "technical": "技术SEO",
            "ai_citation": "AI引用优化"
        }
        
        return name_map.get(focus_area, focus_area)
    
    def evaluate_strategies(self, strategies: List[Dict], data_collection: Dict[str, Any]) -> List[Dict]:
        """评估策略"""
        print("   🧠 开始策略评估...")
        
        evaluated_strategies = []
        
        for strategy in strategies:
            evaluation = self._evaluate_single_strategy(strategy, data_collection)
            evaluated_strategies.append(evaluation)
        
        # 按置信度排序
        evaluated_strategies.sort(key=lambda s: s.get("confidence_score", 0), reverse=True)
        
        print(f"   ✅ 策略评估完成，评估{len(evaluated_strategies)}个策略")
        return evaluated_strategies
    
    def _evaluate_single_strategy(self, strategy: Dict, data_collection: Dict[str, Any]) -> Dict:
        """评估单个策略"""
        # 基础评估
        confidence_score = 0.7  # 基础置信度
        
        # 根据策略类型调整置信度
        strategy_type = strategy.get("category", "")
        if strategy_type == "performance":
            # 性能优化通常效果可预测
            confidence_score += 0.1
        elif strategy_type == "content":
            # 内容优化效果较难预测
            confidence_score += 0.05
        
        # 根据历史效果调整（如果有）
        historical_effectiveness = self._get_historical_effectiveness(strategy.get("strategy_id", ""))
        if historical_effectiveness:
            confidence_score = (confidence_score + historical_effectiveness) / 2
        
        # 计算预期改进
        expected_improvement = self._calculate_expected_improvement(strategy, data_collection)
        
        # 评估努力程度
        effort_level = self._assess_effort_level(strategy)
        
        # 评估风险等级
        risk_level = self._assess_risk_level(strategy)
        
        # 计算优先级
        priority = self._calculate_priority(
            confidence_score, expected_improvement, effort_level, risk_level
        )
        
        return {
            **strategy,
            "confidence_score": round(confidence_score, 2),
            "expected_improvement": round(expected_improvement, 2),
            "effort_level": effort_level,
            "risk_level": risk_level,
            "priority": priority,
            "evaluated_at": datetime.now().isoformat()
        }
    
    def _get_historical_effectiveness(self, strategy_id: str) -> Optional[float]:
        """获取历史效果数据"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            effectiveness_data = history.get("strategy_effectiveness", {})
            return effectiveness_data.get(strategy_id, {}).get("average_effectiveness")
            
        except Exception:
            return None
    
    def _calculate_expected_improvement(self, strategy: Dict, data_collection: Dict[str, Any]) -> float:
        """计算预期改进"""
        base_improvement = 0.15  # 基础改进率
        
        # 根据策略类型调整
        strategy_type = strategy.get("category", "")
        if strategy_type == "performance":
            base_improvement = 0.20  # 性能优化通常效果明显
        elif strategy_type == "ai_citation":
            base_improvement = 0.25  # AI引用优化可能有较大提升空间
        
        # 根据数据质量调整
        data_quality = data_collection.get("data_quality", {}).get("score", 50)
        quality_factor = data_quality / 100
        
        # 根据策略置信度调整
        strategy_confidence = strategy.get("success_rate", 0.7)
        
        expected = base_improvement * quality_factor * strategy_confidence
        return min(expected, 0.5)  # 最大预期改进50%
    
    def _assess_effort_level(self, strategy: Dict) -> str:
        """评估努力程度"""
        implementation = strategy.get("implementation", "")
        
        # 简单启发式评估
        if any(word in implementation.lower() for word in ["简单", "快速", "微调", "调整"]):
            return "low"
        elif any(word in implementation.lower() for word in ["重构", "重写", "重建", "大量"]):
            return "high"
        else:
            return "medium"
    
    def _assess_risk_level(self, strategy: Dict) -> str:
        """评估风险等级"""
        strategy_type = strategy.get("category", "")
        
        # 风险评估规则
        risk_rules = {
            "technical": "medium",  # 技术修改可能有风险
            "content": "low",       # 内容修改风险较低
            "performance": "low",   # 性能优化风险低
            "ai_citation": "low"    # AI引用优化风险低
        }
        
        return risk_rules.get(strategy_type, "medium")
    
    def _calculate_priority(self, confidence: float, improvement: float, 
                           effort: str, risk: str) -> int:
        """计算优先级（1-10）"""
        # 基础分数
        base_score = confidence * improvement * 10
        
        # 努力程度调整
        effort_factors = {"low": 1.2, "medium": 1.0, "high": 0.8}
        base_score *= effort_factors.get(effort, 1.0)
        
        # 风险等级调整
        risk_factors = {"low": 1.1, "medium": 1.0, "high": 0.9}
        base_score *= risk_factors.get(risk, 1.0)
        
        # 转换为1-10的优先级
        priority = min(10, max(1, int(base_score)))
        return priority
    
    def _save_analysis(self, analysis_report: Dict[str, Any]):
        """保存分析结果"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # 添加分析记录
            if "analyses" not in history:
                history["analyses"] = []
            
            history["analyses"].append(analysis_report)
            history["total_decisions"] = len(history["analyses"])
            
            # 只保留最近50条记录
            if len(history["analyses"]) > 50:
                history["analyses"] = history["analyses"][-50:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"   ⚠️ 保存分析结果失败: {str(e)}")
    
    def get_next_recommendations(self) -> List[str]:
        """获取下一步推荐"""
        recommendations = []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            analyses = history.get("analyses", [])
            if not analyses:
                return ["执行首次数据分析", "收集更多数据源", "建立基准指标"]
            
            # 分析最近的分析结果
            recent_analyses = analyses[-5:] if len(analyses) >= 5 else analyses
            
            # 检查常见问题模式
            problem_patterns = {}
            for analysis in recent_analyses:
                categories = analysis.get("problem_categories", {})
                for category, count in categories