// Capturar foto

$("#id_picture").change(function () {
  var img = this.files[0];

  // validar formato

  if (img["type"] != "image/jpeg" && img["type"] != "image/png") {
    $("#id_picture").val("");

    swal({
      title: "Error al subir la imagen",
      text: "La imagen debe estar en formato JPG O PGN!",
      type: "error",
      confirmButtonText: "Cerrar",
    });
  } else if (img["size"] > 2000000) {
    $("#id_picture").val("");

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
