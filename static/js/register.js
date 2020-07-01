"use strict";


$( document ).ready(function() {
    $('#user-reg-form').on('submit', (evt) => {
        if ($('#password-field').val() !== $('#password-confirm-field').val()) {
            evt.preventDefault()
            alert("Password fields do not match. Please try again.");
        };
    });
});