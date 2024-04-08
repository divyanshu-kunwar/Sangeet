<script setup>
import TextInput_ from '@/components/atomic/TextInput_.vue';
import Button_ from '@/components/atomic/Button_.vue';

import { ref } from 'vue';

const profileName = ref("")
const profileImg = ref("")
const id = ref("")

const oldPassword = ref("")
const newPassword = ref("")

const haveUserRole = ref("")
const isCreator = ref("")

// 
fetch(import.meta.env.VITE_BACKEND_URL +  "user", {
    method: "GET",
    headers: {
        "Authorization" : localStorage.getItem("token"),
        "Content-Type": "application/json"
    }
})
    .then(response => response.json())
    .then(data => {
        profileName.value = data["name"]
        id.value = data["id"]
        console.log(data["role"])
        if(data.role == "Admin" || data.role == "Creator"){
            haveUserRole.value = false;
        }else{
            haveUserRole.value = true;
        }
        profileImg.value = data["image"]
        if(!data["image"]){
            profileImg.value="https://picsum.photos/200?random=1"
        }
    })
    .catch(error => {
        console.log(error)
    })

function editProfile(){
    fetch(import.meta.env.VITE_BACKEND_URL +  "user", {
    method: "PUT",
    headers: {
        "Authorization" : localStorage.getItem("token"),
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: profileName.value,
        image: profileImg.value,
        isCreator: isCreator.value
    })
    }).then(response => response.json())
    .then(data => {
        console.log(data)
        if(data["success"])
            window.alert("updated successfully")
        else
            console.log(data)
    }).catch(error => {
        console.log(error)
    })
}

function updatePass(){
    fetch(import.meta.env.VITE_BACKEND_URL +  "user", {
    method: "PUT",
    headers: {
        "Authorization" : localStorage.getItem("token"),
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        oldPassword: oldPassword.value,
        newPassword: newPassword.value
    })
    }).then(response => response.json())
    .then(data => {
        console.log(data)
        if(data["success"])
            window.alert("updated successfully")
        else
            console.log(data)
    }).catch(error => {
        console.log(error)
    })
}
const upload = (event) => {
    // get the file from the event
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => profileImg.value = reader.result
}
</script>

<template>
    <div class="main">
        <div class="form">
            <h1 class="center">Edit Profile</h1>
            <img :src="profileImg" width="200" height="250" class="preview" />
            <br />
            <input type="file" class="fileInp" @change="upload($event)" />
            <br />
            <br />
            <TextInput_ label="Name" :initialValue="profileName" type="name" size="small"
                @inp="(value) => profileName = value" />
            <br />

            <div class="artist" v-if="haveUserRole" >
                    <input class="cursor" id="check" type="checkbox" v-model="isCreator"/>
                    <label class="cursor" for="check">Register As an Artist</label>
            </div>

            <br />
            <Button_ class="submitBtn center" label="Update Profile" type="bordered" size="small" shape="rectangle"
                @click="editProfile" />
        </div>

        <div class="form">
            <TextInput_ label="Current Password" size="small" type="password"
                @inp="(value) => oldPassword = value" />
            <br />
            <TextInput_ label="New Password"  size="small" type="password"
                @inp="(value) => newPassword = value" />
            <br />
            <Button_ class="submitBtn center" label="Update Password" type="bordered" size="small" shape="rectangle"
                @click="updatePass" />
        </div>


    </div>
</template>

<style scoped>
.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: fit-content;
    width: 100%;
    height: fit-content;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.form {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    outline: 1px dashed var(--back-2);
    min-width: 400px;
    border-radius: 8px;
}

.fileInp::-webkit-file-upload-button {
    visibility: hidden;
}

.fileInp::before {
    content: 'Upload Profile Picture';
    display: inline-block;
    background-color: var(--back-2);
    padding: 8px 16px;
    border-radius: 4px;
}

.center {
    width: 100%;
    text-align: center;
}

.preview {
    width: 150px;
    height: 150px;
    align-self: center;
    border-radius: 50%;
    object-fit: cover;
}
</style>