import { defineStore } from "pinia";
import api from "@/utils/api";
import useUserStore from "@/stores/user";

const useDocStore = defineStore("doctor", {
    state: () => ({
        doctors: [],
        singdoc: null,
    }),


    actions: {

        async getAll() {
            const res = await api.get("/doctors");
            this.doctors = res;
            return res;
        },

        async getbyId(id) {
            const res = await api.get(`/doctors/${id}`);
            this.singdoc = res;
            return res;
        },

        async del(id) {
            const userStore=useUserStore();
            const docres=await api.get(`/doctors/${id}`);
            const res= await userStore.del(docres.details.id);
            await this.getAll();
            return res;
        },

        async update(id, data) {
            let specId = null;

            if (data.specialization) {
                try {
                    const specRes = await api.get(`/specialization?name=${data.specialization}`);
                    specId = specRes.id;
                } catch (err) {
                    const specCreate = await api.post('/specializations', { name: data.specialization, description: data.specialization });
                    specId = specCreate.id;
                }
            }

            const doctorData = {
                specialization_id: specId,
                contact_number: data.contact_number,
            };

            const userData = {
                name: data.name,
                email: data.email,
            };
            if (data.password) userData.password = data.password;
            const docres = await this.getbyId(id);
            await api.patch(`/doctors/${id}`, doctorData);
            await api.patch(`/users/${docres.details.id}`, userData);

            await this.getAll();
        },


        async create(data) {
            const spec = data.specialization
            let specid = null

            try {
                const specres = await api.get(`/specializations?name=${spec}`)
                specid = specres.id
            } catch {
                const specreate = await api.post('/specializations', { name: spec, description: spec })
                specid = specreate.id
            }

            const userPayload = {
                name: data.name,
                email: data.email,
                password: data.password,
                role: 'doctor'
            }

            let docdata=null
            try {
                docdata = await api.post('/auth/register', userPayload)
            } catch (error) {
                throw { message: error.message || "Unknown error" }
            }

            const doctorPayload = {
                u_id: docdata.id,
                specialization_id: specid,
                contact_number: data.contact_number,
                availability: null
            }

            const res = await api.post('/doctors', doctorPayload)
            await this.getAll()
            return res
        },

        async blacklist(id) {
            const userStore=useUserStore();

            const doctor = await this.getbyId(id);

            const userId = doctor.details.id;   // u_id correctly returned

            await userStore.edit(userId, {
                active: false
            });

            await this.getAll();

            return { message: "Doctor blacklisted successfully" };
        },




    },
});

export default useDocStore;