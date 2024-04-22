<template>
  <div style="display: flex; flex-direction: column; height: 100%;">
    <div style=" flex-grow: 1">
      <el-form :rules="rules" :model="form" label-width="auto" :inline="true">
        <el-form-item label="sheet名称" prop="sheetName">
          <el-input v-model="form.sheetName" />
        </el-form-item>
        <el-form-item label="名称所在行" prop="nameRow">
          <el-input-number v-model="form.nameRow" />
        </el-form-item>
        <el-form-item label="数据起始行" prop="dataRow">
          <el-input-number v-model="form.dataRow" />
        </el-form-item>
        <el-form-item label="名称起始列" prop="nameStart">
          <el-input-number v-model="form.nameStart" />
        </el-form-item>
        <el-form-item label="名称结束列" prop="nameEnd">
          <el-input-number v-model="form.nameEnd" />
        </el-form-item>
        <el-form-item label="生成的起始id" prop="generateStartId">
          <el-input-number v-model="form.generateStartId" />
        </el-form-item>
        <el-form-item label="扩展信息起始列" prop="extensionStart">
          <el-input-number v-model="form.extensionStart" />
        </el-form-item>
        <el-form-item label="扩展信息起始列" prop="extensionEnd">
          <el-input-number v-model="form.extensionEnd" />
        </el-form-item>
        <el-form-item>
          <!-- <el-upload ref="upload" action="http://localhost:5000/upload" :limit="1" :on-exceed="handleExceed" style="margin-bottom: -10px;margin-right: 10px;">
          <template #trigger>
            <el-button type="primary">上传文件</el-button>
          </template>
        </el-upload> -->
          <el-button type="primary" @click="runScript">执行</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
      <el-upload ref="upload" class="upload-demo" drag :on-exceed="handleExceed" action="http://localhost:5000/upload"
        :limit="1">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
      </el-upload>
    </div>
    <el-divider />
    <el-scrollbar class="log-container" >
      <div v-for="log in logs" :key="log.id">{{ log.message }}</div>
    </el-scrollbar>
  </div>
</template>
 
<script setup>
import { ref, onMounted, reactive } from 'vue';
import io from 'socket.io-client';
import axios from 'axios';
import { genFileId } from 'element-plus'
import {
  UploadFilled
} from '@element-plus/icons-vue'

const logs = ref([]);

onMounted(() => {
  const socket = io('http://localhost:5000');
  socket.on('log_message', message => {
    logs.value.push({ id: logs.value.length + 1, message });
  });
});

const rules = reactive({
  excelFilePath: [
    { required: true, message: 'Please input Excel file path', trigger: 'blur' },
  ],
  sheetName: [
    { required: true, message: 'Please input Sheet name', trigger: 'blur' },
  ],
  nameRow: [
    { required: true, message: 'Please input Name row', trigger: 'blur' },
  ],
  dataRow: [
    { required: true, message: 'Please input Data row', trigger: 'blur' },
  ],
  nameStart: [
    { required: true, message: 'Please input Name start', trigger: 'blur' },
  ],
  nameEnd: [
    { required: true, message: 'Please input Name end', trigger: 'blur' },
  ],
  generateStartId: [
    { required: true, message: 'Please input Generate start id', trigger: 'blur' },
  ],
  extensionStart: [
    { required: true, message: 'Please input Extension start', trigger: 'blur' },
  ],
  extensionEnd: [
    { required: true, message: 'Please input Extension end', trigger: 'blur' },
  ],
});

// do not use same name with ref
const form = reactive({
  // 文件路径
  excelFilePath: "demo.xlsx",
  // sheet名称
  sheetName: "菜单结构",
  // 名称所在行
  nameRow: 1,
  // 数据起始行
  dataRow: 2,
  // 名称起始列
  nameStart: 0,
  // 名称结束列
  nameEnd: 6,
  // 生成的起始id
  generateStartId: 8000,
  // 扩展信息起始列
  extensionStart: 7,
  // 扩展信息结束列
  extensionEnd: 10,
})

const runScript = async () => {
  try {
    const response = await axios.get('http://localhost:5000/run_script');
    console.log(response.data); // 输出 'Script started'
  } catch (error) {
    console.error('Error:', error);
  }
};

const upload = ref()

const handleExceed = (files) => {
  upload.value.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  upload.value.handleStart(file)
}

</script>
 

<style scoped>
.log-container {
  padding: 10px;
  height: auto;
}

</style>
 