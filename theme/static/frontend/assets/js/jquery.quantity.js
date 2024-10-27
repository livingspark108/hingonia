// ************************************************
// Shopping Cart API
// ************************************************
var shoppingCart = (function() {
  // =============================
  // Private methods and propeties
  // =============================
  cart = [];

  // Constructor
  function Item(name, id,img, price, count, max_qty) {
    this.name = name;
    this.price = price;
    this.img = img;
    this.count = count;
    this.id = id;
    this.max_qty = max_qty;
  }

  // Save cart
  function saveCart() {
    sessionStorage.setItem('shoppingCart', JSON.stringify(cart));
  }

    // Load cart
  function loadCart() {
    cart = JSON.parse(sessionStorage.getItem('shoppingCart'));
  }
  if (sessionStorage.getItem("shoppingCart") != null) {
    loadCart();
  }


  // =============================
  // Public methods and propeties
  // =============================
  var obj = {};

  // Add to cart
  obj.addItemToCart = function(name, id,img, price, count, max_qty) {

    for(var item in cart) {
      if(cart[item].id === id) {
        cart[item].count ++;
        saveCart();
        return;
      }
    }
    var item = new Item(name, id, img,price,count,max_qty);
    cart.push(item);
    saveCart();
  }
  // Set count from item
  obj.setCountForItem = function(id, count) {
    for(var i in cart) {
      if (cart[i].id === id) {
        cart[i].count = count;
        break;
      }
    }
  };
  // Set Plat from item
  obj.setPlateForItem = function(id, plate,price) {
    for(var i in cart) {
      if (cart[i].id === id) {
        cart[i].plate = plate;
        cart[i].price = price;
        break;
      }
    }
  };
  // Remove item from cart
  obj.removeItemFromCart = function(id) {
      for(var item in cart) {
        if(cart[item].id === id) {
          cart[item].count --;
          if(cart[item].count === 0) {
            $('#totalQtyCount-' + cart[item].id).hide(500);
            cart.splice(item, 1);
          }
          break;
        }
    }
    saveCart();
  }

  // Remove all items from cart
  obj.removeItemFromCartAll = function(id) {
    for(var item in cart) {
      if(cart[item].id === id) {
        $('#totalQtyCount-' + cart[item].id).hide(500);
        cart.splice(item, 1);
        break;
      }
    }
    saveCart();
  }

  // Clear cart
  obj.clearCart = function() {
    $('.totalQtyCount').hide(500);
    cart = [];
    saveCart();
  }

  // Count cart
  obj.totalCount = function() {
    var totalCount = 0;
    for(var item in cart) {

      totalCount += cart[item].count;
    }
    return totalCount;
  }

  // Total cart
  obj.totalCart = function() {
    var totalCart = 0;
    for(var item in cart) {
      totalCart += Number(cart[item].price) * cart[item].count;

    }
    return Number(totalCart.toFixed(2));
  }

  // List cart
  obj.listCart = function() {
    var cartCopy = [];
    for(i in cart) {
      item = cart[i];
      itemCopy = {};
      for(p in item) {
        itemCopy[p] = item[p];

      }
      itemCopy.total = Number(item.price * item.count).toFixed(2);
      cartCopy.push(itemCopy)
    }
    return cartCopy;
  }

  // cart : Array
  // Item : Object/Class
  // addItemToCart : Function
  // removeItemFromCart : Function
  // removeItemFromCartAll : Function
  // clearCart : Function
  // countCart : Function
  // totalCart : Function
  // listCart : Function
  // saveCart : Function
  // loadCart : Function
  return obj;
})();

// Start Old UI
var shoppingCartOld = (function() {
  // =============================
  // Private methods and propeties
  // =============================
  cart_old = [];

  // Constructor
  function ItemOld(name, id, plate,qty) {
    this.name = name;
    this.id = id;
    this.plate = plate;
    this.count = qty;
  }

  // Save cart
  function saveCartOld() {
    sessionStorage.setItem('shoppingCartOld', JSON.stringify(cart_old));
  }

    // Load cart
  function loadCartOld() {
    cart_old = JSON.parse(sessionStorage.getItem('shoppingCartOld'));
  }
  if (sessionStorage.getItem("shoppingCartOld") != null) {
    loadCartOld();
  }


  // =============================
  // Public methods and propeties
  // =============================
  var obj_old = {};

  // Add to cart
  obj_old.addItemToCartOld = function(name, id, plate,qty) {
    for(var item in cart_old) {
      if(cart_old[item].id === id && cart_old[item].plate === plate) {
        cart_old[item].count =  Number(cart_old[item].count) + Number(qty);
        saveCartOld();
        return;
      }
    }
    var item = new ItemOld(name, id, plate,qty);
    cart_old.push(item);
    saveCartOld();
  }

  // List cart
  obj_old.listCart = function() {
    var cartCopy = [];
    for(i in cart_old) {
      item = cart_old[i];
      itemCopy = {};
      for(p in item) {
        itemCopy[p] = item[p];

      }
      itemCopy.total = ""
      cartCopy.push(itemCopy)
    }
    return cartCopy;
  }
  // Clear cart
  obj_old.clearCartOld = function() {
    console.log("Clear method call")
    cart_old = []; // Reset the cart array to an empty array
    saveCartOld(); // Save the empty cart (removes the data from sessionStorage)
  }

  return obj_old;
})();
// End Old UI

// *****************************************
// Triggers / Events
// *****************************************
// Add item
$(document).on("click keypress", ".add-to-cart", function(event) {
  if (event.type === "click" || (event.type === "keypress" && event.which === 13)) {
    event.preventDefault();
    var name = $(this).data('name');
    var plate = $(this).data('plate');
    var img = $(this).data('img');
    var price = Number($(this).data('price'));
    var half_price = Number($(this).data('half-price'));
    var full_price = Number($(this).data('full-price'));
    var max_qty = Number($(this).data('max'));
    var id = $(this).data('id');

    var count = $("input.item-count[data-id='" + id + "']").val();
    if (!isNaN(max_qty)) {
      if (typeof count === "undefined") {
      name, id, img,price,count,maxlength
            shoppingCart.addItemToCart(name, id,img, price, 1, max_qty);
            displayCart();
      }
      if(max_qty > count){
            shoppingCart.addItemToCart(name, id,img, price, 1, max_qty);
            displayCart();
      }
    }else{
      shoppingCart.addItemToCart(name, id,img, price, 1, max_qty);
      displayCart();
    }
  }
});

function make_dropdown(amt){


    var percentages = [8, 12, 14, 16];
    $(".support_option").html('')
    percentages.forEach(function(percent) {
        var value = (amt * percent / 100).toFixed(2);
        var optionText = percent + "% (" + value + ") ▼";
        $(".support_option").append(
            $("<option></option>").val(value).text(optionText)
        );
    });

    $(".support_option").append(
        $("<option></option>").val("other").text("Other ▼")
    );
}


// Clear items
$(document).on("click",".clear-cart",function() {
  shoppingCart.clearCart();
  shoppingCartOld.clearCartOld()
  displayCart();
});


function displayCart() {
  var cartArray = shoppingCart.listCart();
  var output = "";
  var output_tmp = "";
  for(var i in cartArray) {
    if(cartArray[i].plate == 'half'){
        var plate_select = "<select data-id='" + cartArray[i].id + "'   class='form-control plateType'><option selected value='half' data-price='"+cartArray[i].half_price+"' >Half</option><option value='full' data-price='"+cartArray[i].full_price+"'>Full</option></select>"
    }else if(cartArray[i].plate == 'full'){
        var plate_select = "<select data-id='" + cartArray[i].id + "' class='form-control plateType'><option  value='half' data-price='"+cartArray[i].half_price+"' >Half</option><option selected value='full' data-price='"+cartArray[i].full_price+"'>Full</option></select>"

    }else{
        var plate_select = "<select data-id='" + cartArray[i].id + "' data-price='"+cartArray[i].price+"' class='form-control plateType'><option value='flat'>Flat</option></select>"

    }
//    var jain = "<div class='form-check form-check-inline py-2'><input type='checkbox' class='form-check-input' id='jain-" + cartArray[i].id + "'><label class='form-check-label' for='jain-" + cartArray[i].id + "'>Jain</label></div>"
    var jain = ''
//    output += "<tr>"
//      + "<td class='fw-semibold'><p class='mb-0'>" + cartArray[i].name + "</p><p class='mb-0'>Price: <i class='fas fa-rupee-sign'></i>" + cartArray[i].price + "</p></td>"
//      //+ "<td><i class='fas fa-rupee-sign'></i>" + cartArray[i].price + "</td>"
//      + "<td class=''>"+plate_select+jain+"</td>"
//      + "<td><div class='input-group'><button class='minus-item input-group-addon btn btn-primary' data-name='" + cartArray[i].name + "' data-id='" + cartArray[i].id + "'>-</button>"
//      + "<input type='number' data-maxlength="+cartArray[i].max_qty+" class='item-count' data-id='" + cartArray[i].id + "' data-name='" + cartArray[i].name + "' value='" + cartArray[i].count + "'>"
//      + "<button class='plus-item btn btn-primary input-group-addon' data-id='" + cartArray[i].id + "' data-name='" + cartArray[i].name + "'>+</button><button class='ml-3 delete-item btn btn-danger' data-name='" + cartArray[i].name + "' data-id='" + cartArray[i].id + "'>X</button></div></td>"
//     // + " = "
//
//      //+ "<td class='text-right'>" + cartArray[i].total + "</td>"
//      +  "</tr>";
//      $('#totalQtyCount-' + cartArray[i].id).show(500);
//      $('#totalQtyCount-' + cartArray[i].id).html(cartArray[i].count);

     output += "<div class='card card-body shadow border-0 my-3 p-3 rounded-4 campaign-cart'>" +
                  "<div class='row align-items-center g-md-3 g-2'>" +
                      "<div class='col-4'>" +
                          "<img src='"+cartArray[i].img+"' class='img-fluid rounded-4' alt=''>" + // You might want to replace the src with a dynamic value if each product has a different image.
                      "</div>" +
                      "<div class='col-8'>" +
                          "<h6 class='fw-semibold f-14 mb-0'>" + cartArray[i].name + "</h6>" +
                          "<h6 class='text-muted fw-500 mb-0 f-12'>1 unit = 10 kg</h6>" + // This line can also be dynamic if necessary.
                      "</div>" +
                      "<div class='col-6'>" +
                          "<div class='input-group'>" +
                              "<button class='btn border minusBtn minus-item' type='button' data-name='" + cartArray[i].name + "' data-id='" + cartArray[i].id + "'>-</button>" +
                              "<input type='number' class='form-control text-center quantityInput border' data-id='" + cartArray[i].id + "' data-name='" + cartArray[i].name + "' value='" + cartArray[i].count + "' aria-label='Quantity'>" +
                              "<button class='btn plusBtn border plus-item' type='button' data-id='" + cartArray[i].id + "' data-name='" + cartArray[i].name + "'>+</button>" +
                          "</div>" +
                      "</div>" +
                      "<div class='col-6 text-end'>" +
                          "<span class='text-muted fw-500 mb-0 f-12'><i class='bi bi-currency-rupee'></i>" + cartArray[i].total + "</span>" +
                          "<a href='#' class='ps-3'><i data-id='"+cartArray[i].id+"' class='delete-item bi bi-trash'></i></a>" + // Consider adding a data-id or data-name attribute here for the delete functionality.
                      "</div>" +
                  "</div>" +
              "</div>";
      output_tmp += '<span class="badge bg-2 m-1">'+ cartArray[i].name +' Qty. '+ cartArray[i].count +' * <i class="bi bi-currency-rupee text-white"></i> '+ cartArray[i].total +'</span>'

      }

  $('.show-cart').html(output);
  if(shoppingCart.totalCart() > 0){
    $('.show-cart').show()

    make_dropdown(shoppingCart.totalCart())
    var tip_amt = $('.support_option').val()
    var total = shoppingCart.totalCart()
    var all_total = 0
    all_total = parseFloat(total) + parseFloat(tip_amt)
    $('.active_price').val(all_total);
    $('.active_amt_html').html(all_total);
    $('.donate_amt_1').val(total);
    $('.active_amt').val(all_total);


    $('.tmp_amount').val(tip_amt);


    $('.donationAmount_html').html(all_total);
    $('.all_ctm_amount').hide()
    $('.cart_item_html_tmp').show()
    $('.cart_item_html_tmp .ct_item_tmp').html(output_tmp)

//    generateOptions(shoppingCart.totalCart())
  }else{
    $('.show-cart').hide()
    $('.all_ctm_amount').show()
    $('.cart_item_html_tmp').hide()
  }

  $('.total-count').html(shoppingCart.totalCount());
  $('.all_item_data').val('')
  var jsonString = JSON.stringify(cartArray);
  $('.all_item_data').val(jsonString)
}

const percentages = [0.00,0.08, 0.12, 0.14, 0.16];

function generateOptions(totalAmount) {
    const supportOption = document.getElementById('support-option');
    supportOption.innerHTML = ''; // Clear existing options
    percentages.forEach((percentage, index) => {
        const calculatedAmount = (totalAmount * percentage).toFixed(2);
        const option = document.createElement('option');
        option.value = calculatedAmount;
        option.innerHTML = `${(percentage * 100).toFixed(0)}% (<i class="bi bi-currency-rupee"></i>${calculatedAmount}) ▼`;
        supportOption.appendChild(option);
    });
//    const otherOption = document.createElement('option');
//    otherOption.value = 'other';
//    otherOption.text = 'Other ▼';
//    supportOption.appendChild(otherOption);

    // Automatically select the second option (8%)
    supportOption.selectedIndex = 1;
    updateAmount(); // Update amount based on the selected option
}

function displayCartOld() {
  var cartArray = shoppingCartOld.listCart();


  var output = "";
  for(var i in cartArray) {
        output += '<tr><td>' + cartArray[i].name + '</td><td>' + cartArray[i].count + '</td></tr>'

  }
  $('.table_add_item').html('')
  $('.table_add_item').append(output)
}

// Delete item button

$(document).on("click", ".delete-item", function(event) {
  var id = $(this).data('id')
  shoppingCart.removeItemFromCartAll(id);
  displayCart();
  $('.add-to-cart[data-id="' + id + '"]').show()
  $('.qtyBoxCmp[data-id="' + id + '"]').hide();
  $('.quantityInput[data-id="' + id + '"]').val(1);

})


// -1
$(document).on("click", ".minus-item", function(event) {
  var id = $(this).data('id')
  shoppingCart.removeItemFromCart(id);
  displayCart();
})
// +1
$(document).on("click", ".plus-item", function(event) {
  var id = $(this).data('id')
  var name = $(this).data('name')
  var img = $(this).data('img')
  var price = $(this).data('price')
  var count = $("input.item-count[data-id='" + id + "']").val();

  var inputElement = $("input.item-count[data-id='" + id + "']");

  var maxlength = inputElement.data("maxlength");

  if (!isNaN(maxlength)) {
      if(maxlength > count){
      shoppingCart.addItemToCart(name, id, img,price,count,maxlength);
      displayCart();
      }
  }else{
      shoppingCart.addItemToCart(name, id, img,price,count,maxlength);
      displayCart();
  }
})

// Item count input
$(document).on("change", ".item-count", function(event) {
   var name = $(this).data('name');
   var maxlength = $(this).data('maxlength');
   var count = Number($(this).val());
   if (!isNaN(maxlength)) {
      if(maxlength > count){
      shoppingCart.addItemToCart(name, id);
      displayCart();
      }
  }else{
      shoppingCart.addItemToCart(name, id);
      displayCart();
  }
});

$(document).on("change", ".plateType", function(event) {
   var id = $(this).data('id')
   var price = $(this).find(':selected').attr('data-price')
  var plate = $(this).val()
  shoppingCart.setPlateForItem(id, plate,price);
  displayCart();
});



displayCart();


// Old one
$(document).on("click keypress", ".add-to-cart-old", function(event) {
  if (event.type === "click" || (event.type === "keypress" && event.which === 13)) {
    event.preventDefault();
    var name = $('.product_name').select2('data')[0].text
    var price = 10
    var plate = $('.plate_type').val()

    var qty = $('.quantity').val()
    var id = $('.product_name').val()

    price = 10
    half_price = 0
    full_price = 0

    if (!isNaN(qty)) {
        shoppingCartOld.addItemToCartOld(name, id, plate, qty);
        displayCartOld();
  }
  }
});