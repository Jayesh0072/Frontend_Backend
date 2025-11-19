
var socket ;
var roomarr=[];
var selected_utility='';
var selected_sub_utility='';
var selected_data_parameter='';
function connectWS(mdlid){
  console.log('mdlid ',mdlid)
  let endpoint = "ws://127.0.0.1:8000/modelval/chat/?room="+mdlid+'&type=model'
  if(roomarr.indexOf(mdlid)>=0)
    return false;
  socket = new WebSocket(endpoint)
socket.onopen = async function (e){ 
  console.log('connected',socket)
  roomarr.push(mdlid);
  console.log('roomarr ',roomarr)
}


socket.onmessage = async function(e){
    let data = JSON.parse(e.data)
    let message = data['message']
    console.log('data ',data)  
    let qtnArr=''
    $("#notification_header").text(message.split('|')[0])
    $("#notification_msg").text(message.split('|')[1])
    if(data['type']=='msg'){ 
        }
    else if(data['type']=='vt_discussion'){
      
      arrScreen=['','Variables by Type n Count','Data Statistics of Numerical Variables','View Correlation on independent Numeric variables','View Multivariate Graphs','View Frequency of Categorical Variable','View Distribution of Numeric for Categorical Variable','Confirm data source and quality','Conceptual Soundness','Audit & Regulatory Compliance Response','Roles Responsibility Question Response','Documentation','Output Run Base Model','Validation Findings','Implementation and Controls','Model Usage'];
        // console.log(' utility is ',data['utility'],arrScreen.indexOf(data['utility']),selected_utility,$("#txtSelUtil").val().replaceAll('&','n'));

        var chatWndow=arrScreen.indexOf(data['utility']);
        if($('#lblcurruid').text()!=data['sent_by']){
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
        qtnArr +='   <p class="mb-0 fs--2 text-600 fw-semi-bold ">'+data['commented_by']+'</p>';
        if(data['filename']!=''){
          qtnArr +='<div style="background-color: #d0d0d040;width: 100%;float: left;padding-top: 5px;padding-bottom: 5px;padding: 5px;" class="row">'
          qtnArr +='<table>'
          qtnArr +='<tbody><tr>'
          qtnArr +='<td align="center">'
          qtnArr +='<img src="/static/Front/dist/assets/svg/svgs/google-docs-icon.svg" alt="Image Description" style="/*! height: 200%; */height: 50px;">'
          qtnArr +='</td>'
          qtnArr +='</tr>'
          qtnArr +='<tr>'
          qtnArr +='<td align="center">'
          qtnArr +='<a class="text-dark" href="'+data['filename']+'" target="_blank">' +data['filename'].split('\\').at(-1) +'</a>'
          qtnArr +='</td>'
          qtnArr +='</tr>'
          qtnArr +='</tbody></table> '
          qtnArr +='</div>' 
        
        }
        qtnArr +=' </div>';
        qtnArr +=' </div>';
        qtnArr +='  </div>';
        console.log('comp ',($("#txtSelUtil").val().replaceAll('&','n'),', ',data['utility']),', ',($("#txtSelUtil").val().replaceAll('&','n')==data['utility']))
        if($("#txtSelUtil").val().replaceAll('&','n')==data['utility']){
          $('#divresp').append(qtnArr) 
           
              $('#divresp').animate({
                scrollTop: $('#divresp').get(0).scrollHeight
            }, 200);
          } 
            $("#imgbob_"+ data['utility'].replaceAll(' ','').replaceAll('&','n') +"_" +  data['sub_utility'].replaceAll(' ','') +"_" +  data['utility_type'].replaceAll(' ','') ).show();
         
            }
            else{
              qtnArr +=' <div class="d-flex chat-message_sent">';
              qtnArr +=' <div class="d-flex mb-2 justify-content-end flex-1"  style="-webkit-box-flex: 1;  -ms-flex: 1;  flex: 1;">';
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
                              qtnArr +=' <p class="mb-0 fs--2 text-600 fw-semi-bold">'+data['commented_by']+'</p>';
                              qtnArr +=' </div>';
                              if(data['filename']!=''){
                                qtnArr +='<div style="background-color: #d0d0d040;width: 50%;float: right;padding-top: 5px;padding-bottom: 5px;padding: 5px;" class="row">'
                                qtnArr +='<table>'
                                qtnArr +='<tbody><tr>'
                                qtnArr +='<td align="center">'
                                qtnArr +='<img src="/static/Front/dist/assets/svg/svgs/google-docs-icon.svg" alt="Image Description" style="/*! height: 200%; */height: 50px;">'
                                qtnArr +='</td>'
                                qtnArr +='</tr>'
                                qtnArr +='<tr>'
                                qtnArr +='<td align="center">'
                                qtnArr +='<a class="text-dark" href="'+data['filename']+'" target="_blank">' +data['filename'].split('\\').at(-1) +'</a>'
                                qtnArr +='</td>'
                                qtnArr +='</tr>'
                                qtnArr +='</tbody></table> '
                                qtnArr +='</div>'
                              
                              } 
                              
                              qtnArr +=' </div>';
                              qtnArr +=' </div>';
                              qtnArr +=' </div> ';
                              $('#divresp').append(qtnArr) 
           
                              $('#divresp').animate({
                                scrollTop: $('#divresp').get(0).scrollHeight
                            }, 500);
                          
            }
            
        
       
    }
    else{
    if($('#lblcurruid').text()!=data['sent_by'])
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
}
function sendPerfMonmsg(msg,from ,to ,thread_id,type,mdl_id,commented_by,utility,sub_utility,utility_type,filename){ 
console.log('filename in sendperf ',filename)
   let data = {
       'message': msg,
       'sent_by': from,
       'send_to': to,
       'thread_id': thread_id,
       'type':type,
       'mdl_id':mdl_id,
       'commented_by':commented_by,
       'utility':utility,
       'sub_utility':sub_utility,
       'utility_type':utility_type,
       'filename':filename
   }
      data = JSON.stringify(data)
      //console.log("data",data)
      socket.send(data)
        
        // $(this)[0].reset()
}

  