let NameError = document.getElementById("Name-error")
let lnameError = document.getElementById("lname-error")
let EmailError = document.getElementById("Email-error")
let PhoneError = document.getElementById("Phone-error")
let CountryError = document.getElementById("Country-error")
let StateError = document.getElementById("State-error")
let PinError   = document.getElementById("Pin-error")
// let landmarkError   = document.getElementById("landmark-error")
let AddressError   = document.getElementById("Address-error")
let TownError   = document.getElementById("Town-error")
// let houseError   = document.getElementById("house-error")
let SubmitError = document.getElementById("SUBMIT")

console.log("addresssssssssssssssssss")
function validateFName(){
    console.log("nameeeeeeeeeeeeeeeeeeeee")
    let name = document.getElementById("fname").value;
    console.log("name: ",name)
    if(name.length == 0){
        console.log("fname validation")
        NameError.innerHTML='First name Required';
        return false
    }
    if(!name.match(/^(?!-)[a-zA-Z-]/)){
        NameError.innerHTML='enter name';
        return false
    }
    NameError.innerHTML=''
    return true
}
function validateLName(){
    let name = document.getElementById("lname").value
    if(name.length == 0){
        lnameError.innerHTML='Last name Required';
        return false
    }
    if(!name.match(/^(?!-)[a-zA-Z-]/)){
        lnameError.innerHTML='entername';
        return false
    }
    lnameError.innerHTML=''
    return true
}


function validateEmailAddress(){
        
    var email=document.getElementById('check-email').value;
    if(email.length==0){
        EmailError.innerHTML ='Email is required';
        return false;

    }
   else if(!email.match(/^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/)){
        EmailError.innerHTML='Email Invalid';
        return false;
    }
    else{
        EmailError.innerHTML ='';
        return true;
    }
}

function validatePhoneNo(){
    var phone=document.getElementById('mobile').value
    if(phone.length == 0){
        PhoneError.innerHTML='Phone number is required'
        return false
    }
    if(!phone.match(/^\d{10}$/)){
        PhoneError.innerHTML='Enter valied Phone number'
        return false
    }
    PhoneError.innerHTML=''
    return true
}

function validateCountry(){
    let country = document.getElementById("country").value
    if(country.length<1){
        CountryError.innerHTML= "enter valid country Name"
        return false
    }
    CountryError.innerHTML= ""
    return true
}
function validateState(){
    let state = document.getElementById("country").value
    if(state.length<1){
        StateError.innerHTML= "enter valid state Name"
        return false
    }
    StateError.innerHTML= ""
    return true
}

function validatePin(){
    var pin = document.getElementById("pin").value
    if(pin.length < 6|| pin.length > 6){
        PinError.innerHTML='Enter valid pin '
        return false 
    }
    PinError.innerHTML=''
    return true

}
// function validateHouse(){
//     let houseNo = document.getElementById("houseNo").value
//     if(houseNo.length<1){
//         houseError.innerHTML='Enter valied House / Flat Number';
//         return false
//     }
//     houseError.innerHTML=''
//     return true
// }
// function validateLandmark(){
//     let landmark = document.getElementById("landmarkad").value
//     if(landmark.length<1){
//         landmarkError.innerHTML='Enter valied landmark'
//         return false
//     }
//     landmarkError.innerHTML=''
//     return true
// }

function validateAddress(){
    let address = document.getElementById("address").value
    if(address.length<1){
        AddressError.innerHTML= "enter valid address"
        return false
    }
    AddressError.innerHTML=''
    return true
}

function validateTown(){
    let town = document.getElementById("town").value
    if(town.length<1){
        TownError.innerHTML= "enter valid town Name"
        return false
    }
    TownError.innerHTML= ""
    return true
}
function validateAddressForm(){
        console.log("formmmmmmmmmmm")
    var submit =document.getElementById('Confirm-submit').value;
    if(! validateFName() || ! validateLName() || ! validateEmailAddress() || ! validatePhoneNo() || ! validateCountry() || ! validateState() || !validatePin() || ! validateAddress() || ! validateTown()  || ! validatephonenumber()){
        SubmitError.style.display ='block';
        SubmitError.innerHTML='please fill the form';
        setTimeout(function(){SubmitError.style.display ='none';},3000);
        return false;
    }
    else{
        return true;
    }
      
}

// function submitAdd(){
//     if(validateName ()!= true|| validatePhone() || validateAddress ()|| validateHouse () || validateLandmark () || validatePin() || validateTown ()){
//         submitError.innerHTML = "Please Enter Details"
//         return false
//     }
//     submitError.innerHTML = ""

//     return true
// }


// $("#address_form").submit((e)=>{
//     e.preventDefault()
//     if(validateName()&& validatePhone() && validateHouse() && validateAddress() && validatePin() && validateLandmark() && validateTown()){
//         $.ajax({
//             url:'http://localhost:8001/user/addAddress',
//             data:$('#address_form').serialize(),
//             method:'post',
//             success:(response)=>{
//                 window.location.reload()
//             }
//         })
//     }else{
//         submitError.innerHTML='Enter all Data required'
//         return false
//     }
// })


// $("#address_Prof_form").submit((e)=>{
//     e.preventDefault()
//     if(validateName()&& validatePhone() && validateHouse() && validateAddress() && validatePin() && validateLandmark() && validateTown()){
//         $.ajax({
//             url:'http://localhost:8001/user/addAddress',
//             data:$('#address_Prof_form').serialize(),
//             method:'post',
//             success:(response)=>{
//                 window.location.reload()
//             }
//         })
//     }else{
//         submitError.innerHTML='Enter all Data required'
//         return false
//     }
// })