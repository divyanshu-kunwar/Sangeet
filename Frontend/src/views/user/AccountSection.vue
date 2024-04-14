<script setup>
import { ref } from 'vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import studioIcon from '@/assets/artist_studio.svg'
import editIcon from '@/assets/edit.svg'
import adminIcon from '@/assets/admin.svg'
import keyIcon from '@/assets/key.svg'
import supportIcon from '@/assets/support.svg'
import CircularEffect from '@/components/atomic/CircularEffect.vue'
import sampleImage from '@/assets/sampleImage.png';

// TODO : Fetch Profile & Set menu according to user_type
const user_name = ref("Loading...")
const user_email = ref("Loading...")
const user_image = ref(sampleImage)
const user_type = ref("Loading...")


let headers = {
    "Content-Type": "application/json",
}
if (localStorage.getItem("token")) {
    headers["Authorization"] = localStorage.getItem("token")
}

fetch(import.meta.env.VITE_BACKEND_URL +  "user", {
    method: "GET",
    headers: headers
})
    .then(response => response.json())
    .then(data => {
        user_name.value = data["name"]
        user_email.value = data["email"]
        user_type.value = data["role"]
        user_image.value = data["image"]
        if(!data["image"]){
            user_image.value="https://picsum.photos/200?random=1"
        }
    })
    .catch(error => {
        console.log(error)
    })

const menus = [
    {
        name: "Edit Profile",
        icon: editIcon,
        href: "/app/profile",
    },
    {
        name: "Artist's Studio",
        icon: studioIcon,
        href: "/studio",
        target: "_blank",
        condition: () => {
            return user_type.value == "Creator" || user_type.value == "Admin"
        }
    },
    {
        name: "Admin Panel",
        icon: adminIcon,
        href: "/admin",
        target: "_blank",
        condition: () => user_type.value == "Admin"
    },
    {
        name: "Logout",
        icon: keyIcon,
        click: () => {
            localStorage.removeItem("token")
            router.push("/")
        }
    },
    {
        name: "Support",
        icon: supportIcon,
        href: "/app/support"
    }
]
</script>

<template>
    <CircularEffect />
    <div id="Account">
        <div class="profile">
            <img :src="user_image" />
            <div class="description">
                <span class="name">{{ user_name }}</span>
                <span class="email">{{ user_email }}</span>
                <span class="artist">{{ user_type }}</span>
            </div>
        </div>

        <div id="menu">
            <div v-for="menu in menus">
                <div v-if="menu.condition ? menu.condition() : true">
                    <RouterLink class="listItem" v-if="menu.href" :to="menu.href" :target="menu.target">
                        <img :src="menu.icon" />
                        <span>{{ menu.name }}</span>
                    </RouterLink>
                    <div class="listItem" v-else @click="menu.click">
                        <img :src="menu.icon" />
                        <span>{{ menu.name }}</span>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>

<style scoped>
#Account {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    width: clamp(30rem, 35rem, 100%);
    background-color: var(--back-1);
    align-self: center;
    justify-self: center;
    border-radius: 1rem;
    justify-content: center;
    margin: auto;
    border: 1px dashed var(--back-2);
}

.listItem {
    display: flex;
    width: 100%;
    height: fit-content;
    align-items: center;
    justify-content: start;
    margin: 1px 0rem;
    padding: 0.7rem;
    cursor: pointer;
    color: var(--fore-2);
    opacity: 0.5;
    transition: opacity 0.2s linear;
    padding-left: 1rem;
}

.listItem:hover {
    opacity: 1;
}

.listItem img {
    margin: 0rem 1rem;
    background-color: var(--back-2);
    padding: 0.7rem;
    border-radius: 4px;
}

#menu {
    display: flex;
    flex-direction: column;
    margin-top: 2rem;
}

.description {
    display: flex;
    flex-direction: column;
    margin-left: 1rem;
}

.description .name {
    font-size: xx-large;
    color: var(--shade);
}

.description .email {
    font-size: small;
    margin-bottom: 4px;
}

.description .artist {
    font-size: large;
}

.profile {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding: 0.7;
    padding-left: 1rem;
}

.profile img {
    width: 120px;
    height: 120px;
    margin: 0rem 1rem;
    padding: 0.7rem;
    border-radius: 50%;
    object-fit: cover;
}
</style>
