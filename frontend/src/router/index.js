import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import AdminDash from '@/components/AdminDash.vue'
import PatientDash from '@/components/PatientDash.vue'
import DoctorDash from '@/components/DoctorDash.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    {path: '/adash', component: AdminDash},
    {path: '/pdash', component: PatientDash},
    {path: '/ddash', component: DoctorDash},

  ],
})

export default router
