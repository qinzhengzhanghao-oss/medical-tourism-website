# Cross-Channel Task Workflow

目标：让 WebChat、Telegram 等不同入口的任务尽量不丢、不分裂、可追踪。

## 现状判断

- WebChat 默认连接主 session，但 UI 可以切换 session。
- 某些原生命令/特殊入口会使用隔离 session，而不是当前聊天主 session。
- 因此“机器人已连上 Telegram”不等于“Telegram 与 WebChat 自动共享同一个连续上下文”。

## 默认执行规则（立即生效）

1. 凡是以下任务，默认都要落盘：
   - 搜索
   - 潜在客户收集
   - 名单整理
   - 研究结果
   - 输出交付物

2. 每次执行时，至少产出以下两类记录：
   - `deliverables/` 下的结果文件
   - `memory/YYYY-MM-DD.md` 下的任务摘要

3. 每次任务完成后，回复里必须包含：
   - 是否完成
   - 产物文件路径
   - 如果未完成，卡在哪一步

4. 跨端继续任务前，优先依据文件而不是纯聊天上下文。

## 推荐使用方式

### 用户侧
- 在任一端发任务时，尽量带一个短任务名。
  - 例：`任务：IG牙医潜客搜索（Austin）`
- 继续之前任务时，直接说任务名或文件名。
  - 例：`继续 IG牙医潜客搜索（Austin）`

### 助手侧
- 收到任务后，先判断是否属于“必须落盘”的任务类型。
- 若是：
  - 创建/更新 deliverable 文件
  - 在当天 memory 中追加摘要
  - 回复中回传文件路径

## 诊断结论

当前更像是“多入口、多 session、无强制落盘”导致的任务分裂，不是单纯模型短时失忆。

## 后续排查建议

1. 检查 Telegram 当前是否固定到同一主 session。
2. 检查是否使用了 native commands / isolated sessions。
3. 统一把关键任务的最终结果写入 workspace。
