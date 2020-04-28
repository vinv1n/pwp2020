// This is an example client for the WeatherTalk API.
//
// This client is based on the example client implemented in the fourth
// exercise of the PWP course.  The functions that are directly
// borrowed from there are marked as such.

"use strict"; // TODO: remove when delivering

const COLLECTIONJSON = "application/vnd.collection+json";
const PLAINJSON = "application/json";

// Directly borrowed from the PWP exercise 4.
function renderError(jqxhr) {
    let msg = jqxhr.responseJSON["collection"]["error"]["message"];
    $("div.notification").html("<p class='error'>" + msg + "</p>");
}

// Directly borrowed from the PWP exercise 4.
function getResource(href, renderer) {
    $.ajax({
        url: href,
        success: renderer,
        error: renderError,
    });
}

function observationRow(item) {
    let itemLink = "<a href='"
        + item.href
        + "'>more...</a>";
    data = {}
    item.data.forEach(function (entry) {
        data[entry["name"]] = entry["value"];
    });
    return "<tr>"
        + "<td>" + data["location"] + "</td>"
        + "<td>" + data["observed-at"] + "</td>"
        + "</tr>";
}

function renderObservationForm(collection, method) {
    let form = $("<form>");
    form.attr("action", collection.href);
    form.attr("method", method);
    form.submit(submitObservation);
    namedescs = {}
    data.forEach(function (item) {
        namedescs[item["name"]] = item["prompt"];
    });
    form.append("<label>" + namedescs.temperature + "</label>");
    form.append("<input type='text' name='temperature'>");
    form.append("<input type='submit' name='submit' value='Submit'>");
    $("div.form").html(form);
}

function renderObservations(body) {
    $("div.navigation").empty();
    $(".resulttable thead").html(
        "<tr><th>Location</th><th>Observed at</th></tr>"
    );
    let tbody = (".resulttable tbody");
    tbody.empty();
    body.collection.items.forEach(function (item) {
        tbody.append(observationRow(item));
    });
    renderObservationForm(body.collection);
}

// Directly borrowed from the PWP exercise 4.
function sendData(href, method, item, postProcessor) {
    $.ajax({
        url: href,
        type: method,
        data: JSON.stringify(item),
        contentType: PLAINJSON,
        processData: false,
        success: postProcessor,
        error: renderError,
    });
}

$(document).ready(function () {
    getResource("http://localhost:5000/api/observations/", renderObservations);
});