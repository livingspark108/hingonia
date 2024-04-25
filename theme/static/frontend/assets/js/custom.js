// Add sticky and animation classes to the header on scroll
window.addEventListener('scroll', function () {
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

function calculate_total(){
    var qty = $('#quantityInput').val()
    var amt_vl = $('.active').attr('data-amount');
    var total = qty * amt_vl
    $('.amt_vl').val(total)
    $('.amt').html(total)

}

// Show/hide scroll-to-top button on scroll
window.addEventListener('scroll', function () {
  var scrollToTop = document.querySelector('.scroll-to-top');
  if (window.pageYOffset > 200) {
    scrollToTop.classList.add('show');
  } else {
    scrollToTop.classList.remove('show');
  }
});

// Scroll to top on click of scroll-to-top button
document.querySelector('.scroll-to-top').addEventListener('click', function () {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

//============ Collage Hover home START ============
$(document).ready(function () {
  $('.collage-1').hover(
    function () {
      $('.collage-desc-box-1 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-1 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function () {
      $('.collage-desc-box-1 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-1 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
  $('.collage-2').hover(
    function () {
      $('.collage-desc-box-2 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-2 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function () {
      $('.collage-desc-box-2 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-2 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
  $('.collage-3').hover(
    function () {
      $('.collage-desc-box-3 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-3 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function () {
      $('.collage-desc-box-3 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-3 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
  $('.collage-4').hover(
    function () {
      $('.collage-desc-box-4 .clg-desc span').addClass('collageSpanHover');
      $('.collage-desc-box-4 .clg-btn').addClass('collageBtnHover');
      $(this).find('img').addClass('collageImgHover');
    },
    function () {
      $('.collage-desc-box-4 .clg-desc span').removeClass('collageSpanHover');
      $('.collage-desc-box-4 .clg-btn').removeClass('collageBtnHover');
      $(this).find('img').removeClass('collageImgHover');
    }
  );
});
//============ Collage Hover home END ============

//==========Number
$(document).ready(function () {
  $('.section-number').hover(
    function () {
      // Mouseenter event handler
      $(this).find('img').attr('src', '/static/frontend/assets/images/number-hover.png'); // Change the 'src' attribute of the 'img' tag inside the hovered '.collage-1' element to 'new-image-src.jpg'
    },
    function () {
      // Mouseleave event handler (optional)
      $(this).find('img').attr('src', '/static/frontend/assets/images/number.png'); // Change the 'src' attribute of the 'img' tag inside the hovered '.collage-1' element back to its original value ('original-image-src.jpg')
    }
  );
});



 document.getElementById('plusBtn').addEventListener('click', function () {
   var input = document.getElementById('quantityInput');
   var value = parseInt(input.value, 10);
   input.value = isNaN(value) ? 1 : value + 1;
   calculate_total()
 });

 document.getElementById('minusBtn').addEventListener('click', function () {
   var input = document.getElementById('quantityInput');
   var value = parseInt(input.value, 10);
   input.value = isNaN(value) || value < 2 ? 1 : value - 1;
   calculate_total()
 });


$(document).ready(function () {
  $(".plusBtn").on("click", function () {
    var input = $(this).prev(".quantityInput");
    var currentValue = parseInt(input.val());
    input.val(currentValue + 1);
  });

  $(".minusBtn").on("click", function () {
    var input = $(this).next(".quantityInput");
    var currentValue = parseInt(input.val());
    if (currentValue > 1) {
      input.val(currentValue - 1);
    }
  });
});



//======== Mataji Popup custom amount =====
const checkbox = document.getElementById('customAmountCheckbox');
const customAmountBox = document.querySelector('.custom-amount-box');
if(checkbox){
checkbox.addEventListener('change', function () {
  if (this.checked) {
    $(customAmountBox).show(500);

    //customAmountBox.style.display = 'block';
  } else {
    var amt = $('.active').attr('data-amount');
    $('.amt').html(amt)
    $('.amt_vl').val(amt)
    $(customAmountBox).hide(500);
    //customAmountBox.style.display = 'none';
  }
});
}
$(document).on("change",".ctm_amount",function() {
    var vv = $(this).val()
    $('.amt').html(vv)
    $('.amt_value').val(vv)
})