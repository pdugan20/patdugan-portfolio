$(function() {
    $('.image_wrapper').fluidbox();
});

function playVideo(video) {
    if (video.paused) {
        video.play();
    } else {
        video.pause();
    }
}

$(function(){
   $('.play_link').click(function () {
      $(this).text(function(i, text){
          return text === 'Play video' ? 'Pause video' : 'Play video';
      })
   });
})
