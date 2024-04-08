<script setup>
import sampleImage from '@/assets/sampleImage.png'
import CardH_ from "@/components/atomic/CardH_.vue"
import dismissIcon from '@/assets/dismiss.svg'
import musicIcon from '@/assets/musicIcon.svg'

import { store } from '@/utility/store.js'
import { ref , watch } from 'vue'

let cachedData = {}

const queue = ref(store.queue)
const queueLength = ref(store.queueLength)
const queueSong = ref({})

function fetchSongs(){
        queueSong.value = []
        for(let i = 0 ; i < queue.value.length ; i++){
            if(cachedData[queue.value[i]] != undefined){
                queueSong.value.push(cachedData[queue.value[i]])
            }else{
                fetch(`${import.meta.env.VITE_BACKEND_URL}songs?id=${queue.value[i]}`, {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": localStorage.getItem("token")
                        }
                    }).then(response => response.json())
                        .then(data => {
                            if(data['success']){
                                let artists = ""
                                for (let i = 0; i < data['artists'].length; i++) {
                                    if(i != 0)
                                        artists += ", " + data['artists'][i]['name']
                                    else
                                        artists += data['artists'][i]['name']
                                }
                                data['artists'] = artists
                                cachedData[queue.value[i]] = data
                                queueSong.value.push(data)
                            }
                        })
                        .catch(error => {
                            console.log(error)
                        })
            }
        }
}

watch(store, () => {
    if (store.queueLength != queueLength.value){
        queue.value = store.queue
        queueLength.value = store.queueLength
        fetchSongs()
    }
})

fetchSongs()

</script>

<template>
    <div class="Queue">
        <div class="Header">
            <img :src="musicIcon" />
            <span>Queue</span>
        </div>

        <div v-for="song in queueSong" :key="song.id"
        :class="queue[store.currentPlaying] == song.id ? 'active queuelistItem' : 'queuelistItem'">
            <CardH_ @click="store.addToQueueFront(song.id)"
            :label="song.name" :artist="song.artists" :image="song.image" />
            <img class="option cursor" :src="dismissIcon" @click="store.removeFromQueue(song.id)" />
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
    font-size: large;
    font-weight: bold;
}

.queuelistItem {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 0.5rem 7%;
    color: var(--fore-0);
    margin: 2px 0px;
    border-radius: 4px;
}

.queuelistItem:hover {
    background-color: var(--back-2);
}

.option {
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.queuelistItem:hover .option {
    opacity: 0.8;
}
.active{
    background-color: var(--back-2);
}
</style>