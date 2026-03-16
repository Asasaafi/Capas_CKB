<script setup>
const logoUrl = new URL('../assets/LOGO.png', import.meta.url).href
</script>

<template>
    <div class="sidebar">
        <div class="logo-container">
            <img :src="logoUrl" alt="CAPAS Logo" class="logo" />
        </div>

        <ul>
            <li>
                <router-link 
                    to="/" 
                    class="menu-item"
                    exact-active-class="router-link-active"
                >
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="7" height="7"/>
                        <rect x="14" y="3" width="7" height="7"/>
                        <rect x="14" y="14" width="7" height="7"/>
                        <rect x="3" y="14" width="7" height="7"/>
                    </svg>
                    Dashboard
                </router-link>
            </li>

            <li>
                <router-link 
                    to="/storage" 
                    class="menu-item"
                >
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <ellipse cx="12" cy="5" rx="9" ry="3"/>
                        <path d="M3 5v4c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/>
                        <path d="M3 9v4c0 1.66 4.03 3 9 3s9-1.34 9-3V9"/>
                        <path d="M3 13v4c0 1.66 4.03 3 9 3s9-1.34 9-3v-4"/>
                    </svg>
                    Storage Calculation
                </router-link>

                <ul class="submenu">
                    <li>
                        <router-link 
                            to="/storage/bulking" 
                            class="menu-item"
                        >
                            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                                <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                                <line x1="12" y1="22.08" x2="12" y2="12"/>
                            </svg>
                            Bulking Input
                        </router-link>
                    </li>
                    <li>
                        <router-link 
                            to="/storage/upload" 
                            class="menu-item"
                        >
                            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                                <polyline points="17 8 12 3 7 8"/>
                                <line x1="12" y1="3" x2="12" y2="15"/>
                            </svg>
                            File Upload
                        </router-link>
                    </li>
                </ul>
            </li>

            <li>
                <router-link to="/mhe" class="menu-item">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="1" y="3" width="15" height="13"/>
                        <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
                        <circle cx="5.5" cy="18.5" r="2.5"/>
                        <circle cx="18.5" cy="18.5" r="2.5"/>
                    </svg>
                    MHE Calculation
                </router-link>
            </li>

            <li>
                <router-link 
                    to="/manpower" 
                    class="menu-item"
                >
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    Manpower Calculation
                </router-link>

                <ul class="submenu">
                    <li>
                        <router-link 
                            to="/manpower/li" 
                            class="menu-item"
                        >
                            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="18" y1="20" x2="18" y2="10"/>
                                <line x1="12" y1="20" x2="12" y2="4"/>
                                <line x1="6" y1="20" x2="6" y2="14"/>
                            </svg>
                            LI-Based
                        </router-link>
                    </li>
                    <li>
                        <router-link 
                            to="/manpower/activity" 
                            class="menu-item"
                        >
                            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="18" y1="20" x2="18" y2="10"/>
                                <line x1="12" y1="20" x2="12" y2="4"/>
                                <line x1="6" y1="20" x2="6" y2="14"/>
                            </svg>
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

.icon {
    width: 18px;
    height: 18px;
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