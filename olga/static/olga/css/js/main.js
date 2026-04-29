$(document).ready(function() {
    $('.btn-add-to-cart').click(function() {
        var productId = $(this).data('id');
        window.location.href = '/cart/add/' + productId + '/';
    });
});