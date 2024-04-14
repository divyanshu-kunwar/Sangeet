<script setup>
import Button_ from '@/components/atomic/Button_.vue';
import editIcon from '@/assets/edit.svg'
import deleteIcon from '@/assets/delete.svg'
import sampleImage from '@/assets/sampleImage.png';

import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const navigateToAdd = () => router.push({ name: 'AddCategory' })
const navigateToEdit = (id) => router.push({ name: 'EditCategory', params: { id: id } })
const deleteCategory = (id) => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}tags?id=${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data["success"]) {
            window.location.reload();
        }
    })
    .catch(error => {
        console.log(error)
    })
}

const categories = ref([])

fetch(import.meta.env.VITE_BACKEND_URL +  "all_tags")
    .then(response => response.json())
    .then(data => {
        categories.value = data["tags"]
    })
    .catch(error => {
        console.log(error)
    })

</script>

<template>
    <div class="main">
        <h1>Manage Categories</h1>
            <div>
                <div  class="top_action">
                    <Button_ :icon="musicIcon" type="grayscale" size="small" shape="rectangle" label="Add New Category"
                    @click="navigateToAdd()" />
                </div>
            </div>

            <table class="editableTable">
                <tr v-for="category in categories">
                    <td>
                        <div class="song_detail">
                            <div class="song_info">
                                <img :src="category.image ? category.image : sampleImage" class="song_image"/>
                                <span>{{ category.name }}</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="actions">
                                <Button_ :icon="editIcon" type="none" size="small" shape="rectangle" 
                                @click="navigateToEdit(category.id)" />
                                <Button_ :icon="deleteIcon" type="none" size="small" shape="rectangle"
                                @click="deleteCategory(category.id)"/>
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
    align-items: center;
    width: 100%;
    height: fit-content;
    margin: 1rem;
}
.editableTable{
    width: 90%;
}
.editableTable tr{
    display: table-row;
    background-color: var(--back-1);
}
.editableTable td, .editableTable th {
    padding: 0.5rem;
    text-align: center;

}
.top_action{
    margin-bottom: 1rem;
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

</style>