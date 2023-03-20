function apply_coupon() {
    var coupon_code=document.getElementById('coupon_code').value
    var grand_total=document.getElementById('grand_total').value
    $.ajax({
        url:'cart/apply_coupon',
        method:"GET",
        data:{
            coupon_code:coupon_code,
            grand_total:grand_total,
        },
        succes:(response) =>{
            
        }

    })
}
