"""
L4-SEO智能体 - 监控系统模块
智能监控优化效果和系统状态
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import statistics

@dataclass
class MonitoringAlert:
    """监控告警"""
    alert_id: str
    timestamp: str
    alert_type: str  # performance, seo, ai_citation, system
    severity: str  # info, warning, error, critical
    title: str
    description: str
    metric_name: str
    current_value: float
    threshold_value: float
    recommendation: str
    status: str  # active, acknowledged, resolved

@dataclass
class OptimizationEffect:
    """优化效果"""
    effect_id: str
    strategy_id: str
    action_id: str
    timestamp: str
    metric_type: str
    metric_name: str
    before_value: float
    after_value: float
    improvement: float
    confidence: float
    notes: str

class MonitoringSystem:
    """智能监控系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/qinzheng/.openclaw/workspace")
        self.monitoring_dir = self.workspace / "monitoring_data"
        self.monitoring_dir.mkdir(exist_ok=True)
        
        # 文件路径
        self.effects_file = self.monitoring_dir / "optimization_effects.json"
        self.alerts_file = self.monitoring_dir / "monitoring_alerts.json"
        self.metrics_file = self.monitoring_dir / "performance_metrics.json"
        
        # 初始化监控
        self.init_monitoring()
        
        # 监控阈值
        self.thresholds = {
            "performance": {
                "lcp": {"warning": 2.5, "error": 4.0},
                "fid": {"warning": 100, "error": 300},
                "cls": {"warning": 0.1, "error": 0.25}
            },
            "seo": {
                "page_speed": {"warning": 70, "error": 50},
                "mobile_friendly": {"warning": 0.8, "error": 0.6},
                "security": {"warning": 0.7, "error": 0.5}
            },
            "ai_citation": {
                "structured_data": {"warning": 0.5, "error": 0.3},
                "semantic_richness": {"warning": 0.6, "error": 0.4},
                "citation_frequency": {"warning": 0.05, "error": 0.01}
            },
            "system": {
                "failure_rate": {"warning": 0.1, "error": 0.2},
                "response_time": {"warning": 5.0, "error": 10.0},
                "data_quality": {"warning": 70, "error": 50}
            }
        }
    
    def init_monitoring(self):
        """初始化监控"""
        if not self.effects_file.exists():
            with open(self.effects_file, 'w', encoding='utf-8') as f:
                json.dump({"effects": [], "created_at": datetime.now().isoformat()}, f, indent=2)
        
        if not self.alerts_file.exists():
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump({"alerts": [], "created_at": datetime.now().isoformat()}, f, indent=2)
        
        if not self.metrics_file.exists():
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump({"metrics": [], "created_at": datetime.now().isoformat()}, f, indent=2)
    
    def monitor_optimization_effects(self, execution_results: List[Dict], 
                                   baseline_data: Dict[str, Any]) -> Dict[str, Any]:
        """监控优化效果"""
        print("   📈 监控优化效果...")
        
        effects = []
        alerts = []
        
        for execution in execution_results:
            strategy_id = execution.get("strategy_id")
            action_id = execution.get("action_id")
            
            if not strategy_id or not action_id:
                continue
            
            # 模拟效果监控（实际应该比较前后数据）
            effect = self._simulate_effect_monitoring(strategy_id, action_id, baseline_data)
            if effect:
                effects.append(effect)
                
                # 检查是否需要告警
                alert = self._check_for_alert(effect)
                if alert:
                    alerts.append(alert)
        
        # 保存效果记录
        if effects:
            self._save_effects(effects)
        
        # 保存告警
        if alerts:
            self._save_alerts(alerts)
        
        # 生成监控报告
        monitoring_report = {
            "timestamp": datetime.now().isoformat(),
            "effects_monitored": len(effects),
            "alerts_generated": len(alerts),
            "average_improvement": self._calculate_average_improvement(effects),
            "effectiveness_summary": self._summarize_effectiveness(effects),
            "recommendations": self._generate_monitoring_recommendations(effects, alerts)
        }
        
        print(f"   ✅ 监控完成，记录{len(effects)}个效果，生成{len(alerts)}个告警")
        return monitoring_report
    
    def _simulate_effect_monitoring(self, strategy_id: str, action_id: str, 
                                  baseline_data: Dict[str, Any]) -> Optional[OptimizationEffect]:
        """模拟效果监控"""
        # 注意：实际实现应该比较优化前后的真实数据
        # 这里使用模拟数据
        
        # 根据策略类型确定监控指标
        strategy_type = strategy_id.split("_")[0] if "_" in strategy_id else "general"
        
        metric_mapping = {
            "perf": ("performance", "页面性能综合得分", 65, 75),
            "content": ("content", "内容质量得分", 70, 80),
            "tech": ("technical", "技术SEO得分", 60, 70),
            "ai": ("ai_citation", "AI引用友好度", 55, 70)
        }
        
        metric_info = metric_mapping.get(strategy_type, ("general", "综合得分", 50, 60))
        
        metric_type, metric_name, before_value, after_value = metric_info
        
        # 添加一些随机性
        import random
        improvement = random.uniform(0.05, 0.25)  # 5-25%的改进
        after_value = before_value * (1 + improvement)
        
        effect = OptimizationEffect(
            effect_id=f"effect_{action_id}",
            strategy_id=strategy_id,
            action_id=action_id,
            timestamp=datetime.now().isoformat(),
            metric_type=metric_type,
            metric_name=metric_name,
            before_value=round(before_value, 2),
            after_value=round(after_value, 2),
            improvement=round(improvement * 100, 2),  # 转换为百分比
            confidence=0.7,  # 置信度
            notes=f"策略 {strategy_id} 的效果监控"
        )
        
        return effect
    
    def _check_for_alert(self, effect: OptimizationEffect) -> Optional[MonitoringAlert]:
        """检查是否需要告警"""
        # 检查改进是否达到预期
        expected_improvement = 10.0  # 预期改进10%
        
        if effect.improvement < expected_improvement * 0.5:  # 低于预期50%
            alert = MonitoringAlert(
                alert_id=f"alert_{effect.effect_id}",
                timestamp=datetime.now().isoformat(),
                alert_type=effect.metric_type,
                severity="warning",
                title=f"优化效果低于预期: {effect.metric_name}",
                description=f"策略 {effect.strategy_id} 的改进仅为{effect.improvement}%，低于预期{expected_improvement}%",
                metric_name=effect.metric_name,
                current_value=effect.improvement,
                threshold_value=expected_improvement,
                recommendation="检查策略实施或调整预期",
                status="active"
            )
            return alert
        
        # 检查是否有负面效果
        if effect.improvement < 0:
            alert = MonitoringAlert(
                alert_id=f"alert_{effect.effect_id}_negative",
                timestamp=datetime.now().isoformat(),
                alert_type=effect.metric_type,
                severity="error",
                title=f"优化产生负面效果: {effect.metric_name}",
                description=f"策略 {effect.strategy_id} 导致{effect.metric_name}下降{abs(effect.improvement)}%",
                metric_name=effect.metric_name,
                current_value=effect.improvement,
                threshold_value=0,
                recommendation="立即回滚并检查策略",
                status="active"
            )
            return alert
        
        return None
    
    def _save_effects(self, effects: List[OptimizationEffect]):
        """保存效果记录"""
        try:
            with open(self.effects_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for effect in effects:
                data["effects"].append(asdict(effect))
            
            # 只保留最近500条记录
            if len(data["effects"]) > 500:
                data["effects"] = data["effects"][-500:]
            
            with open(self.effects_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"   ⚠️ 保存效果记录失败: {str(e)}")
    
    def _save_alerts(self, alerts: List[MonitoringAlert]):
        """保存告警"""
        try:
            with open(self.alerts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for alert in alerts:
                data["alerts"].append(asdict(alert))
            
            # 只保留最近200条告警
            if len(data["alerts"]) > 200:
                data["alerts"] = data["alerts"][-200:]
            
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"   ⚠️ 保存告警失败: {str(e)}")
    
    def _calculate_average_improvement(self, effects: List[OptimizationEffect]) -> float:
        """计算平均改进"""
        if not effects:
            return 0.0
        
        improvements = [effect.improvement for effect in effects]
        return round(statistics.mean(improvements), 2)
    
    def _summarize_effectiveness(self, effects: List[OptimizationEffect]) -> Dict[str, Any]:
        """总结效果"""
        if not effects:
            return {"status": "无数据", "effectiveness": "未知"}
        
        # 按类型分组
        type_groups = {}
        for effect in effects:
            metric_type = effect.metric_type
            if metric_type not in type_groups:
                type_groups[metric_type] = []
            type_groups[metric_type].append(effect.improvement)
        
        # 计算各类型平均改进
        type_effectiveness = {}
        for metric_type, improvements in type_groups.items():
            type_effectiveness[metric_type] = round(statistics.mean(improvements), 2)
        
        # 总体评估
        all_improvements = [effect.improvement for effect in effects]
        avg_improvement = statistics.mean(all_improvements)
        
        effectiveness_status = "优秀"
        if avg_improvement < 5:
            effectiveness_status = "需要改进"
        elif avg_improvement < 10:
            effectiveness_status = "一般"
        elif avg_improvement < 15:
            effectiveness_status = "良好"
        
        return {
            "status": effectiveness_status,
            "average_improvement": round(avg_improvement, 2),
            "by_type": type_effectiveness,
            "total_effects": len(effects)
        }
    
    def _generate_monitoring_recommendations(self, effects: List[OptimizationEffect], 
                                           alerts: List[MonitoringAlert]) -> List[str]:
        """生成监控建议"""
        recommendations = []
        
        if not effects:
            recommendations.append("暂无优化效果数据，建议执行更多优化")
            return recommendations
        
        # 分析效果
        positive_effects = [e for e in effects if e.improvement > 0]
        negative_effects = [e for e in effects if e.improvement < 0]
        
        if negative_effects:
            recommendations.append(f"发现{len(negative_effects)}个负面效果，建议检查相关策略")
        
        # 分析告警
        if alerts:
            error_alerts = [a for a in alerts if a.severity == "error"]
            warning_alerts = [a for a in alerts if a.severity == "warning"]
            
            if error_alerts:
                recommendations.append(f"有{len(error_alerts)}个错误告警需要立即处理")
            if warning_alerts:
                recommendations.append(f"有{len(warning_alerts)}个警告告警需要注意")
        
        # 效果分布建议
        type_counts = {}
        for effect in effects:
            metric_type = effect.metric_type
            type_counts[metric_type] = type_counts.get(metric_type, 0) + 1
        
        # 检查是否某些类型优化不足
        total_effects = len(effects)
        for metric_type, count in type_counts.items():
            percentage = count / total_effects * 100
            if percentage < 20:  # 少于20%的优化属于该类型
                recommendations.append(f"{metric_type}类型优化较少，建议增加相关策略")
        
        if not recommendations:
            recommendations.append("监控状态良好，继续保持当前优化节奏")
        
        return recommendations
    
    def check_system_health(self) -> Dict[str, Any]:
        """检查系统健康状态"""
        print("   🏥 检查系统健康状态...")
        
        health_checks = {
            "data_collection": self._check_data_collection_health(),
            "decision_engine": self._check_decision_engine_health(),
            "strategy_library": self._check_strategy_library_health(),
            "security_system": self._check_security_system_health(),
            "ai_optimizer": self._check_ai_optimizer_health()
        }
        
        # 总体健康状态
        all_healthy = all(check.get("status") == "healthy" for check in health_checks.values())
        overall_status = "healthy" if all_healthy else "degraded"
        
        # 生成报告
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "component_checks": health_checks,
            "unhealthy_components": [
                name for name, check in health_checks.items() 
                if check.get("status") != "healthy"
            ],
            "recommendations": self._generate_health_recommendations(health_checks)
        }
        
        print(f"   ✅ 系统健康检查完成，状态: {overall_status}")
        return health_report
    
    def _check_data_collection_health(self) -> Dict[str, Any]:
        """检查数据收集健康状态"""
        # 简单检查：查看是否有最近的数据
        data_dir = self.workspace / "seo_data"
        if not data_dir.exists():
            return {"status": "unhealthy", "issue": "数据目录不存在", "recommendation": "初始化数据收集系统"}
        
        # 检查数据库文件
        db_file = data_dir / "seo_data.db"
        if not db_file.exists():
            return {"status": "unhealthy", "issue": "数据库文件不存在", "recommendation": "创建数据库"}
        
        # 检查数据新鲜度
        try:
            import sqlite3
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(timestamp) FROM seo_data_points")
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                last_data_time = datetime.fromisoformat(result[0].replace('Z', '+00:00'))
                time_diff = datetime.now() - last_data_time
                
                if time_diff.days > 7:
                    return {
                        "status": "degraded", 
                        "issue": f"数据已{time_diff.days}天未更新",
                        "recommendation": "执行数据收集"
                    }
                
                return {"status": "healthy", "last_update": result[0]}
            else:
                return {"status": "unhealthy", "issue": "无数据记录", "recommendation": "收集初始数据"}
                
        except Exception as e:
            return {"status": "unhealthy", "issue": f"数据库错误: {str(e)}", "recommendation": "修复数据库"}
    
    def _check_decision_engine_health(self) -> Dict[str, Any]:
        """检查决策引擎健康状态"""
        history_file = self.workspace / "decision_history.json"
        
        if not history_file.exists():
            return {"status": "unhealthy", "issue": "决策历史文件不存在", "recommendation": "初始化决策引擎"}
        
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            analyses = data.get("analyses", [])
            if not analyses:
                return {"status": "degraded", "issue": "无决策记录", "recommendation": "执行数据分析"}
            
            # 检查最近决策时间
            last_analysis = analyses[-1]
            last_time = datetime.fromisoformat(last_analysis.get("timestamp", "").replace('Z', '+00:00'))
            time_diff = datetime.now() - last_time
            
