<script setup>
import Sidebar from './Sidebar.vue'
import { ref } from 'vue'

defineProps({
  msg: String
})

// Reactive state for sidebar visibility
const sidebarVisible = ref(false)
</script>

<template>
  <nav class="navbar bg-primary sticky-top">
    <div class="container-fluid">
      <!-- Toggle sidebar -->
      <button @click="sidebarVisible = !sidebarVisible"
              class="btn z-3 btn-outline-info fs-1 fw-bolder text-white">≡</button>

      <a class="navbar-brand mx-auto text-white pulse fs-2 fw-bold">{{ msg }}</a>
    </div>
  </nav>

  <!-- Pass state to Sidebar -->
  <Sidebar :isSeen="sidebarVisible" />
</template>
