/* variable loca storage */

// if (localStorage.getItem("catchRange") != null) {
//   $("#daterange-btn span").html(localStorage.getItem("catchRange"));
// } else {
//   $("#daterange-btn span").html(
//     '<i class="fa fa-calendar"></i> Rando de fecha'
//   );
// }

$(".tableSaleProduct").DataTable({
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
    url: "api/v1",
    dataSrc: "",
    deferRender: true,
    retrieve: true,
    processing: true,
  },
  columns: [
    { data: "#" },
    { data: "Imagen" },
    { data: "Descripcion" },
    { data: "Codigo" },
    { data: "Stock" },
    { data: "Acciones" },
  ],
});

$("#create-client").modalForm({
  formURL: "ajax/get/client",
});

$("#form-client").on("submit", function (e) {
  e.preventDefault();
  var uri = "ajax/get/client";
  $.ajax({
    type: "POST",
    url: uri,
    data: $("#form-client").serialize(),
    success: function (response) {
      let row = "";
      row += `<option selected value="${response.client_info.id}">${response.client_info.first_name}</option>`;
      $("#id_fkclient").append(row);
      $("#close").trigger("click");
    },
    error: function (response) {
      console.log(response);
    },
  });
});

// Add product desde la tabla

$(".tableSaleProduct tbody").on("click", "button.addProduct", function () {
  var idproduct = $(this).attr("idProduct");
  $(this).removeClass("btn-primary addProduct");
  $(this).addClass("btn-default");
  $.ajax({
    url: "http://inventory.armaiden.com/dashboard/show/product/api/v4",
    method: "GET",
    data: {
      idproduct: idproduct,
    },
    dataType: "json",
    success: function (data) {
      var description = data[0]["description"];
      var stock = data[0]["stock"];
      var price = data[0]["sale_price"];

      //evitar add product cuanto el stock esta en cero
      if (stock == 0) {
        swal({
          title: "No hay stock disponible",
          type: "error",
          confirmButtonText: "Cerrar",
        });
        $("button[idProduct='" + idproduct + "']").addClass(
          "btn-primary addProduct"
        );
        return;
      }

      $(".newProduct").append(`
        <div class="row" style="padding:5px 15px">
          <div class="col-xs-6" style="padding-right: 0px;">
            <div class="input-group">
              <span class="input-group-addon"><button class="btn btn-danger btn-xs removeProduct" idProduct="${idproduct}"><i class="fa fa-times"></i></button></span>
              <input type="text" class="form-control newDesProduct" idProduct="${idproduct}" name="addProduct" value="${description}" readonly>
            </div>
          </div>
          <div class="col-xs-3 inCount" style="padding-right: 0px;">
            <div class="input-group">
              <input type="text" class="form-control newCountProduct" name="newCountProduct" min="1" value="1" stock="${stock}" newStock="${
        Number(stock) - 1
      }">
            </div>
          </div>
          <div class="col-xs-3 inPrice" style="padding-left: 0px;">
            <div class="input-group">
              <span class="input-group-addon"><i class="ion ion-social-usd"></i></span>
              <input type="text" class="form-control newPriceProduct" name="newPriceProduct" initPrice="${price}" value="${price}" readonly>
            </div>
          </div>
        </div>
      `);
      // suma total de precios
      sumAllPrice();
      addTax();
      listProduct();
      //format price
      $(".newPriceProduct").number(true, 2);
    },
  });
});

// cuando cargue la tabla cada vez que navegue en ella

$(".tableSaleProduct").on("draw.dt", function () {
  if (localStorage.getItem("removeProduct") != null) {
    var listIdProduct = JSON.parse(localStorage.getItem("removeProduct"));
    for (var i = 0; i < listIdProduct.length; i++) {
      $(
        "button.recoveryButton[idProduct='" + listIdProduct[i]["idpro"] + "']"
      ).removeClass("btn-default");
      $(
        "button.recoveryButton[idProduct='" + listIdProduct[i]["idpro"] + "']"
      ).addClass("btn-primary addProduct");
    }
  }
});

// eliminar productos
var idQuitarProduct = [];
$(".formSale").on("click", "button.removeProduct", function () {
  $(this).parent().parent().parent().parent().remove();
  var idpro = $(this).attr("idProduct");
  // almacenar en el local storage el id de producto
  if (localStorage.getItem("removeProduct") == null) {
    idQuitarProduct = [];
  } else {
    idQuitarProduct.concat(localStorage.getItem("removeProduct"));
  }
  idQuitarProduct.push({
    idpro: idpro,
  });
  localStorage.setItem("removeProduct", JSON.stringify(idQuitarProduct));

  $("button.recoveryButton[idProduct='" + idpro + "']").removeClass(
    "btn-default"
  );
  $("button.recoveryButton[idProduct='" + idpro + "']").addClass(
    "btn-primary addProduct"
  );
  if ($(".newProduct").children().length == 0) {
    // $("#newTotalSale").val(0);
    $("#id_new_total_sale").val(0);
    $("#totalSale").val(0);
    // $("#newTaxSale").val(0);
    $("#id_new_tax_sale").val(0);
    // $("#newTotalSale").attr("total", 0);
    $("#id_new_total_sale").attr("total", 0);
  } else {
    // suma total de precios
    sumAllPrice();
    addTax();
    listProduct();
  }
});

// Agregar productos desde  dispositivos moviles
var numProduct = 0;

$(".btnAddProduct").click(function () {
  numProduct++;
  $.ajax({
    url: "http://inventory.armaiden.com/dashboard/show/product/api/v5",
    method: "GET",
    dataType: "json",
    success: function (data) {
      $(".newProduct").append(`
        <div class="row" style="padding:5px 15px">
          <div class="col-xs-6" style="padding-right: 0px;">
            <div class="input-group">
              <span class="input-group-addon"><button class="btn btn-danger btn-xs removeProduct" idProduct><i class="fa fa-times"></i></button></span>
              <select class="form-control newDesProduct addProduct" id="product${numProduct}" idProduct name="newDesProduct" required>
                <option>Seleccione Producto</option>
              </select>
            </div>
          </div>
          <div class="col-xs-3 inCount" style="padding-right: 0px;">
            <div class="input-group">
              <input type="text" class="form-control newCountProduct" name="newCountProduct" min="1" value="1" stock newStock>
            </div>
          </div>
          <div class="col-xs-3 inPrice" style="padding-left: 0px;">
            <div class="input-group">
              <span class="input-group-addon"><i class="ion ion-social-usd"></i></span>
              <input type="text" class="form-control newPriceProduct" initPrice name="newPriceProduct">
            </div>
          </div>
        </div>
      `);
      data.forEach(functionForEach);
      function functionForEach(item, index) {
        // console.log(item.id);
        if (item.stock != 0) {
          $("#product" + numProduct).append(
            `<option idProduct="${item.id}" value="${item.id}">${item.description}</option>`
          );
        }
      }
      // suma total de precios
      sumAllPrice();
      addTax();
      $(".newPriceProduct").number(true, 2);
    },
  });
});

// seleccionar producto

$(".formSale").on("change", "select.newDesProduct", function () {
  var idproduct = $(this).val();
  var newPriceProduct = $(this)
    .parent()
    .parent()
    .parent()
    .children(".inPrice")
    .children()
    .children(".newPriceProduct");
  var newCountProduct = $(this)
    .parent()
    .parent()
    .parent()
    .children(".inCount")
    .children()
    .children(".newCountProduct");
  $.ajax({
    url: "http://inventory.armaiden.com/dashboard/show/product/api/v4",
    method: "GET",
    data: {
      idproduct: idproduct,
    },
    dataType: "json",
    success: function (data) {
      $(newCountProduct).attr("stock", data[0]["stock"]);
      $(newCountProduct).attr("newStock", Number(data[0]["stock"] - 1));
      $(newPriceProduct).val(data[0]["sale_price"]);
      $(newPriceProduct).attr("initPrice", data[0]["sale_price"]);
      listProduct();
    },
  });
});

// modificar cantidad

$(".formSale").on("change", "input.newCountProduct", function () {
  var price = $(this)
    .parent()
    .parent()
    .parent()
    .children(".inPrice")
    .children()
    .children(".newPriceProduct");
  var priceFinal = $(this).val() * price.attr("initPrice");
  price.val(priceFinal);
  var newStock = Number($(this).attr("stock")) - $(this).val();
  $(this).attr("newStock", newStock);
  if (Number($(this).val()) > Number($(this).attr("stock"))) {
    // si la cantidad es superior al stock regresa valores iniciales
    $(this).val(1);
    var priceFinal = $(this).val() * price.attr("initPrice");
    price.val(priceFinal);
    // sumAllPrice();
    swal({
      title: "La cantidad supera el stock",
      text: "Solo hay" + $(this).attr("stock") + " unidades!",
      type: "error",
      confirmButtonText: "Cerrar!",
    });
  }
  // suma total de precios
  sumAllPrice();
  addTax();
  listProduct();
});

// sumar todos los precios
function sumAllPrice() {
  var priceItem = $(".newPriceProduct");
  var arraySumPrice = [];
  for (var i = 0; i < priceItem.length; i++) {
    arraySumPrice.push(Number($(priceItem[i]).val()));
  }
  function sumArrayPrices(total, num) {
    return total + num;
  }
  var sumTotalPrice = arraySumPrice.reduce(sumArrayPrices);
  // $("#newTotalSale").val(sumTotalPrice);
  $("#id_new_total_sale").val(sumTotalPrice);
  $("#totalSale").val(sumTotalPrice);
  // $("#newTotalSale").attr("total", sumTotalPrice);
  $("#id_new_total_sale").attr("total", sumTotalPrice);
}

// function agregar impuesto

function addTax() {
  // var tax = $("#newTaxSale").val();
  var tax = $("#id_new_tax_sale").val();
  // var priceTotal = $("#newTotalSale").attr("total");
  var priceTotal = $("#id_new_total_sale").attr("total");
  var priceTax = Number((priceTotal * tax) / 100);
  var totalWithTax = Number(priceTax) + Number(priceTotal);
  // $("#newTotalSale").val(totalWithTax);
  $("#id_new_total_sale").val(totalWithTax);
  $("#totalSale").val(totalWithTax);
  $("#newPriceTax").val(priceTax);
  $("#newPriceNet").val(priceTotal);
}

// $("#newTaxSale").change(function () {
//   addTax();
// });
$("#id_new_tax_sale").change(function () {
  addTax();
});
// add format
// $("#newTotalSale").number(true, 2);
$("#id_new_total_sale").number(true, 2);

// select method pay

$("#id_new_method_pay").change(function () {
  // $("#newMethodPay").change(function () {
  var method = $(this).val();
  if (method == "efectivo") {
    $(this).parent().parent().removeClass("col-xs-6");
    $(this).parent().parent().addClass("col-xs-4");
    $(this).parent().parent().parent().children(".boxMethodPay").html(`
    <div class="col-xs-4">
      <div class="input-group">
        <span class="input-group-addon"><i class="ion ion-social-usd"></i></span>
        <input type="text" class="form-control" id="newValueMoney" name="newValueMoney" placeholder="00000" required>
      </div>
    </div>
    <div class="col-xs-4" id="catchChangeMoney" style="padding-left: 0px;">
      <div class="input-group">
        <span class="input-group-addon"><i class="ion ion-social-usd"></i></span>
        <input type="text" class="form-control" id="newChangeMoney" name="newChangeMoney" placeholder="00000" readonly>
      </div>
    </div>
    `);
    $("#newValueMoney").number(true, 2);
    $("#newChangeMoney").number(true, 2);
    listMethod();
  } else {
    $(this).parent().parent().removeClass("col-xs-4");
    $(this).parent().parent().addClass("col-xs-6");
    $(this).parent().parent().parent().children(".boxMethodPay").html(`
    <div class="col-xs-6" style="padding-left:0px">
      <div class="input-group">
      <input type="text" class="form-control" id="newCodeTransaction" placeholder="Código transacción" required>
      <span class="input-group-addon"><i class="fa fa-lock"></i></span>
      </div>
    </div>
    `);
  }
});

// cambio en efectivo

$(".formSale").on("change", "input#newValueMoney", function () {
  var money = $(this).val();
  // var change = Number(money) - Number($("#newTotalSale").val());
  var change = Number(money) - Number($("#id_new_total_sale").val());
  var newChangeMoney = $(this)
    .parent()
    .parent()
    .parent()
    .children("#catchChangeMoney")
    .children()
    .children("#newChangeMoney");
  newChangeMoney.val(change);
});

// cambio transaccion

$(".formSale").on("change", "input#newCodeTransaction", function () {
  listMethod();
});

// listar productos
function listProduct() {
  var listProducts = [];
  var description = $(".newDesProduct");
  var count = $(".newCountProduct");
  var price = $(".newPriceProduct");

  for (var i = 0; i < description.length; i++) {
    listProducts.push({
      id: $(description[i]).attr("idProduct"),
      description: $(description[i]).val(),
      count: $(count[i]).val(),
      stock: $(count[i]).attr("newStock"),
      price: $(price[i]).attr("initPrice"),
      total: $(price[i]).val(),
    });
  }
  $("#listProduct").val(JSON.stringify(listProducts));
}

// medodo pago

function listMethod() {
  var listMethod = "";
  if ($("#id_new_method_pay").val() == "efectivo") {
    // if ($("#newMethodPay").val() == "efectivo") {
    $("#listMethodPay").val("Efectivo");
  } else {
    $("#listMethodPay").val(
      $("#id_new_method_pay").val() + "-" + $("#newCodeTransaction").val()
      // $("#newMethodPay").val() + "-" + $("#newCodeTransaction").val()
    );
  }
}

$("#daterange-btn").daterangepicker(
  {
    ranges: {
      Hoy: [moment(), moment()],
      Ayer: [moment().subtract(1, "days"), moment().subtract(1, "days")],
      "Ultimos 7 dias": [moment().subtract(6, "days"), moment()],
      "Ultimos 30 dias": [moment().subtract(29, "days"), moment()],
      "Este mes": [moment().startOf("month"), moment().endOf("month")],
      "Ultimo mes": [
        moment().subtract(1, "month").startOf("month"),
        moment().subtract(1, "month").endOf("month"),
      ],
    },
    startDate: moment().subtract(29, "days"),
    endDate: moment(),
  },
  function (start, end) {
    $("#daterange-btn span").html(
      start.format("MMMM D, YYYY") + "- " + end.format("MMMM D, YYYY")
    );
    var initDate = start.format("YYYY-M-D");
    var endDate = end.format("YYYY-M-D");
    var catchRange = $("#daterange-btn span").html();

    localStorage.setItem("catchRange", catchRange);
  }
);

/* cancelar rango de fecha*/
// $(".daterangepicker .range_inputs .cancelBtn").on("click", function () {
//   localStorage.removeItem("catchRange");
//   localStorage.clear();
//   window.location = "sale";
// });
