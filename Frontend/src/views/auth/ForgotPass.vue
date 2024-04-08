<template>
    <Outer>

        <div id="LoginPage">
            <img id="illu" :src="illustration" />

            <div class="card">

                <!-- -------------------------- entering details --------------------------------------------------- -->
                <TextInput_ v-if="form_state == 'entering'" class="inputs" label="Email" type="name" size="large"
                    placeholder="user@mail.com" @inp="(value) => emailInput = value" />
                <Button_ v-if="form_state == 'entering'" class="loginBtn" label="Submit" type="bordered" size="small"
                shape="rectangle" @click="requestOTP"/>

                <!-- -------------------------- processing --------------------------------------------------- -->
                <h5 v-if="form_state == 'processing'"> Just Hold On! We are Verifying your account details.</h5>

                <!-- -------------------------- detail wrong failed --------------------------------------------------- -->
                <h5 v-if="form_state == 'failed'">
                    <pre>{{ message }}</pre>
                    🤗 Not a problem you can always retry with correct input.<br />
                </h5>
                <Button_ v-if="form_state == 'failed'" class="registerBtn" label="Retry" type="bordered" size="small"
                    shape="rectangle" @click="retry" />
                <br />

                <!-- -------------------------- OTP sent --------------------------------------------------- -->
                <h5 v-if="form_state == 'otp_sent'">We have sent a Mail to {{ emailInput }}</h5>
                <TextInput_ v-if="form_state == 'otp_sent'" class="inputs" label="OTP" type="password" size="large"
                    placeholder="********" @inp="(value) => OTPInput = value" />
                <TextInput_ v-if="form_state == 'otp_sent'" class="inputs" label="New Password" type="password" size="large"
                    placeholder="********" @inp="(value) => passwordInput = value" />
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

import { useRouter } from 'vue-router';
const router = useRouter();

import { ref } from 'vue';
const emailInput = ref("")
const passwordInput = ref("")
const OTPInput = ref("")

const message = ref("")

// entering, processing, failed , otp_sent, processing_otp, otp_wrong
const form_state = ref("entering") 

function requestOTP(){

    form_state.value = 'processing'
    let url = import.meta.env.VITE_BACKEND_URL +  "request_otp" 
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: emailInput.value
        })
    })
        .then(response => response.json())
        .then(data => {
            form_state.value = data["success"] ? 'otp_sent' : 'failed'
            message.value = data["message"]
        })
        .catch(error => {
            form_state.value = 'failed'
            message.value = "❌ System error could not send otp \n"
            console.log(error)
        })

}

function retry() {
    form_state.value = 'entering'
}

function otp_submit(){

form_state.value = 'processing_otp'
let url = import.meta.env.VITE_BACKEND_URL +  "verify_otp2"
fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        email: emailInput.value,
        code: OTPInput.value,
        password: passwordInput.value
    })
})
    .then(response => response.json())
    .then(data => {
        form_state.value = data["success"] ? 'processing_otp' : 'otp_wrong'
        message.value = data["message"]
        if(data["success"]){
            localStorage.setItem("token", data["token"])
            rou
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

</script>

<style scoped>
#LoginPage {
    display: flex;
    align-items: center;
    justify-content: center;
}

#illu{
    margin-right: 5%;
    height: min(60vh, 50vw);
    opacity: 0.8;
}

.card {
    display: flex;
    flex-direction: column;
    padding: 4rem 2rem 2rem 2rem;
    margin: 2rem;
    border: 1px dashed var(--back-2);
    border-radius: 0.5rem;
    width: 400px;
    height: fit-content;
}

a{
    display: block;
    margin: 4px;
    margin-bottom: 1.5rem;
    color: var(--fore-0);
}

a:hover {
    opacity: 1;
    color: var(--shade);
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

@media screen and (max-width: 1200px) {
    #LoginPage{
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