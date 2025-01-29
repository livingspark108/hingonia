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


var swiper = new Swiper(".bannerSwiper", {
  spaceBetween: 30,
  centeredSlides: true,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});


var swiper = new Swiper(".campaignSwiper", {
  slidesPerView: 1,
  spaceBetween: 10,
  // autoplay: {
  //   delay: 2500,
  //   disableOnInteraction: false,
  // },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  breakpoints: {
    320: {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    576: { 
      slidesPerView: 2,
      spaceBetween: 10,
    },
    768: { 
      slidesPerView: 2,
      spaceBetween: 20,
    },
    992: {
      slidesPerView: 4,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 4,
      spaceBetween: 20,
    },
  },

});


var swiper = new Swiper(".testimonialsSwiper", {
  slidesPerView: 4,
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    450: { 
      slidesPerView: 2,
      spaceBetween: 10,
    },
    768: { 
      slidesPerView: 3,
      spaceBetween: 20,
    },
    992: {
      slidesPerView: 4,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 4,
      spaceBetween: 20,
    },
  },

});


var swiper = new Swiper(".heavenCowSwiper", {
  slidesPerView: 3.7, 
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    576: { 
      slidesPerView: 1.7,
      spaceBetween: 10,
    },
    768: { 
      slidesPerView: 2,
      spaceBetween: 20,
    },
    992: {
      slidesPerView: 3.7,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 3.7,
      spaceBetween: 20,
    },
  },
});



var swiper = new Swiper(".sustainableSwiper", {
  slidesPerView: 3.7, 
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    576: { 
      slidesPerView: 1.7,
      spaceBetween: 10,
    },
    768: { 
      slidesPerView: 2,
      spaceBetween: 20,
    },
    992: {
      slidesPerView: 3.7,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 3.7,
      spaceBetween: 20,
    },
  },
});


var swiper = new Swiper(".trusteeSwiper", {
  slidesPerView: 3,
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    480: { 
      slidesPerView: 2,
      spaceBetween: 10,
    },
    600: { 
      slidesPerView: 3,
      spaceBetween: 10,
    },
    768: { 
      slidesPerView: 3,
      spaceBetween: 20,
    },
    992: {
      slidesPerView: 3,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 3,
      spaceBetween: 20,
    },
  },
});


var swiper = new Swiper(".factSwiper", {
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
  },
});


var swiper = new Swiper(".objectiveCowSwiper", {
  slidesPerView: 3.7, 
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: {
      slidesPerView: 1,
      spaceBetween: 10,
    },
    576: { 
      slidesPerView: 1.7,
      spaceBetween: 10,
    },
    768: { 
      slidesPerView: 2,
      spaceBetween: 20,
    },
    992: {
      slidesPerView: 3.7,
      spaceBetween: 20,
    },
    1200: {
      slidesPerView: 3.7,
      spaceBetween: 25,
    },
  },
});


// Event Box
// Event Box
document.addEventListener("DOMContentLoaded", function() {
  const checkboxes = document.querySelectorAll('.eventCheckbox');
  checkboxes.forEach(checkbox => {
    checkbox.checked = false;
  });
});

$(document).on("change",".cps-radio",function() {
  console.log("Test Test")
  $('.cps-amount-radio label').removeClass('cps-active');
  $(this).siblings('.cps-amount-radio label').addClass('cps-active');
});


function selectEvent(selectedCheckbox) {
  const checkboxes = document.querySelectorAll('.eventCheckbox');

  checkboxes.forEach(checkbox => {
    if (checkbox !== selectedCheckbox) {
      checkbox.checked = false;
      checkbox.closest('.eventBox').classList.remove('active');
    }
  });

  if (selectedCheckbox.checked) {
    selectedCheckbox.closest('.eventBox').classList.add('active');
  } else {
    selectedCheckbox.closest('.eventBox').classList.remove('active');
  }
}





document.addEventListener('DOMContentLoaded', function () {
  var swiper = new Swiper(".gallerySwiper", {
    effect: "cards",
    grabCursor: true,
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
  });

  // Add click event listener to each Swiper slide
//  document.querySelectorAll('.swiper-slide').forEach(function(slide) {
//    slide.addEventListener('click', function() {
//      if (swiper.isEnd) {
//        swiper.slideTo(0);
//      } else {
//        swiper.slideNext();
//      }
//    });
//  });
});




  var swiper = new Swiper(".CSRSwiper", {
    spaceBetween: 10,
    slidesPerView: 9,
    freeMode: true,
    watchSlidesProgress: true,
  });

  var swiper2 = new Swiper(".CSRSwiper2", {
    spaceBetween: 10,
      autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    thumbs: {
      swiper: swiper,
    },
  });



document.addEventListener('DOMContentLoaded', () => {
    const indianBtn = document.getElementById('indian-btn');
    const nonIndianBtn = document.getElementById('non-indian-btn');

    const buttons = document.querySelectorAll('.countryBtn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            buttons.forEach(btn => btn.classList.remove('active')); // Remove active class from all buttons
            button.classList.add('active'); // Add active class to the clicked button
        });
    });

    // Set initial active button if it exists
    if (indianBtn) {
        indianBtn.classList.add('active');
    }
});




// Quantity

$(document).ready(function () {
  // Event delegation for dynamically added .add-button
  $(document).on('click', '.add-button', function () {
    const cardDonate = $(this).closest('.card_donate');
    const buttonContainer = cardDonate.find('.add_button');
    const quantityContainer = cardDonate.find('.quantity-container');

    if (buttonContainer.length && quantityContainer.length) {
      buttonContainer.hide();
      quantityContainer.css('display', 'flex');
    }
  });

  // Increment and decrement button handling
  $(document).on('click', '.decrement-btn', function () {
    const cardDonate = $(this).closest('.card_donate');
    const quantityValue = cardDonate.find('.quantity-value');
    let quantity = parseInt(quantityValue.text());

    if (quantity > 0) {
      quantity--;
      quantityValue.text(quantity);
    }
  });

  $(document).on('click', '.increment-btn', function () {
    const cardDonate = $(this).closest('.card_donate');
    const quantityValue = cardDonate.find('.quantity-value');
    let quantity = parseInt(quantityValue.text());

    quantity++;
    quantityValue.text(quantity);
  });

  // Handle enter button logic
  $(document).on('click', '.enter-button', function () {
    const cardDonate = $(this).closest('.card_donate');
    const quantityValue = parseInt(cardDonate.find('.quantity-value').text());
    const quantityContainer = cardDonate.find('.quantity-container');
    const addedButton = cardDonate.find('.added-button');

    if (quantityValue > 0) {
      quantityContainer.hide();
      addedButton.css('display', 'inline-flex');
    }
  });
});



// New Seva donate

document.querySelectorAll('.sevaWr').forEach(seva => {
  seva.addEventListener('click', () => {
      document.querySelector('.fixDonateBottom').style.display = 'block';
  });
});
document.querySelectorAll('.pplus').forEach(plus => {
  plus.addEventListener('click', event => {
      const pnum = event.target.previousElementSibling;
      let count = parseInt(pnum.textContent);
      pnum.textContent = ++count;
      updateAmount();
  });
});

document.querySelectorAll('.pminus').forEach(minus => {
  minus.addEventListener('click', event => {
      const pnum = event.target.nextElementSibling;
      let count = parseInt(pnum.textContent);
      if (count > 1) pnum.textContent = --count;
      updateAmount();
  });
});

function updateAmount() {
  let totalAmount = 0;
  document.querySelectorAll('.sevaWr').forEach(seva => {
      const amount = parseInt(seva.querySelector('.amount_box span').textContent);
      const count = parseInt(seva.querySelector('.pnum').textContent);
      totalAmount += amount * count;
  });
  document.getElementById('donationAmount').textContent = totalAmount;
}




// Rehabilitation Sliders
const rehabilitationSlider1 = new Swiper(".rehabilitationSlider1", {
  slidesPerView: 1,
  spaceBetween: 0,
  pagination: {
    el: ".swiper-pagination",
  },
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
});

const rehabilitationSlider2 = new Swiper(".rehabilitationSlider2", {
  slidesPerView: 1,
  spaceBetween: 0,
  pagination: {
    el: ".swiper-pagination",
  },
  autoplay: {
    delay: 2000,
    disableOnInteraction: false,
  },
});

// Campaign Slider
const campaignSwiper = new Swiper(".campaingSwiper", {
  slidesPerView: 1.2,
  spaceBetween: 20,
  centeredSlides: true,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
});

// Progress Bar Update
let currentStep = 1;

function updateProgressBar(step) {
  const progressBar = document.getElementById('progress-bar');
  const progress = (step / 3) * 100;
  progressBar.style.width = `${progress}%`;
  progressBar.setAttribute('aria-valuenow', progress);

  document.querySelectorAll('.circle').forEach((circle, index) => {
    if (index < step) {
      circle.classList.add('active');
    } else {
      circle.classList.remove('active');
    }
  });
}

function nextStep(step) {
  document.querySelectorAll('.step').forEach(el => el.classList.add('d-none'));
  document.getElementById(`step-${step}`).classList.remove('d-none');
  currentStep = step;
  updateProgressBar(step);
}

function prevStep(step) {
  document.querySelectorAll('.step').forEach(el => el.classList.add('d-none'));
  document.getElementById(`step-${step}`).classList.remove('d-none');
  currentStep = step;
  updateProgressBar(step);
}

// Product Sliders
const productSlider1 = new Swiper(".productslide1", {
  slidesPerView: 1,
  spaceBetween: 0,
  pagination: {
    el: ".swiper-pagination",
  },
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
});

const AEForCSRSlider = new Swiper(".AEForCSRSlider", {
  slidesPerView: 3.7,
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: { slidesPerView: 1, spaceBetween: 10 },
    576: { slidesPerView: 1.7, spaceBetween: 10 },
    768: { slidesPerView: 2, spaceBetween: 20 },
    992: { slidesPerView: 3.7, spaceBetween: 20 },
    1200: { slidesPerView: 5.7, spaceBetween: 25 },
  },
});

// Other Sliders
const whyComWithHingoSlider = new Swiper(".whyComWithHingoSlider", {
  slidesPerView: 3.7,
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    320: { slidesPerView: 1, spaceBetween: 10 },
    576: { slidesPerView: 1.7, spaceBetween: 10 },
    768: { slidesPerView: 2, spaceBetween: 20 },
    992: { slidesPerView: 3.7, spaceBetween: 20 },
    1200: { slidesPerView: 3.7, spaceBetween: 25 },
  },
});

// Tooltip Toggle
document.addEventListener('DOMContentLoaded', () => {
  const tooltipIcons = document.querySelectorAll('.tooltipIcon');

  tooltipIcons.forEach(icon => {
    icon.addEventListener('click', function () {
      const cardDonate = this.closest('.card_donate');
      const tooltipContent = cardDonate.querySelector('.tooltipeContentWr');
      const cardBody = cardDonate.querySelector('.card-body');
      const cardImgTop = cardDonate.querySelector('.card-img-top.img-fluid');

      tooltipContent.classList.toggle('d-none');
      cardBody.classList.toggle('d-none');
      cardImgTop.classList.toggle('d-none');
    });
  });
});

// ONAtH Swiper
const ONAtHSwiper = new Swiper(".ONAtHwiper", {
  spaceBetween: 10,
  slidesPerView: 7,
  freeMode: true,
  watchSlidesProgress: true,
});

const ONAtHSwiper2 = new Swiper(".ONAtHwiper2", {
  spaceBetween: 10,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  thumbs: {
    swiper: ONAtHSwiper,
  },
});

// Support Sliders
const supportSlider1 = new Swiper(".supportSlider1", {
  slidesPerView: 1,
  spaceBetween: 0,
  pagination: {
    el: ".swiper-pagination",
  },
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
});

const ourSupportSlider1 = new Swiper(".oursupportSlider1", {
  slidesPerView: 1,
  spaceBetween: 0,
  pagination: {
    el: ".swiper-pagination",
  },
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
});

// Campaign Gallery Slider
const campaignGallerySwiper = new Swiper(".campaignGallerySwiper", {
  slidesPerView: 2,
  spaceBetween: 10,
  breakpoints: {
    640: { slidesPerView: 2, spaceBetween: 20 },
    768: { slidesPerView: 3, spaceBetween: 10 },
    1024: { slidesPerView: 4, spaceBetween: 10 },
  },
});

// Quantity Input Control
$(document).ready(function () {
  $(".plusBtn").on("click", function () {
    var input = $(this).prev(".quantityInput");
    var currentValue = parseInt(input.val());
    input.val(currentValue + 1);
    if (currentValue === 0) {
      $(this).closest(".col-5").find(".qty-box-btn").show();
      $(this).closest(".col-5").find(".qtyBoxCmp").hide();
    }
  });

  $(".minusBtn").on("click", function () {
    var input = $(this).next(".quantityInput");
    var currentValue = parseInt(input.val());
    if (currentValue > 1) {
      input.val(currentValue - 1);
    } else {
      $(this).closest(".col-5").find(".qty-box-btn").show();
      $(this).closest(".col-5").find(".qtyBoxCmp").hide();
    }
  });
});

// Social Share Toggle
document.querySelectorAll('.social_share_btn').forEach(button => {
  button.addEventListener('click', event => {
    event.preventDefault();
    const shareContainer = button.closest('.social_share_container');
    const shareDiv = shareContainer.querySelector('.social_share_box');
    shareDiv.classList.toggle('active');
  });
});

        /**************/
