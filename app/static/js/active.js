(function ($) {
    'use strict';

    if ($.fn.owlCarousel) {
        // Hero Slider Active Code
        $(".features-slides").owlCarousel({
            items: 5,
            loop: true,
            autoplay: false,
            smartSpeed: 2000,
            margin: 50,
            nav: false,
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 2
                },
                992: {
                    items: 3
                },
                1200: {
                    items: 5
                }
            }
        })
    }

    // Search Active Code
    $('#search-btn, #closeBtn').on('click', function () {
        $('body').toggleClass('search-form-on');
    });
    
    // matchHeight Active Code
    if ($.fn.matchHeight) {
        $('.equal-height').matchHeight();
    }
    
    // ScrollUp Active Code
    if ($.fn.scrollUp) {
        $.scrollUp({
            scrollSpeed: 1500,
            scrollText: '<i class="pe-7s-angle-up" aria-hidden="true"></i>'
        });
    }

    // onePageNav Active Code
    if ($.fn.onePageNav) {
        $('#listingNav').onePageNav({
            currentClass: 'active',
            scrollSpeed: 2000,
            easing: 'easeOutQuad'
        });
    }

    // PreventDefault a Click
    $("a[href='#']").on('click', function ($) {
        $.preventDefault();
    });

    // wow Active Code
    if ($.fn.init) {
        new WOW().init();
    }

    var $window = $(window);

    // Sticky Active JS
    $window.on('scroll', function () {
        if ($window.scrollTop() > 0) {
            $('body').addClass('sticky');
        } else {
            $('body').removeClass('sticky');
        }
    });

    // Preloader Active Code
    $window.on('load', function () {
        $('#preloader').fadeOut('slow', function () {
            $(this).remove();
        });
    });

})(jQuery);



$(document).ready(function() {
    var owl = $(".features-slides").owlCarousel({
        loop: true,
        margin: 10,
        autoplay: true, // Enable automatic autoplay
        autoplayTimeout: 4000, // Change items every 4 seconds
        smartSpeed: 500, // Set smart speed for smoother transitions
        nav: false, // Disable navigation arrows
        dots: false // Disable pagination dots
    });

    // Function to start auto-scrolling
    function startAutoScroll() {
        owl.trigger('next.owl.carousel'); // Move to the next item
    }

    // Set interval for continuous auto-scroll
    var scrollInterval = setInterval(startAutoScroll, 4000); // Change every 4 seconds

    // Stop scrolling on hover
    $(".features-slides").hover(
        function() {
            clearInterval(scrollInterval); // Stop auto-scroll
            owl.trigger('stop.owl.autoplay'); // Stop autoplay
        },
        function() {
            scrollInterval = setInterval(startAutoScroll, 4000); // Resume auto-scroll
            owl.trigger('play.owl.autoplay'); // Resume autoplay
        }
    );
});

