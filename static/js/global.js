$(document).ready(function () {
    $('.select2').each(function () {
        $(this).select2({
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: $(this).data('placeholder') || 'Select an option',
            allowClear: true
        });
    });
});