<script setup>
import CardH_ from '@/components/atomic/CardH_.vue';
import sampleImage from '@/assets/sampleImage.png';

</script>

<template>
    <div class="dashboard">



        <div class="top_stats">

            <div class="stat_cards">
                <div class="stat">
                    <div>Total</div>
                    <div>Jan</div>
                    <div>Febraury</div>
                    <div>1.1K</div>
                    <div>10</div>
                    <div>10</div>
                </div>
                <div>
                    songs
                </div>
            </div>

            <div class="stat_cards">
                <div class="stat">
                    <div>Total</div>
                    <div>Jan</div>
                    <div>Febraury</div>
                    <div>1.1K</div>
                    <div>10</div>
                    <div>10</div>
                </div>
                <div>
                    albums
                </div>
            </div>

        </div>

        <div class="graphs_">
            <div> Song Stats - A bar Graph </div>
            <div> Album Stats - A bar Graph </div>
            <div>Song popularity Stats - A Line graph </div>
        </div>        
        
        <div class="top_stats">
            <div class="stat_cards2">
                <CardH_ class="hcard" label="Looking for Love" artist="Henry, Arthur" :image="sampleImage" />
                <CardH_ class="hcard" label="Looking for Love" artist="Henry, Arthur" :image="sampleImage" />
                <div>
                    Most Played Songs
                </div>
            </div>

            <div class="stat_cards2">
                <CardH_ class="hcard" label="Looking for Love" artist="Henry, Arthur" :image="sampleImage" />
                <CardH_ class="hcard" label="Looking for Love" artist="Henry, Arthur" :image="sampleImage" />
                <div>
                    Most Played Album
                </div>
            </div>

        </div>


    </div>
</template>

<style scoped>
.top_stats {
    display: flex;
    flex-direction: row;
    padding: 1rem;
}

.dashboard {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

.stat_cards {
    display: flex;
    flex-direction: column;
    border-radius: 8px;
    align-items: center;
    padding: 0px 20px;
    margin: 2%;
    outline: 1px dashed var(--back-2);
    background-color: var(--back-1);
}

.stat_cards>div {
    margin: 10px;
}

.stat_cards .stat {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    column-gap: 20px;
}

.stat_cards2 {
    width: fit-content;
    display: flex;
    flex-direction: column;
    border-radius: 8px;
    align-items: center;
    padding: 0px 20px;
    margin: 2%;
    outline: 1px dashed var(--back-2);
    background-color: var(--back-1);
}

.stat_cards2>div {
    margin: 15px;
}
</style>