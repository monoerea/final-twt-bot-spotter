// get Twitter Username
/*let screen_name = document.querySelectorAll(['div.css-1dbjc4n div > div > div > div > div > div > div > div > div > div > div > div > a > div > span'])
screen_name = Array.prototype.map.call(screen_name, ((t) => { return t.textContent; }))*/
let screen_name = document.querySelector(['div.css-1dbjc4n div > div > div > div > div > div > div > div > div > div > div > div > a > div > span']).textContent

// get datetime of tweet in UTC format
let time = document.querySelector(['time[datetime]']).getAttribute('datetime')

// get entire tweet
let tweet = document.querySelector(['article[data-testid=tweet]'])
//does not work for some reason
let prevTweet = tweet.previousElementSibling
let nextTweet = tweet.nextElementSibling

// get timeline
let timeline_tweets = document.querySelector('section.css-1dbjc4n')

// get username through profile
let profile = document.querySelector(['[data-testid=UserName] > div > div > div > div > div > div > span'])

// dms in through timeline
let dms = document.querySelector(['[data-testid=messageEntry] [data-testid=tweetText] > span'])

let screen_name_datetime = {
    "screen_name" : document.querySelector(['div.css-1dbjc4n > div > div > div > div > div > div > div > div > div > div > div > div > a > div > span']).textContent,
    "datetime" : document.querySelector(['time[datetime]']).getAttribute('datetime')
}

fetch('https://twitter.com/home', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        screen_name: screen_name
    })
})
    .then((res) => { return res.json })
    .then((data) => { console.log(data) })
    .catch(() => { console.error('ERROR') })

// 
exports.login = (req, res) => {
    const{ username, email, password} = req.body;
    
    let userFound = UserModel.findByUnique({username});

    if(userFound){
        //perform matching and auth
        res.redirect('/form');
    }
    if(err){//err
        errHandling(err);
    }
}

/**
 *  TODO: * get code to use double quotes for JSON objects
 *        * get mutated object into a list of JSON objects
 *        * figure out how to extract all tweets with low time complexity
 *          > try to use MutationObserver
 *          > otherwise use nextSibling/nextElementSibling
 *        * figure out how to use use Flask API
 * 
 *  DONE: * object data has been mutated
 *        * figured out how to get screen_name, datetime, tweet text, and tweet article
 */