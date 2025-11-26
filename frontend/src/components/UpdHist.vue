<template>
    <div class="ms-4 d-flex justify-content-center overflow-hidden mt-4">
        <div class="entity-card">
            <div class="card-header p-2 mb-4 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-arrow-repeat me-2"></i>Update History</span>

                <i class="btn btn-outline-primary bi-arrow-left-circle fs-6" @click="$router.back()">&nbsp;Back</i>
            </div>

            <!-- Patient + Doctor Info -->
            <div class="mb-3 p-2 rounded-2 bg-light">
                <p><strong>Patient Name:</strong> {{ pat?.details?.name }}</p>
                <p><strong>Doctor's Name:</strong> {{ doc?.details?.name }}</p>
                <p><strong>Department:</strong> {{ doc?.specializations?.name }}</p>
                <p><strong>Appointment Date:</strong> {{ formDate(appt?.appointment_date) }}</p>
            </div>

            <!-- Update Form -->
            <div class="card p-3 mb-3">

                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="form-label fw-bold">Tests Done</label>
                        <input type="text" v-model="form.tests_done" class="form-control"
                            placeholder="CBC, Blood Sugar...">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label fw-bold">Diagnosis</label>
                        <input type="text" v-model="form.diagnosis" class="form-control"
                            placeholder="Viral Fever, Diabetes...">
                    </div>
                </div>

                <!-- PRESCRIPTION TABLE -->
                <label class="fw-bold">Prescription</label>
                <table class="table table-bordered text-center">
                    <thead class="table-light">
                        <tr>
                            <th>Medicine</th>
                            <th>Dose</th>
                            <th>Duration</th>
                            <th>Timing</th>
                            <th>Remove</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(p, idx) in form.prescription" :key="idx">
                            <td><input v-model="p.med" class="form-control"></td>
                            <td><input v-model="p.dose" class="form-control"></td>
                            <td><input v-model="p.duration" class="form-control"></td>
                            <td>
                                <select v-model="p.timing" class="form-control hover:cursor-pointer">
                                    <option disabled value="">Select</option>
                                    <option>1-1-1</option>
                                    <option>1-0-1</option>
                                    <option>1-1-0</option>
                                    <option>0-1-1</option>
                                    <option>1-0-0</option>
                                    <option>0-1-0</option>
                                    <option>0-0-1</option>
                                    <option>SOS</option>
                                </select>
                            </td>

                            <td>
                                <button class="btn btn-sm btn-danger" @click="removeRow(idx)">
                                    <i class="bi bi-dash-circle"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <button class="btn btn-sm btn-outline-success mb-3" @click="addRow">
                    <i class="bi bi-plus-circle"></i> Add Medicine
                </button>

                <!-- Notes -->
                <div class="mb-3">
                    <label class="form-label fw-bold">Advice / Notes</label>
                    <textarea class="form-control" v-model="form.notes" rows="3"></textarea>
                </div>

                <!-- Submit -->
                <button class="btn btn-primary fw-bold" @click="submitUpdate">
                    <i class="bi bi-check2-circle"></i> Update History
                </button>
            </div>
        </div>
    </div>

    <!-- Loader -->
    <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Updating...
    </div>
</template>

<script>
import useAppointmentStore from "@/stores/appointments";
import useDocStore from "@/stores/doctors";
import usePatientStore from "@/stores/patients";

export default {
    name: "UpdateHistory",

    data() {
        return {
            pid: null,
            did: null,
            appt: null,
            doc: null,
            pat: null,
            loading: false,

            form: {
                tests_done: "",
                diagnosis: "",
                notes: "",
                prescription: [
                    { med: "", dose: "", duration: "", timing: "" }
                ]
            }
        };
    },

    methods: {
        addRow() {
            this.form.prescription.push({ med: "", dose: "", duration: "", timing: "" });
        },

        removeRow(i) {
            this.form.prescription.splice(i, 1);
        },

        formDate(date) {
            if (!date) return "";
            const arr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            const d = date.split('-');
            return `${d[2]}th ${arr[d[1] - 1]}, ${d[0]}`;
        },

        async submitUpdate() {
            this.loading = true;

            const apptStore = useAppointmentStore();

            await apptStore.update(this.appt.id, {
                status: 'completed',
                treatment: {
                    tests_done: this.form.tests_done,
                    diagnosis: this.form.diagnosis,
                    prescription: this.form.prescription,
                    notes: this.form.notes
                }
            });

            this.loading = false;

            this.$router.push(`/ddash/${this.did}`);
        }
    },

    async created() {
        this.pid = this.$route.query.pid;
        this.did = this.$route.query.did;

        const apptStore = useAppointmentStore();
        const docStore = useDocStore();
        const patStore = usePatientStore();

        this.loading = true;

        this.doc = await docStore.getbyId({ id: this.did, uid: null });
        this.pat = await patStore.getbyId(this.pid);

        // fetch the appointment to update (status = scheduled)
        this.appt = await apptStore.getById(this.$route.query.aid);

        this.loading = false;
    }
};
</script>

<style scoped>
.entity-card {
    max-width: 1200px;
    width: 100%;
}

.tab {
    max-height: 400px;
    max-width: 95vw;
    overflow-y: auto;
}

.card-header {
    background-color: rgb(251, 176, 122);
}

.fs-header {
    font-size: 2rem;
}

.pulse {
    animation: pulseanim 0.5s ease-out infinite;
}

@keyframes pulseanim {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.5);
    }

    100% {
        transform: scale(1);
    }
}

.loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(255, 255, 255, 0.7);
    z-index: 2000;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
