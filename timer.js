function updateTimer() {
    var endDate = new Date("2024-12-31 23:59:59"); // Укажите дату окончания акции
    var now = new Date();
    var diff = endDate - now;
  
    if (diff <= 0) {
      clearInterval(timerInterval);
      document.getElementById("timer").innerHTML = "Акция завершена!";
    } else {
      var days = Math.floor(diff / (1000 * 60 * 60 * 24));
      var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((diff % (1000 * 60)) / 1000);
  
      document.getElementById("timer").innerHTML = days + "д " + hours + "ч "
        + minutes + "м " + seconds + "с ";
    }
  }
  
  updateTimer();
  var timerInterval = setInterval(updateTimer, 1000);
  