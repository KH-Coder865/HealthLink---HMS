<template>
    <div class="mdev mt-4">
        
    <div class="d-flex flex-column align-items-center">
            <!-- Header -->
            <div
                class="card-header p-2 ms-0 rounded-2 mb-1 fw-bold m-0 d-flex fs-header justify-content-between align-items-center">
                <span><i :class="headcon"></i>{{ title }}</span>
                <i v-if="!$route.path.includes('adash') && !$route.path.includes('pdash')" class="btn btn-outline-primary bi-arrow-left-circle fs-6 " @click="$router.back()">&nbsp;Back</i>
                <button id="crt" class="btn btn-success btn-sm" v-if="$route.path.includes('adash') && emptyLabel==='doctors'" @click="$emit('create')">
                    <i class="fs-6 bi bi-person-plus"></i> Create
                </button>
            </div>
            <div style="max-width:80vw" class="input-group mb-4">
                <span class="input-group-text p-sm-2 px-1 w-sm-full">
                    <i class="bi bi-search me-2"></i>
                    {{ emptyLabel.charAt(0).toUpperCase() + emptyLabel.slice(1) }}
                </span>
                <input type="text" class="form-control" :placeholder="placer" :value="srchstring"
                    @input="$emit('update:srchstring', $event.target.value); filtfunc()" />
            </div>


            <!-- Table -->
            <div class="table-responsive mt-2 tab">
                <table class="table table-hover align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-999">
                        <tr>
                            <th v-if="$route.path.includes('pdash')">S. No.</th>
                            <th v-else>ID</th>
                            <th>{{ nameColumn }}</th>
                            <th>{{ specont }}</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>

                        <!-- If empty -->
                        <tr v-if="(!items)||(!items.length && !loading)">
                            <td colspan="4" class="text-muted p-4">
                                No {{ emptyLabel }} found.
                                <button @click="$emit('refresh')" class="btn btn-sm btn-outline-primary">
                                    Refresh
                                </button>
                            </td>
                        </tr>

                        <!-- If loading -->
                        <tr v-else-if="loading">
                            <td colspan="4" class="text-center p-4">
                                <div class="spinner-border spinner-border-sm text-primary" role="status">
                                    <span class="visually-hidden"></span>
                                </div>Loading...
                            </td>
                        </tr>

                        <!-- List rows -->
                        <tr v-else v-for="(item,i) in items" :key="item.id">
                            <td>
                                <div v-if="$route.path.includes('pdash')" class="d-flex justify-content-center align-items-center gap-2">
                                    {{ i + 1 }}
                                </div>
                                <div v-else class="d-flex justify-content-center align-items-center gap-2">
                                    {{ item.id }}
                                </div>
                            </td>
                            <td>
                                <div class="d-flex justify-content-center align-items-center gap-2">
                                    <i :class="iconClass"></i>
                                    <span class="fw-semibold">{{ item.details.name }}</span>
                                </div>
                            </td>

                            <td>
                                <div v-if="!$route.path.includes('pdash')" class="d-flex justify-content-center align-items-center gap-2">
                                    <div v-if="specont === 'Specialization'">
                                        {{ item.specializations?.name || item.specializations?.[0]?.name || '-' }}
                                    </div>
                                    <div v-else>
                                        {{ item.contact_number || '-' }}
                                    </div>
                                </div>
                            </td>

                            <td>
                                <div class="d-flex justify-content-center gap-2 action-buttons">

                                    <button v-if="$route.path.includes('adash')" class="btn btn-warning btn-sm" @click="$emit('edit', item.id)">
                                        <i class="bi bi-pencil-square"></i> Edit
                                    </button>

                                    <button v-if="$route.path.includes('adash')" class="btn btn-danger btn-sm" @click="$emit('delete', item.id)">
                                        <i class="bi bi-trash"></i> Delete
                                    </button>

                                    <button
                                        v-if="$route.path.includes('adash')"
                                        :class="item.details.active ? 'btn btn-outline-dark btn-sm' : 'btn btn-success btn-sm'"
                                        @click="$emit('toggle', item)">
                                        <i
                                            :class="item.details.active ? 'bi bi-person-fill-slash' : 'bi bi-person-check'"></i>
                                        {{ item.details.active ? 'Blacklist' : 'Un-Blacklist' }}
                                    </button>

                                    <button v-if="$route.path.includes('pdash')" class="btn text-wrap fw-bold btn-outline-secondary" @click="$emit('check', {did: item.id})"><i class="bi bi bi-clock-fill me-2"></i>Check Availability</button>
                                    <button v-if="$route.path.includes('pdash')" class="btn text-wrap fw-bold btn-outline-primary" @click="$emit('prof', {uid: item?.details?.id, did: item.id})"><i class="bi bi-file-earmark-person-fill me-2"></i>View Profile</button>

                                    <button class="btn btn-success fw-bold" v-if="$route.path.includes('ddash')" @click="$emit('view', {pid: item.id})"><i class="bi bi-eye me-2"></i>View</button>

                                </div>
                            </td>
                        </tr>

                    </tbody>

                </table>
            </div>
</div>
        </div>
</template>

<script>
export default {
    name: "AdminTable",

    data() {
        return {
            srch: "",
        }
    },

    created() {
        this.srch = this.srchstring
    },

    props: {
        title: String,
        specont: String,
        srchstring: String,
        filtfunc: Function,
        placer: String,
        headcon: String,
        nameColumn: { type: String, default: "Name" },
        items: { type: Array, default: () => [] },
        loading: Boolean,
        emptyLabel: { type: String, default: "items" },
        iconClass: { type: String, default: "bi bi-person-circle fs-4 text-primary" }
    }
};
</script>

<style scoped>
.tab {
    max-height: 300px;
}

.fs-header {
    font-size: 2rem;
}

.card-header {
    background-color: rgb(251, 176, 122);
}

.action-buttons {
    flex-direction: row;
}

@media (max-width: 800px) {
    

    .fs-header {
        font-size: 1.5rem;
    }

    table {
        width: 60vw;
    }

    table th,
    table td {
        padding: 0.5rem;
        white-space: nowrap;
    }
    .card-header {
        width: 100vw !important;
    }
    .action-buttons {
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
    }


    .btn {
        width: 100%;
        max-width: 120px;
        padding: 0.5rem;
    }
}

@media (max-width: 400px) {
    

    .fs-header {
        font-size: 1.3rem;
        text-wrap: nowrap;
    }

    .tab {
        max-width: 300px;
    } 

    table th:first-child,
    table td:first-child {
        position: sticky;
        left: 0;
        background-color: rgb(241, 239, 239);
    }

    table th,
    table td {
        padding: 0.5rem;
        white-space: nowrap;
    }

    

    .action-buttons {
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
    }


    #crt {
        width: 50px !important;
        font-size: small;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
        overflow-x: hidden;
        padding: 0;
    }
}
</style>
