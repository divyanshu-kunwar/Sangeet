<script setup>

import { ref } from 'vue';
import deleteIcon from '@/assets/dismiss.svg'
import Button_ from '@/components/atomic/Button_.vue';

const notifications = ref({})

fetch(import.meta.env.VITE_BACKEND_URL +  "notifications", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    }
})
    .then(response => response.json())
    .then(data => {
        notifications.value = data['notifications']
        for (let i = 0; i < notifications.value.length; i++) {
            notifications.value[i]["message"] = JSON.parse(notifications.value[i]["message"])
            notifications.value[i]["collapsed"] = true
        }
    })
    .catch(error => {
        console.log(error)
    })

function deleteNotification(id){
    fetch(import.meta.env.VITE_BACKEND_URL +  "notifications?id=" + id, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": localStorage.getItem("token")
        }
    })
        .then(response => response.json())
        .then(data => {
            if(data['success'])
                notifications.value = notifications.value.filter(notification => notification['id'] != id)
        })
        .catch(error => {
            console.log(error)
        })
}

</script>

<template>
    <div class="notification_list">
        
        <h1>Notifications</h1>

        <div class="notification" v-for="notification in notifications" 
        @click="notification['collapsed'] = !notification['collapsed']">
            <div class="notification_data">
                <div class="notification_meta">
                    <span class="created_at">
                        {{ notification["created_at"] }}
                    </span>
                    <Button_ :icon="deleteIcon" size="small" shape="circle" 
                    type="none" @click="deleteNotification(notification['id'])"/>
                </div>
                <span class="subject">
                    {{ notification["message"]["Subject"] }}
                </span>
            </div>
            <p :class="notification['collapsed'] ? 'html_content' : 'html_content_exp' " v-html="notification['message']['html']"></p>
        </div>

    </div>
</template>

<style scoped>
.notification_list {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 2rem;
}

.notification {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    max-width: 900px;
    background-color: var(--back-1);
    border-radius: 2px;
    margin-bottom: 2px;
    overflow-y: hidden;
}


.notification_data{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    padding: 2rem;
    background-color: var(--back-2);
}
.subject{
    color: var(--fore-2);
    margin-top: 4px;
}
.created_at{
    align-self: flex-start;
}
.html_content{
    width: 100%;
    height: 0px;
    margin: 0px;
    overflow-y: hidden;
}
.html_content_exp{
    width: 100%;
    display: flex;
    height: fit-content;
}
.html_content_exp::v-deep table{
    margin-left: auto;
    margin-right: auto;
}
.html_content_exp::v-deep img{
    max-width: 100px;
    border-radius: 4px;
}
.html_content_exp::v-deep td{
    padding: 8px 20px;
    text-align: center;
    font-size: small;
}
.notification_meta{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.notification_meta > div{
    margin-top: -25px;
    margin-right: -25px;
    margin-bottom: 10px;
}
</style>
