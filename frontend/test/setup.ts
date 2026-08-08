import {expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'

// Global setup for all tests
vi.useFakeTimers()

beforeEach(() => {
  setActivePinia(createPinia())
})

// Provide Pinia to all tests
export const createTestPinia = () => {
    const pinia = createPinia()
    return pinia
}