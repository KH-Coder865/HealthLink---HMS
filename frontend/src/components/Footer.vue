<script setup>
</script>

<template>
  <footer class="text-white shadow-sm footer-fixed" style="background-color:#E65100;">
    <div class="container py-3">

      <div
        class="d-flex flex-column flex-md-row justify-content-between align-items-md-center footer-row"
      >

        <!-- Left -->
        <div class="footer-brand mb-3 mb-md-0">
          <h5 class="fw-bold mb-1">Hello</h5>
          <p class="small mb-0">Crafted with care. Simple. Clean.</p>
        </div>

        <!-- Middle links -->
        <ul class="list-unstyled d-flex align-items-center gap-4 mb-3 mb-md-0">
          <li><a class="text-white nav-link fw-semibold foot-underline" href="#">About</a></li>
          <li><a class="text-white nav-link fw-semibold foot-underline" href="#">Privacy</a></li>
          <li><a class="text-white nav-link fw-semibold foot-underline" href="#">Terms</a></li>
          <li><a class="text-white nav-link fw-semibold foot-underline" href="#">Support</a></li>
        </ul>

        <!-- Right (Stay Connected) -->
        <div class="footer-social text-md-end">
          <p class="small mb-1">Stay Connected</p>
        </div>

      </div>

      <div class="text-center small mt-3 opacity-75">
        © {{ new Date().getFullYear() }} Hello. All rights reserved.
      </div>

    </div>
  </footer>
</template>

<style scoped>
.footer-fixed {
  width: 100%;
  min-height: 90px;
  position: relative;
  bottom: 0;
}

/* Gap between left-middle-right */
.footer-row {
  gap: 20px;
}

/* Brand */
.footer-brand {
  min-width: 180px;
}

/* Social section size */
.footer-social {
  min-width: 150px;
}

/* Hover underline */
.foot-underline {
  position: relative;
  padding-bottom: 2px;
}
.foot-underline::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0%;
  height: 2px;
  background: white;
  transition: width 0.3s ease-in-out;
}
.foot-underline:hover::after {
  width: 100%;
}
</style>
