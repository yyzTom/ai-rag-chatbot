<script setup lang="ts">
import { ref } from 'vue'

const userMessage = ref('')
</script>

<template>
  <div class="chat-container">
    <!-- Message display area -->
    <div class="chat-messages">
      <!-- Message display area -->
    </div>

    <!-- Input area -->
    <div class="chat-input">
      <el-input
        placeholder="Type your message..."
        v-model="userMessage"
      />
      <el-button type="primary">Send</el-button>
    </div>
  </div>
</template>

<style>
/* Add basic styling for layout */
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
}
.chat-input {
  display: flex;
  gap: 10px;
  padding: 20px;
}
</style>

