var questionTitle;
var questionContent;
var codeContent;

//页面加载完毕后执行
// window.onload = function () {





//     chrome.runtime.sendMessage({
//         greeting: "hello",

//     },
//         function (response) {
//             console.log(response.farewell);
//         });

// }

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log(sender.tab ?
            "from a content script:" + sender.tab.url :
            "from the extension");
        if (request.greeting == "hello") {

            try {
                questionTitle = document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div.css-xfm0cl-Container.eugt34i0 > h4 > a").innerText;
                questionContent = document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div.content__1Y2H > div").innerHTML;
                codeContent = document.querySelector("div.view-lines").innerText;
            }
            catch (err) {
                // alert("data not complete, please refresh the page!");
                console.log(err);
            }
            console.log(questionTitle);
            console.log(questionContent);
            console.log(codeContent);
            if (!(questionTitle && questionContent && codeContent)) {
                sendResponse({ farewell: "nodt" });
            } else {
                sendResponse({
                    farewell: "got",
                    title: questionTitle,
                    qContent: questionContent,
                    codeText: codeContent
                });
            }

        }
    }
);