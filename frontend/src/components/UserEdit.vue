<template>

    <div class="position-relative d-flex justify-content-center align-items-center min-h-100 bg-light p-3 p-sm-5">
        <div class="mt-1 card shadow-lg px-4 py-1 p-md-5 border-0 login-card">
            <div class="card-body">
                <div style="z-index: 999; top: 5px; left: 5px;" class="position-absolute">
                    <i class="btn btn-outline-primary shadow-smbi bi-arrow-left-circle fs-6"
                        @click="$router.back()">Back</i>
                </div>
                <div class="text-center mb-4">
                    <div class="fs-1 pulse mb-2 txt-orng">✏️</div>
                    <h3 class="h4 text-dark fw-bold">{{ title }}</h3>
                    <p class="text-muted small">Update information below.</p>
                </div>

                <form class="d-flex align-items-center flex-column" @submit.prevent="submitForm">
                    <div class="d-flex lg justify-content-between gap-2 flex-wrap">

                        <div class="mb-3">
                            <label class="form-label fw-medium">Full Name:</label>
                            <input v-model="form.name" type="text" class="form-control" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label fw-medium">Contact Number:</label>
                            <input v-model="form.contact_number" type="tel" class="form-control" required>
                        </div>

                        <div v-if="showEmrgency" class="mb-3">
                            <label class="form-label fw-medium">Emergency Contact Number:</label>
                            <input v-model="form.emer_contact_number" type="tel" class="form-control" required>
                        </div>

                        <div v-if="showAge" class="mb-3">
                            <label class="form-label fw-medium">Age:</label>
                            <input v-model="form.age" type="number" class="form-control" min="1" required>
                        </div>

                        <div v-if="showGender" class="mb-3">
                            <label class="form-label fw-medium">Gender:</label>
                            <select v-model="form.gender" class="form-select" required>
                                <option value="">Select</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div v-if="showAddress" class="mb-3">
                            <label class="form-label fw-medium">Address:</label>
                            <textarea v-model="form.address" class="form-control" rows="2" cols="23" required></textarea>
                        </div>

                        <div v-if="showSpecialization" class="mb-4">
                            <label class="form-label fw-medium">Specialization:</label>
                            <input v-model="form.specialization" type="text" class="form-control" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label fw-medium">Email:</label>
                            <input v-model="form.email" type="email" class="form-control" disabled>
                        </div>

                        <div class="mb-4">
                            <label class="form-label fw-medium">Password:</label>
                            <input type="password" class="form-control" value="************" disabled>
                        </div>
                    </div>

                    <button type="submit" class="btn btn-orng btn-lg fw-bold w-100" :disabled="loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                        {{ loading ? "Updating.." : "Update" }}
                    </button>
                </form>

                <div v-if="error" class="alert mt-3 w-100 text-center"
                    :class="error.includes('success') ? 'alert-success' : 'alert-danger'">
                    {{ error }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "UserEditForm",

    props: {
        title: String,
        showSpecialization: Boolean,
        showEmrgency: Boolean,
        showAge: Boolean,
        showGender: Boolean,
        showAddress: Boolean,
        load: Function,
        save: Function,
    },

    data() {
        return {
            loading: false,
            error: "",
            form: {
                name: "",
                email: "",
                contact_number: "",
                emer_contact_number: "",
                specialization: "",
                age: "",
                gender: "",
                address: ""
            },
        };
    },

    async created() {
        this.loading = true;
        try {
            const data = await this.load();

            this.form.name = data.details.name;
            this.form.email = data.details.email;
            this.form.contact_number = data.contact_number;

            if (this.showSpecialization) {
                this.form.specialization = data.specializations?.name || "";
            }

            if (this.showEmrgency) {
                this.form.emer_contact_number = data.emergency_contact || "";
            }

            if (this.showAge) {
                this.form.age = data.age || "";
            }

            if (this.showGender) {
                this.form.gender = data.gender || "";
            }

            if (this.showAddress) {
                this.form.address = data.address || "";
            }

        } catch {
            this.error = "Failed to load data.";
        }
        this.loading = false;
    },

    methods: {
        async submitForm() {
            this.error = "";
            this.loading = true;

            try {
                await this.save(this.form);
                this.error = "Updated successfully!";
            } catch {
                this.error = "Update failed!";
            }

            this.loading = false;
        }
    }
};
</script>

<style scoped>
.txt-orng {
    color: #ff8000 !important;
}

.pulse {
    animation: pulseanim ease-out infinite .5s;
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

.btn-orng {
    background: #ff8000;
    border-color: #ff8000;
    min-width: 60%;
    color: white
}

.btn-orng:hover {
    background: #e67300;
    color: white
}

.login-card {
    max-width: 600px;
    width: 100%;
    border-radius: 1rem;
    border-top: 5px solid #ff8000;
    background: white
}

@media (max-width: 600px) {
    .lg {
        display: block !important;
    }
}
</style>
