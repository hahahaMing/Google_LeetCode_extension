// Copyright 2013 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

var port = null;

var getKeys = function (obj) {
    var keys = [];
    for (var key in obj) {
        keys.push(key);
    }
    return keys;
}


//估计是修改html页面元素，然后在response部分显示text
function appendMessage(text) {
    document.getElementById('response').innerHTML += "<p>" + text + "</p>";
}

function updateUiState() {
    if (port) {
        document.getElementById('connect-button').style.display = 'none';
        document.getElementById('input-text').style.display = 'block';
        document.getElementById('send-message-button').style.display = 'block';
    } else {
        document.getElementById('connect-button').style.display = 'block';
        document.getElementById('input-text').style.display = 'none';
        document.getElementById('send-message-button').style.display = 'none';
    }
}

function sendNativeMessage() {
    console.log("sending...");
    message = { "text": document.getElementById('input-text').value };
    port.postMessage(message);
    appendMessage("Sent message: <b>" + JSON.stringify(message) + "</b>");
}

function onNativeMessage(message) {
    appendMessage("Received message: <b>" + JSON.stringify(message) + "</b>");
}

function onDisconnected() {
    appendMessage("Failed to connect: " + chrome.runtime.lastError.message);
    port = null;
    updateUiState();
}


function contentGet(){
    // var queTitle = document.getElementsByClassName("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div.css-xfm0cl-Container.eugt34i0");
    appendMessage("test content.")
    console.log("test log.");
    var queTitle = document.getElementsByClassName("css-xfm0cl-Container.eugt34i0");
    console.log(queTitle);

}

function connect() {
    var hostName = "com.google.chrome.example.echo";
    appendMessage("Connecting to native messaging host <b>" + hostName + "</b>")
    port = chrome.runtime.connectNative(hostName);
    port.onMessage.addListener(onNativeMessage);
    port.onDisconnect.addListener(onDisconnected);
    updateUiState();
}

document.addEventListener('DOMContentLoaded', function () {
    //点击connect按钮 执行connect函数
    document.getElementById('connect-button').addEventListener(
        'click', connect);
    document.getElementById('send-message-button').addEventListener(
        'click', sendNativeMessage);
    updateUiState();
});
