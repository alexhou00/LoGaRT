function readURL(input) {
if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
        var image = new Image();
        image.src = e.target.result;
        image.onload = function () {
            var factor = Math.floor(this.height / 250);
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