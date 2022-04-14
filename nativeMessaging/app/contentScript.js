/*
 * @Author: your name
 * @Date: 2021-05-21 13:08:33
 * @LastEditTime: 2021-09-06 14:44:53
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \Google_LeetCode_extension\nativeMessaging\app\contentScript.js
 */
var questionTitle;
var questionContent;
var codeContent;
var resultInfo;

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log(sender.tab ?
            "from a content script:" + sender.tab.url :
            "from the extension");
        if (request.greeting == "hello") {

            try {
                // 跳转题目描述页面
                document.evaluate('//*[@id="question-detail-main-tabs"]/div[1]/div/div[1]', document).iterateNext().click();
                questionTitle = document.evaluate('//*[@id="question-detail-main-tabs"]/div[2]/div/div[1]/h4', document).iterateNext().innerText;
                questionContent = document.evaluate('//*[@id="question-detail-main-tabs"]/div[2]/div/div[2]', document).iterateNext().innerHTML;
                codeContent = document.evaluate('//*[@id="lc-home"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div[2]', document).iterateNext().innerText;
                document.document.evaluate('//*[@id="question-detail-main-tabs"]/div[1]/div/div[3]', document).iterateNext().click();
                try {
                    if (document.evaluate('//*[@id="question-detail-main-tabs"]/div[5]/div/div/div[1]/div/div[1]/div[1]/div[1]', document).iterateNext().innerText == "通过") {
                        resultInfo = document.evaluate('//*[@id="question-detail-main-tabs"]/div[5]/div/div/div[1]/div/div[2]', document).iterateNext().innerText;
                        resultInfo += document.evaluate('//*[@id="question-detail-main-tabs"]/div[5]/div/div/div[1]/div/div[3]', document).iterateNext().innerText;
                    }
                }
                catch (err) {
                    resultInfo = "";
                    console.log("no resultInfo");
                    console.log(err);
                }
            }
            catch (err) {
                // alert("data not complete, please refresh the page!");
                console.log(err);
            }
            console.log('【***** questionTitle *****】' + questionTitle);
            console.log('【***** questionContent *****】' + questionContent);
            console.log('【***** codeContent *****】' + codeContent);
            console.log('【***** resultInfo *****】' + resultInfo);
            if (!(questionTitle && questionContent && codeContent)) {
                console.log("send nodt!");
                sendResponse({ farewell: "nodt" });
            } else {
                console.log("send data!");
                sendResponse({
                    farewell: "got",
                    title: questionTitle,
                    qContent: questionContent,
                    codeText: codeContent,
                    resultText: resultInfo
                });
            }

        }
    }
);

