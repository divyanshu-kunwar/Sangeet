<script setup>
import Button_ from '@/components/atomic/Button_.vue';

import musicIcon from '@/assets/musicIcon.svg'
import editIcon from '@/assets/edit.svg'
import deleteIcon from '@/assets/delete.svg'
import eyeIcon from '@/assets/new/eye.svg'
import likeIcon from '@/assets/new/like.svg'
import dislikeIcon from '@/assets/new/dislike.svg'

import { useRouter } from 'vue-router';
const router = useRouter();

const navigateToAdd = () => router.push({ name: 'AddSong' })
const navigateToEdit = (id) => router.push({ name: 'EditSong', params: { id: id } })

import { ref } from 'vue';

const song_data = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "user_songs", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        song_data.value = data['songs']
    })
    .catch(error => {
        console.log(error)
    })

const deleteSong = (id) => {
    fetch(import.meta.env.VITE_BACKEND_URL +  "songs?id=" + id, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    })
        .then(response => response.json())
        .then(data => {
            window.location.reload()
        })
        .catch(error => {
            console.log(error)
        })
}

</script>

<template>
    <div class="main">
        <h1>Manage Songs</h1>
        <div class="top_action">
            <Button_ :icon="musicIcon" type="grayscale" size="small" shape="rectangle" label="Upload"
                @click="navigateToAdd()" />
        </div>
        <table class="editableTable">
            <tr>
                <th>Song</th>
                <th>Upload Date</th>
                <th>Views</th>
                <th>Albums</th>
                <th>Actions</th>
            </tr>

            <tr v-for="song in song_data">
                <td>
                    <div class="song_detail">
                        <img :src="song['image'] ? song['image'] : 'https://picsum.photos/200?random=1'"
                            class="song_image" />
                        <div class="song_info">
                            <span>{{ song.name }}</span>
                            <span>
                                <span v-for="creator in song.creators">{{ creator }}</span>
                            </span>
                            <span>
                                <span v-for="tags in song.tags">{{ tags }} <span></span></span>
                            </span>
                        </div>
                    </div>
                </td>
                <td>{{ song.created_at }}</td>
                <td class="views">
                    <div>
                        <span>
                            {{ song.play_count }}
                        </span>
                        <img class="icons" :src="eyeIcon" /> <br />
                    </div>
                    <div>
                        <span>
                            {{ song.like_count }}
                        </span>
                        <img class="icons" :src="likeIcon" />
                        <span>
                            {{ song.dislike_count }}
                        </span>
                        <img class="icons" :src="dislikeIcon" />
                    </div>
                </td>
                <td>
                    <div class="album">
                        <RouterLink to="/admin" v-for="album in song.albums">{{ album }}</RouterLink>
                    </div>
                </td>
                <td>
                    <div class="actions">
                        <Button_ :icon="editIcon" type="none" size="small" shape="rectangle" 
                        @click="navigateToEdit(song['id'])"
                        />
                        <Button_ :icon="deleteIcon" type="none" size="small" shape="rectangle"
                        @click="deleteSong(song['id'])"/>
                    </div>
                </td>
            </tr>
        </table>

    </div>
</template>

<style scoped>
.main {
    display: flex;
    flex-direction: column;
    align-items: start;
    width: 100%;
    height: fit-content;
    padding: 2%;
}

.editableTable {
    width: 90%;
    margin-top: 2rem;
}

.editableTable tr {
    display: table-row;
}

.editableTable td,
.editableTable th {
    padding: 0.5rem;
    text-align: center;
    border: 1px solid var(--back-2);
}

.song_image {
    width: 80px;
    height: 80px;
    border: 8px;
    margin-right: 1rem;
}

.actions {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}

.album {
    display: flex;
    flex-direction: column;
}

.song_detail {
    display: flex;
    align-items: center;
    justify-content: center;
}

.song_info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.top_action {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.icons {
    width: 20px;
    height: 20px;
    opacity: 0.7;
}

.views{
    display: flex;
    flex-direction: column;
    align-items: center;
    row-gap: 1rem;
}

.views div{
    display: flex;
    flex-direction: row;
    align-items: center;
    column-gap: 8px;
}
</style>