<script setup>
import Floating from "@/components/atomic/Floating.vue"
import { ref, watch } from 'vue';
import { appStore } from '@/utility/store.js';

import { useRouter } from 'vue-router';
const router = useRouter()
const emits = defineEmits(['close'])
defineProps({
    id : Array    
})

const playlists = ref([])

fetch(import.meta.env.VITE_BACKEND_URL + "playlist_all",{
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        if(data["success"])
            playlists.value = data["playlists"]
    })
    .catch(error => {
        console.log(error)
})

const addToPlaylist = (song_id , playListId)=>{
    console.log(song_id , playListId)
    fetch(import.meta.env.VITE_BACKEND_URL + "playlist", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body : JSON.stringify({
            "id": playListId,
            "song_id_to_add" : song_id
        })
    }).then(response => response.json())
        .then(data => {
            if (data['success']) {
                appStore.refreshPlaylist = true
                emits('close')
            }
        })
}

</script>

<template>
    <Floating @clickedOut="() => $emit('close')">
        <div class="playlists">
            <h4>Select Playlist</h4>
            <span v-for="playlist in playlists" @click="() => addToPlaylist(id , playlist.id)">{{ playlist.name }}</span>
        </div>
    </Floating>
</template>

<style scoped>
.playlists{
    display: flex;
    flex-direction: column;
    background-color: var(--back-2);
    color: var(--fore-2);
}
.playlists > h4{
    margin: 0px;
    padding: 1rem 2rem 1rem 1rem;
}
.playlists > *{
    padding: 0.5rem 2rem 0.5rem 1rem;
}

.playlists > span:hover{
    background-color: var(--shade);
}
</style>