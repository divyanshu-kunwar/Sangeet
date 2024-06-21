<script setup>
import { ref } from 'vue'
import LineGraph from '@/components/molecular/LineGraph.vue'
import CardH_ from '@/components/atomic/CardH_.vue';

let popular_song_data = ref([
    {
        name : "Play Count",
        type: 'bar',
        marker: {
            color: '#50FEFE9F'
        }
    },
    {
        name : "Like Count",
        type: 'bar',
        marker: {
            color: '#105BDB9F'
        }
    }
])
let popular_song_annotation = ref([])

let popular_album_data = ref([
    {
        name : "Play Count",
        type: 'bar',
        marker: {
            color: '#50FEFE9F'
        }
    }
])
let popular_album_annotation = ref([])


fetch(import.meta.env.VITE_BACKEND_URL + "popular_analytics?user=true", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        if (data['success']){
            console.log(data)

            popular_song_data.value[0].x = []
            popular_song_data.value[0].y = []
            popular_song_data.value[1].x = []
            popular_song_data.value[1].y = []
            for(let i = 0; i < data['songs'].length; i++){
                popular_song_data.value[0].x.push(data['songs'][i]['name'].slice(0, 8))
                popular_song_data.value[1].x.push(data['songs'][i]['name'].slice(0, 8))
                popular_song_data.value[0].y.push(data['songs'][i]['play_count'])
                popular_song_data.value[1].y.push(data['songs'][i]['like_count'])
                popular_song_annotation.value.push({
                    id : data['songs'][i]['id'],
                    name : data['songs'][i]['name'],
                    image: data['songs'][i]['image'],
                    play_count : data['songs'][i]['play_count'],
                    like_count : data['songs'][i]['like_count']
                })
            }

            popular_album_data.value[0].x = []
            popular_album_data.value[0].y = []
            for(let i=0; i < data["albums"].length; i++){
                popular_album_data.value[0].x.push(data["albums"][i]['name'].slice(0, 8))
                popular_album_data.value[0].y.push(data["albums"][i]['play_count'])
                popular_album_annotation.value.push({
                    id : data["albums"][i]['id'],
                    name : data["albums"][i]['name'],
                    image: data["albums"][i]['image'],
                    play_count : data["albums"][i]['play_count']
                })
            }
        }
    })
    .catch(error => {
        console.log(error)
    })

</script>

<template>
    <h1>Creator's Dashboard</h1>
    <div class="dashboard">
        
        <div class="popular_card">
            <h3>Popular Song</h3>
            <div class="Horizontal_cards">
                <CardH_ :label="song.name" :artist="'Play Count :'+ song.play_count+ ' Likes : ' + song.like_count" :image="song.image" v-for="song in popular_song_annotation" :href="'/app/song/' + song.id" />
            </div>
        </div>
        

        <LineGraph v-if="popular_song_data[0].x" 
        :data="popular_song_data" 
        title="Popular Song" xTitle="Date" 
        yTitle="Play Count / Likes" :width="600" :height="400" />


        <div class="popular_card">
            <h3>Popular Albums</h3>
            <div class="Horizontal_cards">
                <CardH_ :label="album.name" :artist="'Play Count :'+ album.play_count" :image="album.image" v-for="album in popular_album_annotation" :href="'/app/album/' + album.id" />
            </div>
        </div>
        
        <LineGraph v-if="popular_album_data[0].x" :data="popular_album_data" 
        title="Popular Album" 
        xTitle="Date" yTitle="Play Count" :width="600" :height="400" />

    </div> 
</template>

<style scoped>
h1 {
    align-self: center;
    width: fit-content;
    margin: 2rem;
}

.dashboard {
    display: grid;
    grid-template-columns: 1fr 1fr;
    width: fit-content;
    padding: 1rem 2rem;
    align-items: center;
    justify-content: center;
    align-self: center;
}

@media screen and (max-width: 1000px) {
    .dashboard {
        grid-template-columns: 1fr;
    }   
}

.card_gallery {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 1rem;
    row-gap: 1rem;
    width: fit-content;
    height: fit-content;
    justify-content: center;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
}

.card_gallery .card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem 2rem;
    border-radius: 8px;
}

.card h3 {
    margin: 4px;
}

.card h2 {
    margin: 6px;
}

.card h4 {
    margin: 2px;
}

.user_card {
    background-color: #398aee0f;
    border: 1px solid #398aee44;
}

.creator_card {
    background-color: #50fefe0f;
    border: 1px solid #50fefe44;
}

.song_card {
    background-color: #105bdb0f;
    border: 1px solid #105bdb44;
}

.album_card {
    background-color: #50fefe0f;
    border: 1px solid #50fefe44;
}

.Horizontal_cards{
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 1rem;
}
.popular_card{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    background-color: var(--back-1);
    margin: 1rem;
    height: calc(100% - 2rem);
}
</style>
