<script setup>
import TextInput_ from '@/components/atomic/TextInput_.vue';
import Button_ from '@/components/atomic/Button_.vue';

import { ref } from 'vue';
import MultiSelect from '@/components/atomic/MultiSelect.vue';

import { useRouter } from 'vue-router';
const router = useRouter()

const categoryName = ref("")
const categoryDescription = ref("")
const categoryImg = ref("https://placehold.co/200x200/398aee/FFF?font=montserrat&text=image")

const songs = ref([])
const selectedSong = ref([])
const songId = ref([])

const tags = ref([])
const selectedTag = ref([])
const tagId = ref([])

fetch(import.meta.env.VITE_BACKEND_URL +  "all_songs", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        for (let i = 0; i < data['songs'].length; i++) {
            songs.value.push(data['songs'][i]['name'])
            songId.value.push(data['songs'][i]['id'])
        }
    })
    .catch(error => {
        console.log(error)
    })


fetch(import.meta.env.VITE_BACKEND_URL +  "all_tags", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        for (let i = 0; i < data['tags'].length; i++) {
            tags.value.push(data['tags'][i]['name'])
            tagId.value.push(data['tags'][i]['id'])
        }
    })
    .catch(error => {
        console.log(error)
    })

const upload = (event) => {
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => categoryImg.value = reader.result
}

const submit = () => {
    let songs = []
    for (let i = 0; i < selectedSong.value.length; i++) {
        songs.push(songId.value[selectedSong.value[i]])
    }
    let tags = []
    for (let i = 0; i < selectedTag.value.length; i++) {
        tags.push(tagId.value[selectedTag.value[i]])
    }
    fetch(import.meta.env.VITE_BACKEND_URL +  "album" ,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    , body: JSON.stringify({
        name: categoryName.value,
        description: categoryDescription.value,
        img: categoryImg.value,
        songs: songs,
        tags: tags
    })} 
    ).then(res => res.json())
    .then(data => {
        if(data['success']) {
            router.push({name: 'studio_albums'})
        }
    })
}

</script>

<template>
    <div class="main">
        <div class="form">
        <h1 class="center">Add Album</h1>
        <TextInput_ label="Name" type="name" size="small" placeholder="Name" @inp="(value) => categoryName = value" /><br />
        <TextInput_ label="Description" type="name" placeholder="Description" size="small" @inp="(value) => categoryDescription = value" /><br />
            <img :src="categoryImg" 
            width="200" height="250" class="preview"/>
            <br />
            <input type="file" class="fileInp" @change="upload($event)"/>
            <br/>

            <MultiSelect :options="songs" label="Select Songs" 
            @selectionChange="(value) => selectedSong = value" 
            /> <br />

            <MultiSelect :options="tags" label="Select Categories" 
            @selectionChange="(value) => selectedTag = value"
            /><br/>

            <Button_ class="submitBtn center" 
            label="Submit" type="bordered" size="small"
             shape="rectangle" @click="submit"/>
        </div>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    align-items: center;
    justify-content: center;
    height: fit-content;
    width: 100%;
    height: fit-content;
    padding: 4rem 0rem;

}

.form {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    outline: 1px dashed var(--back-2);
    min-width: 400px;
    border-radius:8px;
}

.fileInp::-webkit-file-upload-button {
  visibility: hidden;
}

.fileInp::before{
    content: 'Upload Image';
    display: inline-block;
    background-color: var(--back-2);
    padding: 8px 16px;
    border-radius: 4px;
}
.center{
    width:100%;
    text-align: center;
}
.preview{
    border-radius: 8px;
    object-fit: cover;
}
</style>