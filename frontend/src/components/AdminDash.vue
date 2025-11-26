<template>
    <div class="d-flex mt-2 justify-content-center gap-5 flex-wrap mb-4">
        <div class="summary-card text-center bg-light p-3 rounded">
            <h5>Total Doctors</h5>
            <p class="fs-2 text-primary fw-bold">{{ docStore.doctors.length }}</p>
        </div>
        <div class="summary-card text-center bg-light p-3 rounded">
            <h5>Total Patients</h5>
            <p class="fs-2 text-success fw-bold">{{ patientStore.patients.length }}</p>
        </div>
        <div class="summary-card text-center bg-light p-3 rounded">
            <h5>Total Appointments Till Date</h5>
            <p class="fs-2 text-danger fw-bold">{{ appointmentStore.appointments.length }}</p>
        </div>
    </div>

    <AdminTable title="Registered Doctors" placer="Search by name or specialization" v-model:srchstring="doctorSearch"
        :filtfunc="filterDoctors" emptyLabel="doctors" nameColumn="Doctor Name"
        :items="doctorSearch ? filteredDoctors : docStore.doctors" :loading="loading" headcon="bi bi-hospital me-2"
        iconClass="bi bi-person-circle fs-4 text-primary" specont="Specialization"
        @create="router.push('/adash/doctor/create')" @refresh="fetchItems('doctor')" @edit="editItem('doctor', $event)"
        @delete="deleteItem('doctor', $event)" @toggle="toggleBlacklist('doctor', $event)" />

    <AdminTable title="Registered Patients" placer="Search by name, id or contact no."
        headcon="bi bi-person-lines-fill me-2" emptyLabel="patients" nameColumn="Patient Name"
        v-model:srchstring="patientSearch" :filtfunc="filterPatients"
        :items="patientSearch ? filteredPatients : patientStore.patients" :loading="loading"
        iconClass="bi bi-person-fill fs-4 text-success" specont="Contact No."
        @create="router.push('/adash/patient/create')" @refresh="fetchItems('patient')"
        @edit="editItem('patient', $event)" @delete="deleteItem('patient', $event)"
        @toggle="toggleBlacklist('patient', $event)" />

    <AppointmentsTable @refresh="fetchItems('appointment')"
        @view="router.push({ path: '/adash_view/appts', query: $event })" @cancel="cancelAppointment" />

    <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<script>
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';
import useDocStore from '@/stores/doctors';
import usePatientStore from '@/stores/patients';
import useAppointmentStore from '@/stores/appointments';
import AdminTable from '@/components/AdminTable.vue';
import AppointmentsTable from '@/components/ApptTable.vue';
import api from "@/utils/api";

export default {
    name: 'AdminDash',

    components: { AdminTable, AppointmentsTable },

    data() {
        return {
            router: null,
            userStore: null,
            docStore: null,
            patientStore: null,
            appointmentStore: null,
            loading: false,
            doctorSearch: '',
            patientSearch: '',
            filteredDoctors: [],
            filteredPatients: [],
        };
    },

    created() {
        this.router = useRouter();
        this.userStore = useUserStore();
        this.docStore = useDocStore();
        this.patientStore = usePatientStore();
        this.appointmentStore = useAppointmentStore();
    },

    mounted() {
        if (!this.userStore.isAdmin || !this.userStore.isAuthenticated) {
            this.router.replace('/');
            return;
        }
        this.fetchItems("doctor");
        this.fetchItems("patient");
        this.fetchItems("appointment");
    },

    methods: {
        getStore(type) {
            if (type === "doctor") return this.docStore;
            if (type === "patient") return this.patientStore;
            return this.appointmentStore;
        },


        async cancelAppointment(id) {
            this.loading = true;
            try {
                await this.appointmentStore.changeStatus(id, "cancelled");
                // refresh child table immediately
                this.$refs.apptTable.refreshData();
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
                if (type === "doctor") this.filteredDoctors = store.doctors;
                if (type === "patient") this.filteredPatients = store.patients;
            } catch (_) { }
            finally { this.loading = false; }
        },

        filterDoctors() {
            const search = this.doctorSearch.toLowerCase();
            this.filteredDoctors = this.docStore.doctors.filter(d =>
                d.details.name.toLowerCase().includes(search) ||
                d.specializations?.name?.toLowerCase().includes(search)
            );
        },

        filterPatients() {
            const search = this.patientSearch.toLowerCase();
            this.filteredPatients = this.patientStore.patients.filter(p =>
                p.details.name.toLowerCase().includes(search) ||
                p.id.toString().includes(search) ||
                p.contact_number?.toLowerCase().includes(search)
            );
        },

        async refreshAll() {
            await Promise.all([
                this.docStore.getAll(),
                this.patientStore.getAll(),
                this.appointmentStore.getAll(),
            ])
        },

        async editItem(type, id) {
            const store = this.getStore(type);
            try {
                if (type === 'doctor')
                    await store.getbyId({ id: id, uid: null })
                else
                    await store.getbyId(id);
                this.router.push(`/adash/${type}/${id}/edit`);
            } catch (_) { }
        },

        async deleteItem(type, id) {
            const store = this.getStore(type);
            this.loading = true;
            try {
                await store.del(id);
                await this.refreshAll();

                if (type === "doctor" && this.doctorSearch) this.filterDoctors();
                if (type === "patient" && this.patientSearch) this.filterPatients();
            } catch (_) { }
            finally { this.loading = false; }
        },

        async toggleBlacklist(type, item) {
            this.loading = true;
            const store = this.getStore(type);
            try {
                if (item.details.active) {
                    await store.blacklist(item.id);
                } else {
                    await api.patch(`/users/${item.details.id}`, { active: true });
                }
                await store.getAll();

                if (type === "doctor" && this.doctorSearch) this.filterDoctors();
                if (type === "patient" && this.patientSearch) this.filterPatients();
            } catch (_) { }
            finally { this.loading = false; }
        },
    },
};
</script>

<style>
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