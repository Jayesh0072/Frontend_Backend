
var socket ;
function connectWS(mdlid){
  console.log('mdlid ',mdlid)
  let endpoint = "ws://127.0.0.1:8000/modelval/chat/?room="+mdlid+'&type=model'
  socket = new WebSocket(endpoint)
socket.onopen = async function (e){ 
  console.log('connected',socket)
}


socket.onmessage = async function(e){
    let data = JSON.parse(e.data)
    let message = data['message']
    console.log('data ',data) 
    console.log('type '+ $('#lblcurruid').text()) 
    let qtnArr=''
    $("#notification_header").text(message.split('|')[0])
    $("#notification_msg").text(message.split('|')[1])
    if(data['type']=='msg'){
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
                              qtnArr +=' <p class="mb-0 fs--2 text-600 fw-semi-bold">'+data['commented_by']+'</p>';
                              qtnArr +=' </div>';                               
                              qtnArr +=' </div>';
                              qtnArr +=' </div>';
                              qtnArr +=' </div> ';
            }
        $('#divresp').append(qtnArr) 
          $('#divMdlPerfMontresp').animate({
            scrollTop: $('#divMdlPerfMontresp').get(0).scrollHeight
        }, 200);
        }
    else if(data['type']=='vt_discussion'){
      
        arrScreen=['','Variables by Type n Count','Data Statistics of Numerical Variables','View Correlation on independent Numeric variables','View Multivariate Graphs','View Frequency of Categorical Variable','View Distribution of Numeric for Categorical Variable','Confirm data source and quality','Conceptual Soundness','Audit & Regulatory Compliance Response','Roles Responsibility Question Response','Documentation','Output Run Base Model','Validation Findings','Implementation and Controls','Model Usage'];
        console.log(' utility is ',data['utility'],arrScreen.indexOf(data['utility']));
        var chatWndow=arrScreen.indexOf(data['utility']);
        console.log('users ',$('#lblcurruid').text(),',',data['sent_by'])
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
          qtnArr +='<div style="background-color: #d0d0d040;width: 50%;float: left;padding-top: 5px;padding-bottom: 5px;padding: 5px;" class="row">'
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
            }
        $('#divresp_VT_Comm_Chat').append(qtnArr) 
        $('#divresp_VT_Comm_Chat').animate({
          scrollTop: $('#divresp_VT_Comm_Chat').get(0).scrollHeight
      }, 200);
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

function getVT_Comm_History(divid,utility,subutility,mdl_id){
  debugger
  $('#'+divid).empty()
  $.ajax({ 
    url: '/ValidationCommentHistory/',
    data:{'utility':utility,'subutility': subutility,'mdl_id':mdl_id,'chat_data':$('#txtChatData').val()},
    dataType: 'json',
    success: function (data) {
      $('#txtReportComments_VT_Comm_Chat').val(data.comment[0].comment)
     
      if($('#lblcurruid').text()!=data.comment[0].added_by){
        $('#btnSave_VT_Comm_Chat').hide();
        $('#txtReportComments_VT_Comm_Chat').prop('disabled',true)
      }
      else{
        $('#btnSave_VT_Comm_Chat').show();
        $('#txtReportComments_VT_Comm_Chat').prop('disabled',false)
      }
    qtnArr = '';
    $.each(data.data, function(key, val) { 
        if(val.msgcss=='R')
        {
        qtnArr +=' <div class="d-flex chat-message">';
        qtnArr +='         <div class="d-flex mb-2 flex-1">';
            qtnArr +='           <div class="w-100 w-xxl-75">';
            qtnArr +='             <div class="d-flex hover-actions-trigger">';                     
                qtnArr +='               <div class="chat-message-content received me-2">';
                qtnArr +='                 <div class="mb-1 received-message-content border rounded-2 p-3">';
                    qtnArr +='                    <p class="mb-0">'+val.Comment+'</p>';
                    qtnArr +='                 </div>';
                    qtnArr +='     </div>         ';                  
                        
                    qtnArr +='  </div>';
                    qtnArr +='   <p class="mb-0 fs--2 text-600 fw-semi-bold ">'+val.uinitials +' commented on '+val.createdt+'</p>';
                    if(val.filename!=''){
                      qtnArr +='<div style="background-color: #d0d0d040;width: 50%;float: left;padding-top: 5px;padding-bottom: 5px;padding: 5px;" class="row">'
                      qtnArr +='<table>'
                      qtnArr +='<tbody><tr>'
                      qtnArr +='<td align="center">'
                      qtnArr +='<img src="/static/Front/dist/assets/svg/svgs/google-docs-icon.svg" alt="Image Description" style="/*! height: 200%; */height: 50px;">'
                      qtnArr +='</td>'
                      qtnArr +='</tr>'
                      qtnArr +='<tr>'
                      qtnArr +='<td align="center">'
                      qtnArr +='<a class="text-dark" href="'+val.filename+'" target="_blank">' +val.filename.split('\\').at(-1) +'</a>'
                      qtnArr +='</td>'
                      qtnArr +='</tr>'
                      qtnArr +='</tbody></table> '
                      qtnArr +='</div>'
                    
                    
                    }
                    qtnArr +=' </div>';
                    qtnArr +=' </div>';
                    qtnArr +='  </div>';
        }
        else if(val.msgcss=='S')
        {

        qtnArr +=' <div class="d-flex chat-message">';
            qtnArr +=' <div class="d-flex mb-2 justify-content-end flex-1">';
            qtnArr +=' <div class="w-100 w-xxl-75">';
            qtnArr +=' <div class="d-flex flex-end-center hover-actions-trigger">';
            qtnArr +=' <div class="d-sm-none hover-actions align-self-center me-2 start-0">';                 
            
                qtnArr +='<div class="bg-white rounded-pill d-flex align-items-center border border-300 px-2 actions">';
                // qtnArr +='<button class="btn p-2" type="button"><span class="fa-solid fa-reply text-primary"></span></button>';
                qtnArr +='<button class="btn p-2" type="button"><span class="fa-solid fa-pen-to-square text-primary"></span></button>';
                // qtnArr +='<button class="btn p-2" type="button"><span class="fa-solid fa-trash text-primary"></span></button>';
                // qtnArr +='<button class="btn p-2" type="button"><span class="fa-solid fa-share text-primary"></span></button>';
                // qtnArr +='<button class="btn p-2" type="button"><span class="fa-solid fa-face-smile text-primary"></span></button>';
                qtnArr +='</div>';
                qtnArr +='</div>';
            qtnArr +='   <div class="d-none d-sm-flex">';
                qtnArr +=' <div class="hover-actions position-relative align-self-center">';
                // qtnArr +=' <button class="btn p-2 fs--2"><span class="fa-solid fa-reply text-primary"></span></button>';
                qtnArr +=' <button class="btn p-2 fs--2" onclick="getCommentforEdit(' + val.Response_id +')" ><span class="fa-solid fa-pen-to-square text-primary" ></span></button>';
                // qtnArr +=' <button class="btn p-2 fs--2"><span class="fa-solid fa-share text-primary"></span></button>';
                // qtnArr +=' <button class="btn p-2 fs--2"><span class="fa-solid fa-trash text-primary"></span></button>';
                // qtnArr +=' <button class="btn p-2 fs--2"><span class="fa-solid fa-face-smile text-primary"></span></button>';
                qtnArr +='  </div>';
                qtnArr +=' </div>';
                qtnArr +=' <div class="chat-message-content me-2">';
                qtnArr +='  <div class="mb-1 sent-message-content light bg-primary rounded-2 p-3 text-white">';
                    qtnArr +=' <p class="mb-0">'+val.Comment+'</p>';
                    qtnArr +=' </div>';
                    qtnArr +='  </div>';
                    qtnArr +=' </div>';
                    qtnArr +=' <div class="text-end">';
                    qtnArr +=' <p class="mb-0 fs--2 text-600 fw-semi-bold">'+val.uinitials +' commented on '+val.createdt+' </p>';
                    qtnArr +=' </div>';
                    if(val.filename!=''){
                      qtnArr +='<div style="background-color: #d0d0d040;width: 50%;float: right;padding-top: 5px;padding-bottom: 5px;padding: 5px;" class="row">'
                      qtnArr +='<table>'
                      qtnArr +='<tbody><tr>'
                      qtnArr +='<td align="center">'
                      qtnArr +='<img src="/static/Front/dist/assets/svg/svgs/google-docs-icon.svg" alt="Image Description" style="/*! height: 200%; */height: 50px;">'
                      qtnArr +='</td>'
                      qtnArr +='</tr>'
                      qtnArr +='<tr>'
                      qtnArr +='<td align="center">'
                      qtnArr +='<a class="text-dark" href="'+val.filename+'" target="_blank">' +val.filename.split('\\').at(-1) +'</a>'
                      qtnArr +='</td>'
                      qtnArr +='</tr>'
                      qtnArr +='</tbody></table> '
                      qtnArr +='</div>'
                    
                    
                    }
                    qtnArr +=' </div>';
                    qtnArr +=' </div>';
                    qtnArr +=' </div> ';
        } 
    })  
    $('#divresp_VT_Comm_Chat').append(qtnArr);
    $('#divresp_VT_Comm_Chat').animate({
      scrollTop: $('#divresp_VT_Comm_Chat').get(0).scrollHeight
  }, 500);
    }
    });
   

}

function showSelectedAttachmentFile(){
  $('#lblFileSelected_VT_Comm_Chat').text('')
  var file  = document.getElementById('chatAttachment-0').files[0]; 
  console.log('file selected')
  if(file != undefined){
    $('#lblFileSelected_VT_Comm_Chat').text(file.name)
  }
}

function update_VT_Dicsussion_Chat(utility,sub_utility,comment,mdl_id,utility_type)
{
  var  filename=''
    var file  = document.getElementById('chatAttachment-0').files[0]; 
    if(file != undefined){
      filename = file.name; 
    } 
    var csrftoken = $("[name=csrfmiddlewaretoken]").val(); 
    var x = new XMLHttpRequest();
    x.open("POST","/insert_VT_Discussion_Comments/",true); 
    x.setRequestHeader( "X-CSRFToken",csrftoken); 
    //x.send('{"comment":"'+comment+'"}');
    var fd = new FormData();
    if(file != undefined){
    fd.append("filename", file,filename);
    
    fd.append("filenm", filename);
    }
    fd.append('utility',utility.replaceAll('&','n'));
    fd.append('comment',  comment);
    fd.append('sub_utility',sub_utility.replaceAll('&','n'));
    fd.append('mdl_id',mdl_id);
    fd.append('chat_data',$('#txtChatData').val())
   //fd.append("myfile", filename );
    x.send(fd);
    x.onreadystatechange = function () { 
        if (x.readyState == 4 && x.status == 200) {
            var data = JSON.parse(x.responseText); 
            if(data.is_taken)
            { 
              sendPerfMonmsg(comment,$('#lblcurruid').text(),9,5,'vt_discussion',mdl_id,JSON.parse(data.data)[0].uinitials+' commented on '+ JSON.parse(data.data)[0].createdt,utility.replaceAll('&','n'),sub_utility,utility_type,data.fileinfo)   
            }
    }
    }
}

function saveReportComment_VT_Comm_Chat(mdl_id)
{ 
$.ajax({ 
    url: '/save_desc_comments/',
    data:{'utility':$("#txtSelUtil").val(),'comment':  $("#txtReportComments_VT_Comm_Chat").val(),'type':$("#txtSelUtilType").val(),'tableType':$("#txtSelSubUtil").val(),'mdl_id':mdl_id,'data_parameter':$('#txtChatData').val()},
    dataType: 'json',
    success: function (data) {
            if(data.is_taken)
            { 
            alert('Comment saved sucessfully.')             
            }   
    }
    });
} 

function enableSave_VT_Comm_Chat(){ 
  if($("#txtReportComments_VT_Comm_Chat").val().length>0){
    $("#btnSave_VT_Comm_Chat").prop("disabled",false)
  }
  else{
    $("#btnSave_VT_Comm_Chat").prop("disabled",true)
  }
}
