<script setup>
import { ref } from 'vue'
import LineGraph from '@/components/molecular/LineGraph.vue'
import CardH_ from '@/components/atomic/CardH_.vue';

let data_ = ref({})

let user_data = ref([
    {
        name: "Users",
        type: 'scatter',
        mode: 'lines+markers',
        fill: 'tozeroy',
        fillcolor: '#50FEFE0f',
        line: {
            shape: 'spline',
            width: 3
        },
        marker: {
            color: '#50FEFE',
        }
    },
    {
        name: "Creators",
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'lines+markers',
        fillcolor: '#105BDB0F',
        line: {
            shape: 'spline',
            width: 3
        },
        marker: {
            color: '#105BDB',
        }
    }
])
let song_data = ref([
    {
        name: "Songs",
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'lines+markers',
        fillcolor: '#105BDB07',
        line: {
            shape: 'spline',
            width: 3
        },
        marker: {
            color: '#105BDB',
        }
    }
])
let albums_data = ref([
    {
        name: "Albums",
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'lines+markers',
        fillcolor: '#50FEFE0F',
        line: {
            shape: 'spline',
            width: 3
        },
        marker: {
            color: '#50FEFE',
        }
    }
])

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

let popular_artist_data = ref([
    {
        name : "Play Count",
        type: 'bar',
        marker: {
            color: '#50FEFE9F'
        }
    }
])
let popular_artist_annotation = ref([])

let popular_tags_data = ref([
    {
        name : "Play Count",
        type: 'bar',
        marker: {
            color: '#50FEFE9F'
        }
    }
])
let popular_tags_annotation = ref([])

fetch(import.meta.env.VITE_BACKEND_URL + "analytics", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        data_.value = data
        if (data["success"]) {
            console.log("Setting all the values")
            user_data.value[0].x = data["users"]["date"]
            user_data.value[0].y = data["users"]["data"]
            user_data.value[1].x = data["creators"]["date"]
            user_data.value[1].y = data["creators"]["data"]
            song_data.value[0].x = data["songs"]["date"]
            song_data.value[0].y = data["songs"]["data"]
            albums_data.value[0].x = data["albums"]["date"]
            albums_data.value[0].y = data["albums"]["data"]
        }
    })
    .catch(error => {
        console.log(error)
    })


fetch(import.meta.env.VITE_BACKEND_URL + "popular_analytics", {
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

            popular_artist_data.value[0].x = []
            popular_artist_data.value[0].y = []
            for(let i=0; i < data["artists"].length; i++){
                popular_artist_data.value[0].x.push(data["artists"][i]['name'].slice(0, 8))
                popular_artist_data.value[0].y.push(data["artists"][i]['play_count'])
                popular_artist_annotation.value.push({
                    id : data["artists"][i]['id'],
                    name : data["artists"][i]['name'],
                    image: data["artists"][i]['image'],
                    play_count : data["artists"][i]['play_count']
                })
            }

            popular_tags_data.value[0].x = []
            popular_tags_data.value[0].y = []
            for(let i=0; i < data["tags"].length; i++){
                popular_tags_data.value[0].x.push(data["tags"][i]['name'].slice(0, 8))
                popular_tags_data.value[0].y.push(data["tags"][i]['play_count'])
                popular_tags_annotation.value.push({
                    id : data["tags"][i]['id'],
                    name : data["tags"][i]['name'],
                    image: data["tags"][i]['image'],
                    play_count : data["tags"][i]['play_count']
                })
            }
            
        }
    })
    .catch(error => {
        console.log(error)
    })

</script>

<template>
    <h1>Admin Dashboard</h1>
    <div class="dashboard">

                
        <div class="card_gallery">
            <div class="card user_card">
                <h3>All Users</h3>
                <h2>{{ data_["total_users"] }}</h2>
                <h4>+{{ data_["del_users"] }} Joined Today</h4>
            </div>

            <div class="card creator_card">
                <h3>Creators</h3>
                <h2>{{ data_["total_creators"] }}</h2>
                <h4>+{{ data_["del_creators"] }} Joined Today</h4>
            </div>

            <div class="card album_card">
                <h3>Albums</h3>
                <h2>{{ data_["total_albums"] }}</h2>
                <h4>+{{ data_["del_albums"] }} Published Today</h4>
            </div>

            <div class="card song_card">
                <h3>Songs</h3>
                <h2>{{ data_["total_songs"] }}</h2>
                <h4>+{{ data_["del_songs"] }} Uploaded Today</h4>
            </div>


        </div>
        
        <LineGraph v-if="user_data[0].x" :data="user_data" title="Users & Creators" xTitle="Date" yTitle="No Of Users" :width="600" :height="400" />
        
        <LineGraph v-if="song_data[0].x" :data="song_data" title="Songs Published" xTitle="Date" yTitle="No Of Songs" :width="600" :height="400" />
        
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

        <LineGraph v-if="albums_data[0].x" :data="albums_data" title="Albums Published" xTitle="Date" yTitle="No Of Albums" :width="600" :height="400" />

        <div class="popular_card">
            <h3>Popular Albums</h3>
            <div class="Horizontal_cards">
                <CardH_ :label="album.name" :artist="'Play Count :'+ album.play_count" :image="album.image" v-for="album in popular_album_annotation" :href="'/app/album/' + album.id" />
            </div>
        </div>
        
        <LineGraph v-if="popular_album_data[0].x" :data="popular_album_data" 
        title="Popular Album" 
        xTitle="Date" yTitle="Play Count" :width="600" :height="400" />


        <div class="popular_card">
            <h3>Popular Artist</h3>
            <div class="Horizontal_cards">
                <CardH_ :label="artist.name" :artist="'Play Count :'+ artist.play_count" :image="artist.image" v-for="artist in popular_artist_annotation" :href="'/app/artist/' + artist.id" />
            </div>
        </div>

        <LineGraph v-if="popular_artist_data[0].x" :data="popular_artist_data" 
        title="Popular Artist" 
        xTitle="Date" yTitle="Play Count" :width="600" :height="400" />

        
        <div class="popular_card">
            <h3>Popular Tags</h3>
            <div class="Horizontal_cards">
                <CardH_ :label="tag.name" :artist="'Play Count :'+ tag.play_count" 
                :image="tag.image" v-for="tag in popular_tags_annotation" 
                :href="'/app/tags/' + tag.id" />
            </div>
        </div>

        <LineGraph v-if="popular_tags_data[0].x" :data="popular_tags_data" title="Popular Tags" 
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
