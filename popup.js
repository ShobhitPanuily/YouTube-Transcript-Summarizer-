const btn = document.getElementById("summarise");

btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Summarizing...";

    chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
        var url = tabs[0].url;
        console.log("URL: ", url); // Log URL for debugging

        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
        
        xhr.onload = function() {
            var text = xhr.responseText;
            const p = document.getElementById("output");
            p.innerHTML = text;
            btn.disabled = false;
            btn.innerHTML = "Summarize";
        };

        xhr.onerror = function() {
            const p = document.getElementById("output");
            p.innerHTML = "Error fetching summary. Please try again.";
            btn.disabled = false;
            btn.innerHTML = "Summarize";
        };

        xhr.send();
    });
});
