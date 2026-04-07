import { createRouter, createWebHistory } from "vue-router"
import MainLayout from "../layouts/MainLayout.vue"
import Dashboard from "../pages/Dashboard.vue"
import StorageCalculation from "../pages/StorageCalculation.vue"
import BulkingInput from "../pages/storage/BulkingInput.vue"
import FileUpload from "../pages/storage/FileUpload.vue"
import MHECalculation from "../pages/MHECalculation.vue"
import ManpowerCalculation from "../pages/ManpowerCalculation.vue"
import LIBased from "../pages/manpower/LIBased.vue"
import ActivityBased from "../pages/manpower/ActivityBased.vue"
import LiterBased from "../pages/manpower/LiterBased.vue"
import CbmBased from "../pages/manpower/CbmBased.vue"
// import History from "../pages/History.vue"

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [

      {
        path: "",
        name: "Dashboard",
        component: Dashboard
      },

      {
        path: "storage",
        name: "Storage",
        component: StorageCalculation
      },

      {
        path: "storage/bulking",
        name: "BulkingInput",
        component: BulkingInput
      },

      {
        path: "storage/upload",
        name: "FileUpload",
        component: FileUpload
      },

      {
        path: "mhe",
        name: "MHE",
        component: MHECalculation
      },

      {
        path: "manpower",
        name: "Manpower",
        component: ManpowerCalculation
      },

      {
        path: "manpower/li",
        name: "LIBased",
        component: LIBased
      },

      {
        path: "manpower/activity",
        name: "ActivityBased",
        component: ActivityBased
      },

      {
        path: "manpower/liter",
        name: "LiterBased",
        component: LiterBased
      },

      {
        path: "manpower/cbm",
        name: "CbmBased",
        component: CbmBased
      }

      // {
      //   path: "history",
      //   name: "History",
      //   component: History
      // }

    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router