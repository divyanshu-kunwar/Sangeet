<script setup>
import CardH_ from "@/components/atomic/CardH_.vue"
import PlayerVisual from '@/components/atomic/PlayerVisual.vue'
import PlayerController from "@/components/molecular/PlayerController.vue"
import PlayerOptions from "@/components/molecular/PlayerOptions.vue"

import logoIcon from '@/assets/logo.svg'
import accountIcon from '@/assets/accountIcon.svg'
import searchIcon from '@/assets/searchIcon.svg'

import Button_ from '@/components/atomic/Button_.vue'
import Navigation from '@/components/molecular/Navigation.vue'
import PlayList from '@/components/molecular/LeftPlaylist.vue'
import QueueList from '@/components/molecular/QueueList.vue'

import { store } from '@/utility/store.js'

import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
const curr_route = computed(() => useRouter().currentRoute.value.name)

import homeIcon from "@/assets/navigationIcon/home.svg"
import home_sIcon from "@/assets/navigationIcon/home_s.svg"
import browse_sIcon from "@/assets/navigationIcon/browse_s.svg"
import browseIcon from "@/assets/navigationIcon/browse.svg"
import whatnewIcon from "@/assets/navigationIcon/whatnew.svg"
import whatnew_sIcon from "@/assets/navigationIcon/whatnew_s.svg"

const navigations = [
    {
        "name": "Home",
        "Icon": homeIcon,
        "Icon_selected": home_sIcon,
        "route": "app"
    },
    {
        "name": "Browse",
        "Icon": browseIcon,
        "Icon_selected": browse_sIcon,
        "route": "browse"
    }, 
    {
        "name": "What's New",
        "Icon": whatnewIcon,
        "Icon_selected": whatnew_sIcon,
        "route": "notification"
     } 
]

const songId = ref(store.songId)
const playing = ref(store.playing)
const volume = ref(store.volume)
const muted = ref(store.isMuted)
const songDetail = ref({})

watch(store, () => {
    let sourceNode = document.getElementById('source')
    let src = import.meta.env.VITE_BACKEND_URL +  "stream?id=" + store.songId 
    sourceNode.setAttribute('src', src)
    sourceNode.setAttribute('type', 'audio/mpeg')
    if(store.songId != songId.value){
        songId.value = store.songId 
        document.getElementById('player').load()
        fetchSongDetails()
    }
    playing.value = store.playing
    if(store.playing){
        document.getElementById('player').play()
    }else
        document.getElementById('player').pause()

    if(store.seekRequestedTime != 0){
        document.getElementById('player').currentTime = store.seekRequestedTime
        store.seekRequestedTime = 0
    }
    if(store.volume != volume.value){
        document.getElementById('player').volume = store.volume/100
        volume.value = store.volume
    }
    if(store.isMuted != muted.value){
        document.getElementById('player').muted = store.isMuted
        muted.value = store.isMuted
    }
})

onMounted(() => {
if(store.queue.length != 0)
    fetchSongDetails()
document.getElementById('player').addEventListener('durationchange', () => {
    store.totalTime = document.getElementById('player').duration
})
document.getElementById('player').addEventListener('ended', () => {
    store.playing = true
    store.playNext(true)
    fetchSongDetails()
})
document.getElementById('player').addEventListener('timeupdate', () => {
    store.seekTime = document.getElementById('player').currentTime
    if(document.getElementById('player').buffered.length > 0)
        store.bufferedTime =  document.getElementById('player').buffered.end(0)
})
})

function fetchSongDetails(){
    let detailToFetch = store.songId==="-1" ? store.queue[0] : store.songId
    fetch(`http://localhost:5000/api/songs?id=${detailToFetch}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    }).then(response => response.json())
    .then(data => {
        let artist = ""
        for (let i = 0; i < data['artists'].length; i++) {
            if(i != 0)
                artist += ", " + data['artists'][i]['name']
            else
                artist += data['artists'][i]['name']
        }
        data['artists'] = artist
        songDetail.value = data
    })
    .catch(error => {
        console.log(error)
    })
}

function checkIfLoggedIn(){
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
    })
}
checkIfLoggedIn()
</script>

<template>
    <div id="main">
        <div id="left">
            <Navigation :navigations="navigations"/>
            <PlayList />
        </div>

        <div id="center">
            <div class="topHead">
                <img :src="logoIcon" />
                <div>
                    <Button_ v-if="curr_route == 'app'" :icon="searchIcon" type="none" size="small" shape="circle"
                        @click="$router.push({ name: 'browse' })" class="actbtn"/>
                    <Button_ :icon="accountIcon" type="none" size="small" shape="circle" class="actbtn"
                        @click="$router.push({ name: 'account' })"/>
                </div>
            </div>
            <div class="view">
                <router-view :key="$route.fullPath"/>
            </div>
        </div>

        <div id="right">
            <audio id="player">
                <source id="source" />
            </audio>
            <PlayerVisual :isPlaying="playing" :amplitude="100" />
            <QueueList />
        </div>
    </div>

    <div id="playbar">
        <CardH_ :label="songDetail.name" :artist="songDetail.artists" :image="songDetail.image" :class="songId=='-1' ? 'hidden' : ''"/>
        <PlayerController />
        <PlayerOptions />
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
    align-items: center;
    width: 350px;
    margin: 2px;
}

#left>div {
    width: 100%;
    background-color: var(--back-1);
    margin-top: 2px;
}

#center {
    display: flex;
    width: calc(100% - 704px);
    flex-direction: column;
    padding: 2rem 2rem;
    background-color: var(--back-1);
    margin: 4px 1px;
}

#right {
    width: 350px;
    margin: 2px;
    background-color: var(--back-1);
    padding: 1rem;
    font-size: larger;
}

.topHead {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.topHead > div {
    display: flex;
    margin-right: 1rem;
}
.actbtn{
    background-color: var(--back-0);
    margin-right: 1rem;
}

.topHead>img {
    width: 120px;
}

#playbar {
    display: grid;
    justify-content: space-between;
    grid-template-columns: 2fr 5fr 2fr;
    padding: 0px 2rem;
    height: 6rem;
    column-gap: 10%;
}

.view{
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    height: 100%;
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

.hidden{
    visibility: hidden;
}
</style>