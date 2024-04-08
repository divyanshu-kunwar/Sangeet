<script setup>
import Button_ from '@/components/atomic/Button_.vue';
import Seekbar from '@/components/atomic/Seekbar.vue'

import playIcon from '@/assets/pause.svg'
import pauseIcon from '@/assets/play.svg'
import nextIcon from '@/assets/next.svg'
import previousIcon from '@/assets/previous.svg'
import prev10Icon from '@/assets/prev10.svg'
import next10Icon from '@/assets/next10.svg'
import { ref, watch } from 'vue';
import { store } from '@/utility/store.js'

const isRemaining = ref(true);
const isPlaying = ref(store.playing);
const seekTime = ref(0)
const totalTime = ref(0)
const bufferedTime = ref(0)


const formatTime = (sec)=> Math.floor(sec/60)+":"+(Math.round(sec % 60).toString().padStart(2, "0"))

watch(store, () => {
    if(isPlaying.value != store.playing){
        isPlaying.value = store.playing
    }
    if(seekTime.value != store.seekTime){
        seekTime.value = store.seekTime
    }
    if(totalTime.value != store.totalTime){
        totalTime.value = store.totalTime
    }
    if(bufferedTime.value != store.bufferedTime){
        bufferedTime.value = store.bufferedTime
    }
})

const updateSeeked = (n) => {
    store.seekRequestedTime = n
}

function changePlayState(){
    if(store.songId == "-1")
        store.songId = store.queue[0]
    store.playing = !store.playing
}

</script>

<template>
    <div id="PlayerController">
        <div class="control">
            <Button_ :icon="prev10Icon" shape="circle" type="none" size="small" 
            @click="store.seekBack10()"/>
            <Button_ :icon="previousIcon" shape="circle" type="none" size="small" 
            @click="store.playPrevious()"/>
            <Button_ @click="changePlayState()" 
            :icon="isPlaying ? playIcon : pauseIcon" shape="circle" type="none" size="small" />
            <Button_ :icon="nextIcon" shape="circle" type="none" size="small" 
            @click="store.playNext()"/>
            <Button_ :icon="next10Icon" shape="circle" type="none" size="small" 
            @click="store.seek10()"/>
        </div>
        <div id="seekbar">
            <span class="time">{{formatTime(seekTime)}}</span>

            <Seekbar :totalLength="totalTime" :seekLength="seekTime" :bufferedLength="bufferedTime"
            @seekTo="(n) => updateSeeked(n)" :strokeWidth="8"/>

            <span @click="isRemaining = !isRemaining" v-if="isRemaining" class="time">{{formatTime(totalTime)}}</span>
            <span @click="isRemaining = !isRemaining" v-else class="time">-{{formatTime(totalTime - seekTime)}}</span>

        </div>
    </div>
</template>

<style scoped>
.control {
    display: flex;
}

#seekbar {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 0.5rem;
}

#PlayerController {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.time{
    width: 2rem;
    padding: 0px 0.5rem;
    font-size: small;
}

</style>