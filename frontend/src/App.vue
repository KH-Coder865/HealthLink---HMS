<script setup>
import Navbar from './components/Navbar.vue'
import AdminTable from './components/AdminTable.vue';
</script>

<template>
  <Navbar msg="Welcome my Admin" />
  <AdminTable nm="Dr. ABCDE" type="doc" hd="Registered Doctors" />
  <AdminTable nm="Mr. FGHIJ" type="pat" hd="Registered Patients" />
</template>

<style scoped>

</style>
