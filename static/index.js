/*
    TODO:
        Give purpose of this file:
            - This will be for user language. (at least on <main> tag)
              Give users feature to choose between Serbian and English.
*/

const vm = new Vue({
    el: '#vm',
    delimiters: ['${', '}'],
    data: {
        tekst: 'cao narode od Vue!'
    }
});