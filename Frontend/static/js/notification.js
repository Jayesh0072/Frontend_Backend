let endpoint = "ws://127.0.0.1:8000/modelval/chat/?room="+$('#txtuid').val()+'&type=user'
var socket = new WebSocket(endpoint)
 
socket.onopen = async function (e){ 
}


socket.onmessage = async function(e){
    console.log('message', e) 
    let data = JSON.parse(e.data)
    let message = data['message']
    console.log('type '+ $('#txtuid').val()) 
    let qtnArr=''
    $("#notification_header").text(message.split('|')[0])
    $("#notification_msg").text(message.split('|')[1])
    if(data['type']=='msg'){
        if($('#txtuid').val()!=data['sent_by']){
        qtnArr +=' <div class="d-flex chat-message">';
    qtnArr +='         <div class="d-flex mb-2 flex-1">';
    qtnArr +='           <div class="w-100 w-xxl-75">';
    qtnArr +='             <div class="d-flex hover-actions-trigger">';                     
    qtnArr +='               <div class="chat-message-content received me-2">';
    qtnArr +='                 <div class="mb-1 received-message-content border rounded-2 p-3">';
    qtnArr +='                    <p class="mb-0">'+message+'</p>';
    qtnArr +='                 </div>';
    qtnArr +='     </div>         ';                  

    qtnArr +='  </div>';
    qtnArr +='   <p class="mb-0 fs--2 text-600 fw-semi-bold "> commented on </p>';
    qtnArr +=' </div>';
    qtnArr +=' </div>';
    qtnArr +='  </div>';
        }
        else{
            qtnArr +=' <div class="d-flex chat-message">';
                qtnArr +=' <div class="d-flex mb-2 justify-content-end flex-1">';
                qtnArr +=' <div class="w-100 w-xxl-75">';
                  qtnArr +=' <div class="d-flex flex-end-center hover-actions-trigger">';
                  qtnArr +=' <div class="d-sm-none hover-actions align-self-center me-2 start-0">';                 
                  
                    qtnArr +='<div class="bg-white rounded-pill d-flex align-items-center border border-300 px-2 actions">';
                   qtnArr +='<button class="btn p-2" type="button"><span class="fa-solid fa-pen-to-square text-primary"></span></button>';
                        qtnArr +='</div>';
                      qtnArr +='</div>';
                  qtnArr +='   <div class="d-none d-sm-flex">';
                    qtnArr +=' <div class="hover-actions position-relative align-self-center">'; 
                    //   qtnArr +=' <button class="btn p-2 fs--2" onclick="getCommentforEdit(' + val.Response_id +')" ><span class="fa-solid fa-pen-to-square text-primary" ></span></button>';
                      
                      qtnArr +='  </div>';
                      qtnArr +=' </div>';
                    qtnArr +=' <div class="chat-message-content me-2">';
                      qtnArr +='  <div class="mb-1 sent-message-content light bg-primary rounded-2 p-3 text-white">';
                        qtnArr +=' <p class="mb-0">'+message+'</p>';
                        qtnArr +=' </div>';
                        qtnArr +='  </div>';
                        qtnArr +=' </div>';
                        qtnArr +=' <div class="text-end">';
                          qtnArr +=' <p class="mb-0 fs--2 text-600 fw-semi-bold"> commented on  </p>';
                          qtnArr +=' </div>';
                          qtnArr +=' </div>';
                          qtnArr +=' </div>';
                          qtnArr +=' </div> ';
        }
    $('#divMdlPerfMontresp').append(qtnArr)
    }
    else{
    if($('#txtuid').val()!=data['sent_by'])
        $("#liveToastBtn").click();
    }
    //newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
} 
function sendNotification(msg,from ,to ,thread_id,type, mdl_id){
     console.log('msg content is '+msg,from ,to ,thread_id,type)
//     let input_message = $('#message').val()
// let send_by = $('#send_by').val()
// let send_to = $('#send_to').val()
// let thread_id = $('#thread_id').val()
//     console.log('params',send_to)
    ///send_message_form.on('submit', function (e){
       // e.preventDefault()
       // let message =msg;// input_message.val()
        //let send_to =to;//get_active_other_user_id()
       // let thread_id =treadid;// get_active_thread_id()
        //USER_ID=from;
        let data = {
            'message': msg,
            'sent_by': from,
            'send_to': to,
            'thread_id': thread_id,
            'type':type,
            'mdl_id':mdl_id
        }
        data = JSON.stringify(data)
        //console.log("data",data)
        socket.send(data)
        
        // $(this)[0].reset()
}

  