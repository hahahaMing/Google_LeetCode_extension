//页面加载完毕后执行
window.onload = function () {
    var questionTitle = document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div.css-xfm0cl-Container.eugt34i0 > h4 > a").innerText;
    var questionContent = document.querySelector("#question-detail-main-tabs > div.tab-pane__1SHj.css-12hreja-TabContent.e16udao5 > div > div.content__1Y2H > div").innerHTML;
    var codeContent = document.querySelector("div.view-lines").innerText;

    console.log(questionTitle);
    console.log(questionContent);
    console.log(codeContent);

    chrome.runtime.sendMessage({
        greeting: "hello", 
        title: questionTitle, 
        qContent: questionContent, 
        codeText: codeContent 
    }, 
    function (response) {
        console.log(response.farewell);
    });


}

