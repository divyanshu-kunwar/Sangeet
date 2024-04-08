<script setup>
import Button_ from '@/components/atomic/Button_.vue';
import sampleIcon from '@/assets/sIcon.svg'
import { ref } from 'vue';

import eyeIcon from '@/assets/new/eye.svg'
import likeIcon from '@/assets/new/like.svg'
import dislikeIcon from '@/assets/new/dislike.svg'

const blockUser = (id) => {
    
}

const userData = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "all_users", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        userData.value = data['users']
    })
    .catch(error => {
        console.log(error)
    })


</script>

<template>
    <div class="main">
            <div>
                <h1>Manage Users</h1>
                <div>
                </div>
            </div>

            <table class="editableTable">
                <tr>
                    <th>User</th>
                    <th>Joined On</th>
                    <th>Views</th>
                    <th>Actions</th>
                </tr>

                <tr v-for="user in userData">
                    <td>
                        <div class="song_detail">
                            <img :src="user['image'] ? user['image'] : 'https://picsum.photos/200?random=1'" 
                            class="song_image"/>
                            <div class="song_info">
                                <span>{{ user["name"] }}</span>
                                <span>{{ user["email"] }}</span>
                                <span>{{ user["role"] }}</span>
                            </div>
                        </div>
                    </td>
                    <td>{{ user["joined_on"] }}</td>
                    <td>
                        <td class="views">
                    <div>
                        <span>
                            {{ user['total_likes'] }}
                        </span>
                        <img class="icons" :src="likeIcon" />
                        <span>
                            {{ user['total_dislikes'] }}
                        </span>
                        <img class="icons" :src="dislikeIcon" />
                    </div>
                </td>
                    </td>
                    <td>
                        <Button_ label="block" type="grayscale" size="small" shape="rectangle" 
                        @click="blockUser(user['id'])"/>
                    </td>
                </tr>
            
            </table>
    </div>
</template>

<style scoped>
.main{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: fit-content;
    border: 1px dashed var(--back-2);
}
.editableTable{
    width: 90%;
    margin-top: 2rem;
}
.editableTable tr{
    display: table-row;
    border: 1px dashed var(--back-2);
}
.editableTable td, .editableTable th {
    padding: 0.5rem;
    text-align: center;
    outline: 1px solid var(--back-1);
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