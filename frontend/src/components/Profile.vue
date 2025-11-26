<template>
    <!--Something wrong!-->
  <div class="profile-card card shadow-sm p-3 rounded">
    <div class="d-flex align-items-center mb-3">
      <i class="bi bi-person-circle fs-1 me-3 text-primary"></i>
      <div>
        <h5 class="mb-0">{{ displayName }}</h5>
        <small class="text-muted">{{ roleLabel }}</small>
      </div>
    </div>

    <ul class="list-group list-group-flush">
      <li class="list-group-item">
        <strong>Email:</strong> {{ user.email }}
      </li>

      <li class="list-group-item" v-if="isDoctor || isPatient">
        <strong>Contact:</strong> {{ profile.contact_number || '—' }}
      </li>

      <li class="list-group-item" v-if="isPatient">
        <strong>Age:</strong> {{ profile.age || '—' }}
      </li>

      <li class="list-group-item" v-if="isPatient">
        <strong>Gender:</strong> {{ profile.gender || '—' }}
      </li>

      <li class="list-group-item" v-if="isPatient">
        <strong>Emergency Contact:</strong> {{ profile.emergency_contact || '—' }}
      </li>

      <li class="list-group-item" v-if="isDoctor">
        <strong>Specialization:</strong> {{ specializationName || '—' }}
      </li>
    </ul>

    <div class="mt-3 text-end">
      <router-link :to="editLink" class="btn btn-sm btn-outline-primary">
        Edit Profile
      </router-link>
    </div>
  </div>
</template>

<script>
import useUserStore from "@/stores/user";
import useDocStore from "@/stores/doctors";
import usePatientStore from "@/stores/patients";

export default {
  name: "ProfileCard",
  data() {
    return {
      userStore: null,
      docStore: null,
      patientStore: null,
    };
  },
  computed: {
    user() {
      return this.userStore?.user || {};
    },
    roles() {
      return this.user.roles || [];
    },
    isAdmin() {
      return this.roles.some(r => r.name === "admin");
    },
    isDoctor() {
      return this.roles.some(r => r.name === "doctor");
    },
    isPatient() {
      return this.roles.some(r => r.name === "patient");
    },
    roleLabel() {
      if (this.isAdmin) return "Administrator";
      if (this.isDoctor) return "Doctor";
      if (this.isPatient) return "Patient";
      return "User";
    },
    profile() {
      if (this.isDoctor) return this.docStore.doctors.find(d => d.u_id === this.user.id) || {};
      if (this.isPatient) return this.patientStore.patients.find(p => p.u_id === this.user.id) || {};
      return {};
    },
    specializationName() {
      if (!this.isDoctor || !this.profile.specialization_ref) return "";
      return this.profile.specialization_ref.name;
    },
    displayName() {
      return this.user.name || this.user.email || "Account";
    },
    editLink() {
      if (this.isAdmin) return `/adash/users/${this.user.id}/profile/edit`;
      if (this.isDoctor) return `/ddash/doctors/${this.user.id}/profile/edit`;
      if (this.isPatient) return `/pdash/patients/${this.user.id}/profile/edit`;
      return "/";
    }
  },
  created() {
    this.userStore = useUserStore();
    this.docStore = useDocStore();
    this.patientStore = usePatientStore();
  }
};
</script>

<style scoped>
.profile-card {
  max-width: 400px;
}
.list-group-item {
  padding: 0.5rem 1rem;
}
</style>
