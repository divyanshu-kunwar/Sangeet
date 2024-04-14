<template>
    <Outer>

        <div id="registerPage">
            <img id="illu" :src="illustration" />

            <div class="card">

                <!-- -------------------------- entering details --------------------------------------------------- -->
                <TextInput_ v-if="form_state == 'entering'" class="inputs" label="Name" type="name" size="large"
                placeholder="Your Name" @inp="(value) => nameInput = value" />
                <TextInput_ v-if="form_state == 'entering'" class="inputs" label="Email" type="name" size="large"
                placeholder="user@mail.com" @inp="(value) => emailInput = value" />
                <TextInput_ v-if="form_state == 'entering'" class="inputs" label="Password" type="password" size="large"
                placeholder="********" @inp="(value) => passwordInput = value" />

                <input v-if="form_state == 'entering'" type="file" class="fileInp" @change="upload($event)"/>
                <br />

                <div v-if="form_state == 'entering'" class="artist">
                    <input class="cursor" id="check" type="checkbox" v-model="registerAsCreator" />
                    <label class="cursor" for="check">Register As an Artist</label>
                </div>
                <Button_ v-if="form_state == 'entering'" class="registerBtn" label="Register" type="bordered" size="small"
                    shape="rectangle" @click="register" />


                <!-- -------------------------- processing --------------------------------------------------- -->
                <h5 v-if="form_state == 'processing'"> Just Hold On! We are creating your account.</h5>


                <!-- -------------------------- detail wrong failed --------------------------------------------------- -->
                <h5 v-if="form_state == 'failed'">
                    <pre>{{ message }}</pre>
                    🤗 Not a problem you can always retry with correct input.<br />
                </h5>
                <Button_ v-if="form_state == 'failed'" class="registerBtn" label="Retry" type="bordered" size="small"
                    shape="rectangle" @click="retry" />


                <!-- -------------------------- OTP sent --------------------------------------------------- -->
                <h5 v-if="form_state == 'otp_sent'">We have sent a Mail to {{ emailInput }}</h5>
                <TextInput_ v-if="form_state == 'otp_sent'" class="inputs" label="OTP" type="password" size="large"
                    placeholder="********" @inp="(value) => OTPInput = value" />
                <Button_ v-if="form_state == 'otp_sent'" class="registerBtn" label="Submit" type="bordered" size="small"
                    shape="rectangle" @click="otp_submit" />

                <!-- -------------------------- processing otp --------------------------------------------------- -->
                    <h5 v-if="form_state == 'processing_otp'"> Just Hold On! We are verifying OTP.</h5>


                <!-- -------------------------- OTP wrong ------------------------------------------------------ -->
                <h5 v-if="form_state == 'otp_wrong'">
                    ❌ Oh! no that's a wrong OTP <br />
                    🤗 Not a problem you can always retry.<br />
                </h5>
                <Button_ v-if="form_state == 'otp_wrong'" class="registerBtn" label="Re-Enter OTP" type="bordered"
                    size="small" @click="otp_retry" shape="rectangle" />
                <br />
                <Button_ v-if="form_state == 'otp_wrong'" class="registerBtn" label="Wrong Email?" type="bordered"
                    size="small" @click="retry" shape="rectangle" />

            </div>

        </div>

    </Outer>
</template>

<script setup>

import Outer from '@/components/molecular/Outer.vue';
import illustration from "@/assets/LoginIllu.png"
import TextInput_ from '@/components/atomic/TextInput_.vue';
import Button_ from '@/components/atomic/Button_.vue';

import { ref } from 'vue';

import { useRouter } from 'vue-router';
const router = useRouter();

const nameInput = ref("")
const emailInput = ref("")
const passwordInput = ref("")
const registerAsCreator = ref(false)
const OTPInput = ref("")
const image = ref("")

const message = ref("")



// processing , failed , otp_sent , otp_wrong
const form_state = ref("entering") 

function register() {
    form_state.value = 'processing';
    let url = import.meta.env.VITE_BACKEND_URL +  "register"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: nameInput.value,
            email: emailInput.value,
            password: passwordInput.value,
            role: registerAsCreator.value ? 'creator' : 'user',
            image: image.value
        })
    })
        .then(response => response.json())
        .then(data => {
            form_state.value = data["success"] ? 'otp_sent' : 'failed'
            message.value = data["message"]
        })
        .catch(error => {
            form_state.value = 'failed'
            message.value = "❌ System error could not create user \n"
            console.log(error)
        })

}

function retry() {
    form_state.value = 'entering'
}

function otp_submit(){

    form_state.value = 'processing_otp'
    let url = import.meta.env.VITE_BACKEND_URL +  "verify_otp"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: emailInput.value,
            code: OTPInput.value
        })
    })
        .then(response => response.json())
        .then(data => {
            form_state.value = data["success"] ? 'otp_sent' : 'otp_wrong'
            message.value = data["message"]
            if(data["success"]){
                console.log(data["token"])
                localStorage.setItem("token", data["token"])
                router.push({ name: 'app' })
            }
        })
        .catch(error => {
            form_state.value = 'otp_wrong'
            message.value = "❌ System error could not verify otp \n"
            console.log(error)
        })

}

function otp_retry() {
    form_state.value = 'otp_sent'
}

const upload = (event) => {
    const file = event.target.files[0]
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => image.value = reader.result
}

</script>

<style scoped>
#registerPage {
    display: flex;
    align-items: center;
    justify-content: center;
}

#illu {
    margin-right: 5%;
    height: min(60vh, 50vw);
    opacity: 0.8;
}

.card {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    margin: 2rem;
    border: 1px dashed var(--back-2);
    border-radius: 0.5rem;
    width: min(400px , 100%);
    height: fit-content;
}

.artist {
    display: block;
    margin: 4px;
    margin-bottom: 1.5rem;
    color: var(--fore-0);
}

.artist:hover {
    opacity: 1;
    color: var(--shade);
}

.artist>label {
    font-size: large;
}

.artist>input {
    margin-right: 0.5rem;
    font-size: large;
    width: 15px;
    height: 15px;
    background-color: var(--back-1);
    color: var(--back-1);
}

.inputs {
    width: 100%;
    margin-bottom: 1.5rem;
}

.registerBtn {
    align-self: start;
    width: 100%;
}

pre{
    font-size: inherit;
    font-weight: inherit;
    font-family: inherit;
}

.fileInp::-webkit-file-upload-button {
  visibility: hidden;
}

.fileInp::before{
    content: 'Upload Profile Picture';
    display: inline-block;
    background-color: var(--back-2);
    padding: 8px 16px;
    border-radius: 4px;
}
@media screen and (max-width: 1200px) {
    #registerPage{
        flex-direction: column-reverse;
    }
    #illu{
        max-width: 80vw;
    }
    .card{
        padding: 8%;
        margin: 2rem 0px;
    }
}
</style>