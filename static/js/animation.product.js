$(".tableProduct").DataTable({
  language: {
    sProcessing: "Procesando...",
    sLengthMenu: "Mostrar _MENU_ registros",
    sZeroRecords: "No se encontraron resultados",
    sEmptyTable: "Ningún dato disponible en esta tabla",
    sInfo: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_",
    sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0",
    sInfoFiltered: "(filtrado de un total de _MAX_ registros)",
    sInfoPostFix: "",
    sSearch: "Buscar:",
    sUrl: "",
    sInfoThousands: ",",
    sLoadingRecords: "Cargando...",
    oPaginate: {
      sFirst: "Primero",
      sLast: "Último",
      sNext: "Siguiente",
      sPrevious: "Anterior",
    },
    oAria: {
      sSortAscending: ": Activar para ordenar la columna de manera ascendente",
      sSortDescending:
        ": Activar para ordenar la columna de manera descendente",
    },
  },
  ajax: {
    // url: "http://inventory.armaiden.com/dashboard/show/product/api/v1",
    url: "product/api/v1",
    dataSrc: "",
    deferRender: true,
    retrieve: true,
    processing: true,
  },
  columns: [
    { data: "#" },
    { data: "Imagen" },
    { data: "Descripcion" },
    { data: "Categoria" },
    { data: "Codigo" },
    { data: "Precio compra" },
    { data: "Precio venta" },
    { data: "Stock" },
    { data: "Acciones" },
  ],
});

// $('#id_code').attr('readonly', true);
// $('#id_code').prop("checked", false);
$('#id_code').prop('readonly', true);

$("#id_fkcategory").change(function () {
  var fkcategory = $(this).val();
  if( fkcategory == ''){
    fkcategory = 0;
  }
  $.ajax({
    url: "http://inventory.armaiden.com/dashboard/show/product/api/v3",
    // url: "../show/product/api/v3",
    method: "GET",
    data: {
      fkcategory: fkcategory,
    },
    dataType: "json",
    success: function (data) {
      if (data[0]['id']=='null') {
        var newCode = Number(data[0]["codigo"])
        $("#id_code").val(newCode);
        // console.log(newCode);
      } else {
        var newCode = Number(data[0]["codigo"])+1;
        $("#id_code").val(newCode);
        // console.log(newCode);
      }
    },
  });
});



// Capturar foto

$("#id_image").change(function () {
  var img = this.files[0];

  // validar formato

  if (img["type"] != "image/jpeg" && img["type"] != "image/png") {
    $("#id_image").val("");

    swal({
      title: "Error al subir la imagen",
      text: "La imagen debe estar en formato JPG O PGN!",
      type: "error",
      confirmButtonText: "Cerrar",
    });
  } else if (img["size"] > 2000000) {
    $("#id_image").val("");

    swal({
      title: "Error al subir la imagen",
      text: "La imagen no debe pesar mas de 2MB!",
      type: "error",
      confirmButtonText: "Cerrar",
    });
  } else {
    var dataImg = new FileReader();
    dataImg.readAsDataURL(img);
    $(dataImg).on("load", function (event) {
      var pathImg = event.target.result;
      $(".preview").attr("src", pathImg);
    });
  }
});


// $("#id_fkcategory").change(function () {
//   var fkcategory = $(this).val();
//   console.log(fkcategory);
//   $.ajax({
//     url:
//       "http://inventory.armaiden.com/dashboard/show/product/api/v2/" +
//       fkcategory,
//     dataType: "json",
//     success: function (data) {
//       console.log(data);
//     },
//   });
// });

// $.ajax({
//     url: "http://inventory.armaiden.com/static/js/example.txt",
//     success: function(response){
//         console.log(response);
//     }
// })

// $.ajax({
//     url: "http://inventory.armaiden.com/dashboard/show/product/api/v2",
//     success: function(response){
//         var array = response;
//         var arrayToString = JSON.stringify(Object.assign({}, array));
//         var stringToSjonObject = JSON.parse(arrayToString);
//         console.log(stringToSjonObject);
//         $(".tableProduct").DataTable({
//             "ajax": stringToSjonObject
//         });
//     }
// })
