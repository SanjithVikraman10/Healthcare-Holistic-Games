var count = 0;

$(".digit").on("click", function () {
  var num = $(this).clone().children().remove().end().text();
  if (count < 54) {
    $("#output").append("<span>" + num.trim() + "</span>");
    count++;
  }
});

$(".fa-long-arrow-left").on("click", function () {
  $("#output span:last-child").remove();
  count--;
});

$("#call").on("click", function () {
  var enteredNumber = $("#output").text();
  console.log("Entered Number:", enteredNumber);
    dialHelpline();
});