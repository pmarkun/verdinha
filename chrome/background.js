function updateIcon() {
  if(localStorage.hasOwnProperty('disabled')) {
    chrome.browserAction.setBadgeText({text: ""});
    chrome.browserAction.setTitle({title:"Verdinha [Ligado]"});
    chrome.browserAction.setIcon({path:"images/icon19.png"});
    delete localStorage.disabled;
  } else {
    chrome.browserAction.setBadgeText({text:"off"});
    chrome.browserAction.setTitle({title:"Verdinha [Desligado]"});
    chrome.browserAction.setIcon({path:"images/icon19_off.png"});
    localStorage.disabled = true;
  }
}

chrome.browserAction.onClicked.addListener(updateIcon);

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.type == "disabled") sendResponse({disabled: localStorage.disabled});
});
