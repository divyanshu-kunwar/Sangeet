<script setup>
import { ref, watch, watchEffect } from 'vue';
import CardH_ from '@/components/atomic/CardH_.vue';
import Button_ from '@/components/atomic/Button_.vue';
import PlayIcon from '@/assets/play.svg'

import editIcon from '@/assets/edit.svg'
import deleteIcon from '@/assets/delete.svg'
import sampleImage from '@/assets/sampleImage.png'

import { store , appStore } from '@/utility/store.js'

import { useRouter } from 'vue-router';
const router = useRouter()
const id = ref(router.currentRoute.value.params.id)

const playlistDetail = ref({})

const loadInitial = () => {
    fetch(import.meta.env.VITE_BACKEND_URL +  "playlist?id=" + id.value, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data['success'])
                playlistDetail.value = data["playlist"]
        })
        .catch(error => {
            console.log(error)
        })
}

const rename = (originalName) => {
    let new_name = prompt("Enter New Name Of The Playlist :", originalName)

    fetch(import.meta.env.VITE_BACKEND_URL +  "playlist", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body: JSON.stringify({
            "id": id.value,
            "name": new_name
        })
    }).then(response => response.json())
        .then(data => {
            if (data['success']) {
                appStore.refreshPlaylist = true
                loadInitial()
            }

        })
        .catch(error => {
            console.log(error)
        })
}

const deletePlayList = () => {
    fetch(import.meta.env.VITE_BACKEND_URL +  "playlist?id=" + id.value, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    }).then(response => response.json())
        .then(data => {
            if (data['success']) {
                appStore.refreshPlaylist = true
                router.push({ name: 'app' })
            }

        })
        .catch(error => {
            console.log(error)
        })
}

const deleteSong = (song_id, playlist_id) => {

    fetch(import.meta.env.VITE_BACKEND_URL +  "playlist", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body: JSON.stringify({
            "id": playlist_id,
            "song_id_to_remove": [song_id]
        })
    }).then(response => response.json())
        .then(data => {
            if (data['success']) {
                appStore.refreshPlaylist = true
                loadInitial()
            }
        })

}
const play = (songs) =>{
    for(let i = 0 ; i < songs.length ; i++){
            store.addToQueueFront(songs[i]['id'])
    }
}

loadInitial()

</script>

<template>
    <div class="main" >
        <div class="form">
            <div class="row">
                <img id="category_img" :src="playlistDetail.image ? playlistDetail.image : sampleImage" />
                <div class="metadata">
                    <div class="title" @click="play(playlistDetail.songs)">
                        <Button_ :icon="PlayIcon" type="gradient" size="small" shape="circle" />
                        {{ playlistDetail.name }}
                    </div>
                    <div class="playSongs" v-if="playlistDetail.no_of_songs < 1">
                        No song added to playlist.
                        Add Song To Playlist by Visiting Song Or Album Page
                    </div>
                    <div class="playSongs" v-else-if="playlistDetail.no_of_songs < 2">
                        Play {{ playlistDetail.no_of_songs }} song in playlist
                    </div>
                    <div class="playSongs" v-else="playlistDetail.no_of_songs < 2">
                        Play {{ playlistDetail.no_of_songs }} songs in playlist
                    </div>
                    <div class="actions">
                        <Button_ label="Rename" :icon="editIcon" type="grayscale" size="small" shape="rect"
                            @click="rename(playlistDetail.name)" />
                        <Button_ label="Delete" :icon="deleteIcon" type="grayscale" size="small" shape="rect"
                            @click="deletePlayList()" />
                    </div>
                </div>
            </div>
        </div>
        <div class="songs column">
            <h1>Songs</h1>
            <div class="song_grid">
                <div class="song_items" v-for="song in playlistDetail.songs">
                    <CardH_ :label="song.name" :artist="song.creators" :image="song.image"
                        :href="'/app/song/' + song.id" />
                    <img class="option cursor" :src="deleteIcon" @click="deleteSong(song.id, playlistDetail.id)" />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: fit-content;
    width: 100%;
    height: fit-content;
    padding: 4rem 0rem;
}

.form {
    display: flex;
    flex-direction: row;
    padding: 2rem;
    width: 100%;
    border-radius: 8px;
    width: 100%;
}

.row {
    width: 100%;
    display: flex;
    flex-direction: row;
}

.column {
    width: 100%;
    display: flex;
    flex-direction: column;
}

.song_grid {
    margin-bottom: 0.5rem;
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, 320px);
    width: 100%;
}

#category_img {
    width: 300px;
    height: 300px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 10%;
}

.title {
    font-weight: bold;
    font-size: xx-large;
    display: flex;
    align-items: center;
}

.metadata {
    width: 100%;
    padding: 0rem 1rem;
}

.playSongs {
    display: flex;
    align-items: center;
    margin-top: 1rem;
}

.title>div {
    margin-right: 1rem;
}

.actions {
    display: flex;
    margin-top: 1rem;
}

.actions>div {
    margin-right: 1rem;
}

.song_items {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 7%;
    color: var(--fore-0);
    margin: 2px 0px;
    border-radius: 4px;
}

.song_items:hover {
    background-color: var(--back-2);
}


.option {
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.song_items:hover .option {
    opacity: 0.8;
}
</style>