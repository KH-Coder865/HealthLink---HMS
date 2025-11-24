<template>
    <div style="margin-left: 18%;" class="mdev mt-4">
        <div class="entity-card">

            <div class="card-header mb-4 p-2 rounded-2 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-file-medical me-2"></i>Upcoming Appointments</span>
            </div>

            <div class="table-responsive mt-2 tab">
                <table class="table table-hover align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-0">
                        <tr>
                            <th>#ID</th>
                            <th>Patient</th>
                            <th>Doctor</th>
                            <th>Department</th>
                            <th>Patient History</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-if="!mapped.length">
                            <td colspan="6" class="text-muted p-4">
                                No appointments found.
                                <button @click="$emit('refresh')" class="btn btn-sm btn-outline-primary">
                                    Refresh
                                </button>
                            </td>
                        </tr>

                        <tr v-else v-for="a in mapped" :key="a.id">
                            <td>{{ a.id }}</td>
                            <td>{{ a.patientName }}</td>
                            <td>{{ a.doctorName }}</td>
                            <td>{{ a.department }}</td>

                            <td>
                                <button
                                    class="btn btn-success btn-sm fw-bold"
                                    @click="$emit('view', {pid: a.pid,did: a.did})"
                                >
                                    <i class="bi bi-eye"></i>&nbsp;View
                                </button>
                            </td>

                            <td>
                                <button
                                    class="btn btn-danger btn-sm fw-bold"
                                    @click="$emit('cancel', a.id)"
                                >
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

    computed: {
        mapped() {
            const apptStore = useAppointmentStore();
            const docStore = useDoctorStore();
            const patStore = usePatientStore();

            return apptStore.upcoming.map(a => {
                const doc = docStore.doctors.find(d => d.id === a.doctor_id);
                const pat = patStore.patients.find(p => p.id === a.patient_id);

                return {
                    id: a.id,
                    pid: a.patient_id,
                    did: a.doctor_id,
                    patientName: pat?.details?.name || "Unknown",
                    doctorName: doc?.details?.name || "Unknown",
                    department: doc?.specializations?.name || "—"
                };
            });
        }
    },

    async mounted() {
        const apptStore = useAppointmentStore();
        await apptStore.getAll();
    }
};
</script>

<style scoped>
.entity-card { max-width: 70vw; }
.tab { max-height: 300px; }
.card-header { background-color: rgb(251, 176, 122);}
.fs-header { font-size: 2rem; }
.action-buttons { flex-direction: row; }

@media (max-width: 768px) {
    .mdev { margin-left: 3% !important; }
    .ms-4 { margin-left: 0 !important; }
    .entity-card { max-width: 100vw; margin: 0 2rem; }
    .fs-header { font-size: 1.5rem; }
    table th, table td { padding: 0.5rem; white-space: nowrap; }
    .btn { width: 100%; max-width: 120px; padding: 0.5rem; }
}
</style>
