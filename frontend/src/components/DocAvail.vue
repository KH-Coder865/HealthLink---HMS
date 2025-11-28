<template>
    <div class="ms-4 d-flex justify-content-center overflow-hidden mt-4">
        <div class="entity-card">
            <div
                class="card-header rounded-2 p-2 mb-4 fw-bold d-flex fs-header justify-content-between align-items-center">
                <span><i class="bi bi-calendar4-week me-2"></i>
                    <template v-if="$route.path.includes('ddash')">
                        Edit Availability
                    </template>
                    <template v-else-if="$route.path.includes('pdash')">
                        Check Availability
                    </template>
                </span>

                <i class="btn btn-outline-primary bi-arrow-left-circle fs-6 " @click="$router.back()">&nbsp;Back</i>
            </div>

            <div class="table-responsive mt-2 tab">
                <table class="table table-hover table-bordered align-middle text-center mb-0">
                    <thead class="table-light sticky-top z-3">
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
                        <tr v-for="(v, k) in docStore?.singdoc?.availability" :key="k">
                            <td v-if="Object.keys(docStore.singdoc.availability)[0] === k && !checkDate(k)"
                                class="fw-bold bg-warning text-danger">
                                <button v-if="$route.path.includes('ddash')" id="del" class="btn me-2 btn-danger">
                                    <i class="bi bi-trash"></i>
                                </button>{{ k }}
                            </td>
                            <td v-else class="fw-bold">{{ k }}</td>

                            <td v-if="Object.keys(docStore.singdoc.availability)[0] === k && !checkDate(k)"
                                class="fw-bold bg-warning text-danger"><button class="btn z-0 btn-sm btn-danger"
                                    disabled>N/A</button></td>
                            <td v-else-if="v.morning && $route.path.includes('pdash')">
                                <div class="d-flex gap-2 justify-content-center flex-sm-wrap">
                                    <button class="btn btn-sm btn-success" disabled>
                                        Available
                                    </button>
                                    <button class="btn btn-primary btn-sm" @click="handleBooking(k, 'morning')">
                                        <i class="bi bi-bookmark-plus me-2"></i>Book Slot
                                    </button>
                                </div>
                            </td>
                            <td v-else-if="v.morning && $route.path.includes('ddash')"><button class="btn btn-sm btn-success"
                                    @click="toggleAvail(k, 'morning')">Available</button></td>
                            <td v-else-if="!v.morning && $route.path.includes('pdash')">
                                <button class="btn btn-sm btn-danger" disabled>
                                    Not Available
                                </button>
                            </td>
                            <td v-else-if="$route.path.includes('ddash')"><button class="btn btn-sm btn-danger" @click="toggleAvail(k, 'morning')">Not
                                    Available</button></td>

                            <td v-if="Object.keys(docStore.singdoc.availability)[0] === k && !checkDate(k)"
                                class="fw-bold bg-warning text-danger"><button class="btn z-0 btn-sm btn-danger"
                                    disabled>N/A</button></td>
                            <td v-else-if="v.evening && $route.path.includes('pdash')">
                                <div class="d-flex gap-2 justify-content-center flex-sm-wrap">
                                    <button class="btn btn-sm btn-success" disabled>
                                        Available
                                    </button>
                                    <button class="btn btn-primary btn-sm" @click="handleBooking(k, 'evening')">
                                        <i class="bi bi-bookmark-plus me-2"></i>Book Slot
                                    </button>
                                </div>
                            </td>
                            <td v-else-if="v.evening && $route.path.includes('ddash')"><button class="btn btn-sm btn-success"
                                    @click="toggleAvail(k, 'evening')">Available</button></td>
                            <td v-else-if="!v.evening && $route.path.includes('pdash')">
                                <button class="btn btn-sm btn-danger" disabled>
                                    Not Available
                                </button>
                            </td>
                            <td v-else-if="$route.path.includes('ddash')"><button class="btn btn-sm btn-danger" @click="toggleAvail(k, 'evening')">Not
                                    Available</button></td>
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
    max-width: 1200px;
    /* maximum width for large screens */
    width: 100%;
    /* default full width */
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
        max-width: 90%;
        /* slightly narrower on medium screens */
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

    #del {
        width: fit-content;
        padding: 2px 10px;
    }
}
</style>

<script>
import useDocStore from "@/stores/doctors";
import useAppointmentStore from "@/stores/appointments";

export default {
    name: "DocAvail",

    data() {
        return {
            docStore: null,
            apptStore: null,
            loading: false,
            today: '',
        };
    },

    async created() {
        this.loading = true;
        this.apptStore = useAppointmentStore();
        this.docStore = useDocStore();
        await this.docStore.getbyId({ id: this.$route.params.id });

        this.updateToday();

        const avail = this.docStore.singdoc.availability || {};
        const keys = Object.keys(avail).sort((a, b) => new Date(a) - new Date(b));

        if ((!keys.length || keys[0] !== this.today) && this.$route.path.includes('ddash')) {
            await this.ensureSevenDays();
        }
        if(this.$route.path.includes('ddash')) {
            setInterval(() => {
                this.updateToday();
            }, 60 * 1000);
        }

        this.loading = false;
    },


    watch: {
        today(newDate, oldDate) {
            if (newDate !== oldDate && this.$route.path.includes('ddash')) {
                this.shiftAvailability();
            }
        }
    },

    methods: {
        updateToday() {
            const now = new Date();
            const yyyy = now.getFullYear();
            const mm = String(now.getMonth() + 1).padStart(2, '0');
            const dd = String(now.getDate()).padStart(2, '0');
            this.today = `${yyyy}-${mm}-${dd}`;
        },

        async handleBooking(date, slotType) {
            this.loading = true;

            try {
                await this.apptStore.bookSlot({
                    doctor_id: this.$route.params.id,
                    patient_id: this.$route.query.pid,      // if you store logged-in user
                    slot: slotType,                 // morning / evening
                    dateStr: date
                });

                alert("Slot booked successfully!");
            } catch (err) {
                alert(err.message);
            }

            this.loading = false;
        },

        async ensureSevenDays() {
            let avail = this.docStore.singdoc.availability || {};
            const todayDate = new Date(this.today);

            // remove past dates before today
            Object.keys(avail).forEach(k => {
                if (new Date(k) < todayDate) {
                    delete avail[k];
                }
            });

            // ensure exactly 7 consecutive days starting today
            for (let i = 0; i < 7; i++) {
                const d = new Date(todayDate.getFullYear(), todayDate.getMonth(), todayDate.getDate() + i);
                const key = d.toISOString().substring(0, 10);
                if (!avail[key]) avail[key] = { morning: 0, evening: 0 };
            }

            await this.docStore.update(this.$route.params.id, { availability: avail });
            await this.docStore.getbyId({ id: this.$route.params.id });
        },

        async toggleAvail(k, c) {
            this.loading = true;
            let avail = { ...this.docStore.singdoc.availability };
            avail[k] = { ...avail[k] };
            avail[k][c] = avail[k][c] === 1 ? 0 : 1;

            await this.docStore.update(this.$route.params.id, { availability: avail });
            await this.docStore.getbyId({ id: this.$route.params.id });

            this.loading = false;
        },

        async shiftAvailability() {
            this.loading = true;
            let avail = { ...this.docStore.singdoc.availability };
            const keys = Object.keys(avail).sort((a, b) => new Date(a) - new Date(b));

            // only shift if the first date is not today
            if (keys[0] === this.today) {
                this.loading = false;
                return; // first date is already today, nothing to do
            }

            // remove first day
            delete avail[keys[0]];

            // add new 7th day at the end
            const lastDate = new Date(keys[keys.length - 1]);
            lastDate.setDate(lastDate.getDate() + 1);
            const yyyy = lastDate.getFullYear();
            const mm = String(lastDate.getMonth() + 1).padStart(2, '0');
            const dd = String(lastDate.getDate()).padStart(2, '0');
            const newKey = `${yyyy}-${mm}-${dd}`;

            avail[newKey] = { morning: 0, evening: 0 };

            await this.docStore.update(this.$route.params.id, { availability: avail });
            await this.docStore.getbyId({ id: this.$route.params.id });

            this.loading = false;
        },

        checkDate(k) {
            return k === this.today;
        }
    }
};
</script>