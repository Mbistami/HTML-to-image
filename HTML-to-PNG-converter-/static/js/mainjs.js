
$(document).ready(function(){
    
})
var selectedB64 = '';

function readFile() {

    
}

function show(op){
  if(op === 'op2')
    $('.input-group.mb-4').show();
  else
    $('.input-group.mb-4').hide();
}

$('.toFlask').submit(function(e){
  

  var myform = document.getElementById('mainForm')
  var form = new FormData()

  form.append('ziped', $('#zip')[0].files[0])
  form.append('ziped', )

  console.log(myform)
  $.ajax({
    xhr: function() {
      var xhr = new window.XMLHttpRequest();

      // Upload progress
      xhr.upload.addEventListener("progress", function(evt){
          if (evt.lengthComputable) {
              var percentComplete = evt.loaded / evt.total;
              //Do something with upload progress
              console.log(percentComplete);
          }
     }, false);

     // Download progress
     xhr.addEventListener("progress", function(evt){
         if (evt.lengthComputable) {
             var percentComplete = evt.loaded / evt.total;
             // Do something with download progress
             console.log(percentComplete);
         }
     }, false);

     return xhr;
    },
    type: "POST",
    url: '/upload',
    data: form,
    processData: false,
    contentType: false,
    success: function(data)
    {
         window.location = data
    },
    error: function(error){
      console.log(error)
    }
  })
})

