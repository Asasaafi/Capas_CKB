import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'
import Dashboard from '../pages/Dashboard.vue'
import StorageCalculation from '../pages/StorageCalculation.vue'
import BulkingInput from '../pages/storage/BulkingInput.vue'
import FileUpload from '../pages/storage/FileUpload.vue'
import MHECalculation from '../pages/MHECalculation.vue'
import ManpowerCalculation from '../pages/ManpowerCalculation.vue'
import LIBased from '../pages/manpower/LIBased.vue'
import ActivityBased from '../pages/manpower/ActivityBased.vue'
import History from '../pages/History.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
      },

      {
        path: 'storage',
        name: 'Storage',
        component: StorageCalculation,
        children: [
          {
            path: 'bulking',
            component: BulkingInput,
          },
          {
            path: 'upload',
            component: FileUpload,
          },
        ],
      },

      {
        path: 'mhe',
        name: 'MHE',
        component: MHECalculation,
      },

      {
        path: 'manpower',
        name: 'Manpower',
        component: ManpowerCalculation,
        children: [
          {
            path: 'li',
            component: LIBased,
          },
          {
            path: 'activity',
            component: ActivityBased,
          },
        ],
      },

      {
        path: 'history',
        name: 'History',
        component: History,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router