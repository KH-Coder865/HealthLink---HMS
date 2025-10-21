<script setup>
defineProps({
  isSeen: Boolean
})
</script>

<template>
    <div :class="{show: isSeen}" class="sidebar bg-primary position-fixed top-0 start-0 h-100">
      <a class="nav-link fs-5 active text-info fw-bold" href="#">Home</a>
      <a class="nav-link fs-5 text-white fw-bold" href="/summary">Summary</a>
      <a class="nav-link fs-5 text-white fw-bold" href="/logout">Logout</a>
    </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  transform: translateX(-100%);
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 100px 20px;
  transition: transform 0.3s ease;
}

.sidebar.show{
    transform: translateX(0);
}
</style>
