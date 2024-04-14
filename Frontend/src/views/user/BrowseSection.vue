<script setup>
import Card_ from "@/components/atomic/Card_.vue"
import sampleImage from '@/assets/sampleImage.png'
import TextInput_ from "@/components/atomic/TextInput_.vue";
import searchIcon from '@/assets/searchIcon.svg'
import CardH_ from "@/components/atomic/CardH_.vue";

import { ref , watch} from 'vue';
const searchValue = ref('');

const categories = ref([])
const songs = ref([])
const albums = ref([])
const artists = ref([])

fetch(import.meta.env.VITE_BACKEND_URL +  "all_tags")
    .then(response => response.json())
    .then(data => {
        categories.value = data["tags"]
    })
    .catch(error => {
        console.log(error)
    })


    const search = (value) => {
        searchValue.value = value
        if(value.trim() == '') return
        fetch(import.meta.env.VITE_BACKEND_URL +  "search?q=" + value,{
            method: "GET",
        })
            .then(response => response.json())
            .then(data => {
                if(data['success']){
                    songs.value = data['songs']
                    albums.value = data['albums']
                    artists.value = data['artists']
                }
            })
            .catch(error => {
                console.log(error)
            })
    }


</script>

<template>
    
    <div class="SearchBox">
        <TextInput_ class="inputs"  
        type="name" size="large"
        placeholder="What do you want to play?" 
        @inp="(value) => search(value)" 
        shape="search"
        :icon="searchIcon" />
    </div>

    <div class="Result" v-if="searchValue.trim() != ''">
        <h2>Result For {{ searchValue }}</h2>

        <h3 v-if="songs.length">Songs</h3>
        <div class="Grid1"> 
            <Card_ v-for="song in songs" :label="song.name"
            :artist="song.creators" :image="song.image"
            :songId="song.id.toString()" />
        </div>

        <h3 v-if="albums.length">Albums</h3>
        <div class="Grid1">
            <CardH_ v-for="album in albums" :label="album.name"
            :artist="album.creator" :image="album.image"
            :href="'/album/'+album.id" />
        </div>

        <h3 v-if="artists.length">Artists</h3>
        <div class="Grid1">
            <RouterLink v-for="artist in artists" class="circular_card" :to="'/app/artist/'+artist.id">
                <img :src="artist.image ? artist.image : sampleImage" />
                <span>{{ artist.name }}</span>
            </RouterLink>
        </div>

    </div>

    <div class="Result" v-if="searchValue.trim() == ''">
        <h2>Browse</h2>
        <div class="Grid1">
    
        <RouterLink class="card" v-for="category in categories" :to=" '/app/tags/' + category.id">
            <img :src="category.image ? category.image : sampleImage" />
            <span>{{ category.name }}</span>
        </RouterLink>

        </div>
    </div>

</template>

<style scoped>
h3{
    margin-top: 4rem;
    margin-bottom: 0.5rem;
}
.Grid1{
    display: flex;
    flex-direction: row;
    margin-top: 2rem;
    padding: auto;
    flex-wrap: wrap;
    column-gap: 1rem;
    row-gap: 1rem;
    justify-content: start;
    align-items: start;
}
.Result{
    margin-top: 10px;
}

.card{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 250px;
    height: 250px;
    opacity: 0.8;
    transition: opacity 0.3s ease;
}

.card:hover{
    opacity: 1;
}

.card img{
    width: 100%;
    object-fit: cover;
    border-radius: 4px;
    filter: hue-rotate(20deg) grayscale(50%);
    transition: all 0.3s ease;
}

.card:hover img{
    filter: grayscale(20%);
}

.card span{
    position: relative;
    display: inline;
    margin-top: -40px;
    color: var(--back-1);
    font-weight: bold;
    transition: all 0.3s ease;
    padding: 0px 8px;
    border-radius: 4px;
    background-color: var(--fore-2);
    font-size: medium;
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

.SearchBox{
    display: flex;
    width: min(500px, 80vw);
    align-self: center;
    text-align: center;
    margin-top: 2rem;
}
.SearchBox > div{
    width: 100%;
    font-size: large;
}

</style>