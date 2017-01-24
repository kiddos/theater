function setVideoSize() {
  $('#video').width($(window).width() - 12);
  $('#video').height($('#video').width() * 9 / 16);
}

$(document).ready(function() {
  // video size
  setVideoSize();
  $(window).resize(setVideoSize);
  $('.movie-link').on('click', 'a', function(event) {
    event.preventDefault();
    $('.movie-link').hide();

    var link = $(this).attr('href');
    $('#video').fadeIn(300, function() {
      setVideoSize();
      $('#video-source').get(0).src = link;
      $('#video-source').get(0).type = 'video/mp4';
      var video = $(this).get(0);
      video.load();
      video.play();
    });
  });

  // drop-up / drop-down
  $('#drop').on('click', function() {
    if ($('.movie-link').css('display') != 'none') {
      $('#icon').css({
        'transform': 'rotate(180deg)',
        'persist': true
      });
      $('.movie-link').fadeOut(600, function() {
        $('#video').fadeIn(300);
        setVideoSize();
      });
    } else {
      $('#icon').css({'transform': 'rotate(360deg)'});
      $('#video').fadeOut(300, function() {
        $('.movie-link').fadeIn(600);
      });
    }
  });
});