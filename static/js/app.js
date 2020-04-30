
// sidevbar menu
$(".sidebar-menu").tree();

// Datatable

$(".tablas").DataTable({
  "language": {
      "sProcessing":     "Procesando...",
      "sLengthMenu":     "Mostrar _MENU_ registros",
      "sZeroRecords":    "No se encontraron resultados",
      "sEmptyTable":     "Ningún dato disponible en esta tabla",
      "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_",
      "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0",
      "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
      "sInfoPostFix":    "",
      "sSearch":         "Buscar:",
      "sUrl":            "",
      "sInfoThousands":  ",",
      "sLoadingRecords": "Cargando...",
      "oPaginate": {
      "sFirst":    "Primero",
      "sLast":     "Último",
      "sNext":     "Siguiente",
      "sPrevious": "Anterior"
      },
      "oAria": {
          "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
          "sSortDescending": ": Activar para ordenar la columna de manera descendente"
      }
  }
});

$("#create-level").modalForm({
  formURL: "ajax/get/level",
});

$("#form-level").on("submit", function (e) {
  e.preventDefault();
  var uri = "ajax/get/level";
  $.ajax({
    type: "POST",
    url: uri,
    data: $("#form-level").serialize(),
    success: function (response) {
      let row = ''
      row += `<option selected value="${response.level_info.id}">${response.level_info.description}</option>`
      $("#id_level").append(row)
      $("#close").trigger("click");
    },
    error: function (response) {
      console.log(response);
    },
  });
});

// $("#create-user").modalForm({
//   formURL: "ajax/get/user",
// });

// $("#form-user").on("submit", function (e) {
//   e.preventDefault();
//   var uri = "ajax/get/user";
//   $.ajax({
//     type: "POST",
//     url: uri,
//     data: $("#form-user").serialize(),
//     success: function (response) {
//       let row = "";
//       row += `<tr><td>${response.user_info.id}</td>
//       <td>${response.user_info.username}</td>
//       <td>${response.user_info.email}</td>
//       <td>${response.user_info.first_name}</td>
//       <td>${response.user_info.last_name}</td>
//       </tr>`
//       console.log(response.user_info);
//       $("table tbody").append(row);
//       $("#close").trigger("click");
//     },
//     error: function (response) {
//       console.log(response);
//     },
//   });
// });
