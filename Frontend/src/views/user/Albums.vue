<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { store } from '@/utility/store.js'
import Button_ from '@/components/atomic/Button_.vue';
import PlayIcon from '@/assets/play.svg'
import addIcon from '@/assets/add.svg'

import AddToPlaylist from '@/components/molecular/AddToPlaylist.vue';
import CardH_ from '@/components/atomic/CardH_.vue';

const router = useRouter();

const id = router.currentRoute.value.params.id
const openedPlaylist = ref(false)
const albumDetail = ref({})
const songs_id = ref([])


fetch(import.meta.env.VITE_BACKEND_URL +  "album?id=" + id, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
}).then(response => response.json())
    .then(data => {
        if (data["success"]){
            albumDetail.value = data["album"]
            for (let i = 0; i < albumDetail.value.songs.length; i++) {
                songs_id.value.push(albumDetail.value.songs[i]['id'])
            }
        }
    }).catch(error => {
        console.log(error)
    })

const play = (songs) => {
    for (let i = 0; i < songs.length; i++) {
        store.addToQueueFront(songs[i]['id'])
    }
}
</script>

<template>
    <div class="main">
        <div class="form">
            <div class="row">
                <img id="album_img" :src="albumDetail.image" />
                <div class="metadata column">
                    <div class="title" @click="play(albumDetail.songs)">
                        <Button_ :icon="PlayIcon" type="gradient" size="small" shape="circle" />
                        {{ albumDetail.name }}
                    </div>
                    <div class="uploaded_on">
                        {{ albumDetail.created_at }}
                    </div>
                    <div class="tags">
                        <RouterLink v-for="tag in albumDetail.tags" class="tag" :to="'/app/tags/' + tag.id">
                            {{ tag.name }}
                        </RouterLink>
                    </div>
                    <div class="description">{{ albumDetail.description }} </div>
                    <div>
                        <Button_ :icon="addIcon" label="Add To Playlist" size="small" @click="openedPlaylist = true" />
                    </div>
                    <div v-if="openedPlaylist">
                        <addToPlaylist @close="openedPlaylist = false" :id="songs_id" />
                    </div>
                </div>
            </div>

        </div>
    </div>
    <h1>Songs</h1>
    <div class="album_grid">
        <CardH_ :label="song.name" :artist="song.artists" :image="song.image" v-for="song in albumDetail.songs"
            :href="'/app/song/' + song.id" />
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

#album_img {
    width: 300px;
    height: 300px;
    object-fit: cover;
    border-radius: 8px;
    margin-right: 10%;
}

.metadata {
    width: 100%;
    padding: 0rem 1rem;
}

.title {
    display: flex;
    font-weight: bold;
    font-size: xx-large;
    align-items: center;
}

.title>div {
    margin-right: 1rem;
}

.album_grid {
    margin: 0.5rem 0rem;
    display: grid;
    row-gap: 2rem;
    grid-template-columns: repeat(auto-fill, 300px);
}

.grid {
    display: flex;
    flex-wrap: wrap;
}

.tags {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    row-gap: 10px;
    margin: 0.5rem 0rem;
}

.tags>a {
    display: flex;
    margin-right: 4px;
    padding: 2px 16px;
    background-color: var(--shade);
    color: var(--back-1);
    border-radius: 16px;
    font-size: small;
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