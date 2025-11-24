<template>
    <UserEditForm
    title="Edit Patient"
    :showEmrgency="true"
    :showAge="true"
    :showGender="true"
    :showAddress="true"
    :load="loadPatient"
    :save="savePatient"
/>

</template>

<script>
import UserEditForm from "@/components/UserEdit.vue";
import usePatientStore from "@/stores/patients";

export default {
    components: { UserEditForm },

    data() { 
        return { 
            store: usePatientStore(),
            id: this.$route.params.id 
        } 
    },

    methods: {
        async loadPatient() {
            const pt = await this.store.getbyId(this.id);
            return pt;
        },

        async savePatient(form) {
            return this.store.update(this.id, {
                name: form.name,
                contact_number: form.contact_number,
                emergency_contact: form.emer_contact_number,
            });
        }
    }
};
</script>
