<template>
    <div style="margin-left: 18%;" class="mdev mt-4">
        <div class="entity-card">

            <div
                class="card-header mb-4 p-2 rounded-2 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-bank2 me-2"></i>Departments Available</span>

                <i class="btn btn-outline-primary bi-arrow-left-circle fs-6 " @click="$router.back()">&nbsp;Back</i>
            </div>

            <div class="table-responsive mt-2 tab">
                <table class="table table-hover align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-0">
                        <tr>
                            <th>ID</th>
                            <th>Specializations</th>
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
                        <tr v-for="s in specs" :key="s.id">
                            <td>{{ s.id }}</td>
                            <td>{{ s.name }}</td>
                            <td>
                                <button @click="$router.push(`/pdash/${$route.query.id}/docs?sid=${s.id}`)" class="btn fw-bold text-wrap btn-outline-success">
                                    <i class="bi bi-eye me-2"></i>View Details
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
import api from "@/utils/api";

export default {
    name: "SpecTable",

    data() {
        return {
            isLoading: false,
            specs: null,
        };
    },

    async created() {
        this.isLoading=true;
        this.specs=await api.get("/specializations")
        this.isLoading=false;
    },


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
