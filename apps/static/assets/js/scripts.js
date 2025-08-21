$(document).ready(function(){
    
    $('.category_list .category_item_all[cat="all"]').click(function(){
        $('.product-item').css("display", "block");
        $('.input-search').val('');
        // console.log('Select All')
    });
    $('.category_list .category_item').click(function(){
        var canal = $(this).attr('category');
        console.log(canal);
        var grupo = $(this).attr('grupo');
        console.log(grupo);
        var local = $(this).attr('tipoLocal');
        console.log(local);
        // Ocultando contenido
        $('.product-item').hide();

        // Mostrar contenido seleccionado
        $('.products-list .product-item[category="'+canal+'"]').show();
        $('.products-list .product-item[tipoLocal="'+local+'"]').show();
        $('.products-list .product-item[grupo="'+grupo+'"]').show();
        $("html, body").animate({ scrollTop: 0 }, 300);
        
    });
    
    
    $('.input-search').keyup(function(){
        var buscando = $(this).val().toLowerCase(); // Convertir texto de búsqueda a minúsculas
        var nombres = $('.username');

        nombres.each(function() {
            var item = $(this).html().toLowerCase(); // El texto del título de la tarjeta en minúsculas
            
            // Si el texto de búsqueda está en el título, muestra el contenedor del producto. Si no, lo oculta.
            if (item.indexOf(buscando) > -1) {
                $(this).parents('.product-item').show();
            } else {
                $(this).parents('.product-item').hide();
            }
        });
    });
});