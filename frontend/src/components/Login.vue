<template>
  <!-- Main Container: Full height, centered layout, light background -->
  <div class="d-flex justify-content-center align-items-center min-h-100 bg-light p-3 p-sm-5">
    
    <!-- Login Card/Log Container -->
    <div class="card shadow-lg px-4 py-1 p-md-5 border-0 login-card">
        <div class="card-body">
            <div class="text-center mb-4">
                <div class="fs-1 pulse mb-2 txt-orng">❤️</div>
                <h3 class="h4 text-dark fw-bold">Your Reliable Hospital Management Platform</h3>
                <p class="text-muted small">Sign in to access your dashboard.</p>
            </div>

            <!-- Login Form -->
            <form class="d-flex flex-column" @submit.prevent="submitLogin">
                
                <div class="mb-3">
                    <label for="email" class="form-label fw-medium">Registered Email-Id:</label>
                    <input v-model="email" type="email" class="form-control" id="email" placeholder="you@example.com" required>
                </div>

                <div class="mb-4">
                    <label for="pass" class="form-label fw-medium">Password:</label>
                    <input v-model="password" type="password" class="form-control" id="pass" placeholder="Enter Password" required>
                </div>

                <button type="submit" class="btn btn-orng btn-lg fw-bold w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>{{ loading ? "Signing In.." : "Login" }}</button>
            </form>

            <!-- Registration Link -->
            <div class="text-center mt-4">
                <router-link to="/signup" class="txt-orng small fw-medium text-decoration-none">
                    Don't have an account? Create One!
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
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';
import useDocStore from '@/stores/doctors';
import usePatientStore from '@/stores/patients';

export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
            loading: false,
            error: "",
            router: "",
            userStore: null,
            docStore: null,
            patStore: null,
        };
    },

    created() {
        this.userStore = useUserStore();
        this.docStore = useDocStore();
        this.patStore = usePatientStore();
        this.router = useRouter();
        const tok = localStorage.getItem("token");
        if(tok)
            this.router.replace('/');

    },

    methods: {
        async submitLogin(){
            this.error="";
            this.loading=true;
            try{
                await this.userStore.loginWithCredentials("/auth/login", {
                    email: this.email,
                    password: this.password,
                });
                if(this.userStore.isAdmin){
                    this.$router.push('/adash');
                }
                else if(this.userStore.role === 'patient'){
                    const uid=this.userStore.user.id;
                    const patres=await this.patStore.getbyId({id: null, uid});
                    const id=patres.id;
                    this.$router.push(`/pdash?id=${id}`);
                }
                else if(this.userStore.role === 'doctor'){
                    const uid=this.userStore.user.id;
                    const docres=await this.docStore.getbyId({id: null, uid});
                    const id=docres.id;
                    this.$router.push(`/ddash/${id}`);
                }
                else{
                    throw new Error("Role not Defined!")
                }
            } catch(e){
                this.error=e.message || "Login Failed"
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>

<style scoped>
/* Custom styles to bring in the specific orange theme color for Bootstrap */
.txt-orng {
  color: #ff8000 !important; /* A bright, vibrant orange for theme */
}

.pulse{
    animation: pulseanim ease-out infinite 0.5s;
}

@keyframes pulseanim {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
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

.login-card {
    max-width: 400px;
    width: 100%;
    border-radius: 1rem; /* Rounded corners */
    border-top: 5px solid #ff8000; /* Orange accent border top */
    background-color: white;
}

</style>