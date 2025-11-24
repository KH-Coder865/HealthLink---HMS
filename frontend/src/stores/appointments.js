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
            const res = await api.get(`/appointments/${id}`);
            this.single = res;
            return res;
        },

        async create(data) {
            const res = await api.post("/appointments", data);
            await this.getAll();
            return res;
        },

        async getHist({ pid = null, did = null }) {
            try {
                const res = await api.get(`/appointment?pid=${pid}&did=${did}`);
                const finres = res.filter(a => a.status === 'completed');
                return finres;
            } catch (err) {
                console.error("Failed to fetch history:", err);
                return [];
            }
        },

        async update(id, data) {
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