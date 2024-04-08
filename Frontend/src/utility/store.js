// store.js
import { reactive } from 'vue'

export const store = reactive({
  songId: '-1',
  playing: false,
  seekTime: 0,
  totalTime: 0,
  bufferedTime: 0,
  seekRequestedTime: 0,
  muted : false,
  volume : 100,
  queue : [],
  queueLength : 0,
  currentPlaying : -1,
  addToQueue : (songId) => {
    let idx = store.queue.indexOf(songId)
    if(idx != -1){
      store.currentPlaying = idx
      store.songId = store.queue[store.currentPlaying]
      store.playing = true
    }else{
      store.queue.push(songId)
      store.queueLength = store.queueLength + 1
      store.currentPlaying = store.queueLength - 1
      store.songId = store.queue[store.currentPlaying]
      store.playing = true
    }
  },
  addToQueueFront : (songId) => {
    let idx = store.queue.indexOf(songId)
    if(idx != -1){
      store.currentPlaying = idx
      store.songId = store.queue[store.currentPlaying]
      store.playing = true
    }else{
      store.queue.unshift(songId)
      store.currentPlaying = 0
      store.queueLength = store.queueLength + 1
      store.songId = store.queue[store.currentPlaying]
      store.playing = true
    }
  },
  removeFromQueue : (id) => {
    id = id.toString()
    let index = store.queue.indexOf(id)
    store.queue.splice(index, 1)
    store.queueLength = store.queueLength - 1
    if(store.currentPlaying > index)
      store.currentPlaying = store.currentPlaying - 1
    if(store.songId == id)
      store.songId = store.queue[store.currentPlaying]
  },
  playPrevious : () => {
    store.currentPlaying = store.currentPlaying - 1
    if(store.currentPlaying < 0)
      store.currentPlaying = store.queueLength - 1
    
    store.songId = store.queue[store.currentPlaying]
  },
  playNext : () => {
    store.currentPlaying = store.currentPlaying + 1
    if(store.currentPlaying >= store.queueLength)
      store.currentPlaying = 0
    store.songId = store.queue[store.currentPlaying]
  },
  seek10 : () => {
    store.seekRequestedTime = Math.min(store.seekTime + 10, store.totalTime)
  },
  seekBack10 : () => {
    store.seekRequestedTime = Math.max(store.seekTime - 10, 0)
  }
})

export const appStore = reactive({
  refreshPlaylist : false
})