import { defineStore } from "pinia";
import api from "@/utils/api";

const useAppointmentStore = defineStore("appointments", {
    state: () => ({
        appointments: [],
        single: null,
    }),

    getters: {
        upcoming(state) {
            return state.appointments.filter(a => a.status === "scheduled");
        }
    },

    actions: {
        async getAll() {
            const res = await api.get("/appointments");
            this.appointments = res;
            return res;
        },

        async getById(id) {
            const res = await api.get(`/appointment?id=${id}`);
            this.single = res;
            return res;
        },

        async create(data) {
            const res = await api.post("/appointments", data);
            await this.getAll();
            return res;
        },

        async getAllbyIds({ pid = null, did = null, status = null }) {
            try {
                let finres = null;
                let res = null;
                if (pid !== null && did !== null)
                    res = await api.get(`/appointment?pid=${pid}&did=${did}`);
                else if (pid)
                    res = await api.get(`/appointment?pid=${pid}`);
                else if (did)
                    res = await api.get(`/appointment?did=${did}`);
                else
                    throw new Error("PID or DID not found!")
                if (status)
                    finres = res.filter(a => a.status === status);
                console.log("store=", finres[0].doctor_name)
                return finres ? finres : res;
            } catch (err) {
                console.error("Failed to fetch history:", err);
                return [];
            }
        },

        async update(id, data) {
            if ("treatment" in data) {
                const tdat = {
                    appointment_id: id,
                    ...data['treatment']
                }
                await api.post('/treatments', tdat)
            }
            const res = await api.patch(`/appointments/${id}`, data);
            await this.getAll();
            return res;
        },

        async del(id) {
            const res = await api.delete(`/appointments/${id}`);
            await this.getAll();
            return res;
        },

        async changeStatus(id, newStatus) {
            const res = await api.patch(`/appointments/${id}`, { status: newStatus });
            await this.getAll();
            return res;
        },

        async bookSlot({ doctor_id, patient_id, slot, dateStr }) {
            const dur = 10;
            const buf = 5;
            const gap = dur + buf;

            const sm = slot === "morning" ? 9 * 60 : 16 * 60;
            const em = slot === "morning" ? 12 * 60 : 21 * 60;

            const res = await this.getAllbyIds({ id: null, did: `${doctor_id}`, status: "scheduled" });
            const filtered = res.filter(a => a.appointment_date === dateStr);
            const times = filtered.map(a => a.appointment_time);


            const xs = times.map(v => {
                const [h, m] = v.split(":").map(Number);
                return h * 60 + m;
            });

            let cur = sm;

            const todayStr = new Date().toISOString().slice(0, 10);
            const isToday = dateStr === todayStr;

            if (isToday) {
                const now = new Date();
                const curMins = now.getHours() * 60 + now.getMinutes();

                if (curMins <= em) {
                    const after20 = curMins + 20;

                    if (after20 > cur) {
                        cur = after20;
                    }
                }
            }

            while (cur <= em) {
                const clash = xs.some(x => Math.abs(cur - x) < gap);

                if (!clash) {
                    const hh = String(Math.floor(cur / 60)).padStart(2, "0");
                    const mm = String(cur % 60).padStart(2, "0");
                    const tt = `${hh}:${mm}`;

                    const data = {
                        doctor_id,
                        patient_id,
                        appointment_date: dateStr,
                        appointment_time: tt,
                        status: "scheduled"
                    };

                    return await api.post("/appointments", data);
                }

                cur += gap;
            }

            throw new Error("No available time slot");
        },



    }
});


export default useAppointmentStore;