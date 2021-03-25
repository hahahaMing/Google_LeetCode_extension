var questionTitle, questionContent, codeContent;


function onDisconnected() {
  console.log("Failed to connect: " + chrome.runtime.lastError.message);
  port = null;
}


function sendMessages2PythonScript() {
  var hostName = "com.google.chrome.example.echo";
  console.log("Connecting to native messaging host" + hostName);
  port = chrome.runtime.connectNative(hostName);
  port.onDisconnect.addListener(onDisconnected);

  if (questionTitle && questionContent && codeContent) {
    console.log("sending...");
    message = {
      "title": questionTitle,
      "qContent": questionContent,
      "codeText": codeContent
    };
    port.postMessage(message);
    console.log("Sent message: " + JSON.stringify(message));
  }
}





chrome.action.onClicked.addListener(sendMessages2PythonScript);

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
  }
);


