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
                document.querySelector("#question-detail-main-tabs > div.css-eminw3-TabViewHeader.e16udao1 > div > div:nth-child(1)").click();
                questionTitle = document.querySelector("#question-detail-main-tabs > div.css-fwb2av-layer1.css-12hreja-TabContent.e16udao5 > div > div.css-xfm0cl-Container.eugt34i0 > h4 > a").innerText;
                questionContent = document.querySelector("#question-detail-main-tabs > div.css-fwb2av-layer1.css-12hreja-TabContent.e16udao5 > div > div.content__1Y2H > div").innerHTML;
                codeContent = document.querySelector("#lc-home > div > div.main__1pRE > div.css-wfkj6v-Content.e1aolq224 > div > div.css-1gcn2k5-RightContainer.e1aolq221 > div.css-pwvbgl-CodeAreaContainer.ejldciv0 > div.css-w8jsc9-EditorContainer.ejldciv1 > div > div.css-1sdn0mk.css-ilak5e-Container.euyvu2f0 > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text").innerText;
                document.querySelector("#question-detail-main-tabs > div.css-eminw3-TabViewHeader.e16udao1 > div > div:nth-child(4)").click();
                try {
                    if (document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div > div.result-container__ADcY > div > div.css-vkm4ym-Result.e18r7j6f2 > div.css-1uwxigo-SubmitResultInfo.e18r7j6f3 > div.css-11bwh4m-SubmissionResult.e18r7j6f0").innerText == "通过") {
                        resultInfo = document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div > div.result-container__ADcY > div > div:nth-child(3)").innerText + document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div > div.result-container__ADcY > div > div:nth-child(4)").innerText;
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
            console.log(questionTitle);
            console.log(questionContent);
            console.log(codeContent);
            console.log(resultInfo);
            if (!(questionTitle && questionContent && codeContent)) {
                sendResponse({ farewell: "nodt" });
            } else {
                sendResponse({
                    farewell: "got",
                    title: questionTitle,
                    qContent: questionContent,
                    codeText: codeContent,
                    resultText:resultInfo
                });
            }

        }
    }
);

