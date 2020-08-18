// JS for Index.html for the Monitor system.
$(document).ready(function () {
    // Boot strap tooltip stuff
    $('[data-toggle="tooltip"]').tooltip();
    $('#add-panel').hide()
    $('#remove-panel').hide()

    // Unhide the choice panel.  Hide the others.
    $('#hosts-modal').on('shown.bs.modal', function() {
        $('#choice-panel').show();
        $('#add-panel').hide()
        $('#remove-panel').hide()
    });

    // Click on "add host" from choice panel button.
    $('#add-host-selection').click(function () {
        // Hide the choice panel / show the add host panel.
        $('#choice-panel').hide();
        $('#remove-panel').hide()
        $('#add-panel').show();
        $('#add-panel-input').val("");
    });

    // Click on "Remove host" from the choice panel button.
    $('#delete-host-selection').click(function () {
        // Hide the choice panel / show the remove host panel.
        $('#choice-panel').hide();
        $('#remove-panel').show()
        $('#add-panel').hide();
        // Get the items for the selection.  First clear all...
        $('#host-selection').empty()
        // Get the data from the route.
        let revajax = $.ajax({
            type: 'GET',
            url: '/gethosts',
            statusCode: {
                // Failed.
                500: function () {
                    alert("Could not load hosts.  Please try again in a few minutes.");
                    return
                }
            },
            contentType: "application/json",
            dataType: 'json',
            success: function (result) {
                // Got something back...
                for (var key in result) {
                    // Data has been returned!
                    $('#host-selection').append("<option>"+ key + "</option>")
                }
            }
        });
    });

    // Click on "Add host" from add panel.
    $('#button-add-host').click(function () {
        // Send the function back to /addhost
        hostVal = $('#add-panel-input').val();
        hostVal = hostVal.trim();
        if (hostVal === "") {
            return
        }
        // Determined that this is a real value...
        let outVal = {}
        outVal['host']=hostVal
        // Sending out...
        $retv = $.ajax( {
            type: "POST",
            url: "/addhost",
            data: JSON.stringify(outVal),
            contentType: "application/json",
            dataType: "json"
        });
        $("#hosts-modal").modal('toggle');
    });

    // If remove host is clicked...
    $("#button-remove-host").click(function () {
        // Figure out what value is highlighted and remove it.
        let hostToDelete = $('#host-selection').val();
        // Dictionary to send as json.
        let hostOut = {}
        hostOut['remove']=hostToDelete;
        // Sending out...
        $retv = $.ajax ( {
            type: "POST",
            url: "/deletehost",
            data: JSON.stringify(hostOut),
            contentType: "application/json",
            dataType: "json"
        });
        $("#hosts-modal").modal('toggle');
    });

    // If refresh is clicked from the menu.
    $('#a-refresh').click(refreshNow);
});

function refreshNow () {
    let hostOut = {}
    hostOut['refresh'] = 'now';
    // Sending out...
    $retv = $.ajax({
        type: "POST",
        url: "/refresh",
        data: JSON.stringify(hostOut),
        contentType: "application/json",
        dataType: "json",
        success: function() {
            window.location.reload(true);
        },
        beforeSend: function() {
            $('body').append('<div id="requestOverlay" class="request-overlay"></div>'); /*Create overlay on demand*/
            $("#requestOverlay").show();/*Show overlay*/
        },
        complete: function () {
            $("#requestOverlay").remove();/*Remove overlay*/
        }
    });
}

