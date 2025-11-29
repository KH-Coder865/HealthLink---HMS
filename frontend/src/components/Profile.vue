<template>
  <div class="d-flex flex-column align-items-center">
    <div style="min-width: 42vw;" class="d-flex justify-content-between head align-items-center">
      <h2 style="color: orangered; text-decoration: underline;" class="m-3 fw-bold">Profile Details</h2>
      <i class="btn btn-outline-primary bi-arrow-left-circle fs-6 " @click="$router.back()">&nbsp;Back</i>
    </div>

    <div class="d-flex mt-2 ms-2 me-2 prof_card rounded shadow-sm">

      <div class="d-flex flex-md-row flex-column gap-4 align-items-start">

        <!-- Icon -->
        <div style="color: orangered;" class="d-flex w-100 justify-content-center">
          <i class="bi bi-person-circle" style="font-size: 6rem;"></i>
        </div>

        <!-- Info -->
        <div class="ps-md-4 border-md-start border-3 border-dark w-100">
          <div class="border-bottom border-4 w-full border-black">
            <template v-if="isAdmin">
              <h4 class="fw-bold">{{ userStore?.singuser.name }}</h4>
              <p class="mb-1 text-muted"><i class="bi bi-envelope-at me-2"></i>{{ userStore.singuser?.email }}</p>
            </template>
            <template v-else-if="isDoc">
              <h4 class="fw-bold">{{ docStore?.singdoc?.details?.name }}</h4>
              <p class="mb-1 text-muted"><i class="bi bi-envelope-at me-2"></i>{{ docStore?.singdoc?.details?.email }}
              </p>
            </template>
            <template v-else>
              <template v-if="$route.query.did">
                <h4 class="fw-bold">{{ docStore?.singdoc?.details?.name }}</h4>
                <p class="mb-1 text-muted"><i class="bi bi-envelope-at me-2"></i>{{ docStore?.singdoc?.details?.email }}
                </p>
              </template>
              <template v-else>
                <h4 class="fw-bold">{{ patStore?.singpat?.details?.name }}</h4>
                <p class="mb-1 text-muted"><i class="bi bi-envelope-at me-2"></i>{{ patStore?.singpat?.details?.email }}
                </p>
              </template>
            </template>
          </div>

          <!-- Doctor -->
          <div v-if="isDoc" class="mt-3">
            <h6 class="fw-semibold text-decoration-underline mb-2">Doctor Info:</h6>
            <p class="mb-1"><b>Specialization:</b> MBBS in {{ docStore?.singdoc?.specializations.name }}</p>

            <p class="mb-1"><b>Contact:</b> {{ docStore?.singdoc?.contact_number }}</p>
            <p class="mb-1"><b>More Info:</b>
              {{ getName(docStore?.singdoc?.details?.name) }} is an experienced medical practitioner and holds a degree
              of MBBS in
              {{ docStore?.singdoc?.specializations?.name }}
            </p>

          </div>

          <!-- Patient -->
          <div v-if="isPat" class="mt-3">
            <div v-if="$route.query.did" class="mt-3">
              <h6 class="fw-semibold text-decoration-underline mb-2">Doctor Info:</h6>
              <p class="mb-1"><b>Specialization:</b> MBBS in {{ docStore?.singdoc?.specializations.name }}</p>

              <p class="mb-1"><b>Contact:</b> {{ docStore?.singdoc?.contact_number }}</p>
              <p class="mb-1"><b>More Info:</b>
                {{ getName(docStore?.singdoc?.details?.name) }} is an experienced medical practitioner and holds a
                degree of MBBS
                in {{ docStore?.singdoc?.specializations?.name }}
              </p>
            </div>

            <div v-else class="mt-3">
              <h6 class="fw-semibold text-decoration-underline mb-2">Patient Info:</h6>

              <p class="mb-1"><b>Age:</b> {{ this.patStore.singpat.age }}</p>
              <p class="mb-1"><b>Gender:</b> {{ this.patStore.singpat.gender }}</p>
              <p class="mb-1"><b>Contact:</b> {{ this.patStore.singpat.contact_number }}</p>
              <p class="mb-1"><b>Address:</b> {{ this.patStore.singpat.address }}</p>
              <p class="mb-1"><b>Emergency:</b> {{ this.patStore.singpat.emergency_contact }}</p>
              <router-link :to="`/pdash/patient/${patStore.singpat.id}/edit`" class="btn mt-4 btn-primary"><i class="bi bi-pencil me-2">Edit Profile</i></router-link>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>

  <div v-if="loading" class="loader-overlay d-flex flex-column">
        <div class="text-danger pulse fs-1" role="status"><i class="bi bi-heart-pulse-fill"></i></div>
        Loading.....
    </div>
</template>

<script>
import useDocStore from "@/stores/doctors";
import usePatientStore from "@/stores/patients";
import useUserStore from "@/stores/user";

export default {
  name: "Profile",

  data() {
    return {
      userStore: null,
      docStore: null,
      patStore: null,
      loading: false,
    };
  },

  async created() {
    this.userStore = useUserStore();
    this.patStore = usePatientStore();
    this.docStore = useDocStore();
    this.loading=true;
    if (this.userStore.role === 'patient') {
      if (this.$route.query.did)
        await this.docStore.getbyId({ id: this.$route.query.did });
      else
        await this.patStore.getbyId({ uid: this.$route.params.id });
    }
    else if (this.userStore.isAdmin)
      await this.userStore.getbyId(this.$route.params.id);
    else
      await this.docStore.getbyId({ uid: this.$route.params.id });
    this.loading=false
  },

  methods: {
    getName(nm) {
      if (nm?.includes("Dr"))
        return nm
      else
        return `Dr. ${nm}`
    },
  },

  computed: {
    isPat() {
      return this.userStore.role === 'patient'
    },
    isAdmin() {
      return this.userStore.isAdmin
    },
    isDoc() {
      return this.userStore.role === 'doctor'
    },
  },
}
</script>

<style>
.prof_card {
  background: #f4f0f0;
  width: fit-content;
  padding: 40px;
}

.pulse {
    animation: pulseanim 0.5s ease-out infinite;
}

@keyframes pulseanim {
    0% { transform: scale(1); }
    50% { transform: scale(1.5); }
    100% { transform: scale(1); }
}

.loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(255, 255, 255, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
    backdrop-filter: blur(1px);
}

@media (max-width:500px) {
  .head {
    min-width: 95vw !important;
  }
}

@media (min-width:501px) {
  .head {
    min-width: 70vw !important;
  }
}
</style>
