import $ from 'jquery'
import _ from 'lodash'
import { Tooltip } from 'bootstrap';

export default {
    apiError: function(resp){
        var error_str = '';
        if (resp.status === 400) {
            try {
                obj = JSON.parse(resp.responseText);
                error_str = obj.non_field_errors[0].replace(/[\[\]"]/g,'');
            } catch(e) {
                error_str = resp.responseText.replace(/[\[\]"]/g,'');
            }
        }
        else if ( resp.status === 404) {
            error_str = 'The resource you are looking for does not exist.';
        }
        else{
            error_str = resp.responseText.replace(/[\[\]"]/g,'');
        }
        return error_str;
    },
    apiVueResourceError: function(resp){
        var error_str = '';
        if (resp.status === 400) {
            var text = resp.body[0];
            try {
                obj = JSON.parse(text);
                error_str = obj.non_field_errors[0].replace(/[\[\]"]/g,'');
            } catch(e) {
                error_str = text.replace(/[\[\]"]/g,'');
            }
        }
        else if ( resp.status === 404) {
            error_str = 'The resource you are looking for does not exist.';
        }
        return error_str;
    },
    goBack:function(vm){
        vm.$router.go(window.history.back());
    },
    getCookie: function(name) {
        var value = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1).trim() === (name + '=')) {
                    value = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return value;
    },
    namePopover:function ($,vmDataTable) {
        vmDataTable.on('mouseover','.name_popover',function (e) {
            $(this).popover('show');
            $(this).on('mouseout',function () {
                $(this).popover('hide');
            });
        });
    },
    add_endpoint_json: function ( string, addition ) {
        var res = string.split( ".json" )
        return res[ 0 ] + '/' + addition + '.json';
      },
    dtPopover: function(value,truncate_length=30,trigger='hover'){
        var ellipsis = '...',
        truncated = _.truncate(value, {
            length: truncate_length,
            omission: ellipsis,
            separator: ' '
        }),
        result = '<span>' + truncated + '</span>',
        popTemplate = _.template('<a href="#" ' +
            'role="button" ' +
            'data-toggle="popover" ' +
            'data-trigger="'+trigger+'" ' +
            'data-placement="top auto"' +
            'data-html="true" ' +
            'data-content="<%= text %>" ' +
            '>more</a>');
        if (_.endsWith(truncated, ellipsis)) {
            result += popTemplate({
                text: value
            });
        }
        return result;
    },
    dtPopoverCellFn: function(cell){
        $(cell).find('[data-toggle="popover"]')
            // 1. Find elements that trigger popovers using jQuery.
            //    The selector is updated to 'data-bs-toggle' for Bootstrap 5.
            const popoverTriggerList = $(cell).find('[data-bs-toggle="popover"]');

            // 2. Iterate over each of the found elements.
            popoverTriggerList.each(function () {
                // 'this' refers to the current DOM element in the loop.

                // 3. Initialize the Popover using the Bootstrap 5 JavaScript API.
                const popover = new window.bootstrap.Popover(this, {
                    // Options are not specified here, so they will be read
                    // from the element's data-bs-* attributes in the HTML.
                });

                // 4. Replicate the original click event handler.
                //    We can still use jQuery's .on() method for this.
                $(this).on('click', function (e) {
                    // Prevent the default action of the click event (e.g., following a link).
                    e.preventDefault();
                    // The original 'return true;' is not necessary for preventDefault to work.
                });
            });
    },

    /**
     * Provides a reusable showErrors function for form validation.
     */
    useFormErrors: function() {
        /**
         * Displays validation errors using Bootstrap 5 tooltips.
         * @param {Object} errorMap - Not used, but passed for compatibility.
         * @param {Array} errorList - List of validation errors.
         * @param {HTMLElement[] | jQuery} validElements - List of valid elements (can be jQuery object).
         */
        function showErrors(errorMap, errorList, validElements) {
            const elements = Array.from(validElements);

            // Clear tooltips and error classes from valid elements
            elements.forEach(element => {
                element.removeAttribute("title");

                const tooltip = Tooltip.getInstance(element);
                if (tooltip) {
                    tooltip.dispose();
                }

                const formGroup = element.closest('.form-group');
                if (formGroup) {
                    formGroup.classList.remove('has-error');
                }
            });

            // Add or update tooltips for invalid elements
            for (let i = 0; i < errorList.length; i++) {
                const error = errorList[i];
                const el = error.element;

                const existingTooltip = Tooltip.getInstance(el);
                if (existingTooltip) {
                    existingTooltip.dispose();
                }

                el.setAttribute("title", error.message);

                new Tooltip(el, {
                    trigger: "focus"
                });

                const formGroup = el.closest('.form-group');
                if (formGroup) {
                    formGroup.classList.add('has-error');
                }
            }
        }

        return { showErrors };
    }
};
