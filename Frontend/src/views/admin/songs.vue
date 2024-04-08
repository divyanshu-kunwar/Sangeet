<script setup>
import Button_ from '@/components/atomic/Button_.vue';
import deleteIcon from '@/assets/delete.svg'

import eyeIcon from '@/assets/new/eye.svg'
import likeIcon from '@/assets/new/like.svg'
import dislikeIcon from '@/assets/new/dislike.svg'

import { useRouter } from 'vue-router';
const router = useRouter();

import { ref } from 'vue';

const song_data = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "all_songs", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        song_data.value = data['songs']
    })
    .catch(error => {
        console.log(error)
    })


</script>

<template>
    <div class="main">
        <h1>Manage Songs</h1>

        <div>
            <div class="top_action">

                <div class="selectbox">
                    <label>Sort By</label>
                    <select name="sort" id="sort">
                        <option>Name (A-Z)</option>
                        <option>Name (Z-A)</option>
                        <option>Newest to oldest</option>
                        <option>Oldest to newest</option>
                        <option>Popularity</option>
                    </select>
                </div>

            </div>
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
                        <Button_ :icon="deleteIcon" type="none" size="small" shape="rectangle" />
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
    align-items: center;
    width: 100%;
    height: fit-content;
    border: 1px dashed var(--back-2);
}

.editableTable {
    width: 90%;
    margin-top: 2rem;
}

.editableTable tr {
    display: table-row;
    border: 1px dashed var(--back-2);
}

.editableTable td,
.editableTable th {
    padding: 0.5rem;
    text-align: center;
    outline: 1px solid var(--back-1);
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
    align-items: center;
    justify-content: space-between;
}

select {
    margin-right: 1rem;
    font-size: large;
    padding: 0.5rem;
    background-color: var(--back-1);
    border: none;
    color: var(--fore-0);
}

.selectbox {
    display: flex;
    background-color: var(--back-1);
    align-items: center;
    padding: 0.25rem 1rem;
    border-radius: 0.5rem;
    margin: 1rem;
}

select:focus {
    outline: none;
}

.selectbox label {
    margin-left: 0.5rem;
    font-size: large;
    color: var(--fore-0);
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