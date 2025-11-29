<template>
    <AppointmentsTable :loading="loading" @refresh="fetchItems('appointment')"
        @view="router.push({ path: '/ddash_view/appts', query: $event })" @cancel="cancelAppointment" />

    <AdminTable title="Assigned Patients" placer="Search by name, id or contact no."
        headcon="bi bi-person-lines-fill me-2" emptyLabel="patients" nameColumn="Patient Name"
        v-model:srchstring="patientSearch" :filtfunc="filterPatients"
        :items="patientSearch ? filteredPatients : doctorPatients" :loading="loading"
        iconClass="bi bi-person-fill fs-4 text-success" specont="Contact No."
        @view="(p) => $router.push(`/ddash_view/appts?pid=${p.pid}&did=${id}`)" @refresh="fetchItems('patient')" />

    <router-link :to="`/ddash/${id}/avail`" style="margin-left: 46vw;" class="btn btn-warning fw-bold mt-5">Change Availability</router-link>



    <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<script>
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';
import usePatientStore from '@/stores/patients';
import useAppointmentStore from '@/stores/appointments';
import AdminTable from '@/components/AdminTable.vue';
import AppointmentsTable from '@/components/ApptTable.vue';

export default {
    name: 'DoctorDash',

    components: { AdminTable, AppointmentsTable },

    data() {
        return {
            router: null,
            userStore: null,
            id: null,
            patientStore: null,
            appointmentStore: null,
            loading: false,
            patientSearch: '',
            filteredPatients: [],
        };
    },

    created() {
        this.router = useRouter();
        this.userStore = useUserStore();
        this.id = this.$route.params.id;
        this.patientStore = usePatientStore();
        this.appointmentStore = useAppointmentStore();
    },

    mounted() {
        if (this.userStore.role !== 'doctor' || !this.userStore.isAuthenticated) {
            this.router.replace('/');
            return;
        }
        this.fetchItems("patient");
        this.fetchItems("appointment");
    },

    methods: {
        getStore(type) {
            if (type === "patient") return this.patientStore;
            return this.appointmentStore;
        },

        async cancelAppointment(id) {
            this.loading = true;
            try {
                await this.appointmentStore.changeStatus(id, "cancelled");
            } catch (err) {
                console.error(err);
            } finally {
                this.loading = false;
            }
        },


        async fetchItems(type) {
            const store = this.getStore(type);
            this.loading = true;
            try {
                await store.getAll();
            } catch (_) { }
            finally { this.loading = false; }
        },

        filterPatients() {
            const search = this.patientSearch.toLowerCase();
            this.filteredPatients = this.doctorPatients.filter(p =>
                p.details.name.toLowerCase().includes(search) ||
                p.id.toString().includes(search) ||
                p.contact_number?.toLowerCase().includes(search)
            );
        },

        async refreshAll() {
            await Promise.all([
                this.patientStore.getAll(),
                this.appointmentStore.getAll(),
            ])
        },

        async deleteItem(type, id) {
            const store = this.getStore(type);
            this.loading = true;
            try {
                await store.del(id);
                await this.refreshAll();
            } catch (_) { }
            finally { this.loading = false; }
        },


    },
    computed: {
        doctorPatients() {
            console.log()
            if (!this.appointmentStore.appointments || !this.patientStore.patients) return [];


            // Get all active appointments of this doctor
            const activeAppts = this.appointmentStore.appointments.filter(
                a => a.doctor_id === Number(this.id) && a.status !== 'cancelled'
            );
            console.log(activeAppts)
            // Get unique patient IDs from these appointments
            const patientIds = [...new Set(activeAppts.map(a => a.patient_id))];

            // Return patients whose ID is in the list
            return this.patientStore.patients.filter(p => patientIds.includes(p.id));
        }
    }

};
</script>

<style>
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
    z-index: 10000;
    backdrop-filter: blur(1px);
}

.summary-card {
    width: 200px;
    margin: 0.5rem;
    box-shadow: #e4dbdb 11px 10px 20px 3px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
</style>