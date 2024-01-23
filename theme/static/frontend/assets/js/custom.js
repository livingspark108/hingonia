// Add sticky and animation classes to the header on scroll
window.addEventListener('scroll', function() {
  var header = document.querySelector('.sticky-header');
  var headerHeight = header.offsetHeight;
  var scrollTop = window.pageYOffset;
  
  if (scrollTop >= 100) {
    header.classList.add('sticky');
    header.classList.add('animate');
  } else {
    header.classList.remove('sticky');
    header.classList.remove('animate');
  }
});


// Show/hide scroll-to-top button on scroll
window.addEventListener('scroll', function() {
  var scrollToTop = document.querySelector('.scroll-to-top');
  if (window.pageYOffset > 200) {
    scrollToTop.classList.add('show');
  } else {
    scrollToTop.classList.remove('show');
  }
});

// Scroll to top on click of scroll-to-top button
document.querySelector('.scroll-to-top').addEventListener('click', function() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

//============ Collage Hover home START ============
$(document).ready(function() {
  $('.collage-1').hover(
    function() {
      $('.collage-desc-box-1 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-1 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function() {
      $('.collage-desc-box-1 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-1 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
  $('.collage-2').hover(
    function() {
      $('.collage-desc-box-2 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-2 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function() {
      $('.collage-desc-box-2 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-2 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
  $('.collage-3').hover(
    function() {
      $('.collage-desc-box-3 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-3 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function() {
      $('.collage-desc-box-3 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-3 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
  $('.collage-4').hover(
    function() {
      $('.collage-desc-box-4 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-4 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function() {
      $('.collage-desc-box-4 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-4 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
});
//============ Collage Hover home END ============

//==========Number
$(document).ready(function() {
  $('.section-number').hover(
    function() {
      // Mouseenter event handler
      $(this).find('img').attr('src', 'assets/images/number-hover.png'); // Change the 'src' attribute of the 'img' tag inside the hovered '.collage-1' element to 'new-image-src.jpg'
    },
    function() {
      // Mouseleave event handler (optional)
      $(this).find('img').attr('src', 'assets/images/number.png'); // Change the 'src' attribute of the 'img' tag inside the hovered '.collage-1' element back to its original value ('original-image-src.jpg')
    }
  );
});


