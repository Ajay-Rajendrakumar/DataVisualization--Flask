$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
 $(".navbar a, footer a[href='#Home1']").on('click', function(event) {
    if (this.hash !== "") {
     event.preventDefault();
     var hash = this.hash;
    $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function(){
            window.location.hash = hash;
      });
    }
  });
});
$("#go").click(function() {  
    var id = '#dialog';
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();
    $('#mask').css({'width':maskWidth,'height':maskHeight});
    $('#mask').fadeIn(500); 
    $('#mask').fadeTo("slow",0.9);
    var winH = $(window).height();
    var winW = $(window).width();
    $(id).css('top',  winH/2-$(id).height()/2);
    $(id).css('left', winW/2-$(id).width()/2);
    $(id).fadeIn(2000);   
  $('.window .close').click(function (e) {
    e.preventDefault();
    window.location.href="{{ url_for('dash') }}";
    $('#mask').hide();
    $('.window').hide();
  });   
  

  $('#mask').click(function () {
    $(this).hide();

    $('.window').hide();
  });

});


