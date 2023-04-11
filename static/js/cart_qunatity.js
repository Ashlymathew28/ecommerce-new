function decrementQunatity(qty,qty1,id,sub_total){
    var qty = $('#' +qty)
    var sub_total=$('#'+sub_total )
    console.log("decrement")
    let qtynum = qty.val()
    console.log(qtynum);
        if(qtynum >1 ){
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
                      $('#tax').text("₹"+r.tax)
                    // $('#saved').text("-"+r.saved)
                    $('#grand_total').text("₹"+r.grand_total)
                },
                error:function(r){
                    alert('Error Ocuured')
                }
        
            });
        }else{
            document.getElementById('minus').classList.add('invisible')
        }
        
}

function incrementQunatity(qty,id,sub_total){
    var qty = $('#' +qty)
    var sub_total=$('#'+sub_total)
    console.log("increment")
    document.getElementById('minus').classList.remove('invisible')
    $.ajax({
        type:"GET",
        url: "/cart/increment_cart",
        data:{
            'id':id
        },
        success : function(r){
            console.log('jhjdhfdhfdj')
            console.log('ashhhhhh')
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total_price)
            $('#tax').text("₹"+r.tax)
            $('#grand_total').text("₹"+r.grand_total)
            console.log(r.tax);
            $('#saved').text("-"+r.saved)

        },
        error:function(r){
            alert('Out of stock')
        }

    });
}


//decrement code

