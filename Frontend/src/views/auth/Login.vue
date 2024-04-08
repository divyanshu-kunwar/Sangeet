<template>
    <Outer>

        <div id="LoginPage">
            <img id="illu" :src="illustration" />

            <div class="card">

                <!-- -------------------------- entering details --------------------------------------------------- -->
                <TextInput_ v-if="form_state == 'entering'" class="inputs" label="Email" type="name" size="large"
                    placeholder="user@mail.com" @inp="(value) => emailInput = value" />
                <TextInput_ v-if="form_state == 'entering'" class="inputs" label="Password" type="password" size="large" placeholder="********"
                    @inp="(value) => passwordInput = value" />
                <div  v-if="form_state == 'entering'">
                    <router-link to="/forgot-password">Forgot Password ? Reset</router-link>
                </div>
                <Button_ v-if="form_state == 'entering'" class="loginBtn" label="Login" type="bordered" size="small"
                shape="rectangle" @click="login"/>

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
                <Button_ v-if="form_state == 'failed'" class="registerBtn" label="Forget Password?" type="bordered"
                size="small" @click="forgot_password" shape="rectangle" />

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
const router = useRouter()

import { ref } from 'vue';
const emailInput = ref("")
const passwordInput = ref("")
const message = ref("")

// entering, processing, failed
const form_state = ref("entering") 

function login() {
    form_state.value = 'processing'
    let url = import.meta.env.VITE_BACKEND_URL +  "login"
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: emailInput.value,
            password: passwordInput.value
        })
    })
        .then(response => response.json())
        .then(data => {
            form_state.value = data["success"] ? 'processing' : 'failed'
            message.value = data["message"]
            if(data["success"]){
                localStorage.setItem("token", data["token"])
                router.push({ name: 'app' })
            }
        })
}
function retry() {
    form_state.value = 'entering'
}

function forgot_password() {
    window.location.href = '/forgot-password'
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
    width: min(400px , 100%);
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