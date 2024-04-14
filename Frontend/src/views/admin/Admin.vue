<script setup>
import logoIcon from '@/assets/logo.svg'
import dashboardIcon from "@/assets/AdminNavIcon/dashboard.svg"
import dashboard_sIcon from "@/assets/AdminNavIcon/dashboard_s.svg"
import musicIcon from "@/assets/AdminNavIcon/music.svg"
import music_sIcon from "@/assets/AdminNavIcon/music_s.svg"
import usersIcon from "@/assets/AdminNavIcon/users.svg"
import users_sIcon from "@/assets/AdminNavIcon/users_s.svg"
import categoriesIcon from "@/assets/AdminNavIcon/categories.svg"
import categories_sIcon from "@/assets/AdminNavIcon/categories_s.svg"
import flagIcon from "@/assets/AdminNavIcon/flag.svg"
import flag_sIcon from "@/assets/AdminNavIcon/flag_s.svg"
import settingsIcon from "@/assets/AdminNavIcon/settings.svg"
import settings_sIcon from "@/assets/AdminNavIcon/settings_s.svg"

import Navigation from '@/components/molecular/Navigation.vue'
import CircularEffect from '@/components/atomic/CircularEffect.vue'

const navigations = [
    {
        "name": "Dashboard",
        "Icon": dashboardIcon,
        "Icon_selected": dashboard_sIcon,
        "route": "admin"
    },
    {
        "name": "Songs",
        "Icon": musicIcon,
        "Icon_selected": music_sIcon,
        "route": "admin_songs"
    }, 
    {
        "name": "Users",
        "Icon": usersIcon,
        "Icon_selected": users_sIcon,
        "route": "admin_users"
     },
     {
        "name": "Categories",
        "Icon": categoriesIcon,
        "Icon_selected": categories_sIcon,
        "route": "admin_categories"
     },
     {
        "name": "Flagged Items",
        "Icon": flagIcon,
        "Icon_selected": flag_sIcon,
        "route": "admin_flagged"
     }
]

function checkIfAdmin(){
    if(localStorage.getItem("token") == null){
        window.location.href = "/login"
    }
    fetch(`${import.meta.env.VITE_BACKEND_URL}verify`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data['valid'] == false){
            localStorage.removeItem("token")
            window.location.href = "/login"
        }
        else if(data['admin'] == false){
            window.location.href = "/app"
        }
    })
}
checkIfAdmin()

</script>

<template>
    <div id="main">
        <CircularEffect />
        <div id="left">
            <img :src="logoIcon" />
            <Navigation :navigations="navigations"/>
        </div>

        <div class="view">
                <router-view />
        </div>

    </div>
</template>
<style scoped>
#main {
    display: flex;
    flex-direction: row;
    height: calc(100% - 6rem);
    padding: 1px;
}

#left {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    width: 350px;
    margin: 2px;
    background-color: var(--back-1);
    height: 99vh;
}

#left>div {
    width: 100%;
    margin-top: 2px;
}

#left>img{
    margin-top: 2rem;
    margin-left: 2.5rem;
}
.view{
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
    width: 100%;
}

.view::-webkit-scrollbar {
  width: 5px;
}

/* Track */
.view::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--fore-2);
  border-radius: 5px;
}

/* Handle */
.view::-webkit-scrollbar-thumb {
  background: var(--gradient);
  border-radius: 5px;
}
</style>