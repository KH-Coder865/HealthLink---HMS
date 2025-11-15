<script setup>
import { ref } from 'vue'

const nameSys = "HealthLink HMS"

const services = ref([
  { title: "Seamless EMR Integration", icon: '<i class="bi bi-file-earmark-person-fill"></i>', desc: "Manage all patient records in one place." },
  { title: "Smart Appointment Booking", icon: '<i class="bi bi-calendar-date"></i>', desc: "Schedule and manage appointments easily." },
  { title: "Billing & Claims", icon: '<i class="bi bi-credit-card"></i>', desc: "Handle billing, payments, and claims fast." },
])

const reasons = ref([
  { title: "Patient-Centric Care", icon: '<i class="bi bi-activity"></i>', desc: "Designed to reduce admin load and improve care." },
  { title: "Secure & Compliant", icon: '<i class="bi bi-shield-lock"></i>', desc: "Built with strong security and compliance." },
  { title: "24/7 Support", icon: '<i class="bi bi-telephone"></i>', desc: "Support team always ready to help." },
])

</script>

<template>
  <div class="bg-light p-3 p-sm-5 min-vh-100">
    <main class="container">

      <section class="text-center py-5 mb-5 bg-white shadow rounded-3">
        <h1 class="display-4 fw-bold text-dark">
          Powering <span class="text-orange">{{ nameSys }}</span>
        </h1>
        <p class="lead text-secondary mt-3 mx-auto" style="max-width: 700px;">
          A modern system built to improve workflows and patient experience.
        </p>
        <div class="mt-4">
          <button  class="btn btn-orange btn-lg me-3">Request a Demo</button>
          <button  class="btn btn-outline-secondary btn-lg">Contact Sales</button>
        </div>
      </section>

      <section class="mb-5">
        <h2 class="text-center h3 fw-bold text-secondary mb-4 pb-2 border-bottom border-orange-light">
          Core Features
        </h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
          <div v-for="s in services" :key="s.title" class="col">
            <div class="card h-100 shadow-sm border-0 text-center service-card">
              <div class="card-body p-4">
                <div class="fs-1 mb-3 text-orange" v-html="s.icon"></div>
                <h3 class="h5 fw-bold text-dark mb-2">{{ s.title }}</h3>
                <p class="text-secondary small">{{ s.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-5 mb-5">
        <h2 class="text-center h3 fw-bold text-dark mb-5">Why Choose Us?</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
          <div v-for="r in reasons" :key="r.title" class="col">
            <div class="d-flex align-items-start border-start border-4 border-orange-light p-3 h-100">
              <div class="fs-4 me-3 text-orange" v-html="r.icon"></div>
              <div>
                <h4 class="h6 fw-bold text-dark mb-1">{{ r.title }}</h4>
                <p class="text-secondary small mb-0">{{ r.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="bg-orange text-white p-5 rounded-3 shadow-lg text-center">
        <h2 class="h3 fw-bold mb-3">Ready to Upgrade?</h2>
        <p class="lead mb-4 opacity-75">Trusted by top healthcare providers.</p>
        <button  class="btn btn-light text-orange fw-bold btn-lg">Start Free Trial</button>
      </section>

    </main>
  </div>
</template>

<style scoped>
.text-orange { color: #ff8000 !important; }
.bg-orange { background: #ff8000 !important; }
.border-orange-light { border-color: #ffe0b3 !important; }
.btn-orange { background: #ff8000; border-color: #ff8000; color: white; }
.btn-orange:hover { background: #e67300; border-color: #e67300; color: white; }
.service-card { transition: 0.2s; }
.service-card:hover { transform: translateY(-5px); box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1) !important; }
</style>
