function send(){
  var message = document.getElementById("message");
  var screen1 = document.getElementById("screen");
  if(message.value != ""){
    screen1.innerHTML += "<div class='message txt2'>" + message.value + "</div>"
    message.value = ""
  }

}


fetch('http://127.0.0.1:5000/messages')
  .then(response => {
    return response.json()
  })
  .then(data => {
    // Work with JSON data here
    console.log(data)
  })
  .catch(err => {
    // Do something for an error here
  })
