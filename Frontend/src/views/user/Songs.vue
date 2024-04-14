<script setup>

import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CardH_ from '@/components/atomic/CardH_.vue';
import addToPlaylist from '@/components/molecular/AddToPlaylist.vue'
import sampleImage from '@/assets/sampleImage.png';

import eyeIcon from '@/assets/new/eye.svg'
import likeIcon from '@/assets/new/like.svg'
import likecIcon from '@/assets/new/likec.svg'
import flagIcon from '@/assets/new/flagged.svg'
import Button_ from '@/components/atomic/Button_.vue';

import PlayIcon from '@/assets/play.svg'
import addIcon from '@/assets/add.svg'

import { store } from '@/utility/store.js';

const router = useRouter();

const id = router.currentRoute.value.params.id

const songDetail = ref({})
const expandedLyrics = ref(false)
const liked = ref(false)
const flagged = ref(false)
const openedPlaylist = ref(false)

fetch(import.meta.env.VITE_BACKEND_URL +  "songs?id=" + id, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        if (data['success'])
            songDetail.value = data
    })
    .catch(error => {
        console.log(error)
    })

fetch(import.meta.env.VITE_BACKEND_URL +  "like?id=" + id, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        if (data['success']) {
            liked.value = data['isliked']
        }
    })
    .catch(error => {
        console.log(error)
    })

fetch(import.meta.env.VITE_BACKEND_URL +  "flagged/resolve?id=" + id, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        if (data['success']) {
            flagged.value = !data['resolved']
        }
    })
    .catch(error => {
        console.log(error)
    })

function toggleLike() {
    fetch(import.meta.env.VITE_BACKEND_URL +  "like?id=" + id, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    }).then(response => response.json())
        .then(data => {
            if (data['success'])
                liked.value = data['liked']
            songDetail.value.like_count = data['like_count']
        })
}

function flagSong() {
    let reason = prompt("Reason to flag this song")
    fetch(import.meta.env.VITE_BACKEND_URL +  "flagged", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body: JSON.stringify({
            id: id,
            reason: reason
        })
    }).then(response => response.json())
        .then(data => {
            if (data['success'])
                flagged.value = true
        })
}

</script>
<template>
    <div class="main">
        <div class="form">
            <div class="row">
                <img id="song_img" :src="songDetail.image ? songDetail.image : sampleImage" />
                <div class="metadata column">
                    <div class="title">{{ songDetail.name }} </div>
                    <div class="hcontainer">
                        <Button_ :icon="PlayIcon" type="gradient" size="small" shape="circle"
                            @click="store.addToQueueFront(songDetail.id)" />
                        <div class="artists">
                            By -
                            <RouterLink v-for="artist in songDetail.artists" class="artist"
                                :to="'/artist/' + artist.id">
                                {{ artist.name }}
                            </RouterLink>
                        </div>
                    </div>
                    <div class="tags">
                        <RouterLink v-for="tag in songDetail.tags" class="tag" :to="'/app/tags/' + tag.id">
                            {{ tag.name }}
                        </RouterLink>
                    </div>
                    <div v-if="flagged" class="msg">
                        <img :src="flagIcon" />
                        <span> Marked by you as Inappropriate </span>
                    </div>
                    <div class="uploaded_on">{{ songDetail.created_at }}</div>
                    <div v-if="openedPlaylist">
                        <addToPlaylist @close="openedPlaylist = false" :id="[id]" />
                    </div>
                    <div class="stats">
                        <Button_ :icon="eyeIcon" :label="songDetail.play_count+' Views'" size="small" />
                        <Button_ v-if="liked" :icon="likecIcon" :label="songDetail.like_count+' Likes'" size="small" @click="toggleLike()"/>
                        <Button_ v-else :icon="likeIcon" :label="songDetail.like_count+' Likes'" size="small" @click="toggleLike()"/>
                        <Button_ :icon="addIcon" label="Add To Playlist" size="small" @click="openedPlaylist = true"/>
                        <Button_ :icon="flagIcon" label="Report" size="small" @click="flagSong()" v-if="!flagged" />
                    </div>

                </div>
            </div>

            <div class="album_grid">
                <h3>Albums</h3>
                <div class="grid">
                    <CardH_ v-for="album in songDetail.albums" :label="album.name" :artist="album.creators"
                        :image="album.image" :href="'/app/album/' + album.id" />
                </div>
            </div>

            <div class="lyricsContainer" @click="expandedLyrics = !expandedLyrics">
                <h3>Lyrics</h3>
                <pre :class="expandedLyrics ? 'expanded' : 'collapsed'">
{{ songDetail.lyrics }}
            </pre>
                <pre v-if="expandedLyrics">
Collapse ...
            </pre>
                <pre v-else>
Read More ...
            </pre>

            </div>



        </div>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    align-items: center;
    justify-content: center;
    height: fit-content;
    width: 100%;
    height: fit-content;
    padding: 4rem 0rem;
}

.form {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    width: 100%;
    border-radius: 8px;
}

.row {
    display: flex;
    flex-direction: row;
}

.column {
    display: flex;
    flex-direction: column;
}

#song_img {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 10%;
}

.metadata {
    width: 100%;
    padding: 0rem 1rem;
}

.title {
    font-weight: bold;
    font-size: xx-large;
}

.album_grid {
    margin: 0.5rem 0rem;
    display: flex;
    flex-direction: column;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, 200px);

}

.tags {
    display: flex;
    flex-direction: row;
    margin: 0.5rem 0rem;
}

.tags>a {
    margin-right: 4px;
    padding: 2px 16px;
    background-color: var(--shade);
    color: var(--back-1);
    border-radius: 16px;
}

.artists {
    font-size: x-large;
    margin: 0.5rem 0rem;
}

.artists a {
    margin-right: 4px;
    color: var(--shade);
}

.uploaded_on {
    margin: 0.5rem 0rem;
}

.stats {
    display: flex;
}

.stats>div {
    margin-right: 1rem;
    display: flex;
    align-items: center;
    min-width: 40px;
    justify-content: space-evenly;
    padding: 4px 10px;
}

.stats>div>span {
    margin-right: 8px;
}

.stats>div>img {
    opacity: 0.8;
    width: 20px;
}

.stats>div:hover {
    background-color: var(--back-2);
}

.like,
.dislike {
    filter: grayscale(100%);
}

.likeSelected,
.dislikeSelected {
    filter: grayscale(0%) brightness(150%);
}

.collapsed {
    height: 100px;
    overflow-y: hidden;
}

.expanded {
    height: auto;
}

.lyricsContainer {
    margin: 0.5rem 0rem;
    text-align: start;
}

.hcontainer {
    display: flex;
    align-items: center;
    margin: 0.5rem 0rem;
}

.hcontainer>div {
    margin-right: 1rem;
}

.msg {
    display: flex;
    align-items: center;
    text-wrap: wrap;
    margin: 0.5rem 0rem;
}

.msg img {
    width: 20px;
    height: 20px;
    margin-right: 8px;
}

</style>