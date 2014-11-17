 /*Responisve Menu */
$('#dl-menu').dlmenu({
    animationClasses: {
        classin: 'dl-animate-in-5',
        classout: 'dl-animate-out-5'
    }
});
/* Responisve Menu */



/* Accordion */
$('.accordion span').click(function () {
    if ($(this).next().is(':hidden')) {
        $('.accordion span').removeClass('active').next().slideUp();
        $(this).addClass('active').next().slideDown();
    }
    return false;
});
/* Accordion */

/* Tabs */
jQuery('.shortcode_tabs').each(function (index) {
    var i = 1;
    jQuery('.shortcode_tab_item_title').each(function (index) {
        jQuery(this).addClass('it' + i);
        jQuery(this).attr('whatopen', 'body' + i);
        jQuery(this).addClass('head' + i);
        jQuery(this).parents('.shortcode_tabs').find('.all_heads_cont').append(this);
        i++;
    });
    var i = 1;
    jQuery('.shortcode_tab_item_body').each(function (index) {
        jQuery(this).addClass('body' + i);
        jQuery(this).addClass('it' + i);
        jQuery(this).parents('.shortcode_tabs').find('.all_body_cont').append(this);
        i++;
    });
});
jQuery('.shortcode_tabs .all_body_cont div:first-child').addClass('active');
jQuery('.shortcode_tabs .all_heads_cont div:first-child').addClass('active');

jQuery('.shortcode_tab_item_title').click(function () {
    jQuery(this).parents('.shortcode_tabs').find('.shortcode_tab_item_body').removeClass('active');
    jQuery(this).parents('.shortcode_tabs').find('.shortcode_tab_item_title').removeClass('active');
    var whatopen = jQuery(this).attr('data-open');
    jQuery(this).parents('.shortcode_tabs').find('.' + whatopen).addClass('active');
    jQuery(this).addClass('active');
});
/* Tabs */

/* Twitter */

/* Twitter */

/* ShowBiz */
jQuery('#portfolio').showbizpro({
    visibleElementsArray: [3, 3, 2, 1],
    mediaMaxHeight: [250, 250, 250, 250],
    carousel: "on",
    heightOffsetBottom: 10
});
jQuery(".fancybox").fancybox();


jQuery('#blog').showbizpro({
    visibleElementsArray: [2, 2, 2, 1],
    mediaMaxHeight: [210, 210, 210, 210],
    carousel: "on",
    heightOffsetBottom: 10
});


jQuery('#clients').showbizpro({
    visibleElementsArray: [6, 5, 3, 2],
    carousel: "on",
    heightOffsetBottom: 10,
    mediaMaxHeight: [76, 76, 76, 76],
});
/* ShowBiz */

/* Animation */
$(window).scroll(function () {
    $(".animated-area").each(function () {
        if ($(window).height() + $(window).scrollTop() - $(this).offset().top > 0) {
            $(this).trigger("animate-it");
        }
    });
});
$(".animated-area").on("animate-it", function () {
    var cf = $(this);
    cf.find(".animated").each(function () {
        $(this).css("-webkit-animation-duration", "0.9s");
        $(this).css("-moz-animation-duration", "0.9s");
        $(this).css("-ms-animation-duration", "0.9s");
        $(this).css("animation-duration", "0.9s");
        $(this).css("-webkit-animation-delay", $(this).attr("data-animation-delay"));
        $(this).css("-moz-animation-delay", $(this).attr("data-animation-delay"));
        $(this).css("-ms-animation-delay", $(this).attr("data-animation-delay"));
        $(this).css("animation-delay", $(this).attr("data-animation-delay"));
        $(this).addClass($(this).attr("data-animation"));
    });
});
/* Animation */

/* Isotope Portfolio */
$(window).load(function () {
    var $container = $('.portfolio');
    $container.isotope({
        filter: '*',
        layoutMode: 'masonry',
    });
    $('.portfolioFilter a').click(function () {
        $('.portfolioFilter .current').removeClass('current');
        $(this).addClass('current');
        var selector = $(this).attr('data-filter');
        $container.isotope({
            filter: selector,
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false
            }
        });
        return false;
    });
});
/* Isotope Portfolio */

/* Testimonials */
// $(window).load(function () {
//     $("#tr1").testimonialrotator({
//         settings_slideshowTime: 3
//     });
// });
/* Testimonials */

/* Tooltip  */
jQuery(function ($) {
    $('.tooltip_s').tooltip()
});
/* Tooltip  */