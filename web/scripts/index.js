$(function () {
  $("input#input-image").on("change", function (e) {
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function () {
      $("img#image-preview").attr("src", reader.result);
    };
  });

  $("button#start-button").on("click", function (_e) {
    if (!$("input#input-image").val()) return;

    let reader = new FileReader();
    reader.readAsDataURL($("input#input-image")[0].files[0]);
    reader.onload = function () {
      let url = `http://${window.location.hostname}:8001/count`
      if (window.location.hostname.endsWith("asse.devtunnels.ms")) {
        url = window.location.href.replace("https", "http").replace("8000", "8001") + "count"
      }
      $.ajax({
        url: url,
        method: "POST",
        data: JSON.stringify({
          image: reader.result,
        }),
        success: function (data) {
          $("span#output").html("试卷总数：" + data.count);
        },
      });
    }
  });
});
