"""
L4-SEO智能体 - 安全追溯系统模块
确保所有优化可追溯、可回滚
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import shutil

@dataclass
class ActionRecord:
    """操作记录"""
    action_id: str
    timestamp: str
    action_type: str  # optimization, rollback, analysis, etc.
    target_element: str
    old_value: str
    new_value: str
    reason: str
    strategy_id: str
    status: str  # pending, executing, completed, failed, rolled_back
    error_message: str = ""
    rollback_action_id: str = ""

@dataclass
class VersionSnapshot:
    """版本快照"""
    snapshot_id: str
    timestamp: str
    description: str
    files_affected: List[str]
    checksum: str
    backup_location: str

class SecuritySystem:
    """安全追溯系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/qinzheng/.openclaw/workspace")
        self.security_dir = self.workspace / "security_logs"
        self.security_dir.mkdir(exist_ok=True)
        
        # 文件路径
        self.actions_file = self.security_dir / "actions.json"
        self.snapshots_file = self.security_dir / "snapshots.json"
        self.rollback_dir = self.security_dir / "rollback_backups"
        self.rollback_dir.mkdir(exist_ok=True)
        
        # 初始化记录
        self.init_records()
    
    def init_records(self):
        """初始化记录文件"""
        if not self.actions_file.exists():
            with open(self.actions_file, 'w', encoding='utf-8') as f:
                json.dump({"actions": [], "created_at": datetime.now().isoformat()}, f, indent=2)
        
        if not self.snapshots_file.exists():
            with open(self.snapshots_file, 'w', encoding='utf-8') as f:
                json.dump({"snapshots": [], "created_at": datetime.now().isoformat()}, f, indent=2)
    
    def log_action(self, action: Any):
        """记录操作"""
        try:
            # 加载现有记录
            with open(self.actions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 添加新记录
            action_dict = asdict(action) if hasattr(action, '__dataclass_fields__') else action
            data["actions"].append(action_dict)
            
            # 只保留最近1000条记录
            if len(data["actions"]) > 1000:
                data["actions"] = data["actions"][-1000:]
            
            # 保存
            with open(self.actions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"   📝 记录操作: {action_dict.get('action_id', '未知')}")
            
        except Exception as e:
            print(f"   ⚠️ 记录操作失败: {str(e)}")
    
    def update_action_status(self, action_id: str, status: str, error_message: str = ""):
        """更新操作状态"""
        try:
            with open(self.actions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 查找并更新操作
            for action in data["actions"]:
                if action.get("action_id") == action_id:
                    action["status"] = status
                    if error_message:
                        action["error_message"] = error_message
                    action["updated_at"] = datetime.now().isoformat()
                    break
            
            with open(self.actions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"   📝 更新操作状态: {action_id} -> {status}")
            
        except Exception as e:
            print(f"   ⚠️ 更新操作状态失败: {str(e)}")
    
    def create_snapshot(self, description: str, files_to_backup: List[str]) -> str:
        """创建版本快照"""
        print(f"   📸 创建版本快照: {description}")
        
        snapshot_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        # 备份文件
        backed_up_files = []
        for file_path in files_to_backup:
            if self._backup_file(file_path, snapshot_id):
                backed_up_files.append(file_path)
        
        # 计算校验和
        checksum = self._calculate_checksum(backed_up_files)
        
        # 创建快照记录
        snapshot = VersionSnapshot(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            description=description,
            files_affected=backed_up_files,
            checksum=checksum,
            backup_location=str(self.rollback_dir / snapshot_id)
        )
        
        # 保存快照记录
        self._save_snapshot(snapshot)
        
        print(f"   ✅ 快照创建完成: {snapshot_id} ({len(backed_up_files)}个文件)")
        return snapshot_id
    
    def _backup_file(self, file_path: str, snapshot_id: str) -> bool:
        """备份单个文件"""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                print(f"   ⚠️ 文件不存在: {file_path}")
                return False
            
            # 创建备份目录
            backup_dir = self.rollback_dir / snapshot_id
            backup_dir.mkdir(exist_ok=True)
            
            # 备份文件
            backup_path = backup_dir / source_path.name
            shutil.copy2(source_path, backup_path)
            
            return True
            
        except Exception as e:
            print(f"   ⚠️ 备份文件失败 {file_path}: {str(e)}")
            return False
    
    def _calculate_checksum(self, files: List[str]) -> str:
        """计算文件校验和"""
        if not files:
            return "empty"
        
        hash_obj = hashlib.sha256()
        for file_path in files:
            try:
                with open(file_path, 'rb') as f:
                    while chunk := f.read(4096):
                        hash_obj.update(chunk)
            except Exception:
                continue
        
        return hash_obj.hexdigest()[:16]
    
    def _save_snapshot(self, snapshot: VersionSnapshot):
        """保存快照记录"""
        try:
            with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data["snapshots"].append(asdict(snapshot))
            
            # 只保留最近100个快照
            if len(data["snapshots"]) > 100:
                data["snapshots"] = data["snapshots"][-100:]
            
            with open(self.snapshots_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"   ⚠️ 保存快照失败: {str(e)}")
    
    def rollback_action(self, action_id: str) -> Dict[str, Any]:
        """回滚操作"""
        print(f"   🔄 尝试回滚操作: {action_id}")
        
        try:
            # 查找操作记录
            with open(self.actions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            action_to_rollback = None
            for action in data["actions"]:
                if action.get("action_id") == action_id:
                    action_to_rollback = action
                    break
            
            if not action_to_rollback:
                return {"success": False, "error": f"未找到操作记录: {action_id}"}
            
            # 检查是否已经回滚
            if action_to_rollback.get("status") == "rolled_back":
                return {"success": False, "error": "操作已回滚"}
            
            # 查找相关快照
            snapshot_id = self._find_snapshot_for_action(action_id)
            if not snapshot_id:
                return {"success": False, "error": "未找到相关快照"}
            
            # 执行回滚
            rollback_result = self._execute_rollback(snapshot_id)
            
            if rollback_result.get("success"):
                # 更新操作状态
                self.update_action_status(action_id, "rolled_back")
                
                # 创建回滚记录
                rollback_action = ActionRecord(
                    action_id=f"rollback_{action_id}",
                    timestamp=datetime.now().isoformat(),
                    action_type="rollback",
                    target_element=action_to_rollback.get("target_element", ""),
                    old_value=action_to_rollback.get("new_value", ""),
                    new_value=action_to_rollback.get("old_value", ""),
                    reason=f"回滚操作: {action_id}",
                    strategy_id=action_to_rollback.get("strategy_id", ""),
                    status="completed"
                )
                self.log_action(rollback_action)
                
                print(f"   ✅ 回滚成功: {action_id}")
                return {"success": True, "snapshot_id": snapshot_id, "files_restored": rollback_result.get("files_restored", 0)}
            else:
                return {"success": False, "error": rollback_result.get("error", "回滚失败")}
            
        except Exception as e:
            print(f"   ❌ 回滚异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _find_snapshot_for_action(self, action_id: str) -> Optional[str]:
        """查找操作相关的快照"""
        try:
            # 简单实现：查找最近的相关快照
            with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            snapshots = data.get("snapshots", [])
            if not snapshots:
                return None
            
            # 返回最新的快照
            return snapshots[-1].get("snapshot_id")
            
        except Exception:
            return None
    
    def _execute_rollback(self, snapshot_id: str) -> Dict[str, Any]:
        """执行回滚"""
        try:
            # 查找快照信息
            with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            snapshot_info = None
            for snapshot in data.get("snapshots", []):
                if snapshot.get("snapshot_id") == snapshot_id:
                    snapshot_info = snapshot
                    break
            
            if not snapshot_info:
                return {"success": False, "error": f"未找到快照: {snapshot_id}"}
            
            # 恢复文件
            backup_dir = Path(snapshot_info.get("backup_location", ""))
            if not backup_dir.exists():
                return {"success": False, "error": f"备份目录不存在: {backup_dir}"}
            
            files_restored = 0
            for backup_file in backup_dir.iterdir():
                if backup_file.is_file():
                    # 恢复文件到原位置
                    target_path = self.workspace / backup_file.name
                    shutil.copy2(backup_file, target_path)
                    files_restored += 1
            
            return {"success": True, "files_restored": files_restored}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def log_execution(self, execution_record: Dict[str, Any]):
        """记录执行"""
        action = ActionRecord(
            action_id=f"exec_{hashlib.md5(str(execution_record).encode()).hexdigest()[:8]}",
            timestamp=datetime.now().isoformat(),
            action_type="execution",
            target_element="workflow",
            old_value="",
            new_value=json.dumps(execution_record.get("result", {}), ensure_ascii=False)[:500],
            reason=execution_record.get("workflow_type", "未知工作流"),
            strategy_id="",
            status="completed"
        )
        self.log_action(action)
    
    def log_error(self, error_record: Dict[str, Any]):
        """记录错误"""
        action = ActionRecord(
            action_id=f"error_{hashlib.md5(str(error_record).encode()).hexdigest()[:8]}",
            timestamp=datetime.now().isoformat(),
            action_type="error",
            target_element="system",
            old_value="",
            new_value=error_record.get("error", "未知错误"),
            reason=error_record.get("workflow_type", "未知工作流"),
            strategy_id="",
            status="failed",
            error_message=error_record.get("error", "")
        )
        self.log_action(action)
    
    def get_risk_assessment(self) -> Dict[str, Any]:
        """获取风险评估"""
        try:
            with open(self.actions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            actions = data.get("actions", [])
            
            # 统计信息
            total_actions = len(actions)
            failed_actions = sum(1 for a in actions if a.get("status") == "failed")
            rolled_back_actions = sum(1 for a in actions if a.get("status") == "rolled_back")
            
            # 计算风险指标
            failure_rate = failed_actions / total_actions if total_actions > 0 else 0
            rollback_rate = rolled_back_actions / total_actions if total_actions > 0 else 0
            
            # 风险评估
            risk_level = "低"
            if failure_rate > 0.2:
                risk_level = "高"
            elif failure_rate > 0.1:
                risk_level = "中"
            
            return {
                "total_actions": total_actions,
                "failed_actions": failed_actions,
                "rolled_back_actions": rolled_back_actions,
                "failure_rate": round(failure_rate, 3),
                "rollback_rate": round(rollback_rate, 3),
                "risk_level": risk_level,
                "recommendations": self._generate_risk_recommendations(failure_rate, rollback_rate)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "risk_level": "未知",
                "recommendations": ["检查安全日志系统"]
            }
    
    def _generate_risk_recommendations(self, failure_rate: float, rollback_rate: float) -> List[str]:
        """生成风险建议"""
        recommendations = []
        
        if failure_rate > 0.15:
            recommendations.append("高失败率，建议检查优化策略的有效性")
        elif failure_rate > 0.05:
            recommendations.append("中等失败率，建议加强策略评估")
        
        if rollback_rate > 0.1:
            recommendations.append("高回滚率，建议改进优化执行过程")
        
        if not recommendations:
            recommendations.append("系统运行稳定，继续保持")
        
        return recommendations
    
    def get_log_count(self) -> int:
        """获取日志数量"""
        try:
            with open(self.actions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return len(data.get("actions", []))
        except Exception:
            return 0
    
    def generate_audit_report(self) -> Dict[str, Any]:
        """生成审计报告"""
        try:
            with open(self.actions_file, 'r', encoding='utf-8') as f:
                actions_data = json.load(f)
            
            with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                snapshots_data = json.load(f)
            
            # 分析活动
            recent_actions = actions_data.get("actions", [])[-50:]  # 最近50个操作
            action_types = {}
            for action in recent_actions:
                action_type = action.get("action_type", "unknown")
                action_types[action_type] = action_types.get(action_type, 0) + 1
            
            # 时间分析
            if recent_actions:
                first_action = recent_actions[0].get("timestamp", "")
                last_action = recent_actions[-1].get("timestamp", "")
            else:
                first_action = last_action = "无记录"
            
            report = {
                "generated_at": datetime.now().isoformat(),
                "audit_period": f"{first_action} 至 {last_action}",
                "summary": {
                    "total_actions": len(actions_data.get("actions", [])),
                    "total_snapshots": len(snapshots_data.get("snapshots", [])),
                    "recent_actions_analyzed": len(recent_actions)
                },
                "activity_analysis": {
                    "action_type_distribution": action_types,
                    "recent_failure_rate": self._calculate_recent_failure_rate(recent_actions),
                    "average_actions_per_day": self._calculate_daily_average(actions_data.get("actions", []))
                },
                "security_assessment": self.get_risk_assessment(),
                "compliance_check": {
                    "traceability": "合规" if len(actions_data.get("actions", [])) > 0 else "不合规",
                    "rollback_capability": "合规" if len(snapshots_data.get("snapshots", [])) > 0 else "不合规",
                    "audit_trail": "合规" if self.actions_file.exists() else "不合规"
                },
                "recommendations": [
                    "定期审查安全日志",
                    "确保所有优化操作都有快照",
                    "监控失败率和回滚率"
                ]
            }
            
            # 保存报告
            report_file = self.security_dir / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S