var scmodel;

$(function () {
  var contactContainer = $('#weblar-container-contact');
  var aboutContainer = $('#weblar-container-about');

  var contactButton = $('#weblar-link-contact');
  var aboutButton = $('#weblar-link-about');

  var aboutClose = $('#weblar-icon-close');
  var contactClose = $('#weblar-icon-contact-close');

  var containers = $('.weblar-container');
  var loading = $('#loading');

  

  /* Setup the environment */
  var clear = function () {
    contactContainer.hide();
    aboutContainer.hide();
  };

  contactButton.on('click', function () {
    clear();
    contactContainer.show();

  
  });

  aboutButton.on('click', function () {
    clear();
    aboutContainer.show();
  });

  aboutClose.on('click', function () {
    aboutContainer.hide();
  });

  contactClose.on('click', function () {
    contactContainer.hide();
  });

  containers.on('mousewheel', function (event) {
    event.stopPropagation();
  });

  $(document).on('keyup', function (event) {
    if(event.keyCode == 27) {
      clear();
    }
  });

});
