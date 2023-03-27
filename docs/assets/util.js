(function() {
    try {
        let storage = window["localStorage"];
        if (storage.getItem("lightModeToggled") === "yes") {
            document.body.classList.toggle("light"); 
        }
    } catch(e) {
        // ignore
    }
})();
