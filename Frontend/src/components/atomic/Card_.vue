<script setup>
import Button_ from '@/components/atomic/Button_.vue'
import playIcon from '@/assets/playIcon.svg'
import { store } from '@/utility/store.js'

import { useRouter } from 'vue-router'
const router = useRouter()

defineProps({
    label:String,
    artist:String,
    image:String,
    songId:String,
    albumId:String,
    album_songsId: Array,
})

function play(songId , albumId , album_songsId){
    if(songId){
        store.addToQueueFront(songId)
    }
    if(albumId){
        for(let i = 0 ; i < album_songsId.length ; i++){
            store.addToQueueFront(album_songsId[i])
        }
    }
}

function navigate(songId , albumId){
    if(songId){
        router.push({ name: 'songDetail', params: { id: songId } })
    }
    if(albumId){
        router.push({ name: 'albumDetail', params: { id: albumId } })
    }
}

</script>
<template>
    <div class="song_card">
        <div class="song_image" @click="play(songId , albumId , album_songsId)">
            <img :src="image"/>
            <Button_ class="buttons" :icon="playIcon" type="" 
            size="large" shape="circle"/>
        </div>
        <div @click="navigate(songId , albumId)">
            <div v-if="label" class="label">{{ label }}</div>
            <div v-if="artist" class="artist">{{ artist }}</div>
        </div>
    </div>
</template>

<style scoped>
    .song_card{
        width: 190px;
        height: max-content;
        background-color: var(--back-1);
        padding: 5px;
        box-sizing: border-box;
        border-radius: 8px;
    }
    .song_image > img{
        width: 180px;
        height: 180px;
        object-fit: cover;
        border-radius: 8px;
    }
    .song_image > .buttons{
        position: static;
        margin-top: -126px;
        margin-left: 60px;
        margin-bottom: 76px;
        opacity: 0;
        scale: 1;
        transition: opacity 0.4s ease-in , scale 0.4s ease-in-out;
    }

    .song_card:hover .buttons{
        opacity: 1;
        scale: 1.5;
    }
    .label , .artist{
        margin:10px;
    }
    .label{
        color: var(--fore-2);
    }
    .artist{
        color: var(--fore-0);
        font-size: small;
    }

    .song_card:hover{
        background-color: var(--back-2);
    }

    .circular{
        border-radius: 50%;
        overflow: hidden;
    }

        
</style>