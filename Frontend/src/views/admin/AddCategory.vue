<script setup>
import TextInput_ from '@/components/atomic/TextInput_.vue';
import Button_ from '@/components/atomic/Button_.vue';
import sampleImage from '@/assets/sampleImage.png';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter()

const categoryName = ref("")
const categoryImg = ref(sampleImage)

const upload = (event) => {
    // get the file from the event
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => categoryImg.value = reader.result
}

const submit = () => {
    fetch(import.meta.env.VITE_BACKEND_URL +  "tags", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        },
        body: JSON.stringify({
            name: categoryName.value,
            image: categoryImg.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data['success']){
            router.push({name: "admin_categories"})
        }
    })
}

</script>

<template>
    <div class="main">
        <div class="form">
        <h1 class="center">Add Category</h1>
        <TextInput_ label="Category Name" type="name" size="small" @inp="(value) => categoryName = value" />
            <br />
            <img :src="categoryImg" 
            width="200" height="250" class="preview"/>
            <br />
            <input type="file" class="fileInp" @change="upload($event)"/>
            <br/>
            <br/>
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
    height: 100%;
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