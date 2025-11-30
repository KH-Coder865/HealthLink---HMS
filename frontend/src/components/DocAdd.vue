<template>
    <div class="d-flex justify-content-center align-items-center min-h-100 bg-light p-3 p-sm-5">
    <div class="card shadow-lg px-4 py-1 p-md-1 border-0 login-card">
      <div class="card-body">
        <div style="z-index: 999; top: 5px; left: 5px;" class="position-absolute">
                    <i class="btn btn-outline-primary shadow-smbi bi-arrow-left-circle fs-6"
                        @click="$router.back()">Back</i>
                </div>
                
        <div class="text-center mb-4">
          <div class="fs-1 pulse mb-2 txt-orng">🩺</div>
          <h3 class="h4 text-dark fw-bold">Your Reliable Hospital Management Platform</h3>
          <p class="text-muted small">Add a Doctor to the Database</p>
        </div>

        <form class="d-flex align-items-center flex-column" @submit.prevent="createDoc">
          <div>

            <div class="mb-3">
              <label for="name" class="form-label fw-medium">Full Name:</label>
              <input v-model="name" type="text" class="form-control" id="name" placeholder="Doctor's Name" required>
            </div>
            
            <div class="mb-3">
              <label for="cno" class="form-label fw-medium">Contact No. of Doctor:</label>
              <input v-model="cno" type="tel" class="form-control" id="cno" placeholder="+12 3456789012" required>
            </div>
            
            <div class="mb-4">
              <label for="spz" class="form-label fw-medium">Specialization:</label>
              <input v-model="spz" type="text" class="form-control" id="spz" placeholder="Orthopedics, Cardio, etc."
              required>
            </div>
            
            <div class="mb-3">
              <label for="email" class="form-label fw-medium">Email-Id:</label>
              <input v-model="email" type="email" class="form-control" id="email" placeholder="you@example.com" required>
            </div>
            
            <div class="mb-4">
              <label for="pass" class="form-label fw-medium">Password:</label>
              <input v-model="password" type="password" class="form-control" id="pass" placeholder="Enter Password"
              required>
            </div>
          </div>


          <button type="submit" class="btn btn-orng btn-lg fw-bold w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>{{ loading ?
              "Creating.." : "Create Doctor" }}
          </button>
        </form>

        <div v-if="error && error !== 'Doctor Added Succesfully!'" class="alert alert-danger mt-3 w-100 text-center">{{
          error }}</div>
        <div v-else-if="error" class="alert alert-success mt-3 w-100 text-center">{{ error }}</div>
      </div>
    </div>
  </div>

  <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<script>
import useDocStore from "@/stores/doctors";
import useAppointmentStore from "@/stores/appointments";

export default {
  name: "DocAdd",
  data() {
    return {
      name: "",
      cno: "",
      email: "",
      password: "",
      spz: "",
      loading: false,
      error: "",
      docStore: null,
      apptStore: null,
    }
  },
  created() {
    this.docStore = useDocStore();
    this.apptStore = useAppointmentStore();
  },
  methods: {
    async createDoc() {
      this.loading = true
      this.error = ""
      try {
        const data = {
          name: this.name,
          email: this.email,
          specialization: this.spz,
          contact_number: this.cno,
          password: this.password,
        }

        const res = await this.docStore.create(data)
        if (res) {
          this.error = "Doctor Added Succesfully!"
        }
      }
      catch (err) {
        this.error =
          err.message ||
          err.response?.data?.message ||
          "Error"
      }
      this.loading = false
    },

  }
}
</script>

<style scoped>
.txt-orng {
  color: #ff8000 !important
}

.pulse {
  animation: pulseanim ease-out infinite .5s
}

@keyframes pulseanim {
  0% {
    transform: scale(1)
  }

  50% {
    transform: scale(1.1)
  }

  100% {
    transform: scale(1)
  }
}

.loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(255, 255, 255, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
    backdrop-filter: blur(1px);
}

.btn-orng {
  background-color: #ff8000;
  border-color: #ff8000;
  color: white
}

.btn-orng:hover {
  background-color: #e67300;
  color: white
}

.login-card {
  max-width: 400px;
  width: 100%;
  border-radius: 1rem;
  border-top: 5px solid #ff8000;
  background-color: white
}
</style>
