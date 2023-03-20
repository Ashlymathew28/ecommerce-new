function decrementQunatity(qty,id,sub_total){
    var qty = $('#' +qty)
    var sub_total=$('#'+sub_total )
    console.log("decrement")
    $.ajax({
        type : "GET",
        url : "/cart/decrement_quantity/",
        data:{
            'id':id
        },
        success : function(r){
            
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total_price)
            $('#saved').text("-"+r.saved)

        },
        error:function(r){
            alert('Error Ocuured')
        }

    });
}
function incrementQunatity(qty,id,sub_total){
    
    var qty = $('#' +qty)
    var sub_total=$('#'+sub_total)
    console.log("increment")
    $.ajax({
        type:"GET",
        url: "/cart/increment_cart",
        data:{
            'id':id
        },

        success : function(r){
            console.log('jhjdhfdhfdj')
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total_price)
            $('#saved').text("-"+r.saved)

        },
        error:function(r){
            alert('Error Ocuured')
        }

    });
}