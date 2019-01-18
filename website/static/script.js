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

var phrases = [
  ["Quel est votre nouveau produit ?", "En quoi consiste votre nouveau produit ?"],
  ["Quand le produit sera-t-il disponible ?", "Quand pourra-t-on en profiter ?",
  "Quand cette IA sera-t-elle sur le marché ?"],
  ["Pourquoi une IA avec des réactions plus humaines ?", "À quoi cela va-t-il servir ?"]
];

var step = 0;


function fillPhrases() {
  $('#phrases_slot').html("");
  if(step < phrases.length) {
    var rand = Math.floor(Math.random() * phrases[step].length);
    $('#phrases_slot').append(phrases[step][rand]);
  }
}

$(document).ready(function(){

  fillPhrases();

  $("#phrases_slot").click(function(){
    const input_message = $('#phrases_slot').html()
    // return if the user does not enter any text
    if (!input_message) return

    $('.chat-container').append(`
        <div style="overflow:hidden"><div class="chat-message human-message">
            ${input_message}
        </div></div>
    `)

    // loading
    $('.chat-container').append(`
        <div style="overflow:hidden"><div class="chat-message bot-message" id="loading_chat">
            <b>...</b>
        </div></div>
    `)

    // clear the text input
    $('#input_message').val('')

    // send the message
    submit_message(input_message)

    step++;
    fillPhrases();
  });

});



 function submit_message(message) {
     $.post( "/send_message", {content: message, author: {name: CLIENT_NAME, id: CLIENT_ID}}, handle_response);

     function handle_response(data) {
       // append the bot repsonse to the div
       $('.chat-container').append(`
             <div style="overflow:hidden"><div class="chat-message bot-message">
                 ${data.message}
             </div></div>
       `)
       console.log(data)
       $('#affect_indicator').html(data.affect);
       // remove the loading indicator
       $( "#loading_chat" ).remove();
     }
 }

$('#begin').on('submit', function(e){
  console.log("hi");
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
           <div style="overflow:hidden"><div class="chat-message human-message">
               ${input_message}
           </div></div>
       `)

       // loading
       $('.chat-container').append(`
           <div style="overflow:hidden"><div class="chat-message bot-message" id="loading_chat">
               <b>...</b>
           </div></div>
       `)

       // clear the text input
       $('#input_message').val('')

       // send the message
       submit_message(input_message)
   });


function updateScroll(){
    var element = document.getElementById("chat_container");
    element.scrollTop = element.scrollHeight;
}

//once a second
//setInterval(updateScroll,1000);
