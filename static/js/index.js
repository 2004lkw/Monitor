// JS for Index.html for the Monitor system.
$(document).ready(function () {
    // Boot strap tooltip stuff
    $('[data-toggle="tooltip"]').tooltip();
    $('#add-panel').hide()
    $('#remove-panel').hide()

    // Unhide the choice panel.  Hide the others.
    $('#hosts-modal').on('shown.bs.modal', function () {
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

    // This creates the summary area.
    countofgreen = $('.led-green').length;
    countofyellow = $('.led-yellow').length;
    countofred = $('.led-red').length;
    counttotal = $('.bar-container').length;
    $('#summary-area').append(
        // the header part of details
        "<div class='accordion' id='main-details'><div class='card'><div class='card-header' id='card-header-one' style='background-color: #c7d6f0; text-align: center;'>" +
        '<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#deatails-pane1" aria-expanded="true" aria-controls="deatails-pane1">' +
        'Monitor Summary' +
        '</button ></div>' +
        // the body of the card that makes the details pane.
        '<div id="deatails-pane1" class="collapse" aria-labelledby="headingOne" data-parent="#main-details">' +
        '<div class="card-body" style="background-color: #c7d6f0;">' +
        // the table that's displayed in the details.
        "<table width='100%'><tbody style='width: 100%; border-bottom: black 1px solid' >" +
        "<tr style='wdith: 100%;'  id='total-clicky' class='total-clicky'><td colspan='3'>Total  " + counttotal +
        "<tr style='wdith: 100%;' id='total-clicky-2'>" +
        "<td class='green-clicky' id='green-clicky'>Good : <span style='color: green; font-weight: bold;'>" + countofgreen + "</span></td>" +
        "<td class='yellow-clicky' id='yellow-clicky'>yellow : <span style='color: #c2c200; font-weight: bold;'>" + countofyellow + "</span></td>" +
        "<td class='red-clicky' id='red-clicky'>red : <span style='color: red; font-weight: bold;'>" + countofred + "</span></td>" +
        "</tbody></table></div ></div ></div ></div >"
    );

    $('#red-clicky').click(function () {
        // Hide all but what is red.
        showOnlyInTables('led-red');
        showImportants();
    });

    $('#yellow-clicky').click(function () {
        // Hide all but what is yellow.
        showOnlyInTables('led-yellow');
        showImportants();
    });

    $('#green-clicky').click(function () {
        // Hide all but what is green.
        showOnlyInTables('led-green');
        showImportants();
    });

    $('#total-clicky').click(function () {
        // show everything.
        $("tr").each(function (index, element) {
            $(this).show();
        });
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
                    $('#host-selection').append("<option>" + key + "</option>")
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
        outVal['host'] = hostVal
        // Sending out...
        $retv = $.ajax({
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
        hostOut['remove'] = hostToDelete;
        // Sending out...
        $retv = $.ajax({
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

function showOnlyInTables(searchid) {
    let prevelement;
    searchid = '.' + searchid
    $("tr").each(function (index, element) {
        $(this).hide();
        if ($(this).find(searchid).length != 0) {
            $(this).show();
            prevelement.show();
        }
        prevelement = $(this);
    });
}

function showImportants() {
    // ensures that important stuff is shown.
    let tc = $('#total-clicky')
    let tc2 = $('#total-clicky-2')
    tc.show();
    tc2.show();
}

function refreshNow() {
    let hostOut = {}
    hostOut['refresh'] = 'now';
    // Sending out...
    $retv = $.ajax({
        type: "POST",
        url: "/refresh",
        data: JSON.stringify(hostOut),
        contentType: "application/json",
        dataType: "json",
        success: function () {
            window.location.reload(true);
        },
        beforeSend: function () {
            $('body').append('<div id="requestOverlay" class="request-overlay"></div>'); /*Create overlay on demand*/
            $("#requestOverlay").show();/*Show overlay*/
        },
        complete: function () {
            $("#requestOverlay").remove();/*Remove overlay*/
        }
    });
}

