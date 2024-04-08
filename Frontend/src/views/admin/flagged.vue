<script setup>
import Button_ from '@/components/atomic/Button_.vue';
import { ref } from 'vue';

const flaggedItems = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "flagged", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        flaggedItems.value = data['songs']
    })
    .catch(error => {
        console.log(error)
    })

function resolved(status, id){
    fetch(import.meta.env.VITE_BACKEND_URL +  "flagged/resolve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body: JSON.stringify({
            id: id,
            resolved: status
        })
    }).then(response => response.json())
        .then(data => {
            if(data['success'])
                window.location.reload()
    })
}
</script>

<template>
    <div class="main">
        <div>
            <h1>Manage Flagged Items</h1>
            <div>
            </div>
        </div>

        <table class="editableTable">
            <tr>
                <th>Song</th>
                <th>Flagged By</th>
                <th>Actions</th>
            </tr>

            <tr v-for="item in flaggedItems">
                <td>
                    <div class="song_detail">
                        <img :src="item['song_image'] ? item['song_image'] : 'https://picsum.photos/200?random=1'" class="song_image" />
                        <div class="song_info">
                            <span>{{ item.song_name }}</span>
                            <span>
                                <span v-for="creator in item.song_creators">{{ creator }}</span>
                            </span>
                        </div>
                    </div>
                </td>
                <td>{{ item.user_name }} <br />
                    {{ item.user_email }}</td>
                <td>
                    <div class="actions">
                        <Button_ type="grayscale" size="small" shape="rectangle" label="Solved" 
                        @click="resolved(true, item['id'])"/>
                        <Button_ type="grayscale" size="small" shape="rectangle" label="Rejected"
                        @click="resolved(false, item['id'])"/>
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
    margin: 1rem;
}

.editableTable {
    width: 90%;
}

.editableTable tr {
    display: table-row;
    outline: 1px solid var(--back-2);
}

.editableTable td,
.editableTable th {
    padding: 0.5rem;
    text-align: center;
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

.actions > * {
    margin: 0px 10px;
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
</style>