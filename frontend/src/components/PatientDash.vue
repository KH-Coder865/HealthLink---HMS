<template>
    <SpecTable :loading="loading" @refresh="fetchItems('appointment')"
        @view="router.push({ path: '/ddash_view/appts', query: $event })" @cancel="cancelAppointment" />

    <AppointmentsTable @refresh="fetchAppointments" @cancel="cancelAppointment" />

    <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<script>
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';
import useAppointmentStore from '@/stores/appointments';
import AppointmentsTable from '@/components/ApptTable.vue';
import SpecTable from './SpecTable.vue';

export default {
    name: 'PatientDash',

    components: { AppointmentsTable, SpecTable },

    data() {
        return {
            router: null,
            userStore: null,
            apptStore: null,
            loading: false,
        };
    },

    created() {
        this.router = useRouter();
        this.userStore = useUserStore();
        this.apptStore = useAppointmentStore();
    },

    mounted() {
        if (this.userStore.role !== 'patient' || !this.userStore.isAuthenticated) {
            this.router.replace('/');
            return;
        }
        this.fetchAppointments();
    },

    methods: {
        async fetchAppointments() {
            this.loading = true;
            try {
                await this.apptStore.getAllbyIds({
                    pid: this.$route.query.id,
                    status: 'upcoming',
                });
            } catch (_) {}
            finally { this.loading = false; }
        },

        async cancelAppointment(id) {
            this.loading = true;
            try {
                await this.apptStore.changeStatus(id, "cancelled");
                await this.apptStore.getAll();
            } catch (err) {
                console.error(err);
            } finally {
                this.loading = false;
            }
        }
    },

    computed: {
        patientAppointments() {
            if (!this.apptStore.appointments) return [];

            const pid = this.userStore.id;

            return this.apptStore.appointments.filter(
                a => a.patient_id === pid && a.status !== "cancelled"
            );
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
</style>
