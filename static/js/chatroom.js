var localhost = "http://127.0.0.1/"
var onlinehost = "https://oshts.pythonanywhere.com/"

function send(){
  var message = document.getElementById("message");
  var screen1 = document.getElementById("screen");
  if(message.value != ""){
      screen1.innerHTML += "<div class='message txt2 sent_msg'>" + message.value + "</div>"
      fetch(onlinehost + 'post_msg/' + message.value)
      message.value = ""
  }

}


function getMsg(){
  fetch(onlinehost + 'messages')
    .then(response => {
      return response.json()
    })
    .then(data => {
      console.log(data)
      var screen1 = document.getElementById("screen")
      // Work with JSON data here
      for(var x = 0; x <= data.length - 1; x++){
        screen1.innerHTML += "<div class='message txt2'>" + data[x].message + "</div>"
        fetch(onlinehost + 'send_msg/' + data[x].id)
      }
    })
    .catch(err => {
      // Do something for an error here
      //alert(err)
    })
}
window.setInterval(getMsg, 1000);
