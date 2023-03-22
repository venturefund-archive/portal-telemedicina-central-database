import { useStorage } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { errorToast, successToast } from '@/toast'
const router = useRouter()

export default [
  {
    path: '/dashboard',
    component: () => import('@/layouts/DashboardLayout.vue'),
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
      },
      {
        path: '/patients/:id',
        name: 'PatientDetails',
        component: () => import('@/views/pages/PatientDetails.vue'),
        props: true,
      },
      {
        path: '/patients',
        name: 'PatientDetailsNobody',
        component: () => import('@/views/pages/PatientDetailsNobody.vue'),
      },
      {
        path: '/map',
        name: 'Map',
        component: () => import('@/views/pages/Map.vue'),
        props: true,
      },
    ],
    beforeEnter: (to, from) => {
      const state = useStorage('app-store', { token: '' })
      if (Boolean(state.value.token)) {
        return true
      }
      errorToast({ text: 'Área autenticada, faça o login primeiro.' })
      return { name: 'Login' }
    },
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/layouts/AuthenticationLayout.vue'),
    children: [
      {
        path: '/',
        name: 'Login',
        component: () => import('@/views/auth/Login.vue'),
      },
      {
        path: '/auth/register',
        name: 'Register',
        component: () => import('@/views/auth/Register.vue'),
      },
      {
        path: '/auth/verify-email',
        name: 'VerifyEmail',
        component: () => import('@/views/auth/VerifyEmail.vue'),
      },
      {
        path: '/auth/forgot-password',
        name: 'ForgotPassword',
        component: () => import('@/views/auth/ForgotPassword.vue'),
      },
      {
        name: 'ResetPassword',
        path: '/auth/reset-password/:uid/:token',
        alias: '/auth/rest-auth/password/reset/confirm/:uid/:token',
        component: () => import('@/views/auth/ResetPassword.vue'),
        props: true,
      },
      // {
      //   path: '/auth/confirm-password',
      //   name: 'ConfirmPassword',
      //   component: () => import('@/views/auth/ConfirmPassword.vue'),
      // },
    ],
    beforeEnter: (to, from) => {
      const state = useStorage('app-store', { token: '' })

      if (!Boolean(state.value.token)) {
        return true
      }

      if (to.params.token) {
        state.value.token = to.params.token
        return true
      }

      // @TODO: Check if the token is valid
      // successToast({ text: 'Você já está autenticado.' })
      return { name: 'Dashboard' }
    },
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/components/pages/NotFound.vue') },
]
