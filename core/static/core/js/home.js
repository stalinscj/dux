var flag_skill = false;
$(function () {
	var $window = $(window);

	function animar_skill_bar() {

		var elementTop = $("#skillbar-wrap").offset().top;
		var elementBottom = elementTop + $("#skillbar-wrap").outerHeight();
		var viewportTop = $(window).scrollTop();
		var viewportBottom = viewportTop + $(window).height();

		if (elementBottom > viewportTop && elementTop < viewportBottom ){
			if (!flag_skill){
				$('.skillbar').skillBars({
					from: 0,
					speed: 4000, 
					interval: 100,
				}); 
				flag_skill = true;
			}
		}else{
			flag_skill = false;
		}
	}

	particlesJS.load('particles-js', particles_url_config, function() {
		/* console.log('callback - particles.js config loaded');*/
	});

	$('.fixed-top .nav-link, .fixed-top .navbar-brand, .jumbotron .btn').click(function() {
		var sectionTo = $(this).attr('href');
		$('html, body').animate({
			scrollTop: $(sectionTo).offset().top
		}, 1500);
	});

	var typed = new Typed('.typed', {
		strings: ['Analista &amp; Desarrollador', 'Analista de Proyectos de IT', 'Desarrollador: Web (Backend)', 'Desarrollador: Desktop', 'Web: HTML, CSS y JS', 'Web (FW): Bootstrap y JQuery', 'Web: PHP y Python', 'Web (FW): Laravel, Zend y Django', 'Desktop: C, C++, Java y Python', 'SGBD: PostgreSQL y MySQL', ],
		typeSpeed: 50,
		backSpeed: 40,
		loop: true
	});

	animar_skill_bar()
	$(window).on('resize scroll',animar_skill_bar);

	$('.proyecto-filtros .btn').click(function() {
		$(".proyecto-filtros").find(".active").removeClass("active");
		$(this).addClass("active");
	});

	var proyectos_items = $('.proyecto-items').isotope({
		itemSelector: '.proyecto-item',
		masonry: {
			isFitWidth: true
		}
	});

	$('.proyecto-filtros .btn').on( 'click', function() {
		var filterValue = $(this).attr('data-filter');
		proyectos_items.isotope({ filter: filterValue });
	});

	$('.counter').counterUp({
		delay: 30,
		time: 3000,
	});

	AOS.init();
});