<script setup>
import sampleImage from '@/assets/sampleImage.png'
import CardH_ from "@/components/atomic/CardH_.vue"
import playlistIcon from '@/assets/playlistIcon.svg'
import playIcon from '@/assets/play.svg'
import addIcon from '@/assets/add.svg'
import Button_ from '../atomic/Button_.vue'

import { useRouter } from 'vue-router';
const router = useRouter()

import { ref, watch } from 'vue'
import { store } from '@/utility/store.js'
import { appStore } from '@/utility/store.js'

const playlists = ref([])


function loadInitial(){
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
}

const play = (songs) =>{
    for(let i = 0 ; i < songs.length ; i++){
            store.addToQueueFront(songs[i])
    }
}

const addPlaylist = () =>{
    let name_ = prompt("Enter Name Of The Playlist :" , "My Playlist")

    fetch(import.meta.env.VITE_BACKEND_URL + "playlist", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body : JSON.stringify({
            "name": name_
        })
    }).then(response => response.json())
    .then(data => {
        if (data['success']){
            appStore.refreshPlaylist = true
            router.push({ name: 'playlistDetail' , params: { id : data["id"] } })
        }

    })
    .catch(error => {
        console.log(error)
    })
}

loadInitial()

watch(appStore , () => {
    if(appStore.refreshPlaylist!=false){
        loadInitial()
        appStore.refreshPlaylist = false
    }
})

</script>

<template>
    <div class="Playlists">
        <div class="Header">
            <img :src="playlistIcon" />
            <span>Your Playlists</span>
            <Button_ class="add" shape="circle" :icon="addIcon" type="none" size="small" 
            @click="addPlaylist()" />
        </div>

        <div class="playlistItem" v-for="playlist in playlists" :key="playlist.id">
            <CardH_ :label="playlist.name" :artist="playlist.no_of_songs+' song(s)'" 
            :image="playlist.image ? playlist.image : sampleImage" 
            :href="'/app/playlist/'+playlist.id"/>
            <img class="option cursor" :src="playIcon" @click="play(playlist.songs)" />
        </div>

    </div>
</template>

<style scoped>

.Header {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0.5rem 8%;
    color: var(--fore-0);
    transition: all 0.2s linear;
    margin: 8px 0px;
}

.Header img {
    height: 26px;
    margin-right: 8%;
}

.Header {
    display: flex;
    justify-content: space-between;
    font-size: large;
    font-weight: bold;
}


.Playlists {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: flex-start;
    padding: 1rem;
    height: 100%;
}

.playlistItem {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 0.5rem 7%;
    color: var(--fore-0);
    margin: 2px 0px;
    border-radius: 4px;
}

.playlistItem:hover {
    background-color: var(--back-2);
}

.option {
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.playlistItem:hover .option {
    opacity: 0.8;
}
.add:hover{
    background-color: var(--back-1);
}
</style>