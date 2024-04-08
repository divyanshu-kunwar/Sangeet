<script setup>
import Button_ from '@/components/atomic/Button_.vue';
import Card_ from '@/components/atomic/Card_.vue';
import CardH_ from '@/components/atomic/CardH_.vue';
import sampleIcon from '@/assets/sIcon.svg'
import sampleImage from '@/assets/sampleImage.png'
import CircularWaves_ from '@/components/atomic/CircularWaves_.vue';
import TextInput_ from '@/components/atomic/TextInput_.vue';
import { ref } from 'vue';

const nameInput = ref("")

</script>

<template>
    <div id="comp">

        <h1>Here Goes All Components</h1>
        <div id="grid">
            <!-----------------------   Button  --------------------------------->
            <div class="subV">
                <pre>
                <code>
        {{ `<Button_ 
        label="" :icon=""
        type="filled | bordered | grad-filled | 
        grad-bordered | none | grayscale"
        size="small | large"  
        shape="rectangle | circle"/>`}}
                </code>
                </pre>

                <Button_ :icon="sampleIcon" type="none" size="small" shape="circle" />
                <Button_ :icon="sampleIcon" type="grayscale" size="small" shape="circle" />
                <Button_ :icon="sampleIcon" type="none" size="large" shape="circle" />
                <Button_ :icon="sampleIcon" type="grayscale" size="large" shape="circle" />
                <Button_ :icon="sampleIcon" type="bordered" size="large" shape="circle" />
                <Button_ :icon="sampleIcon" type="bordered" size="small" shape="circle" />
                <Button_ :icon="sampleIcon" type="filled" size="small" shape="circle" />
                <Button_ :icon="sampleIcon" type="filled" size="large" shape="circle" />
                <Button_ label="Hello World" type="none" size="small" shape="rectangle" />
                <Button_ label="Hello World" type="none" size="large" shape="rectangle" />
                <Button_ label="Hello World" type="grayscale" size="small" shape="rectangle" />
                <Button_ label="Hello World" type="grayscale" size="large" shape="rectangle" />
                <Button_ label="Hello World" type="bordered" size="small" shape="rectangle" />
                <Button_ label="Hello World" type="bordered" size="large" shape="rectangle" />
                <Button_ :icon="sampleIcon" label="Hello World" type="grayscale" size="small" shape="rectangle" />
                <Button_ label="Hello World" type="filled" size="small" shape="rectangle" />
                <Button_ label="Hello World" type="gradient" size="small" shape="rectangle" />
                <Button_ label="Hello World" type="filled" size="large" shape="rectangle" />
                <Button_ :icon="sampleIcon" label="Hello World" type="filled" size="small" shape="rectangle" />

            </div>

            <!-----------------------   Song Cards  --------------------------------->
            <div class="subV">
                <pre>
                <code>
        {{ `<Cards_ 
        label="" artist="" :image="" 
        songid=""/>`}}
                </code>
                </pre>
                <Card_ label="Looking For Love" artist="Miles , Esther" :image="sampleImage" href=""/>

                <Card_ label="Lorem lpsum" artist="Esto , Lovonio" :image="sampleImage" href=""/>

                <Card_ label="Lorem lpsum" artist="Esto , Lovonio" :image="sampleImage" href=""/>

            </div>

            <!-----------------------   Horizontal Cards  --------------------------------->
            <div class="subV">
                <pre>
                <code>
        {{ `<CardH_ label=""
        artist=""
        :image=""
        />` }}
                </code>
                </pre>

                <CardH_ label="Looking for Love" artist="Henry, Arthur" :image="sampleImage" />
            </div>

            <!-----------------------   Music Player  --------------------------------->
            <div class="subV">
                <pre>
                <code>
        {{ `<CircularWaves_  themecolor="" />` }}
                </code>
                </pre>

                <!-- <CircularWaves_ /> -->

            </div>

            <!-----------------------   Input Box   --------------------------------->
            <div class="subV">
                <pre>
                <code>
        {{ `<TextInput_  
        label=""
        type="name| password| number| email"
        size="small| large"
        @input="(value) => nameInput = value"
        />`}}
                </code>
                </pre>
                <TextInput_ label="name" type="name" size="small" @input="(value) => nameInput = value" />
                <TextInput_ label="password" type="password" size="small" />
                <TextInput_ label="number" type="number" size="small" />
                <TextInput_ label="email" type="email" />
                <TextInput_ label="name" type="name" size="large" />
                <TextInput_ label="password" type="password" size="large" />
                <TextInput_ label="number" type="number" size="large" />
            </div>

            <!-----------------------   Drop Up  --------------------------------->
            <!-----------------------   Queue/Playlist List Item  --------------------------------->
            <!-----------------------   Playlist Card  --------------------------------->
            <!-----------------------   Queue Card  --------------------------------->
            <!-----------------------   Subscription Card  --------------------------------->

            <!-----------------------  Slider  --------------------------------->
            <!-----------------------  Timer  --------------------------------->
            <!-----------------------  Volume Knob  --------------------------------->

            <!-----------------------  Text Input  --------------------------------->
            <!-----------------------  Select Input  --------------------------------->

        </div>

    </div>
</template>

<style scoped>
#comp {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

#grid {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    column-gap: 10px;
    padding: 20px;
}

.subV {
    max-width: 600px;
    min-width: 200px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    column-gap: 20px;
    border: 1px solid var(--primary);
    padding: 10px;
    align-items: center;
    justify-content: flex-start;
}

.subV>* {
    margin: 10px;
}

pre {
    display: block;
    width: 100%;
}
</style>