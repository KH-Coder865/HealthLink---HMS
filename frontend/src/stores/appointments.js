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
                let res=null;
                if(pid!==null && did!==null)
                    res = await api.get(`/appointment?pid=${pid}&did=${did}`);
                else if(pid)
                    res = await api.get(`/appointment?pid=${pid}`);
                else if(did)
                    res = await api.get(`/appointment?did=${did}`);
                else
                    throw new Error("PID or DID not found!")
                const finres = res.filter(a => a.status === status);
                return finres;
            } catch (err) {
                console.error("Failed to fetch history:", err);
                return [];
            }
        },

        async update(id, data) {
            if("treatment" in data) {
                const tdat={
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
        }
    }
});


export default useAppointmentStore;