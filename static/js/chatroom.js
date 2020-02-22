function send(){
  var message = document.getElementById("message");
  var screen1 = document.getElementById("screen");
  if(message.value != ""){
    screen1.innerHTML += "<div class='message txt2'>" + message.value + "</div>"
    message.value = ""
  }

}
