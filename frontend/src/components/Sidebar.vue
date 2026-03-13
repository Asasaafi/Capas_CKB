<script setup>
import logo from '../assets/LOGO.png'

import {
  LayoutDashboard,
  Database,
  Box,
  Upload,
  Truck,
  Users,
  BarChart3
} from 'lucide-vue-next'
</script>

<template>
    <div class="sidebar">
        <div class="logo-container">
            <img :src="logo" alt="CAPAS Logo" class="logo" />
        </div>

        <ul>
            <li>
                <router-link 
                    to="/" 
                    class="menu-item"
                    exact-active-class="router-link-active"
                >
                    <LayoutDashboard class="icon"/>
                    Dashboard
                </router-link>
            </li>

            <li>
                <router-link 
                    to="/storage" 
                    class="menu-item"
                >
                    <Database class="icon"/>
                    Storage Calculation
                </router-link>

                <ul class="submenu">
                    <li>
                        <router-link 
                            to="/storage/bulking" 
                            class="menu-item"
                        >
                            <Box class="icon"/>
                            Bulking Input
                        </router-link>
                    </li>
                    <li>
                        <router-link 
                            to="/storage/upload" 
                            class="menu-item"
                        >
                            <Upload class="icon"/>
                            File Upload
                        </router-link>
                    </li>
                </ul>
            </li>

            <li>
                <router-link to="/mhe" class="menu-item">
                    <Truck class="icon"/>
                    MHE Calculation
                </router-link>
            </li>

            <li>
                <router-link 
                    to="/manpower" 
                    class="menu-item"
                >
                    <Users class="icon"/>
                    Manpower Calculation
                </router-link>

                <ul class="submenu">
                    <li>
                        <router-link 
                            to="/manpower/li" 
                            class="menu-item"
                        >
                            <BarChart3 class="icon"/>
                            LI-Based
                        </router-link>
                    </li>
                    <li>
                        <router-link 
                            to="/manpower/activity" 
                            class="menu-item"
                        >
                            <BarChart3 class="icon"/>
                            Activity-Based
                        </router-link>
                    </li>
                </ul>
            </li>

        </ul>
    </div>
</template>

<style scoped>
.sidebar {
    width: 200px;
    background-color: #F4F2F2;
    color: #000;
    padding: 15px 15px 10px 15px;
}

.logo-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.logo {
    width: 240px;
    height: auto;
    object-fit: contain;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
   
li {
    margin: 6px 0;
}

.menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 8px;
    text-decoration: none;
    color: #000;
    transition: all 0.2s ease;
}

.icon{
    width:18px;
    height:18px;
}

.menu-item:hover {
    background-color: #e0e0e0;
    color: #026766;
}

.router-link-active {
    background-color: #026766;
    color: #fff !important;
    pointer-events: none;
}

.submenu {
    padding-left: 16px;
    margin-top: 5px;
}
</style>