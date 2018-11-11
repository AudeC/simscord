// /static/custom.js

var ID = function () {
  // Math.random should be unique because of its seeding algorithm.
  // Convert it to base 36 (numbers + letters), and grab the first 9 characters
  // after the decimal.
  return '_' + Math.random().toString(36).substr(2, 9);
};


var CLIENT_NAME;
const CLIENT_ID = ID();
//const CLIENT_ID = "_waaxpw0gk";

 function submit_message(message) {
     $.post( "/send_message", {content: message, author: {name: CLIENT_NAME, id: CLIENT_ID}}, handle_response);

     function handle_response(data) {
       // append the bot repsonse to the div
       $('.chat-container').append(`
             <div class="chat-message col-md-5 offset-md-7 bot-message">
                 ${data.message}
             </div>
       `)
       // remove the loading indicator
       $( "#loading" ).remove();
     }
 }

$('#begin').on('submit', function(e){
  e.preventDefault();
  const name = $('#input_name').val()
  if (!name) {
    return false;
  }
  CLIENT_NAME = name;
  $('#begin').hide();
  $('#infos_name').text(name);
  $('#chat').fadeIn();

});

 $('#target').on('submit', function(e){
       e.preventDefault();
       const input_message = $('#input_message').val()
       // return if the user does not enter any text
       if (!input_message) {
         return
       }

       $('.chat-container').append(`
           <div class="chat-message col-md-5 human-message">
               ${input_message}
           </div>
       `)

       // loading
       $('.chat-container').append(`
           <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
               <b>...</b>
           </div>
       `)

       // clear the text input
       $('#input_message').val('')

       // send the message
       submit_message(input_message)
   });


function updateScroll(){
    var element = document.getElementById("#chat_container");
    element.scrollTop = element.scrollHeight;
}

//once a second
//setInterval(updateScroll,1000);
