function readURL(input) {
if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
        var image = new Image();
        image.src = e.target.result;
        image.onload = function () {
            var factor = Math.floor(this.height / 320);
            var height = this.height/factor;
            var width = this.width/factor;
        $('#blah').attr('src', this.src).width(width).height(height);
        }
    };

    reader.readAsDataURL(input.files[0]);
    $('#blah').show();
}
else {
    $('#blah').hide();
}
}

$(document).ready(function() {
    var known = { en: true, de: true};
    var lang  = ((navigator.languages && navigator.languages[0]) || navigator.language || navigator.userLanguage || 'en').substr(0, 2);
    if(!known[lang])
        lang = 'en';
    // Find all <div>s with a class of "wrapper" and lang attribute equal to `lang`
    // and make them visibile.
    $('div.wrapper[lang='  + lang + ']').show();
    // Find all <div>s with a class of "wrapper" and lang attribute not equal
    // to `lang` and make them invisibile.
    $('div.wrapper[lang!=' + lang + ']').hide();
});