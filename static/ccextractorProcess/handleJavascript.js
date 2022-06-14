/*
testing stuff
*/
// JQuery
/*$(function () {
    var progressUrl = "{% url 'celery_progress:task_status' task_id %}";
    CeleryProgressBar.initProgressBar(progressUrl)
  });*/

  //custom message pop-up's from django views.

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?.... who tf knows : test
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  } 
  $('.infoSearchBar').on('keypress', function(e) {
    if (e.which == 32){
        console.log('Space Detected');
        return false;
    }
    });

  $(".infoSearchButton").click(function(){
    var str = $(".infoSearchBar").val();
    //var source= $('.infoVideoSource').attr('src');
    //$('.infoVideo').find('Source:first').attr('src');
    var source = document.getElementById('infoVideoSource');
    //$(".answerHidden").css('visibility', 'visible'); // was not working...:(
    $(".searchAnswer").removeClass("answer-hidden").addClass("answer-visible");

    var data=source.getAttribute('src')

    const csrftoken = getCookie('csrftoken');
            $.ajax({
                url: '/info/video-search-answer/',
                type: "POST",
                data: {
                    data:data,
                    str:str
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function (data) {
                    console.log(data);
                    //data["data"]
                    //data["count"]
                    /*
                    confidence: "1.0"
                    endTime: "1.44"
                    fileName: "speech_test1.mp4"
                    sNo: "1"
                    startTime: "0.99"
                    word: "hello"
                    */
                    $("#searchAnswerText").empty();
                    var temp="";
                    for(i = 0; i < data["count"]; i++) { 
                        temp+="<p>"
                            temp+="<span style=\"color:green\">"
                            temp+=data["data"][0]["word"]
                            temp+=": "
                            temp+="</span>"
                            temp+="start at "
                            temp+=data["data"][0]["startTime"]
                            temp+=", "
                            temp+="end at "
                            temp+=data["data"][0]["endTime"]
                            temp+=", "
                            temp+="Confidence="
                            temp+=data["data"][0]["confidence"]
                            temp+="."
                        temp+="</p>"
                      }
                      $("#searchAnswerText").append(
                        $('<p>').text('Words Found: ').append(temp)
                      );
                },
                error: function (error) {
                    console.log(error);
                }
            });

    });

  $('.videoSelector').click(function(){
    key=$(this).data("key");
    //alert("testing: "+key);
    urlPrefix="https://srvnn-django-bezen.s3.ap-south-1.amazonaws.com/media/"

    var video = document.getElementById('infoVideo');
    var source = document.getElementById('infoVideoSource');
    source.setAttribute('src', urlPrefix+key);
    video.load();
    video.play();
    });

  //infoButton
  $('.infoButton').click(function(){
    //alert("testing ok. info button clicked");//test ok.
    window.location.href="/info";
    });

  //refreshButton
  $('.refreshButton').click(function(){
    //alert("testing ok. refreshButton clicked. "); //-- test was ok.
    //location.reload(true); //seems to resubmmit the form when refreshed this way... i dont want that... hm
    //window.location = "http://192.168.68.138:8000/"
    /*

    NEED TO GET THIS CHANGED WHEN I GET THIS HOSTED
    TODO


    */
    // http://ec2-13-233-30-232.ap-south-1.compute.amazonaws.com/
    window.location.replace("http://ec2-13-233-30-232.ap-south-1.compute.amazonaws.com/");//need to change this when i get it hosted 
    });

  $('.uploadButton').click(function(){
    //id=$(this).data("todolist-item-id");
    //data= $('#formfileupload').serialize() --csrf token from form.
    data=$('#uploadVideo').serialize()
    alert("testing ok. uploadButton clicked. "); //-- test was ok.
    const csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/uploadButton/',
            type: "POST",
            data: {
                id:"test"
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                console.log(data);
                location.reload(true)
            },
            error: function (error) {
                console.log(error);
            }
        });
});

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
    }, 5000);