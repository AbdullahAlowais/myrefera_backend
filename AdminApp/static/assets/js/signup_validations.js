
$(document).ready(function(){
    
    $('#signupform').validate({
        rules: {
           
           username:"required",
           role:"required",
           email:"required",
           password: {
            required: true,
            minlength: 5,
           },
           conpassword:{
            required: true,
            minlength: 5,
            equalTo: '[name="password"]'
           },
        },
        messages: {
           
           username:"Please enter Username",
           role:"Please choose a Role",
           email:"Please enter Email",
           password:{
            required:"please enter Password",
            minlength:"password should be 5 characters"
           },
           conpassword:{
            required:"please enter Confirm Password",
            minlength:"password should be 5 characters",
            equalTo: "Password and confirm password does not match"
           }
        }
    });
});




$(document).ready(function(){
    $('#loginform').validate({
        rules: {
           email:"required",
           password: {
            required: true,
           }
        },
        messages: {
           email:"Please enter Email",
           password:{
            required:"please enter Password",
           }
        }
    });
});



$(document).ready(function(){
    $('#changepasswordform').validate({
        rules: {
            password: {
                required: true,
                minlength: 5,
               },
               conpassword:{
                required: true,
                minlength: 5,
                equalTo: '[name="password"]'
               },
        },
        messages: {
            password:{
                required:"please enter Password",
                minlength:"password should be 5 characters"
               },
               conpassword:{
                required:"please enter Confirm Password",
                minlength:"password should be 5 characters",
                equalTo: "Password and confirm password does not match"
               }
        }
    });
});


$(document).ready(function(){
    $('#forgotpasswordform').validate({
        rules: {
           email:"required",
        },
        messages: {
           email:"Please enter Email",
           
        }
    });
});




// $(document).ready(function(){
//     $('#changepasswordform2').validate({
//         rules: {
//             password: {
//                 required: true,
//                 minlength: 5,
//                },
//                conpassword:{
//                 required: true,
//                 minlength: 5,
//                 equalTo: '[name="password"]'
//                },
//         },
//         messages: {
//             password:{
//                 required:"please enter Password",
//                 minlength:"password should be 5 characters"
//                },
//                conpassword:{
//                 required:"please enter Confirm Password",
//                 minlength:"password should be 5 characters",
//                 equalTo: "Password and confirm password does not match"
//                }
//         }
//     });
// });
