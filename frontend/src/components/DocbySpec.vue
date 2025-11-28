<template>

    <AdminTable title="Doctors' List" placer="Search by name or specialization" v-model:srchstring="doctorSearch"
        :filtfunc="filterDoctors" emptyLabel="doctors" nameColumn="Name"
        :items="doctorSearch ? filteredDoctors : docStore.doctors" :loading="loading" headcon="bi bi-hospital me-2"
        iconClass="bi bi-person-circle fs-4 text-primary"
        @refresh="fetchDocs" @check="(a)=>$router.push(`/pdash/${a.did}/avail?pid=${$route.params.id}`)" />
    

    <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<script>
import useDocStore from '@/stores/doctors';
import AdminTable from '@/components/AdminTable.vue';

export default {
    name: 'DocbySpec',

    components: { AdminTable },

    data() {
        return {
            docStore: null,
            loading: false,
            doctorSearch: '',
            filteredDoctors: [],
        };
    },

    created() {
        this.docStore = useDocStore();
    },

    mounted() {
        this.fetchDocs();
    },

    methods: {
        async fetchDocs() {
            this.loading = true;
            try {
                await this.docStore.getbySpec(Number(this.$route.query.sid));
                this.filteredDoctors = this.docStore.doctors;
                console.log(this.docStore.doctors)
                console.log(this.filteredDoctors)
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