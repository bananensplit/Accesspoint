document.querySelector('#discovermore').addEventListener('click', scrollToCharts, false);
document.querySelector('#discovermore').addEventListener('mouseenter', scrollToCharts, false);

function scrollToCharts() {
    document.querySelector('#analyse').scrollIntoView({behavior: "smooth"});
}