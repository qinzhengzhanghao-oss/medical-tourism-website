# 医疗旅游网站设计系统指南 v2.0

## 🎯 概述

本设计系统是基于智能体第二阶段优化成果创建的统一设计标准，确保网站设计一致性、可维护性和用户体验。

## 📊 设计系统核心

### 1. 颜色系统

#### 主色调（专业医疗蓝）
- `--color-primary: #1a73e8` - 主要按钮、重要链接
- `--color-primary-dark: #0d47a1` - 悬停状态
- `--color-primary-light: #4285f4` - 次要元素

#### 辅助色（信任绿色）
- `--color-secondary: #34a853` - 成功状态、确认按钮
- `--color-secondary-dark: #0d8043` - 深色背景
- `--color-secondary-light: #81c995` - 浅色背景

#### 强调色（温暖橙色）
- `--color-accent: #fbbc04` - 警告、重要提示
- `--color-accent-dark: #e37400` - 深色强调
- `--color-accent-light: #fdd663` - 浅色强调

#### 使用原则：
- **一致性**：全站使用统一颜色
- **层次感**：通过颜色深浅建立视觉层次
- **可访问性**：确保颜色对比度符合WCAG标准

### 2. 字体系统

#### 字体家族：
- **基础字体**：`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **标题字体**：`'Helvetica Neue', Arial, sans-serif`
- **等宽字体**：`'SF Mono', Monaco, 'Courier New', monospace`

#### 字体大小（响应式）：
```css
--font-size-xs: 0.75rem;    /* 12px - 辅助文本 */
--font-size-sm: 0.875rem;   /* 14px - 正文小字 */
--font-size-base: 1rem;     /* 16px - 基础正文 */
--font-size-lg: 1.125rem;   /* 18px - 强调正文 */
--font-size-xl: 1.25rem;    /* 20px - 小标题 */
--font-size-2xl: 1.5rem;    /* 24px - 中标题 */
--font-size-3xl: 1.875rem;  /* 30px - 大标题 */
--font-size-4xl: 2.25rem;   /* 36px - 特大标题 */
```

#### 使用原则：
- **层次清晰**：标题 > 正文 > 辅助文本
- **响应式**：根据屏幕尺寸调整字体大小
- **可读性**：确保足够的行高和字间距

### 3. 间距系统

#### 基础单位：4px（--spacing-unit）
```css
--spacing-1: 4px   /* 微小间距 */
--spacing-2: 8px   /* 小间距 */
--spacing-3: 12px  /* 中等间距 */
--spacing-4: 16px  /* 基础间距 */
--spacing-6: 24px  /* 大间距 */
--spacing-8: 32px  /* 超大间距 */
```

#### 使用原则：
- **8点网格**：所有间距基于8px倍数
- **一致性**：相同功能使用相同间距
- **呼吸感**：确保内容有足够空白

### 4. 组件规范

#### 按钮组件：
```html
<!-- 主要按钮 -->
<button class="btn btn-primary">主要操作</button>

<!-- 次要按钮 -->
<button class="btn btn-secondary">次要操作</button>

<!-- 轮廓按钮 -->
<button class="btn btn-outline">轮廓按钮</button>
```

#### 卡片组件：
```html
<div class="card">
  <h3 class="text-xl font-semibold mb-4">卡片标题</h3>
  <p class="text-gray-600">卡片内容...</p>
</div>
```

#### 表单组件：
```html
<div class="form-group">
  <label class="form-label" for="name">姓名</label>
  <input class="form-input" type="text" id="name" placeholder="请输入姓名">
</div>
```

#### 导航组件：
```html
<nav class="navbar">
  <div class="container nav-container">
    <a href="/" class="nav-logo">医疗旅游</a>
    <button class="nav-toggle">
      <span class="nav-toggle-icon"></span>
    </button>
    <ul class="nav-menu">
      <li><a href="/" class="nav-link">首页</a></li>
      <li><a href="/about" class="nav-link">关于我们</a></li>
      <li><a href="/services" class="nav-link">服务</a></li>
    </ul>
  </div>
</nav>
```

### 5. 响应式设计

#### 断点定义：
```css
/* 小屏幕：≥640px */
@media (min-width: 640px) { ... }

/* 中等屏幕：≥768px */
@media (min-width: 768px) { ... }

/* 大屏幕：≥1024px */
@media (min-width: 1024px) { ... }

/* 超大屏幕：≥1280px */
@media (min-width: 1280px) { ... }
```

#### 响应式工具类：
```html
<!-- 移动端隐藏，桌面端显示 -->
<div class="hidden md:block">桌面端内容</div>

<!-- 移动端显示，桌面端隐藏 -->
<div class="block md:hidden">移动端内容</div>

<!-- 响应式网格 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <!-- 列数随屏幕变化 -->
</div>
```

### 6. 工具类系统

#### 排版工具类：
```html
<p class="text-lg font-semibold text-primary">大号强调文本</p>
<p class="text-sm text-gray-600">小号辅助文本</p>
```

#### 间距工具类：
```html
<div class="m-4 p-6">外边距4，内边距6</div>
<div class="mt-2 mb-4 ml-3 mr-5">各方向独立间距</div>
```

#### 布局工具类：
```html
<div class="flex items-center justify-between">
  <div>左对齐</div>
  <div>右对齐</div>
</div>
```

### 7. 最佳实践

#### 设计一致性：
1. **颜色一致**：全站使用设计系统定义的颜色
2. **字体一致**：统一字体家族和大小
3. **间距一致**：使用间距系统定义的距离
4. **组件一致**：复用标准组件，不重复造轮子

#### 可访问性：
1. **颜色对比度**：文本与背景对比度至少4.5:1
2. **键盘导航**：所有交互元素支持键盘访问
3. **屏幕阅读器**：使用语义化HTML和ARIA属性
4. **焦点指示**：清晰的可视化焦点状态

#### 性能优化：
1. **CSS优化**：使用工具类减少自定义CSS
2. **图片优化**：响应式图片和懒加载
3. **JavaScript优化**：按需加载和代码分割
4. **缓存策略**：合理使用浏览器缓存

### 8. 开发工作流

#### 新页面开发：
1. **引入设计系统**：`<link rel="stylesheet" href="design-system.css">`
2. **使用标准组件**：复用现有组件
3. **遵循设计规范**：颜色、字体、间距
4. **响应式测试**：测试所有断点
5. **可访问性检查**：确保符合无障碍标准

#### 现有页面改造：
1. **分析当前设计**：识别不符合规范的地方
2. **逐步替换**：分批替换自定义样式
3. **测试验证**：确保功能不受影响
4. **性能评估**：检查性能改进

### 9. 维护和更新

#### 设计系统更新：
1. **版本控制**：设计系统有明确版本号
2. **变更日志**：记录所有设计变更
3. **向后兼容**：确保更新不影响现有页面
4. **团队沟通**：及时通知设计系统变更

#### 质量保证：
1. **代码审查**：检查设计系统使用情况
2. **视觉测试**：确保设计一致性
3. **性能监控**：跟踪页面性能指标
4. **用户反馈**：收集用户对设计的反馈

## 🚀 快速开始

### 1. 引入设计系统：
```html
<link rel="stylesheet" href="design-system.css">
```

### 2. 使用基础结构：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
  <link rel="stylesheet" href="design-system.css">
</head>
<body>
  <div class="container">
    <!-- 页面内容 -->
  </div>
</body>
</html>
```

### 3. 应用设计原则：
- 使用设计系统变量（`var(--color-primary)`）
- 使用工具类（`.text-primary`, `.p-4`）
- 使用标准组件（`.btn`, `.card`）
- 遵循响应式设计

## 📞 支持和反馈

### 问题报告：
1. **设计不一致**：报告不符合设计系统的地方
2. **组件缺失**：请求新的标准组件
3. **使用困难**：反馈设计系统使用问题
4. **改进建议**：提出设计系统改进建议

### 资源链接：
- **设计系统文件**：`design-system.css`
- **组件示例**：查看现有页面代码
- **设计规范**：本指南文档
- **问题跟踪**：GitHub Issues

---
**版本**：v2.0  
**创建时间**：2026-04-02  
**基于**：智能体第二阶段优化成果  
**目标**：确保医疗旅游网站设计一致性和专业性