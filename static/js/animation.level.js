// $("#formAddLevel").on("submit", function (e) {
//   e.preventDefault();
//   $.ajax({
//     type: "POST",
//     url: 'ajax/level',
//     data:{
//       description:$('#description').val(),
//       csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//       action: 'post'
//     },
//     success: function (response) {
//       console.log(response)
//       swal({
//         type: "success",
//         text: "El nivel se ha actualizado",
//         showConfimButton: true,
//         confirmButtonText: "Cerrar",
//         }).then((result) => {
//             if(result.value){
//               window.location = '../show/level'
//             }
//         })
//     },
//     error: function (response) {
//       console.log(response);
//     },
//   });
// });




// $('#editLevel').on('submit', function(event){
//     event.preventDefault();
//     alert("{% url 'levels:show' %}")
//     console.log("form submitted!")
//     swal({
//         type: "success",
//         text: "El nivel se ha actualizado",
//         showConfimButton: true,
//         confirmButtonText: "Cerrar",
//         }).then((result) => {
//             if(result.value){
//                 window.location = "{% url 'levels:show' %}"
//             }
//         })
// });

//$("#editLevel").on("click", function() {
//  console.log('Se ha actualizado el nivel');
//});

//$("#editLevel").submit(function(event){
//  alert("Handler for .submit() called.");
//  event.preventDefault();
//});

// $("#btnEditLevel").click(function(){        
//   //console.log('Datos actualizados');
//   swal({
//     text: "El nivel se ha actualizado",
//     showConfimButton: true,
//     confirmButtonText: "Cerrar",
//     type: "success",
//   }).then((okay) => {
//     if(okay){
//       $("#formEditLevel").submit();
//     }
//   })
// });



//swal({ title: "WOW!",
// text: "Message!",
// type: "success"}).then(okay => {
//   if (okay) {
//    window.location.href = "URL";
//  }
//});
