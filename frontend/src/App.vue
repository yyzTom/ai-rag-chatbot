<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from './stores/chat'
// import apiClient from './api/client'

const chatStore = useChatStore()
const userMessage = ref('')

function sendMessage() {
  if (userMessage.value.trim()) {
    // Add user message to store
    chatStore.addMessage(userMessage.value, '') // AI response will be added later
    userMessage.value = ""
  }
}
</script>

<template>
  <div class="chat-container">
    <!-- Message display area -->
    <div class="chat-messages">
      <div v-for="(message, index) in chatStore.messages" :key="index" class="messages">
        <div v-if="message.user" class="user-message">
          <div class="message-bubble">
            <p>{{ message.user }}</p>  
          </div>
        </div>
        <div v-if="message.ai" class="ai-message">
          <div class="message-bubble">
            <p>{{ message.ai }}</p>  
          </div>
        </div>
      </div>
    </div>

    <!-- Input area -->
    <div class="chat-input">
      <el-input
        placeholder="Type your message..."
        v-model="userMessage"
        type="textarea"
        :autosize="{ minRows:1, maxRows:4 }"
        @keyup.enter="sendMessage"
      />
      <el-button type="primary" @click="sendMessage">Send</el-button>
    </div>
  </div>
</template>

<style>
:root {
  --chat-bg: #f5f5f5;
  --bubble-padding: 10px 15px;
  --bubble-margin: 5px;
  --bubble-max-inner-width: 95%;
}

/* Add basic styling for layout */
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Arial', sans-serif;
}
.chat-messages {
  flex: 1;
  overflow-wrap: break-word;
  overflow-y: auto;
  padding: 10px;
  background-color: var(--chat-bg);
}
.chat-input {
  display: flex;
  gap: 10px;
  padding: 15px 20px;
  background-color: var(--chat-bg);
  align-items: flex-end;
}
.message {
  margin-bottom: 12px;
  max-width: 70%;
}

.message-bubble {
  padding: var(--bubble-padding);
  margin: var(--bubble-margin);
  display: inline-block;
  width: max-content;
  max-width: var(--bubble-max-inner-width);
}

.user-message {
  display: flex;
  justify-content: flex-end;
  text-align: start;
}
.user-message .message-bubble {
  background-color: #007bff;
  border-radius: 18px 18px 4px 18px;
  color: white;
}

.ai-message {
  display: flex;
  justify-content: flex-start;
  text-align: start;
}
.ai-message .message-bubble {
  background-color: #e9e9eb;
  color: #333;
  border-radius: 18px 18px 18px 4px;
}

.el-textarea__inner {
  border: 1px solid #333;
  overflow-y: overlay;
  resize: none;
  box-sizing: border-box;
}
.el-button {
  min-width: 60px;
  padding: 10px;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}
.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.el-textarea__inner::-webkit-scrollbar {
  width: 6px;
}
.el-textarea__inner::-webkit-scrollbar-track {
  background: #f1f1f1;
  border: 1px solid #ddd; 
  border-radius: 4px;
}
.el-textarea__inner::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border: 1px solid #ddd;
  border-radius: 3px;
}
.el-textarea__inner::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .message {
    max-width: 85%;
  }
  .user-message {
    margin-left: 15%;
  }
  .ai-message {
    margin-right: 15%;
  }
}
</style>

