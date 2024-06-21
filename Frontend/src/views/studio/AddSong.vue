<script setup>
import TextInput_ from '@/components/atomic/TextInput_.vue';
import Button_ from '@/components/atomic/Button_.vue';
import MultiSelect from '@/components/atomic/MultiSelect.vue';
import sampleImage from "@/assets/sampleImage.png"

import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter()

const songName = ref("")
const songImg = ref(sampleImage)
// audio sample
const audio = ref("")
let audioFile = ref(null)

const artists = ref([])
const selectedArtist = ref([])
const artistId = ref([])

fetch(import.meta.env.VITE_BACKEND_URL +  "all_creators", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        for (let i = 0; i < data['artists'].length; i++) {
            artists.value.push(data['artists'][i]['name'])
            artistId.value.push(data['artists'][i]['id'])
        }
    })
    .catch(error => {
        console.log(error)
    })

const tags = ref([])
const selectedTag = ref([])
const tagId = ref([])

const lyrics = ref("")
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
    reader.onload = () => songImg.value = reader.result
}
const uploadAudio = (event) => {
    // get the file from the event
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => audio.value = reader.result
    audioFile = event.target.files[0]
}

const submit = () => {
    let artists = []
    for (let i = 0; i < selectedArtist.value.length; i++) {
        artists.push(artistId.value[selectedArtist.value[i]])
    }
    console.log(artists)

    let tags = []
    for (let i = 0; i < selectedTag.value.length; i++) {
        tags.push(tagId.value[selectedTag.value[i]])
    }

    const formData = new FormData();
    formData.append('name', songName.value);
    formData.append('image', songImg.value);
    formData.append('audio', audioFile) // Access the file from the input element
    formData.append('artists', JSON.stringify(artists))
    formData.append('tags', JSON.stringify(tags));
    formData.append('lyrics', lyrics.value);

    fetch(import.meta.env.VITE_BACKEND_URL +  "songs", {
        method: "POST",
        headers: {
            "Authorization": localStorage.getItem("token")
        },
        body: formData // Use FormData object for handling file uploads
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            router.push({ name: 'studio_songs' })
        })
        .catch(error => {
            console.error("Error:", error);
        });

}

</script>

<template>
    <div class="main">
        <h1 class="center">Add Song</h1>
        <div class="form">
            <div class="column">
                <!-- TODO multi select artists -->
                <TextInput_ label="Song Name" type="name" size="small" @inp="(value) => songName = value" /><br />

                <img :src="songImg" width="200" height="250" class="preview" />
                <br />

                <input type="file" class="fileInp Inp1" @change="upload($event)" /><br /><br />

                <audio controls :src="audio"></audio> <br />
                <input type="file" class="fileInp Inp2" @change="uploadAudio($event)" /><br />
            </div>
            <div class="column">
                <MultiSelect :options="artists" label="Select Artist"
                    @selectionChange="(value) => selectedArtist = value" /> <br />

                <MultiSelect :options="tags" label="Select Categories"
                    @selectionChange="(value) => selectedTag = value" /> <br />

                <textarea spellcheck="false" class="lyricsbox" rows="5" placeholder="Lyrics"
                    v-model="lyrics"> </textarea>

                <Button_ class="submitBtn center" label="Submit" type="bordered" size="small" shape="rectangle"
                    @click="submit" />

            </div>
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
}

.form {
    display: flex;
    flex-direction: row;
    padding: 2rem;
    outline: 1px dashed var(--back-2);
    min-width: 400px;
    border-radius: 8px;
}

.column {
    display: flex;
    flex-direction: column;
    margin: 2cap;
}

.fileInp::-webkit-file-upload-button {
    visibility: hidden;
}

.fileInp::before {
    display: inline-block;
    background-color: var(--back-2);
    padding: 8px 16px;
    border-radius: 4px;
}

.Inp1::before {
    content: 'Upload Image';
}

.Inp2::before {
    content: 'Upload Audio';
}

.center {
    width: 100%;
    text-align: center;
}

.preview {
    border-radius: 8px;
    object-fit: cover;
}

.lyricsbox {
    width: 100%;
    background-color: var(--back-1);
    color: var(--fore-1);
    border-radius: 4px;
    margin-bottom: 1rem;
    outline: none;
    border: none;
    resize: none;
    padding: 1rem;
}

.lyricsbox::-webkit-scrollbar {
    width: 5px;
}

/* Track */
.lyricsbox::-webkit-scrollbar-track {
    box-shadow: inset 0 0 5px var(--fore-2);
    border-radius: 5px;
}

/* Handle */
.lyricsbox::-webkit-scrollbar-thumb {
    background: var(--gradient);
    border-radius: 5px;
}
</style>