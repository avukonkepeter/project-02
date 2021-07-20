$(document).ready(() => {
    let id_number_error_div = $('#id_number_error_div');
    id_number_error_div.hide();
    if (window.location.href.indexOf('edit') == -1){
        $("#clientForm").submit(function (event) {
            id_number_error_div.hide();
            let id_number = $('#id_id_number').val()
            // event.preventDefault();
            // return true;
            $.ajax({
                data: {id_number: id_number},
                type: 'GET',
                url: '/ajax/validate_id/',
                async: false,
                success: function (response) {
                    if (response['is_valid'] !== undefined && response['is_valid'] === true){
                        // ID is valid
                        $.ajax(
                        {
                            data: {id_number: id_number},
                            type: 'GET',
                            url: '/ajax/check_id/',
                            async: false,
                            success: (response) => {
                                if(response['exists'] !== undefined && response['exists'] === true){
                                    id_number_error_div.children('.errorText').text(response['message']);
                                    id_number_error_div.show();
                                    event.preventDefault();
                                }
                            },
                            error: (e) => {
                                console.log(e);
                            }
                        })
                    } else {
                        event.preventDefault();
                        id_number_error_div.children('.errorText').text(response['message']);
                        id_number_error_div.show();
                    }
                },
                error: function (request, status, error) {
                    console.log(request.responseText);
                }
            });
        });
    }

    const user_input = $("#autocomplete_search");
    const search_icon = $('#search-icon')
    const artists_div = $('.client-list-body')
    const endpoint = '/ajax/search_clients/'
    const delay_by_in_ms = 700
    let scheduled_function = false

    let ajax_call = function (endpoint, request_parameters) {
        $.getJSON(endpoint, request_parameters)
            .done(response => {
                // fade out the artists_div, then:
                artists_div.fadeTo('slow', 0).promise().then(() => {
                    // replace the HTML contents
                    artists_div.html(response['html_data'])
                    // fade-in the div with new contents
                    artists_div.fadeTo('slow', 1)
                    // stop animating search icon
                    search_icon.removeClass('blink')
                })
            })
    }

    user_input.on('keyup', function () {

        const request_parameters = {
            term: $(this).val() // value of user_input: the HTML element with ID user-input
        }

        // start animating the search icon with the CSS class
        search_icon.addClass('blink')

        // if scheduled_function is NOT false, cancel the execution of the function
        if (scheduled_function) {
            clearTimeout(scheduled_function)
        }

        // setTimeout returns the ID of the function to be executed
        scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
    })
});

