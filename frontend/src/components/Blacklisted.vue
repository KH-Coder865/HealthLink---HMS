<template>
  <div class="disabled-wrap d-flex flex-column justify-content-center align-items-center text-center">
    <h1 class="text-danger fw-bold mb-3">Oops!</h1>
    <p class="fs-5 mb-1">Your account has been disabled by the Administrator.</p>
    <p class="mb-4">Contact the Admin for more details.</p>

    <router-link to="/" class="btn btn-primary">
      Go to Home
    </router-link>
  </div>
</template>

<script>
export default {
  name: "Blacklisted",
};
</script>

<style scoped>
.disabled-wrap {
  min-height: 100vh;
  padding: 1rem;
}
</style>
