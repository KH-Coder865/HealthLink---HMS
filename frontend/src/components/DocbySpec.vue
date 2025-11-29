<template>
    <div class="d-flex flex-column align-items-center">

        <div class="card-header mt-3 ms-0 p-2 rounded-2 mb-1 fw-bold d-flex fs-header justify-content-between align-items-center">
            <span><i class="bi bi-journal-bookmark me-2"></i>Overview</span>
            <i class="btn btn-outline-primary bi-arrow-left-circle fs-6 "
            @click="$router.back()">&nbsp;Back</i>
        </div>
        <div style="color: #fd7e14; width: 80vw;" class="fw-bolder">
            <span class="fs-1 text-danger"><i class="bi bi-quote me-2"></i></span>{{ this.spec.description }}
        </div>
    </div>
        
        
        <AdminTable title="Doctors' List" placer="Search by name or specialization" v-model:srchstring="doctorSearch"
        :filtfunc="filterDoctors" emptyLabel="doctors" nameColumn="Name"
        :items="doctorSearch ? filteredDoctors : docStore.doctors" :loading="loading" headcon="bi bi-hospital me-2"
        iconClass="bi bi-person-circle fs-4 text-primary" @refresh="fetchDocs"
        @check="(a) => $router.push(`/pdash/${a.did}/avail?pid=${$route.params.id}`)"
        @prof="(a) => $router.push(`/user/${a.uid}/profile?did=${a.did}`)" />
        
        
        <div v-if="loading" class="loader-overlay d-flex flex-column">
            <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
            Loading.....
        </div>
</template>

<script>
import api from '@/utils/api';
import useDocStore from '@/stores/doctors';
import AdminTable from '@/components/AdminTable.vue';

export default {
    name: 'DocbySpec',

    components: { AdminTable },

    data() {
        return {
            docStore: null,
            loading: false,
            spec: null,
            doctorSearch: '',
            filteredDoctors: [],
        };
    },

    async created() {
        this.docStore = useDocStore();
        await this.fetchSpec();
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

        async fetchSpec() {
            this.spec =  await api.get(`/specialization?id=${this.$route.query.sid}`);
        }
    },
};
</script>

<style>
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
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
    backdrop-filter: blur(1px);
}

.fs-header {
    font-size: 2rem;
}

.card-header {
    background-color: rgb(251, 176, 122) !important;
    min-width: 80vw;
    margin-left: 100px;
    max-width: 80vw;
}

.summary-card {
    width: 200px;
    margin: 0.5rem;
    box-shadow: #e4dbdb 11px 10px 20px 3px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

@media (max-width: 800px) {
    .fs-header {
        font-size: 1.5rem;
    }
}

@media (max-width: 400px) { 
    .fs-header {
        font-size: 1.3rem;
    }
}
</style>