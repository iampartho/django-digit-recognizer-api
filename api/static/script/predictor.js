// $(document).ready(function(){
//   $(".home-spinner").hide();

//   $('.submit_btn').click(function(e){
//   	$(this).attr('disabled', true);
//     e.preventDefault();

//     var data = new FormData($('form').get(0));

//     const url = $(this).attr('id');
//     const this_btn = $(this);
//     $(".home-spinner").show();

//     $.ajax({
//       type:"POST",
//       url: url,
//       data:{
//         "csrfmiddlewaretoken":$('input[name=csrfmiddlewaretoken]').val()
//         "data": "abcd"
//       },
//       success:function(response){
//         //console.log('kisu ekta')


//         if (response['flag'] == 'e') {
//         	$('.post-content').addClass('text-danger')
//         	$('.post-content').text(response['error'])
//         	$(".home-spinner").hide();
//         	$('.submit_btn').attr('disabled', false);
//           //console.log('eikhane dhuksee');
//           //this_btn.attr('disabled', true);

          

//         }else if(response['flag'] == 's'){
//         	console.log('Working')

//         } else {
//           console.log('Something is wrong')
//         }
//       },
//       error:function(response){
//         console.log('error', response)
//       }
//     })


//   })


//  })