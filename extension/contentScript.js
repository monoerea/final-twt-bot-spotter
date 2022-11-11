(() => {

    let currentTimeline = ""

    // Reads Timeline Tweets
    let readTimeline = () => {
        let screen_name = document.querySelectorAll(['div.css-1dbjc4n div > div > div > div > div > div > div > div > div > div > div > div > a > div > span'])
        screen_name = Array.prototype.map.call(screen_name, ((t) => { return t.textContent }))

        let datetime = document.querySelectorAll(['a > time[datetime]'])
        datetime = Array.prototype.map.call(datetime, ((t) => { return t.getAttribute('datetime') }))

        let screen_name_datetime = []
        screen_name.forEach((item, index) => {
            screen_name_datetime[index] = {
                "screen_name" : item,
                "datetime" : datetime[index]
            }
        })


        // Creates File For 
        let textFile = null
        let makeTextFile = (text) => {
            let data = new Blob([text], {type: 'application/JSON'});

            // If we are replacing a previously generated file we need to
            // manually revoke the object URL to avoid memory leaks.
            if (textFile !== null) {
                window.URL.revokeObjectURL(textFile);
            }

            textFile = window.URL.createObjectURL(data);

            // returns a URL you can use as a href
            return textFile;
        }

        let json = JSON.stringify(screen_name_datetime)
        makeTextFile(json)
    }


    // Communicates with background.js
    chrome.runtime.onMessage.addListener((obj, sender, response) => {
        let { type, value, timeline } = obj

        // if type of event is new _ loaded
        if(type === "NEW") {
            // set current _ to 
            currentTimeline = timeline
            readTimeline()
        }
    })

    // Select Timeline
    let timeline_tweets = document.querySelector('section.css-1dbjc4n')


    // Observe Timeline Mutations
    let timelineObserver = new MutationObserver(readTimeline())

    // Observes Timeline's divs
    timelineObserver.observe(timeline_tweets, {
        subtree: true
    });

    timelineObserver.disconnect()

    fetch('./data.json')
        .then((response) => response.json())
        .then((json) => console.log(json))

})();