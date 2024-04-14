<script setup>
import Seekbar from '@/components/atomic/Seekbar.vue'
import Button_ from '@/components/atomic/Button_.vue';

import showPlayingIcon from '@/assets/showPlaying.svg'
import pipIcon from '@/assets/pip.svg'
import volumeIcon from '@/assets/volume.svg'
import mutedIcon from '@/assets/muted.svg'
import shuffleIcon from '@/assets/shuffle.svg'
import shuffleOffIcon from '@/assets/shuffleOff.svg'

import { store } from '@/utility/store';
import { ref, watch } from 'vue';

const volume = ref(store.volume)
const isMuted = ref(store.isMuted)
const randomize = ref(store.randomize)

const updateVolume = (n) => {
    store.volume = n
    store.isMuted = false
    volume.value = store.volume
    isMuted.value = store.isMuted
}

const updateMuted = () => {
    store.isMuted = !store.isMuted
    isMuted.value = store.isMuted
}

watch(() => store.volume, (newValue) => {
    volume.value = newValue
})

watch(() => store.randomize, (newValue) => {
    randomize.value = newValue
})

</script>

<template>
    <div id="right_controller">
        
        <Button_ :icon="pipIcon" shape="circle" type="none" style="display: none;"/>
        <Button_ :icon="randomize ? shuffleIcon : shuffleOffIcon" shape="circle" type="none" 
        @click="store.randomize = !store.randomize"/>
        <Button_ :icon="isMuted ? mutedIcon : volumeIcon" shape="circle" @click="updateMuted" />
        <Seekbar class="volumebar" :totalLength="100" :seekLength="volume" @seekTo="(n) => updateVolume(n)" :strokeWidth="32" />
        <Button_ :icon="showPlayingIcon" shape="circle" type="none" />
    </div>
</template>

<style scoped>
#right_controller {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}

.volumebar {
    max-width: 200px;
}
</style>