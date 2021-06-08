const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

Dropzone.autoDiscover = false;
const myDropzone = new Dropzone("#my-dropzone", {
    url : '/upload',
    init : function() {
        this.on('sending', function(file, xhr, formData) {
            formData.append("csrfmiddlewaretoken", csrf);
        })
    }, 
    maxFiles : 3, 
    maxFilesize : 3, 
    acceptedFiles : '.csv'
});