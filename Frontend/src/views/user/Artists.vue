<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import Card_ from '@/components/atomic/Card_.vue';
import CardH_ from '@/components/atomic/CardH_.vue';

const router = useRouter();

const id = router.currentRoute.value.params.id

const artistsDetail = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "artist?id=" + id, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
}).then(response => response.json())
    .then(data => {
        if(data['success'])
            artistsDetail.value = data['data']
    }).catch(error => {
        console.log(error)
    })
</script>
<template>
    <div class="main">
        <div class="form">
            <div class="row">
                <img id="category_img" :src="artistsDetail.image" />
                <div class="metadata">
                    <div class="title">
                        {{ artistsDetail.name }}
                    </div>
                    <div class="uploaded_on">
                        User Since {{ artistsDetail.joined_since }}
                    </div>
                    <div class="albums column">
                        <div class="head">Albums</div>
                        <div class="album_grid">
                            <CardH_ v-for="album in artistsDetail.albums" :label="album.name" :artist="album.creator"
                                :image="album.image" :href="'/app/album/' + album.id" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="songs column">
            <div class="head">Songs</div>
            <div class="song_grid">
                <Card_ v-for="song in artistsDetail.songs" :label="song.name" :artist="song.artists" :image="song.image"
                    :songId="song.id.toString()" />
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
.column{
    width: 100%;
    display: flex;
    flex-direction: column;
}

.album_grid {
    margin-bottom: 0.5rem;
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, 200px);
    width: 100%;
}
.song_grid {
    margin: 0.5rem 0rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, 200px);
    width: 100%;
}
#category_img{
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 50%;
    margin-right: 10%;
}
.title {
    font-weight: bold;
    font-size: xx-large;
}

.metadata {
    width: 100%;
    padding: 0rem 1rem;
}

.head{
    font-size: large;
}
.songs {
    padding: 2rem;
}
.albums{
    margin-top: 2rem;
}
</style>