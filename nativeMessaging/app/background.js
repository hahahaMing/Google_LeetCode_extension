function openPage() {
    browser.tabs.create({
      url: "https://baidu.com"
    });
  }
  
browser.browserAction.onClicked.addListener(openPage);