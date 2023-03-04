const uploadForm = document.getElementById('uploadform')
const input = document.getElementById('id_video')
const alertBox = document.getElementById('alert-box')
const fileBox =  document.getElementById('file-box')
const progressBox = document.getElementById('progress-box')
const cancelBox = document.getElementById('cancel-box')
const uploadBox = document.getElementById('upload-box')
const cancelBtn = document.getElementById('cancel-btn')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const collection = document.getElementsByClassName("wrapper");

$('#loading').hide();
input.addEventListener('change',()=>{
    progressBox.classList.remove('not-visible')
    cancelBox.classList.remove('not-visible')
    uploadBox.classList.remove('visibility')
    const video_data = input.files[0]
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken',csrf[0].value)
    fd.append('video',video_data)
    $.ajax({
        type:'POST',
        url : uploadForm.action,
        enctype: 'multipart/form-data',
        data : fd,
        beforeSend: function(){
            // alertBox.innerHTML= ""
            // fileBox.innerHTML = ""
        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress',e=>{
                if(e.lengthComputable){
                    const percent = e.loaded/e.total *100
                    progressBox.innerHTML = `
                    <p style = "font-size: 20px;color:rgb(246, 116, 10);margin-top:20px;">${percent.toFixed(1)}%</p>
                    <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width:${percent}%; background-color:#2cd735;": ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100" "style:" color":green"></div>
                </div>`
                if (percent == 100){
                    $('#loading').show();
                    $("label[for = 'id_video']").text("Wait for some time")
                    $("#spinner").hide()
                    $(".btn").hide()
                }
                else{
                    $('#loading').hide(); 
                }
            }
            });
            cancelBtn.addEventListener('click',()=>{
                xhr.abort()
                setTimeout(()=>{
                    uploadForm.reset();
                },2000)
                alertBox.innerHTML=""
                progressBox.innerHTML = ""
                $('#loading').hide(); 
                cancelBox.classList.remove('not-visible')
            })
            return xhr
        },
        success: function(response){
            alertBox.innerHTML = `<div class="alert alert-success" role="alert">
            Video Uploaded Successfully
          </div>`
          var x = document.getElementById('id_video').files[0].name;
          $("#loading").hide()
          $("label[for = 'id_video']").text(x)
          cancelBox.remove()
          $(".btn").show()

        },
        error:function(error){
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
            0ops!!Something gone Wrong!
          </div>`

        },
        cache : false,
        contentType : false,
        processData : false,

    })

});
