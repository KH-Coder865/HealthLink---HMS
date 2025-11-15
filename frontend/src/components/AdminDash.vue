<script setup>
    import useUserStore from '@/stores/user'
    import {onMounted} from 'vue'
    import {useRouter} from 'vue-router'

    const router=useRouter();
    const userStore=useUserStore();
    onMounted(()=>{

        if(!userStore.isAdmin || !userStore.isAuthenticated)
            router.replace('/');
    });
</script>

<template>
    <h1> Admin Page</h1>
</template>