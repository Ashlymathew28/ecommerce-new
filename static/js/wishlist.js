function addToWishlist(id){
    event.preventDefault();
    console.log(id)
    $.ajax({
        method:"GET",
        url: "/cart/AddWhishlist/",
        data:{
            'product_id':id,
            // 'csrfmiddlewaretoken' :token
        },
        success:function(response){
            console.log(response)
            alertify.success(response.status)

        }
        
    });
};