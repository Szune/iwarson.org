(function() {
    function toggleLightTheme() {
        let light = document.body.classList.toggle("light");
        try {
            let storage = window["localStorage"];
            storage.setItem("lightModeToggled", light ? "yes" : "no");
        } catch(e) {
            // ignore
        }
    }
    document.getElementById("lightmodetoggle").onclick = () => toggleLightTheme();
})();
