chrome.tabs.onUpdated.addListener((tabId, tab) => {
    // Evaluates url if they are from twitter
    if(tab.url && tab.url.includes("twitter.com/home")) {
        let urlParameters = new URLSearchParams("home")
        console.log(urlParameters)

        chrome.tabs.sendMessage(tabId, {
            type: "NEW",
            timeline: urlParameters.get("home")
        })
    } else if(tab.url && tab.url.includes("twitter.com/*/status/")) {
        let queryParameters = tab.url.split("/")[1]
        let urlParameters = new URLSearchParams(queryParameters)
        console.log(urlParameters)

        chrome.tabs.sendMessage(tabId, {
            type: "NEW",
            timeline: urlParameters.get("status")
        })
    } else if(tab.url && tab.url.includes("twitter.com/")) {
        let queryParameters = tab.url.split("/")[1]
        let urlParameters = new URLSearchParams(queryParameters)
        console.log(urlParameters)

        chrome.tabs.sendMessage(tabId, {
            type: "NEW",
            timeline: urlParameters.get("/")
        })
    }
})

