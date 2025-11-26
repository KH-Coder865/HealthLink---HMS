<template>
    <div class="ms-4 d-flex justify-content-center overflow-hidden mt-4">
        <div class="entity-card">
            <div class="card-header rounded-2 p-2 mb-4 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-calendar4-week me-2"></i>Edit Availability</span>
                
                <i class="btn btn-outline-primary bi-arrow-left-circle fs-6 " @click="$router.back()">&nbsp;Back</i>
            </div>

            <div class="table-responsive mt-2 tab">
                <table class="table table-hover table-bordered align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-0">
                        <tr>
                            <th rowspan="2">Days</th>
                            <th colspan="2">Time Slots</th>
                        </tr>
                        <tr>
                            <th>09:00 am - 12:00 noon</th>
                            <th>04:00 pm - 09:00 pm</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(v,k) in docStore?.singdoc?.availability" :key="k">
                            <td class="fw-bold">{{ k }}</td>
                            <td v-if="v.morning"><button class="btn btn-sm btn-success" @click="toggleAvail(k,'morning')">Available</button></td>
                            <td v-else><button class="btn btn-sm btn-danger" @click="toggleAvail(k,'morning')">Not Available</button></td>
                            <td v-if="v.evening"><button class="btn btn-sm btn-success" @click="toggleAvail(k,'evening')">Available</button></td>
                            <td v-else><button class="btn btn-sm btn-danger" @click="toggleAvail(k,'evening')">Not Available</button></td>
                        </tr>
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
import useDocStore from "@/stores/doctors";

export default {
    name: "DocAvail",

    data() {
        return {
            docStore: null,
            loading: false,
        };
    },

    async created() {
        this.loading=true;
        this.docStore = useDocStore();
        await this.docStore.getbyId({id: this.$route.params.id, uid: null});
        console.log(this.docStore.singdoc)
        if(!this.docStore.singdoc.availability) {
            let avail={};
            const days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
            days.forEach(d => {
                avail[d]={};
                avail[d].morning=0;
                avail[d].evening=0;
            });
            // console.log(avail)
            await this.docStore.update(this.$route.params.id, {
                availability: avail,
            })
        }
        this.loading=false;
    },

    methods: {
        async toggleAvail(k, c) {
            this.loading=true;
            let avail=this.docStore.singdoc.availability;
            avail[k][c]= avail[k][c] == 1 ? 0 : 1;
            await this.docStore.update(this.$route.params.id, {
                availability: avail,
            })
            this.loading=false;
        },
    }

};
</script>