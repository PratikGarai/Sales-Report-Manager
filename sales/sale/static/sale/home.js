console.log("Home Script Loaded!");

const reportBtn = document.getElementById("report-btn");
const img = document.getElementById("img");
const modalBody = document.getElementById("modal-body");
const reportForm = document.getElementById("report-form");

const reportName = document.getElementById('id_name');
const reportRemarks = document.getElementById('id_remarks');
const csrf = document.getElementsByName("csrfmiddlewaretoken")[1].value;

if(img) {
    reportBtn.classList.remove('not-visible');
}

reportBtn.addEventListener('click', () => {
    const im2 = img;
    im2.setAttribute('class', 'w-100');
    modalBody.prepend(im2);
    
    reportForm.addEventListener('submit', e=> {
        e.preventDefault();
        const formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrf);
        formData.append("name", reportName.value);
        formData.append("remarks", reportRemarks.value);
        formData.append("image", img.src);

        $.ajax({
            type : "POST",
            url : '/reports/save/',
            data : formData,
            success : function(response) {
                console.log("Success : ", response)
            },
            error : function(response) {
                console.log("Error : ", response)
            },
            processData : false, 
            contentType : false
        })
    })
});