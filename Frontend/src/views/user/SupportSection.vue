<script setup>
    import { ref } from 'vue'
    const expanded = ref(0)
    const support = ref([
        {
            "Question" : "How To Play Song or Album ?",
            "Answer" : "Hover and Clicke over the Song or Album to play it."

        },
        {
            "Question" : "Question 2",
            "Answer" : "Answer 2"
        },
        {
            "Question" : "Question 3",
            "Answer" : "Answer 3"
        }
    ])

</script>
<template>
    <div>
        <h1>
            Support
        </h1>

        <div class="answer_list">
            <div class="qanswer" v-for="(question, idx) in support">
                <div class="question"
                @click="expanded = expanded = idx"
                >{{ question.Question }}</div>
                <p :class="expanded==idx ? 'answer' : 'answerCollapsed'">
                    {{ question.Answer }}</p>
            </div>
        </div>
    </div>
</template>
<style scoped>
.qanswer{
    width: 100%;
    padding: 2rem 2rem;
    margin-bottom: 4px;
    background-color: var(--back-0);
    border-radius: 4px;
}
.answer_list{
    display: flex;
    flex-direction: column;
    margin-top: 2rem;
}
.question{
    font-size: large;
}
.answer{
    margin-top: 1rem;
    height: fit-content;
    transition: all 1s ease-in-out;
    color: var(--fore-1);
}
.answerCollapsed{
    padding: 0px;
    margin: 0rem;
    height: 0px;
    overflow: hidden;
    transition: all 1s ease-in-out;
    color: var(--shade);
}
h1{
    width: 100%;
    text-align: center;
    margin: 0px;
}
</style>