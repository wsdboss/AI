## 需求分析

用户提出了三个需求：
1. 修复原来的HTTP发送请求tab不显示的问题
2. 支持WebSocket接口关闭和开启
3. 在WebSocket请求tab中增加生成的接口连接，并支持复制

## 实现计划

### 1. 修复HTTP发送请求tab不显示问题

**问题原因**：当`currentInterface`为`null`时，`v-if="!currentInterface?.is_websocket"`条件没有正确处理，导致HTTP请求tab不显示

**修复方案**：
- 修改`InterfaceDetailView.vue`中HTTP请求tab的条件渲染逻辑
- 将`v-if="!currentInterface?.is_websocket"`改为`v-if="!currentInterface || !currentInterface?.is_websocket"`

### 2. 支持WebSocket接口关闭和开启

**当前状态**：已经实现了WebSocket连接的关闭和开启功能
**需要检查**：确保功能正常工作，与后端交互正确

**实现方案**：
- 检查`toggleWebSocketConnection`方法是否正常工作
- 确保连接状态管理正确
- 验证与后端WebSocket服务的交互

### 3. 在WebSocket请求tab中增加生成的接口连接，并支持复制

**实现方案**：
- 在WebSocket请求tab中添加接口连接显示区域
- 生成正确的WebSocket连接URL
- 添加复制功能

**实现步骤**：
1. 在WebSocket请求tab中添加连接显示区域
2. 生成WebSocket连接URL（基于当前页面URL）
3. 添加复制按钮和功能
4. 确保连接URL格式正确

## 涉及文件

- `frontend/views/InterfaceDetailView.vue`

## 详细实现

### 1. 修复HTTP请求tab

**修改位置**：`InterfaceDetailView.vue`第91行
**修改前**：
```vue
<el-tab-pane label="发送请求" name="request" v-if="!currentInterface?.is_websocket">
```
**修改后**：
```vue
<el-tab-pane label="发送请求" name="request" v-if="!currentInterface || !currentInterface?.is_websocket">
```

### 2. WebSocket接口连接显示和复制

**添加位置**：`InterfaceDetailView.vue`WebSocket请求tab中
**添加内容**：
```vue
<!-- WebSocket连接信息 -->
<el-form-item label="WebSocket连接">
  <div class="websocket-url-container">
    <el-input
      v-model="websocketUrl"
      readonly
      placeholder="WebSocket连接URL"
      prefix-icon="el-icon-link"
    ></el-input>
    <el-button type="primary" size="small" @click="copyWebSocketUrl" style="margin-left: 10px;">
      <i class="el-icon-document-copy"></i> 复制
    </el-button>
  </div>
</el-form-item>
```

**添加数据属性**：
```javascript
websocketUrl: '', // WebSocket连接URL
```

**添加计算属性或方法**：
```javascript
// 生成WebSocket连接URL
computed: {
  websocketUrl() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    return `${protocol}//${host}`
  }
}

// 复制WebSocket连接URL
copyWebSocketUrl() {
  navigator.clipboard.writeText(this.websocketUrl)
    .then(() => {
      this.$message.success('WebSocket连接已复制到剪贴板')
    })
    .catch(err => {
      console.error('复制失败:', err)
      this.$message.error('复制失败，请手动复制')
    })
}
```

**添加样式**：
```css
.websocket-url-container {
  display: flex;
  align-items: center;
}
```

## 实现效果

1. **HTTP请求tab**：当没有选择接口或选择的是非WebSocket接口时显示
2. **WebSocket连接管理**：支持连接的开启和关闭，状态实时更新
3. **WebSocket连接显示**：在WebSocket请求tab中显示完整的连接URL，支持一键复制
4. **用户体验**：保持了与原有界面一致的操作习惯和视觉风格

## 测试步骤

1. 启动应用，验证HTTP请求tab是否正常显示
2. 选择一个非WebSocket接口，验证HTTP请求tab显示，WebSocket请求tab不显示
3. 选择一个WebSocket接口，验证WebSocket请求tab显示，HTTP请求tab不显示
4. 测试WebSocket连接的开启和关闭功能
5. 测试WebSocket连接URL的生成和复制功能
6. 验证所有功能正常工作，无错误信息

## 预期结果

- HTTP请求tab和WebSocket请求tab能根据当前接口类型正确切换显示
- WebSocket连接功能正常，状态显示准确
- WebSocket连接URL能正确生成并支持复制
- 整体界面保持一致的视觉风格和操作体验