<script setup>
import Button_ from '@/components/atomic/Button_.vue';

import editIcon from '@/assets/edit.svg'
import deleteIcon from '@/assets/delete.svg'
import albumIcon from '@/assets/AdminNavIcon/categories.svg'
import sampleImage from '@/assets/sampleImage.png';

import eyeIcon from '@/assets/new/eye.svg'
import likeIcon from '@/assets/new/like.svg'
import dislikeIcon from '@/assets/new/dislike.svg'


import { useRouter } from 'vue-router';
import { ref } from 'vue';
const router = useRouter();

const navigateToAdd = () => router.push({ name: 'AddAlbum' })
const navigateToEdit = (id) => router.push({ name: 'EditAlbum', params: { id: id } })

const deleteAlbum = (id) => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}album?id=${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    }).then(() => {
        window.location.reload()
    })
}

const albums = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "user_albums", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        albums.value = data['albums']
    })
    .catch(error => {
        console.log(error)
    })

</script>

<template>
    <div class="main">
        <h1>Manage Albums</h1>
            <div>
                <div>
                    <Button_ :icon="albumIcon" type="grayscale" size="small" shape="rectangle" label="Create New Album"
                    @click="navigateToAdd()" />
                </div>
            </div>

            <table class="editableTable">
                <tr>
                    <th>Album</th>
                    <th>Created On</th>
                    <th>Songs</th>
                    <th>Actions</th>
                </tr>
                <tr v-for="album in albums" :key="album.id">
                    <td>
                        <div class="song_detail">
                            <img :src="album.image ? album.image : sampleImage" class="song_image"/>
                            <div class="song_info">
                                <span>{{ album.name }}</span>
                                <span class="small">
                                    {{ album.description.slice(0,100) }}
                                </span>
                            </div>
                        </div>
                    </td>
                    <td>{{ album.created_at }}</td>
                    <td>
                        <span v-for="song in album.songs">{{ song }}<br /></span>
                    </td>
                    <td>
                        <div class="actions">
                            <Button_ :icon="editIcon" type="none" size="small" shape="rectangle" @click="navigateToEdit(album.id)" />
                            <Button_ :icon="deleteIcon" type="none" size="small" shape="rectangle" @click="deleteAlbum(album.id)" />
                        </div>
                    </td>
                </tr>
            </table>
    </div>
</template>

<style scoped>
.main{
    display: flex;
    flex-direction: column;
    align-items: start;
    width: 100%;
    height: fit-content;
    padding: 2%;
}
.editableTable{
    width: 90%;
    margin-top: 2rem;
}
.editableTable tr{
    display: table-row;
}
.editableTable td, .editableTable th {
    padding: 0.5rem;
    text-align: center;
    border: 1px solid var(--back-2);
}
.song_image{
    width: 80px;
    height: 80px;
    border: 8px;
    margin-right: 1rem;
}
.actions{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
.album{
    display: flex;
    flex-direction: column;
}
.song_detail{
    display: flex;
    align-items: center;
    justify-content: center;
}
.song_info{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.small{
    font-size: smaller;
}
</style>