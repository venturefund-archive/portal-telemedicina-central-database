import { useLoggedUserStore } from '@/stores/loggedUser'
import { useStorage } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { errorToast, successToast } from '@/toast'
const router = useRouter()

export default [
  {
    path: '/patients',
    component: () => import('@/layouts/DashboardLayout.vue'),
    children: [
      {
        path: '/patients',
        name: 'Patients',
        component: () => import('@/views/Patients.vue'),
      },
      {
        path: '/patients/:id',
        name: 'PatientDetails',
        component: () => import('@/views/pages/PatientDetails.vue'),
        props: true,
      },
      // {
      //   path: '/patients',
      //   name: 'PatientDetailsNobody',
      //   component: () => import('@/views/pages/PatientDetailsNobody.vue'),
      // },
      {
        path: '/map',
        name: 'Map',
        component: () => import('@/views/pages/Map.vue'),
        props: true,
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('@/views/pages/Settings.vue'),
      },
      {
        path: '/map/patient/:id',
        name: 'MapPatient',
        component: () => import('@/views/pages/Map.vue'),
        props: true,
      },
      {
        path: '/map/area/:id',
        name: 'MapArea',
        component: () => import('@/views/pages/Map.vue'),
        props: true,
      }
    ],
    beforeEnter: async (to, from, next) => {
      const state = useStorage('app-store', { token: '' })
      state.value.intendedRoute = to.fullPath

      if (Boolean(state.value.token)) {
        const loggedUserStore = useLoggedUserStore()
        try {
          const response = await loggedUserStore.fetchMe()
          next(true)
        } catch (err) {
          errorToast({ text: 'Área autenticada, faça o login primeiro.' })
          next({ name: 'Login' })
        }
      } else {
        errorToast({ text: 'Área autenticada, faça o login primeiro.' })
        next({ name: 'Login' })
      }
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
    beforeEnter: async (to, from, next) => {
      const state = useStorage('app-store', { token: '' })

      if (to.params.token) {
        state.value.token = to.params.token
        return true
      }

      if (Boolean(state.value.token)) {
        const loggedUserStore = useLoggedUserStore()
        try {
          const response = await loggedUserStore.fetchMe()
          next({ name: 'Patients' })
        } catch (err) {
          state.value = null
          console.log(err)
          if (state.value.intendedRoute) {
            router.replace(state.value.intendedRoute)
          } else {
            next({ name: 'Login' })
          }
        }
      }
      next(true)
    },
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/components/pages/NotFound.vue') },
]
