import { defineStore } from "pinia";
import api from "@/utils/api";
import useUserStore from "@/stores/user";

const usePatientStore = defineStore("patient", {
    state: () => ({
        patients: [],
        singpat: null,
    }),

    actions: {
        async getAll() {
            const res = await api.get("/patients");
            this.patients = res;
            return res;
        },

        async getbyId({ id = null, uid = null }) {
            let res = null;
            if (id)
                res = await api.get(`/patient?id=${id}`);
            else if (uid)
                res = await api.get(`/patient?uid=${uid}`);
            this.singpat = res;
            return res;
        },

        async del(id) {
            const userStore = useUserStore();
            const patres = await api.get(`/patient?id=${id}`);
            const res = await userStore.del(patres.details.id);
            await this.getAll();
            return res;
        },

        async update(id, data) {
            const patientData = {
                emergency_contact: data.emergency_contact,
                contact_number: data.contact_number,
                age: data.age,
                gender: data.gender,
                address: data.address,
            };

            const userData = {
                name: data.name,
            };

            const patres = await this.getbyId({id, uid:null});
            await api.patch(`/patients/${id}`, patientData);
            await api.patch(`/users/${patres.details.id}`, userData);

            await this.getAll();
        },

        async edit(id, data) {
            const res = await api.patch(`/patients/${id}`, data);
            await this.getAll();
            return res;
        },

        async blacklist(id) {
            const userStore = useUserStore();
            const patient = await this.getbyId({id, uid: null});
            const userId = patient.details.id;

            await userStore.edit(userId, {
                active: false
            });

            await this.getAll();

            return { message: "Patient blacklisted successfully" };
        },
    },
});

export default usePatientStore;
