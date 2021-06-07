console.log("Home Script Loaded!");

const reportBtn = document.getElementById("report-btn");
const img = document.getElementById("img");

if(img) {
    reportBtn.classList.remove('not-visible');
}