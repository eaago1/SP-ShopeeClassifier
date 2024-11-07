
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {

    if (message.action === 'download') {
        chrome.downloads.download({ url: message.url });
    }
});
