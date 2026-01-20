<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <el-header height="60px" class="app-header">
      <div class="header-content">
        <h1 class="app-title">动态接口生成工具</h1>
        <div class="header-actions">
          <el-button type="primary" size="small" @click="refreshData">刷新</el-button>
        </div>
      </div>
    </el-header>
    
    <!-- 主体内容区 -->
    <el-container class="app-container">
      <!-- 左侧文件上传区 -->
      <el-aside width="300px" class="app-aside-left">
        <router-view name="left"></router-view>
      </el-aside>
      
      <!-- 中间接口列表区 -->
      <el-main class="app-main">
        <router-view name="main"></router-view>
      </el-main>
      
      <!-- 右侧接口详情区 -->
      <el-aside width="400px" class="app-aside-right">
        <router-view name="right"></router-view>
      </el-aside>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // 应用数据
    }
  },
  methods: {
    refreshData() {
      // 刷新数据
      this.$emit('refresh')
    }
  }
}
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f0f2f5;
  color: #303133;
}

/* 应用容器样式 */
#app {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶部导航栏样式 */
.app-header {
  background-color: #2d7ff9;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
  transition: all 0.3s ease;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 24px;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.5px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 主体内容区样式 */
.app-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  background-color: #f0f2f5;
}

/* 左侧文件上传区 */
.app-aside-left {
  background-color: #ffffff;
  border-right: 1px solid #e6e8eb;
  overflow-y: auto;
  transition: all 0.3s ease;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

/* 中间接口列表区 */
.app-main {
  background-color: #f5f7fa;
  overflow-y: auto;
  padding: 24px;
  transition: all 0.3s ease;
  flex: 1;
}

/* 右侧接口详情区 */
.app-aside-right {
  background-color: #ffffff;
  border-left: 1px solid #e6e8eb;
  overflow-y: auto;
  transition: all 0.3s ease;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.05);
}

/* 滚动条样式优化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f3f5;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #909399;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .app-aside-right {
    width: 350px !important;
  }
}

@media (max-width: 992px) {
  .app-aside-left {
    width: 250px !important;
  }
  
  .app-aside-right {
    width: 300px !important;
  }
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .app-aside-left,
  .app-aside-right {
    width: 100% !important;
    height: 300px;
    border: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .app-main {
    padding: 16px;
  }
}
</style>