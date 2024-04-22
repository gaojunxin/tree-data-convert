<script setup>
import { RouterLink, RouterView } from 'vue-router'
import {
  Menu as IconMenu,
  Operation,
  Setting,
} from '@element-plus/icons-vue'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>

  <el-container class="layout-container-demo" style="height: 100vh">
    <!-- <el-aside width="200px"> <el-scrollbar>
        <el-menu :default-openeds="['1', '3']">
          <el-menu-item index="1-1"><el-icon>
              <Operation />
            </el-icon>功能</el-menu-item>
          <el-menu-item index="1-2"><el-icon>
              <setting />
            </el-icon>设置</el-menu-item>
        </el-menu>
      </el-scrollbar>
    </el-aside> -->
    <el-main>
      <RouterView />
    </el-main>
  </el-container>
</template>

<style scoped>
.layout-container-demo {
  padding-top: 20px;
}

.layout-container-demo .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}

.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
  border-right: solid 1px #EBEEF5;
}

.layout-container-demo .el-menu {
  border-right: none;
}

.layout-container-demo .el-main {
  padding: 0;
}

.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}</style>
