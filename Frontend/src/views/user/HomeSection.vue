<script setup>
import Card_ from "@/components/atomic/Card_.vue"

import { ref } from 'vue';

const popular = ref([])
const latest = ref([])
const latestAlbums = ref([])
const popularArtists = ref([])

console.log(import.meta.env.VITE_BACKEND_URL)

fetch(import.meta.env.VITE_BACKEND_URL +  "popularSongs?n=5", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
}).then(response => response.json())
    .then(data => {
        if(data['success'])
            popular.value = data['data']
    })
    .catch(error => {
        console.log(error)
    })

fetch(import.meta.env.VITE_BACKEND_URL +  "latestSongs?n=10", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
}).then(response => response.json())
    .then(data => {
        if(data['success'])
            latest.value = data['data']
    })
    .catch(error => {
        console.log(error)
    })

fetch(import.meta.env.VITE_BACKEND_URL +  "latestAlbums?n=10", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
}).then(response => response.json())
    .then(data => {
        if(data['success'])
            latestAlbums.value = data['albums']['data']
        for (let i = 0; i < latestAlbums.value.length; i++) {
            latestAlbums.value[i].album_songsId = []
            for (let j = 0; j < latestAlbums.value[i]['songs'].length; j++) {
                latestAlbums.value[i].album_songsId.push(latestAlbums.value[i]['songs'][j]['id'])
            }
        }
    })
    .catch(error => {
        console.log(error)
    })

fetch(import.meta.env.VITE_BACKEND_URL +  "popularArtists?n=5", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
}).then(response => response.json())
    .then(data => {
        if(data['success'])
            popularArtists.value = data['artists']
    })
    .catch(error => {
        console.log(error)
    })

</script>

<template>
    <div class="section">
        <h3>Popular </h3>
        <div class="horizontalList">
            <Card_ v-for="song in popular" :label="song.name" 
            :artist="song.creators" :image="song.image"
            :songId="song.id.toString()" />
        </div>
    </div>

    <div class="section">
        <h3>Latest </h3>
        <div class="horizontalList">
            <Card_ v-for="song in latest" :label="song.name" 
            :artist="song.creators" :image="song.image"
            :songId="song.id.toString()" />
        </div>
    </div>

    <div class="section">
        <h3>Latest Album</h3>
        <div class="horizontalList">
            <Card_ v-for="album in latestAlbums" :label="album.name" 
            :artist="album.creator" :image="album.image"
            :albumId="album.id.toString()" :album_songsId="album.album_songsId"/>
        </div>
    </div>

    <div class="section">
        <h3>PopularArtists</h3>
        <div class="horizontalList">
            <RouterLink v-for="artist in popularArtists" class="circular_card" 
              :to="'/app/artist/'+artist.id">
                <img :src="artist.image" />
                <span>{{ artist.name }}</span>
            </RouterLink>
        </div>

    </div>


</template>

<style scoped>
.section {
    margin: 4px 0px;
}

.section h3 {
    font-weight: normal;
    margin-left: 10px;
    margin-bottom: 10px;
}

.horizontalList {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    column-gap: 2px;
}
.horizontalList::-webkit-scrollbar {
    display: none;
}

.circular_card{
    display: flex;
    flex-direction: column;
    padding: 1rem;
    border-radius: 8px;
}
.circular_card:hover{
    cursor: pointer;
}
.circular_card > span{
    margin-top: 1rem;
    max-width: 120px;
    font-size: small;
    text-wrap: nowrap;
    overflow-x: hidden;
    text-overflow: ellipsis;
    text-align: center;
    color: var(--fore-2);
}

.circular_card img{
    width: 120px;
    height: 120px;
    overflow: hidden;
    border-radius: 50%;
}
</style>