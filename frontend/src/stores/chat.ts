import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
    // State: array of chat messages with IDs for tracking
    const messages = ref<Array<{ id: number; user: string; ai: string | null; timestamp: Date }>>([])

    // Track the next message ID
    let nextId = 1

    // Action: add a message to the chat history
    function addMessage(userMessage: string, aiResponse: string | null = null) {
        const message = {
            id: nextId++,
            user: userMessage,
            ai: aiResponse,
            timestamp: new Date()
        }
        messages.value.push(message)
        return message
    }

    // Action: update AI response for a specific message
    function updateAiResponse(messageId: number, aiResponse: string) {
        const messageIndex = messages.value.findIndex(msg => msg.id === messageId)
        if (messageIndex !== -1) {
            messages.value[messageIndex].ai = aiResponse
        }
    }

    function clearMessages() {
        messages.value = []
        nextId = 1
    }

    return {
        messages,
        addMessage,
        updateAiResponse,
        clearMessages
    }
})