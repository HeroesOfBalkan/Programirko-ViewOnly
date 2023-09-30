var vidPage = new Vue({
    el: '#vid_pg',
    delimiters: ['${', '}'],
    data: {
        search: [],

        recommend: [
            [
                {
                    channelID: "load",
                    channelName: "load",
                    desc: "load",
                    thumbnailURL: "load",
                    videoID: "load",
                    videoTitle: "load"
                },
            ],
            [
                {
                    channelID: "load",
                    channelName: "load",
                    desc: "load",
                    thumbnailURL: "load",
                    videoID: "load",
                    videoTitle: "load"
                },
            ],
            [
                {
                    channelID: "load",
                    channelName: "load",
                    desc: "load",
                    thumbnailURL: "load",
                    videoID: "load",
                    videoTitle: "load"
                },
            ],
            [
                {
                    channelID: "load",
                    channelName: "load",
                    desc: "load",
                    thumbnailURL: "load",
                    videoID: "load",
                    videoTitle: "load"
                },
            ],
            [
                {
                    channelID: "load",
                    channelName: "load",
                    desc: "load",
                    thumbnailURL: "load",
                    videoID: "load",
                    videoTitle: "load"
                }
            ]
        ],

        rs: []
    },

    

    methods: {
        searchYt: function () {
            const search = document.getElementById('srch').value;
            fetch('/yts/' + search)
                .then(response => response.json())  
                .then(json => {
                    console.log(json);
                    this.search = json;
                });
        }
    },

    created: function() {
        fetch('/recm')
            .then(response => response.json())
            .then(json => {
                this.rs = json;
            })
            .catch(error => console.error(error));

        fetch('/recm_list')
            .then(response => response.json())
            .then(thing => {
                this.recommend = thing;
            }).catch(error => console.error(error));
    }
})