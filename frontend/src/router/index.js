import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import AdminDash from '@/components/AdminDash.vue'
import PatientDash from '@/components/PatientDash.vue'
import DoctorDash from '@/components/DoctorDash.vue'
import DocAdd from '@/components/DocAdd.vue'
import PatEdit from '@/components/PatEdit.vue'
import DocEdit from '@/components/DocEdit.vue'
import ApptHist from '@/components/ApptHist.vue'
import Profile from '@/components/Profile.vue'
import UpdateHistory from '@/components/UpdHist.vue' 
import DocAvail from '@/components/DocAvail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    {path: '/adash', component: AdminDash},
    {path: '/adash/doctor/create', component: DocAdd},
    {path: '/adash/doctor/:id/edit', component: DocEdit},
    {path: '/adash/patient/:id/edit', component: PatEdit},
    {path: '/user/:id/profile', component: Profile},
    {path: '/:name/appts', component: ApptHist},
    {path: '/ddash/:id/avail', component: DocAvail},
    {path: '/:name/appts/update', component: UpdateHistory},
    {path: '/pdash', component: PatientDash},
    {path: '/ddash/:id', component: DoctorDash},

  ],
})

export default router
