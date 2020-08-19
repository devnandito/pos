// $("#daterange-btn2").daterangepicker(
//   {
//     ranges: {
//       Hoy: [moment(), moment()],
//       Ayer: [moment().subtract(1, "days"), moment().subtract(1, "days")],
//       "Ultimos 7 dias": [moment().subtract(6, "days"), moment()],
//       "Ultimos 30 dias": [moment().subtract(29, "days"), moment()],
//       "Este mes": [moment().startOf("month"), moment().endOf("month")],
//       "Ultimo mes": [
//         moment().subtract(1, "month").startOf("month"),
//         moment().subtract(1, "month").endOf("month"),
//       ],
//     },
//     startDate: moment().subtract(29, "days"),
//     endDate: moment(),
//   },
//   function (start, end) {
//     $("#daterange-btn2 span").html(
//       start.format("MMMM D, YYYY") + "- " + end.format("MMMM D, YYYY")
//     );
//     var initDate = start.format("YYYY-M-D");
//     var endDate = end.format("YYYY-M-D");
//     var catchRange = $("#daterange-btn2 span").html();

//     localStorage.setItem("catchRange2", catchRange);
//   }
// );

// /* cancelar rango de fecha*/
// $(".daterangepicker.opensleft .range_inputs .cancelBtn").on(
//   "click",
//   function () {
//     localStorage.removeItem("catchRange2");
//     localStorage.clear();
//     window.location = "sale";
//   }
// );

// $(".daterangepicker.openleft .ranges li").on("click", function () {
//   var textToday = $(this).attr("data-range-key");
//   if (textToday == "Hoy") {
//     var d = new Date();
//     var day = d.getDate();
//     var month = d.getMonth() + 1;
//     var year = d.getFullYear();
//     var initialDate = year + "-" + month + "-" + day;
//     var endDate = year + "-" + month + "-" + day;
//     localStorage.setItem("cachRange2", "Hoy");
//     windows.location = "report";
//   }
// });

// $(".getData").ready(function () {
//   var uri = "report/api/v6";
//   $.ajax({
//     type: "GET",
//     url: uri,
//     success: function (response) {
//       a = response.data_sale;
//       let txt = "";
//       for (x = 0; x < a.length; x++) {
//         txt += `<p>${a[x]["Invoice"]} ${a[x]["id"]}</p>`;
//       }
//       $(".getData").append(txt);
//     },
//     error: function (response) {
//       console.log(response);
//     },
//   });
// });
