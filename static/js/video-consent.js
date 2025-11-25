(function () {
  if (window.__videoConsentInit) return;
  window.__videoConsentInit = true;

  function loadVideo(placeholder) {
    var videoId = placeholder.getAttribute("data-youtube-id");
    if (!videoId) return;

    var iframe = document.createElement("iframe");
    iframe.setAttribute(
      "src",
      "https://www.youtube-nocookie.com/embed/" + videoId + "?autoplay=1"
    );
    iframe.setAttribute("title", "YouTube video player");
    iframe.setAttribute("frameborder", "0");
    iframe.setAttribute(
      "allow",
      "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    );
    iframe.setAttribute("allowfullscreen", "allowfullscreen");
    //iframe.style.width = "100%";
    //iframe.style.height = "100%";

    placeholder.innerHTML = "";
    placeholder.appendChild(iframe);
  }

  document.addEventListener("click", function (event) {
    var button = event.target.closest(".video-consent-button");
    if (!button) return;

    var placeholder = button.closest(".video-placeholder");
    if (!placeholder) return;

    console.log("Video-Button geklickt, lade YouTube-Video…");
    loadVideo(placeholder);
  });
})();
