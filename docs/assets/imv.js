const imv = 'imv';
const imv_img = 'imv-img';
const imv_enlarge = 'imv-enlarge';

const create = n => document.createElement(n);
const get = i => document.getElementById(i);
const closeViewer = () => get(imv).classList.remove('imv-visible');
const view = src => {
    get(imv_img).setAttribute("src", src);
    get(imv_enlarge).setAttribute("href", src);
    get(imv).classList.add('imv-visible');
};

HTMLCollection.prototype.each = function(f) {
    for(let i = 0; i < this.length; i++) { f(this[i]); }
};

function setupViewer() {
    let container = create('div');
    container.id = imv;

    let modal = create('div');
    modal.classList.add('imv-modal');
    modal.onclick = (e) => {e.stopPropagation();};

    let img = create('img');
    img.id = imv_img;
    img.onclick = container.onclick = () => closeViewer();
    modal.appendChild(img);

    let fullLink = create('a');
    fullLink.id = imv_enlarge;
    let fullButton = create('button');
    fullButton.classList.add(imv_enlarge);
    fullButton.append("View full image");
    fullLink.appendChild(fullButton);
    modal.appendChild(fullLink);

    container.appendChild(modal);

    document.body.appendChild(container);
}

function setupLinks() {
    document
        .getElementsByClassName('box-text')
        .each(e => {
            e.getElementsByTagName('a')
             .each(lnk => {
                    let href = lnk.href;
                    lnk.onclick = () => view(href);
                    lnk.removeAttribute("href");
                    lnk.classList.add("link-cursor");
                })
            });
}

setupViewer();
setupLinks();

addEventListener("keydown", e => {
    if (e.key === "Escape") {
        closeViewer();
    }
});
