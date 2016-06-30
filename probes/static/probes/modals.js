var $confirmationModalDialogElement;

$(function() {
    $confirmationModalDialogElement = $('#confirmationModal').remove();
});

function showConfirmationDialog(title, message, proceedText, cancelText, proceedClass, proceedCallback) {
    $('#confirmationModal').remove();
    $('body').append($confirmationModalDialogElement.clone());
    $('#confirmationModal .modal-title').html(title);
    $('#confirmationModal .modal-body').html(message);
    $('#confirmationModal .cancel-button').html(cancelText);
    $('#confirmationModal .proceed-button').html(proceedText);
    $('#confirmationModal .proceed-button').addClass(proceedClass);
    $('#confirmationModal .proceed-button').click(function () {
        proceedCallback();
        $('#confirmationModal').modal('hide');
    });
    $('#confirmationModal').modal('show');
}
