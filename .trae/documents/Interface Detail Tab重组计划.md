# Interface Detail Tab重组计划

## 目标

1. 将mock配置tab中的默认mock条数功能和保存功能移至响应参数tab中
2. 删除mock配置tab
3. 将"发送请求"和"WebSocket请求"tab合并为"HTTP/WS请求发送"，通过接口类型功能切换显示内容

## 修改内容

### 1. 修改响应参数tab

在响应参数tab中添加mock配置表单，保留原有的mock配置逻辑和数据。

**修改位置**：`frontend/views/InterfaceDetailView.vue` 第69-79行

**修改内容**：
- 在响应参数表格下方添加mock配置表单
- 表单包含默认Mock条数输入框和保存按钮
- 保持原有的`mockConfigForm`数据和`saveMockConfig`方法不变

### 2. 删除mock配置tab

直接移除整个mock配置的el-tab-pane组件。

**修改位置**：`frontend/views/InterfaceDetailView.vue` 第81-93行

**修改内容**：
- 移除`el-tab-pane label="Mock配置" name="mock-config"`整个组件

### 3. 合并发送请求和WebSocket请求tab

将两个tab合并为一个，名称为"HTTP/WS请求发送"，根据接口类型切换显示内容。

**修改位置**：`frontend/views/InterfaceDetailView.vue` 第96-255行

**修改内容**：
- 移除原有的"发送请求"和"WebSocket请求"两个tab
- 添加新的"HTTP/WS请求发送"tab
- 在新tab内部根据`currentInterface?.is_websocket`属性切换显示内容
- 对于HTTP请求，显示原"发送请求"tab的内容
- 对于WebSocket请求，显示原"WebSocket请求"tab的内容

## 代码修改要点

### 响应参数tab修改

```vue
<!-- 响应参数 -->
el-tab-pane label="响应参数" name="responses">
  <div class="detail-section">
    <el-table :data="interfaceResponses" stripe style="width: 100%" v-if="interfaceResponses.length > 0">
      <!-- 表格内容保持不变 -->
    </el-table>
    <el-empty description="暂无响应参数" v-else></el-empty>
    
    <!-- 添加Mock配置表单 -->
    <el-divider>Mock配置</el-divider>
    <el-form :model="mockConfigForm" label-width="120px">
      <el-form-item label="默认Mock条数">
        <el-input-number v-model="mockConfigForm.default_count" :min="1" :max="1000" :step="1"></el-input-number>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveMockConfig">保存配置</el-button>
      </el-form-item>
    </el-form>
  </div>
</el-tab-pane>
```

### 合并请求tab修改

```vue
<!-- HTTP/WS请求发送 -->
el-tab-pane label="HTTP/WS请求发送" name="request-send">
  <div class="detail-section">
    <!-- HTTP请求内容 -->
    <div v-if="!currentInterface?.is_websocket">
      <!-- 原"发送请求"tab内容 -->
    </div>
    
    <!-- WebSocket请求内容 -->
    <div v-else>
      <!-- 原"WebSocket请求"tab内容 -->
    </div>
  </div>
</el-tab-pane>
```

## 预期效果

1. **响应参数tab**：包含响应参数表格和mock配置表单
2. **减少tab数量**：从5个tab减少到4个（接口信息、请求参数、响应参数、HTTP/WS请求发送）
3. **统一请求界面**：通过接口类型开关切换HTTP和WebSocket请求界面，提供一致的用户体验
4. **功能完整保留**：所有原有功能保持不变，只是调整了界面布局

## 风险评估

- **影响范围**：仅涉及InterfaceDetailView.vue文件的界面布局调整，不影响核心功能
- **兼容性**：修改后需要确保所有现有功能正常工作
- **测试要点**：
  - 响应参数tab中的mock配置功能是否正常
  - 接口类型切换时，HTTP/WS请求发送tab内容是否正确切换
  - 原有发送请求和WebSocket请求功能是否正常

## 实施步骤

1. 修改响应参数tab，添加mock配置表单
2. 删除mock配置tab
3. 合并发送请求和WebSocket请求tab
4. 测试所有功能是否正常工作
5. 重新构建前端并部署

## 依赖关系

- 依赖原有的mock配置数据和方法
- 依赖接口类型开关功能

## 修改文件

- `frontend/views/InterfaceDetailView.vue`：主要修改文件

## 预期完成时间

该修改预计需要15-20分钟完成，包括代码修改、测试和构建。