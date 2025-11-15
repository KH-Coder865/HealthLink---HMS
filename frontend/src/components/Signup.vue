
<template>
  <div class="d-flex justify-content-center align-items-center min-h-100 bg-light p-3 p-sm-5">
    <div class="card shadow-lg px-4 py-1 p-md-5 border-0 reg-card">
      <div class="card-body">
        <div class="text-center mb-4">
          <div class="fs-1 pulse mb-2 txt-orng">🧬</div>
          <h3 class="h4 text-dark fw-bold">Create Your Account</h3>
          <p class="text-muted small">Join the platform today.</p>
        </div>

        <form class="d-flex flex-column" @submit.prevent="signup">
          <div class="mb-3">
            <label class="form-label fw-medium">Name:</label>
            <input v-model="name" type="text" class="form-control" placeholder="Enter Name" required>
          </div>

          <div class="mb-3">
            <label class="form-label fw-medium">Email:</label>
            <input v-model="email" type="email" class="form-control" placeholder="Enter Email" required>
          </div>

          <div class="mb-3">
            <label class="form-label fw-medium">Password:</label>
            <input v-model="password" type="password" class="form-control" placeholder="Enter Password" required>
          </div>

          <div class="mb-4">
            <label class="form-label fw-medium">Confirm:</label>
            <input v-model="confirm" type="password" class="form-control" placeholder="Confirm Password" required>
          </div>

          <button type="submit" class="btn btn-orng btn-lg fw-bold w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>{{ loading ? "Signing Up.." : "Register" }}</button>
        </form>

        <div class="text-center mt-4">
          <router-link to="/login" class="txt-orng small fw-medium text-decoration-none">
            Already have an account? Login
          </router-link>
        </div>

        <!-- Error message (if needed) -->
            <div v-if="error" class="alert alert-danger mt-3 w-100 text-center">
                {{ error }}
            </div>

      </div>
    </div>
  </div>
</template>

<script>
import useUserStore from '@/stores/user';

export default {
    name: "Signup",
    data(){
        return {
            name: "",
            email: "",
            password: "",
            confirm: "",
            loading: false,
            error: "",
            userStore: null,
        };
    },

    created(){
        this.userStore = useUserStore();
    },

    methods: {
        async signup(){
            this.error = "";
            this.loading = true;

            if(this.password !== this.confirm){
                this.error = "Passwords do not match";
                this.loading = false;
                return;
            }

            try{
                // REGISTER PATIENT ONLY
                await this.userStore.register("/auth/register", {
                    name: this.name,
                    email: this.email,
                    password: this.password,
                    role: "patient", 
                });

                // Auto-login or redirect after signup
                this.$router.push("/pdash");

            } catch(e){
                this.error = e.message || "Signup Failed";
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>

<style scoped>
.txt-orng {
  color: #ff8000 !important;
}

.pulse {
  animation: rotateanim ease-in-out infinite 1.5s;
}

@keyframes rotateanim {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(90deg); }
  50% { transform: rotate(180deg);}
  75% { transform: rotate(270deg);}
  100% { transform: rotate(360deg); }
}

.btn-orng {
  background-color: #ff8000;
  border-color: #ff8000;
  color: white;
}

.btn-orng:hover {
  background-color: #e67300;
  color: white;
}

.reg-card {
  max-width: 400px;
  width: 100%;
  border-radius: 1rem;
  border-top: 5px solid #ff8000;
  background-color: white;
}
</style>
