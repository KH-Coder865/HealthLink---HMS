<template>
  <nav class="navbar navbar-expand-lg sticky-top shadow-sm" style="background-color:#E65100; z-index: 9999;">
    <div class="container-fluid py-2 px-4">

      <router-link class="navbar-brand text-white fw-bold fs-4" to="/">
        Hello
      </router-link>

      <button class="navbar-toggler bg-orange border-0" type="button" data-bs-toggle="collapse"
        data-bs-target="#navMenu">
        <span class="navbar-toggler-icon" style="filter: invert(1);"></span>
      </button>

      <div class="collapse navbar-collapse" id="navMenu">

        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link v-if="isAdmin" to="/adash"
              class="nav-link nav-underline text-white fw-semibold">Dashboard</router-link>

            <router-link v-else-if="isPatient" :to="patDash"
              class="nav-link nav-underline text-white fw-semibold">Dashboard</router-link>

            <router-link v-else-if="isDoctor" :to="doctorDash"
              class="nav-link nav-underline text-white fw-semibold">Dashboard</router-link>
          </li>

          <li v-if="isPatient" class="nav-item">
            <router-link :to="patHist"
              class="nav-link nav-underline text-white fw-semibold">History</router-link>
          </li>

          <li class="nav-item">
            <router-link to="/" class="nav-link nav-underline text-white fw-semibold">Home</router-link>
          </li>

          <template v-if="!userStore.isAuthenticated">
            <li class="nav-item">
              <router-link to="/login" class="nav-link nav-underline text-white fw-semibold">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/signup" class="nav-link nav-underline text-white fw-semibold">Sign Up</router-link>
            </li>
          </template>
        </ul>

        <div v-if="userStore.isAuthenticated" class="dropdown ms-2 ms-lg-4">


          <button class="btn d-flex align-items-center text-white dropdown-toggle border-0" type="button"
            data-bs-toggle="dropdown">

            <i class="bi bi-person-circle me-2"></i>
            <span v-if="isPatient" class="fw-semibold d-inline">{{ displayName('pat') }}</span>
            <span v-if="isDoctor" class="fw-semibold d-inline">{{ displayName('doc') }}</span>
            <span v-if="isAdmin" class="fw-semibold d-inline">{{ displayName('admin') }}</span>
          </button>

          <ul class="dropdown-menu">
            <li><router-link class="dropdown-item" :to="`/user/${userStore?.user.id}/profile`">Profile</router-link>
            </li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link to="/" class="dropdown-item" @click="userStore.logout">Logout</router-link></li>
          </ul>
        </div>

      </div>
    </div>
  </nav>
</template>

<script>
import useUserStore from '@/stores/user';
import usePatientStore from '@/stores/patients';
import useDocStore from '@/stores/doctors';

export default {
  name: 'Navbar',

  data() {
    return {
      userStore: useUserStore(),
      docStore: useDocStore(),
      patStore: usePatientStore(),
      patDash: "/",
      patHist: "/",
      doctorDash: "/", // resolved URL stored here
    };
  },

  async created() {
    if (this.isDoctor) {
      const uid = this.userStore.user.id;
      const res = await this.docStore.getbyId({ id: null, uid });

      this.doctorDash = `/ddash/${res.id}`;
    }
    else if (this.isPatient) {
      const uid = this.userStore.user.id;
      const res = await this.patStore.getbyId({ id: null, uid });

      this.patDash = `/pdash?id=${res.id}`;
      this.patHist = `/pdash/appts?pid=${res.id}`
    }
  },

  methods: {
    displayName(name) {
      if(name === 'admin')
        return this.userStore?.user?.name ;
      else if(name === 'pat')
        return this.patStore?.singpat?.details?.name;
      return this.docStore?.singdoc?.details?.name;
    },
  },

  computed: {
    isAuthenticated() {
      return this.userStore.isAuthenticated;
    },
    isAdmin() {
      return this.userStore.isAdmin;
    },
    isPatient() {
      return this.isAuthenticated && this.userStore?.user?.role === 'patient';
    },
    isDoctor() {
      return this.isAuthenticated && this.userStore?.user?.role === 'doctor';
    },
  }
};
</script>

<style scoped>
.nav-underline {
  position: relative;
  padding-bottom: 4px;
}

.bg-orange {
  background-color: #cc4902 !important;
}

.nav-underline::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0px;
  width: 0%;
  height: 2px;
  background: white;
  transition: width 0.3s ease-in-out;
}

.nav-underline:hover::after {
  width: 100%;
}

@media screen and (max-width: 991px) {
  .nav-underline:hover::after {
    width: 55px;
  }

  .navbar-nav .nav-link {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 120px;
  }

  .navbar-collapse {
    background-color: #E65100;
    margin-top: 0.5rem;
    padding: 1rem;
    border-radius: 0.375rem;
  }

  .navbar-nav {
    margin: 0 !important;
  }
}
</style>
