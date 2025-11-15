
<template>
  <nav class="navbar navbar-expand-lg sticky-top shadow-sm" style="background-color:#E65100;">
    <div class="container-fluid py-2 px-4">

      <!-- Brand -->
      <a class="navbar-brand text-white fw-bold fs-4" href="#">
        Hello
      </a>

      <!-- Toggler for mobile -->
      <button class="navbar-toggler bg-orange border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
        <span class="navbar-toggler-icon" style="filter: invert(1);"></span>
      </button>

      <!-- Menu + Profile -->
      <div class="collapse navbar-collapse" id="navMenu">

        <!-- Left menu -->
        <ul class="navbar-nav ms-auto gap-3">
          <div class="hov">

            <li class="nav-item">
              <router-link to="/" class="nav-link nav-underline text-white fw-semibold">Home</router-link>
            </li>
          </div>
          <template v-if="!userStore.isAuthenticated">
            <li class="nav-item">
              <router-link to="/login" class="nav-link nav-underline text-white fw-semibold">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/signup" class="nav-link nav-underline text-white fw-semibold">Sign Up</router-link>
            </li>
          </template>
        </ul>

        <!-- Profile Section -->
        <div v-if="userStore.isAuthenticated" class="dropdown ms-4">
          <button 
            class="btn d-flex align-items-center text-white dropdown-toggle border-0" 
            type="button" 
            data-bs-toggle="dropdown">
            
            <!-- Avatar -->
            <i class="bi bi-person-circle"></i>
            <span class="fw-semibold">{{ displayName }}</span>
          </button>

          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#">Profile</a></li>
            <li><a class="dropdown-item" href="#">Settings</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><router-link to="/" class="dropdown-item" @click="userStore.logout">Logout</router-link></li>
          </ul>
        </div>

      </div>
    </div>
  </nav>
</template>

<script>
import useUserStore from '@/stores/user';

export default {
  name: 'Navbar',
  data() {
    return {
      userStore: null
    };
  },

  created() {
    this.userStore = useUserStore();
  },

  computed: {
    isAuthenticated() {
      return this.userStore.isAuthenticated;
    } ,
    isAdmin(){
      return this.userStore.isAdmin;
    },
    isPatient(){
      return this.userStore?.user?.role === 'patient';
    },
    displayName(){
      if(!this.userStore || !this.userStore) return "Account";
      return this.userStore.user.name || this.userStore.user.email || "Account";
    }
  }
};

</script>

<style scoped>
/* Underline hover effect */
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
@media screen and (max-width: 800px) {
  .nav-underline:hover::after {
    width: 55px;
  }
}

</style>
