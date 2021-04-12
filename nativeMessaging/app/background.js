var questionTitle, questionContent, codeContent;
var hostName = "com.google.chrome.example.echo";
var port;
var count = 0;
var connectInterval, sendDataInterval;
var connected = false;
function onDisconnected() {
  console.log("Failed to connect: " + chrome.runtime.lastError.message);
  port = null;
}

function onNativeMessage(message) {
  console.log("Received message:" + JSON.stringify(message));
  if (JSON.stringify(message) == '{"text":"connected"}') {
    connected = true;
    clearInterval(connectInterval);
    console.log("get connected!");
  }
  else if (JSON.stringify(message) == '{"text":"received"}') {
    clearInterval(sendDataInterval);
    console.log("get recieved!");
  }
  else if (JSON.stringify(message) == '{"text":"auto_movement"}') {
    chrome.action.setBadgeText({ text: 'auto' });
  }
  else if (JSON.stringify(message) == '{"text":"bye"}') {
    console.log("close port");
    chrome.action.setBadgeText({ text: 'done' });
  }


}

function connect() {
  count++;
  if (count > 10) clearInterval(connectInterval);//防止无限循环
  console.log("connecting...");
  message = {
    "text": "c"
  };
  port.postMessage(message);

}

function sendData() {
  count++;
  if (count > 10) clearInterval(sendDataInterval);//防止无限循环
  if (!connected) {
    console.log("waiting for connecting!");
    return;
  }

  console.log("sending data...");
  message = {
    "text": "data",
    "title": questionTitle,
    "qContent": questionContent,
    "codeText": codeContent
  };
  port.postMessage(message);
  console.log("Sent message: " + JSON.stringify(message));


}

function sendMessages2PythonScript() {

  //判断data是否准备好
  if (!(questionTitle && questionContent && codeContent)) {
    console.log("data not complete, please refresh the page!");
    chrome.action.setBadgeText({ text: 'nodt' });
  }
  else {
    //连接py脚本
    console.log("Connecting to native messaging host" + hostName);
    port = chrome.runtime.connectNative(hostName);
    port.onMessage.addListener(onNativeMessage);
    port.onDisconnect.addListener(onDisconnected);
    count = 0;
    //发送信息，等待py脚本回复连接成功
    chrome.action.setBadgeText({ text: 'cnet' });
    connectInterval = setInterval(connect, 500);

    count = 0;
    //发送data,等待py回复接收成功
    chrome.action.setBadgeText({ text: 'stdt' });
    sendDataInterval = setInterval(sendData, 500);
    //结束
  }


}

//设置初始图标前文字为空
chrome.action.setBadgeText({ text: '' });
//点击按钮，开始与py脚本通信
chrome.action.onClicked.addListener(sendMessages2PythonScript);

//与内嵌脚本通信，获取data，badge：got
chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    console.log(sender.tab ?
      "from a content script:" + sender.tab.url :
      "from the extension");
    questionTitle = request.title;
    questionContent = request.qContent;
    codeContent = request.codeText;
    console.log(questionTitle);
    console.log(questionContent);
    console.log(codeContent);
    if (request.greeting == "hello")
      sendResponse({ farewell: "got it!" });
    chrome.action.setBadgeText({ text: 'got' });


  }
);


