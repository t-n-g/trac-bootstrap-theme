$(function() {
  /*
   * "PAGE TOP" ボタン制御
   */
  var pageTop = $('#page-top');
  pageTop.hide();

  // ボタン表示を制御
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      pageTop.fadeIn();
    } else {
      pageTop.fadeOut();
    }
  });

  // 移動アニメーションを制御
  pageTop.click(function() {
    $('body,html').animate({
      scrollTop: 0
    }, 500);
    return false;
  });

  /*
   * コンテキストメニュー表示を制御
   */
  var ctxNav = $('#ctxnav'),
      offset  = ctxNav.offset();

  $(window).scroll(function() {
    if ($(window).scrollTop() > offset.top) {
      ctxNav.addClass('ctxnav-fixed container-fluid');
      ctxNav.removeClass('container');

      $('#ctxnav-shadow').addClass('ctxnav-fixed');
    } else {
      ctxNav.addClass('container');
      ctxNav.removeClass('ctxnav-fixed container-fluid');
      
      $('#ctxnav-shadow').removeClass('ctxnav-fixed');
    }
  });
});

