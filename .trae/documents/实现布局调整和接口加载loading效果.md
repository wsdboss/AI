# 实现布局调整和接口加载loading效果

## 1. 布局调整

### 修改内容
- **中间区域**：设置为固定宽度
- **右侧区域**：设置为自适应宽度，并添加最小宽度588px

### 实施步骤
1. 修改 `App.vue` 中的布局配置
   - 将中间 `el-main` 区域设置为固定宽度（例如600px）
   - 将右侧 `el-aside` 区域的宽度属性改为flex: 1
   - 为右侧 `el-aside` 添加最小宽度588px的样式

## 2. 接口加载Loading效果

### 修改内容
- 在store中添加loading状态管理
- 在接口加载过程中显示loading效果

### 实施步骤
1. 修改 `store/index.js`
   - 在state中添加 `loading: false` 状态
   - 在mutations中添加 `SET_LOADING` 方法
   - 在loadInterfaces、loadMockConfig等异步action中添加loading状态管理

2. 修改组件文件
   - 在 `InterfaceListView.vue` 中添加v-loading指令
   - 在 `InterfaceDetailView.vue` 中添加v-loading指令
   - 确保在接口加载过程中显示loading效果

## 3. 预期效果
- 页面布局变为：左侧固定宽度300px，中间固定宽度，右侧自适应宽度且最小588px
- 接口加载过程中显示loading动画，提升用户体验
- 响应式设计保持不变，在小屏幕设备上仍能正常显示

## 4. 技术要点
- 使用Element UI的v-loading指令实现loading效果
- 通过Vuex管理全局loading状态
- 使用CSS flex布局实现响应式调整

## 5. 文件修改列表
- `frontend/App.vue` - 调整布局结构
- `frontend/store/index.js` - 添加loading状态管理
- `frontend/views/InterfaceListView.vue` - 添加loading效果
- `frontend/views/InterfaceDetailView.vue` - 添加loading效果