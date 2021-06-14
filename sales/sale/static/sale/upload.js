const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
const alertBox = document.getElementById("alert-box");

Dropzone.autoDiscover = false;
const myDropzone = new Dropzone("#my-dropzone", {
    url : '/upload',
    init : function() {
        this.on('sending', function(file, xhr, formData) {
            formData.append("csrfmiddlewaretoken", csrf);
        });

        this.on('success', function(file, response) {
            const ex = response.ex;
            if(ex) {
                alertBox.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Error uploading file!
                </div>
                `;
            } else {
                alertBox.innerHTML = `
                <div class="alert alert-success" role="alert">
                    File uploaded successfully!
                </div>
                `;
            }
        });

        this.on('error', function(file, response) {
            alertBox.innerHTML = `
            <div class="alert alert-danger" role="alert">
                Error uploading file!
            </div>
            `;
        })
    }, 
    maxFiles : 3, 
    maxFilesize : 3, 
    acceptedFiles : '.csv'
});