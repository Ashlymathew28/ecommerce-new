// $(document).ready(function(){
//     console.log('entered')
//    $('.payWithRazorpay').click(function(e) {
//     e.preventDefault();
//     console.log('//////////////')
//     var address = $("[name='address']").val();
//     console.log(address)
//     if (address == "") {
//         console.log('--------------')
//         Swal.fire('all fields are mandatory!!')
//         return false;
//     }

$(document).ready(function() {
    console.log('entered');
  
    $('.payWithRazorpay').click(function(e) {
      e.preventDefault();
      console.log('//////////////');
      var address = $("[name='address']:checked").val(); // get selected address
      var token=$('input[name=csrfmiddlewaretoken]').val();
      console.log(address);
      if (!address) { // check if an address is selected
        console.log(address,'Mwonuseee evide und.....');
        Swal.fire('Error', 'Please select an address.', 'error'); // display error message
        return false;
      }
      else
      {
        $.ajax({
            method: "GET",
            url:"/orders/proceed_to_pay",
            success:function(response) {
                console.log("evide undada kuttaaaa....")
                var options = {
                    "key": "rzp_test_2OQT5vz8WgTGvO", // Enter the Key ID generated from the Dashboard
                    "amount": response.total_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "BW-Store", //your business name
                    "description": "Thank you for buying from us",
                    "image": "https://example.com/your_logo",
                    // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (responseb){
                        // alert(response.razorpay_payment_id);
                        console.log(responseb)
                        data={
                            'address':address,
                            'pay_mode':"Razorpay",
                            'pay_id':responseb.razorpay_payment_id,
                            csrfmiddlewaretoken : token
                        }
                        console.log("not working:::::")
                        $.ajax({
                            method:"POST",
                            url:"/orders/place_order/",
                            data:data,
            
                            success:function(responsec){
                            console.log('I am hereeeee........');
                            console.log(responsec)
                             Swal.fire("Congratulations!",`${responsec.status}`,'success').then((value) => {
                                window.location.href='/userptofile/userdetails/'
                            });
                            }
                        });
                        // alert(response.razorpay_order_id);
                        // alert(response.razorpay_signature)
                    },
                    "prefill": {
                        "name": "Gaurav Kumar", //your customer's name
                        "email": "gaurav.kumar@example.com",
                        "contact": "9000090000"
                    },
                    "notes": {
                        "address": "Razorpay Corporate Office"
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options); 
                rzp1.open();
            }


        })
      }
  
     
  
  

   });

});