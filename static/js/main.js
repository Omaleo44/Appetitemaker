$('.carousel.carousel-slider').carousel({
    fullWidth: true
});
$(document).ready(function(){
    $('.NavLateral-DropDown').on('click', function(e){
        e.preventDefault();
        var DropMenu=$(this).next('ul');
        var CaretDown=$(this).children('i.NavLateral-CaretDown');
        DropMenu.slideToggle('fast');
        if(CaretDown.hasClass('NavLateral-CaretDownRotate')){
            CaretDown.removeClass('NavLateral-CaretDownRotate');    
        }else{
            CaretDown.addClass('NavLateral-CaretDownRotate');    
        }
         
    });
    $('.tooltipped').tooltip({delay: 50});
    $('.ShowHideMenu').on('click', function(){
        var MobileMenu=$('.NavLateral');
        if(MobileMenu.css('opacity')==="0"){
            MobileMenu.addClass('Show-menu');   
        }else{
            MobileMenu.removeClass('Show-menu'); 
        }   
    }); 
    $('.btn-ExitSystem').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "Quieres salir del sistema?",   
            text: "La sesión actual se cerrará y saldrá del sistema.",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "SI",
            animation: "slide-from-top",   
            closeOnConfirm: false,
            cancelButtonText: "Cancelar"
        }, function(){   
            window.location='/logout'; 
        });
    }); 
    $('.btn-Search').on('click', function(e){
        e.preventDefault();
        swal({   
            title: "Opcion de  Buscar",   
            text: "Escribe Aqui",   
            type: "input",   
            showCancelButton: true,   
            closeOnConfirm: false,   
            animation: "slide-from-top",   
            inputPlaceholder: "Escribe Aqui",
            confirmButtonText: "Buscar",
            cancelButtonText: "Cancelar" 
        }, function(){   
            window.location='/busqueda'; 
        });
        // }, function(inputValue){   
        //     if (inputValue === false) return false;      
        //     if (inputValue === "") {     swal.showInputError("You must write something");     
        //     return false   
        //     }      
        //     swal("Nice!", "You wrote: " + inputValue, "success"); 
        // });    
    });
    $('.btn-Notification').on('click', function(){
        var NotificationArea=$('.NotificationArea');
        if(NotificationArea.hasClass('NotificationArea-show')){
            NotificationArea.removeClass('NotificationArea-show');
        }else{
            NotificationArea.addClass('NotificationArea-show');
        }
    });     
});
(function($){
    $(window).load(function(){
        $(".NavLateral-content").mCustomScrollbar({
            theme:"light-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
        $(".ContentPage, .NotificationArea").mCustomScrollbar({
            theme:"dark-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
    });
})(jQuery);