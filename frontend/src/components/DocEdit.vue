<template>
    <UserEditForm
    title="Edit Doctor"
    :showEmrgency="false"
    :showAge="false"
    :showSpecialization="true"
    :showGender="false"
    :showAddress="flase"
    :load="loadDoc"
    :save="saveDoc"
/>
</template>

<script>
import UserEditForm from "@/components/UserEdit.vue";
import useDocStore from "@/stores/doctors";

export default {
    components: { UserEditForm },

    data() { 
        return { 
            store: useDocStore(),
            id: this.$route.params.id 
        } 
    },

    methods: {
        async loadDoc() {
            const doc = await this.store.getbyId({id: this.id, uid:null});
            return doc;
        },

        async saveDoc(form) {
            return this.store.update(this.id, {
                name: form['name'],
                contact_number: form.contact_number,
                specialization: form.specialization
            });
        }
    }
};
</script>
