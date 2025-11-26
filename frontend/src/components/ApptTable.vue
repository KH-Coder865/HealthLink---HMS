<template>
    <div style="margin-left: 18%;" class="mdev mt-4">
        <div class="entity-card">

            <div
                class="card-header mb-4 p-2 rounded-2 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-file-medical me-2"></i>Upcoming Appointments</span>
            </div>

            <div class="table-responsive mt-2 tab">
                <table class="table table-hover align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-0">
                        <tr>
                            <th>#ID</th>
                            <th>Patient</th>
                            <th v-if="!$route.path.includes('ddash')">Doctor</th>
                            <th v-if="!$route.path.includes('ddash')">Department</th>
                            <th v-if="$route.path.includes('ddash')">Date</th>
                            <th v-if="$route.path.includes('ddash')">Time</th>
                            <th>Patient History</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-if="isLoading">
                            <td colspan="6" class="text-center p-4">
                                <div class="spinner-border spinner-border-sm text-primary" role="status">
                                    <span class="visually-hidden"></span>
                                </div>Loading...
                            </td>
                        </tr>

                        <tr v-else-if="mappedAppointments.length === 0">
                            <td colspan="6" class="text-muted p-4">
                                No appointments found.
                                <button @click="$emit('refresh')" class="btn btn-sm btn-outline-primary">
                                    Refresh
                                </button>
                            </td>
                        </tr>

                        <tr v-for="a in mappedAppointments" :key="a.id">
                            <td>{{ a.id }}</td>
                            <td>{{ a.patientName }}</td>
                            <td v-if="!$route.path.includes('ddash')">{{ a.doctorName }}</td>
                            <td v-if="!$route.path.includes('ddash')">{{ a.department }}</td>
                            <td v-if="$route.path.includes('ddash')">{{ a.dt }}</td>
                            <td v-if="$route.path.includes('ddash')">{{ a.time }}</td>

                            <td>
                                <button v-if="(!(a.id in isComp))||(a.id in isComp && !isComp[a.id])" class="btn btn-success btn-sm fw-bold"
                                    @click="$emit('view', { pid: a.pid, did: a.did })">
                                    <i class="bi bi-eye"></i>&nbsp;View
                                </button>
                                <button v-else-if="$route.path.includes('ddash') && a.id in isComp && isComp[a.id]" class="btn btn-outline-primary me-2 btn-sm fw-bold text-wrap" @click="$router.push(`/ddash/appts/update?pid=${a.pid}&did=${a.did}&aid=${a.id}`)">
                                    <i class="bi-arrow-repeat"></i>&nbsp;Update History
                                </button>
                            </td>

                            <td class="d-flex gap-1 flex-sm-wrap">
                                <button v-if="$route.path.includes('ddash')" class="btn btn-outline-success me-2 btn-sm fw-bold text-wrap" @click="isComp[a.id]=true">
                                    <i class="bi bi-check2-circle"></i>&nbsp;Mark as Completed
                                </button>
                                <button class="btn btn-danger btn-sm fw-bold" @click="$emit('cancel', a.id)">
                                    <i class="bi bi-x-circle"></i>&nbsp;Cancel
                                </button>
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>

        </div>
    </div>
</template>

<script>
import useAppointmentStore from "@/stores/appointments";
import useDoctorStore from "@/stores/doctors";
import usePatientStore from "@/stores/patients";

export default {
    name: "AppointmentsTable",

    // Remove the 'datas' property
    data() {
        return {
            isLoading: false,
            isComp: {},
        };
    },

    // Move initial data fetching logic to a method that can be called on mount
    async created() {
        // Only run the store's initial data fetching here
        const docStore = useDoctorStore();
        const patStore = usePatientStore();
        const apptStore = useAppointmentStore();

        this.isLoading = true;
        await Promise.all([
            docStore.getAll(),
            patStore.getAll(),
            apptStore.getAll(),
        ]);
        this.isLoading = false;
    },


    computed: {
        // New computed property to read directly from the store's state/getters
        sourceAppointments() {
            const apptStore = useAppointmentStore();
            // Check the current route path to determine the data source
            if (this.$route.path.includes("ddash")) {
                const did = this.$route.params.id;
                return apptStore.appointments.filter(
                    a => a.doctor_id == did && a.status === "scheduled"
                );
            } else {
                // For other views (e.g., Admin), use the store's reactive getter
                return apptStore.upcoming;
            }
        },

        // Update mappedAppointments to use sourceAppointments
        mappedAppointments() {
            if (!this.sourceAppointments.length) return []; // Use the new source

            const docStore = useDoctorStore();
            const patStore = usePatientStore();

            return this.sourceAppointments.map(a => { // Map the new source
                const doc = docStore.doctors.find(d => d.id === a.doctor_id);
                const pat = patStore.patients.find(p => p.id === a.patient_id);

                return {
                    id: a.id,
                    pid: a.patient_id,
                    did: a.doctor_id,
                    dt: this.formDate(a.appointment_date),
                    time: this.formTime(a.appointment_time),
                    patientName: pat?.details?.name || "Unknown",
                    doctorName: doc?.details?.name || "Unknown",
                    department: doc?.specializations?.name || "—",
                };
            });
        }
    },

    methods: {
        // The refreshData method should now only ensure the stores are up-to-date
        async refreshData() {
            const apptStore = useAppointmentStore();
            const docStore = useDoctorStore();
            const patStore = usePatientStore();

            this.isLoading = true;

            await Promise.all([
                docStore.getAll(),
                patStore.getAll(),
                apptStore.getAll(),
            ]);
            
            // The table will automatically update now because `sourceAppointments`
            // and `mappedAppointments` are computed properties based on the store.
            
            this.isLoading = false;
        },

        formTime(time) {
            let a=time.split(':')
            return `${a[0]}:${a[1]} IST`
        },

        formDate(date) {
            const arr= ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            const d=date.split('-')
            return `${d[2]}th ${arr[d[1]-1]}, ${d[0]}`;
        }
    }
};
</script>

<style scoped>
.entity-card {
    max-width: 70vw;
}

.tab {
    max-height: 300px;
    overflow-x: auto;
    overflow-y: auto;
}

.card-header {
    background-color: rgb(251, 176, 122);
}

.fs-header {
    font-size: 2rem;
}

@media (max-width: 800px) {
    .mdev {
        margin-left: 3% !important;
    }

    .entity-card {
        max-width: 100vw;
        margin: 0 2rem;
    }

    .fs-header {
        font-size: 1.5rem;
    }

    table th,
    table td {
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
