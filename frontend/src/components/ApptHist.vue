<template>
    <div class="ms-4 d-flex justify-content-center overflow-hidden mt-4">
        <div class="entity-card">
            <div class="card-header rounded-2 p-2 mb-4 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-hourglass-split me-2"></i>Patient History</span>
                
                <i class="btn btn-outline-primary bi-arrow-left-circle fs-6 " @click="$router.back()">&nbsp;Back</i>
            </div>

            <div class="mb-3 p-2 rounded-2 bg-light">
                <p><strong>Patient Name:</strong> {{ pat?.details?.name }}</p>
                <p v-if="!$route.path.includes('pdash')"><strong>Doctor's Name:</strong> {{ doc?.details?.name }}</p>
                <p v-if="!$route.path.includes('pdash')"><strong>Department:</strong> {{ doc?.specializations?.name }}</p>
            </div>

            <div class="table-responsive mt-2 tab">
                <table class="table table-bordered align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-0">
                        <tr>
                            <th>Visit No.</th>
                            <th v-if="$route.path.includes('pdash')">Doctor Name</th>
                            <th v-if="$route.path.includes('pdash')">Department</th>
                            <th>Visit Date</th>
                            <th>Tests Done</th>
                            <th>Diagnosis</th>
                            <th>Medicines</th>
                            <th>Doses</th>
                            <th>Duration</th>
                            <th>Advice</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="!info.length">
                            <td colspan="7" class="text-muted p-4">
                                No history found.
                                <button @click="refresh" class="btn btn-sm btn-outline-primary ms-2">
                                    Refresh
                                </button>
                            </td>
                        </tr>
                        <template v-else v-for="(v,i) in info" :key="v.id">
                            <tr>
                                <td :rowspan="v?.treatment?.prescription?.length || 1">{{ i + 1 }}</td>
                                <td v-if="$route.path.includes('pdash')" :rowspan="v?.treatment?.prescription?.length || 1">{{v.doctor_name }}</td>
                                <td v-if="$route.path.includes('pdash')" :rowspan="v?.treatment?.prescription?.length || 1">{{ v.dept}}</td>
                                <td :rowspan="v?.treatment?.prescription?.length || 1">{{ formDate(v.appointment_date) }}</td>
                                <td :rowspan="v?.treatment?.prescription?.length || 1">{{ v?.treatment?.tests_done }}</td>
                                <td :rowspan="v?.treatment?.prescription?.length || 1">{{ v?.treatment?.diagnosis }}</td>
                                <td>{{ v?.treatment?.prescription?.[0]?.med }}</td>
                                <td>{{ v?.treatment?.prescription?.[0]?.dose }}</td>
                                <td>{{ v?.treatment?.prescription?.[0]?.duration }}</td>
                                <td :rowspan="v?.treatment?.prescription?.length || 1">{{ v?.treatment?.notes }}</td>
                            </tr>
                            <tr v-for="(p, idx) in v?.treatment?.prescription?.slice(1)" :key="idx">
                                <td>{{ p?.med }}</td>
                                <td>{{ p?.dose }}</td>
                                <td>{{ p?.duration }}</td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<style scoped>
.entity-card {
    max-width: 1200px; /* maximum width for large screens */
    width: 100%;        /* default full width */
}
.tab {
    max-height: 400px;
    max-width: 95vw;
    overflow-y: auto;
    overflow-x: auto;
}
.pulse {
    animation: pulseanim 0.5s ease-out infinite;
}

@keyframes pulseanim {
    0% { transform: scale(1); }
    50% { transform: scale(1.5); }
    100% { transform: scale(1); }
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
    z-index: 2000;
    backdrop-filter: blur(1px);
}
.fs-header {
    font-size: 2rem;
}
.card-header {
    background-color: rgb(251, 176, 122);
}

@media (max-width: 1200px) {
    .entity-card {
        max-width: 90%; /* slightly narrower on medium screens */
        margin: 0 1rem;
    }
}
@media (max-width: 768px) {
    .entity-card {
        max-width: 100%;
        margin: 0 0.5rem;
    }
    .fs-header {
        font-size: 1.5rem;
        max-width: 95vw;
    }
    table th, table td {
        padding: 0.5rem;
        white-space: nowrap;
    }
    .btn {
        width: 100%;
        max-width: 120px;
        padding: 0.5rem;
    }
}
</style>


<script>
import useAppointmentStore from "@/stores/appointments";
import useDocStore from "@/stores/doctors";
import usePatientStore from "@/stores/patients";
import { routeLocationKey } from "vue-router";

export default {
    name: "PatientHistory",

    data() {
        return {
            info: [],
            pid: null,
            did: null,
            doc: null,
            pat: null,
            loading: false,
        };
    },

    methods: {
        async refresh() {
            const apptStore = useAppointmentStore();
            if(this.$route.path.includes('pdash')) {
                const res = await apptStore.getAllbyIds({
                    pid: this.pid,
                    status: 'completed'
                });
                this.info = res;
            }
            else {
                const res = await apptStore.getAllbyIds({
                    pid: this.pid,
                    did: this.did,
                    status: 'completed',
                });
                this.info = res;
            }
        },

        formDate(date) {
            const arr= ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            const d=date.split('-')
            return `${d[2]}th ${arr[d[1]-1]}, ${d[0]}`;
        }
    },

    async created() {
        const docStore = useDocStore();
        const patStore = usePatientStore();
        this.pid = this.$route.query.pid;
        if(this.$route.query.did) {
            this.did = this.$route.query.did;
            this.doc = await docStore.getbyId({id: this.did, uid: null});
        }

        this.pat = await patStore.getbyId({id: this.pid, uid: null});
    },

    async mounted() {
        this.loading=true
        await this.refresh();
        this.loading=false
    },
};
</script>