// This is an example client for the WeatherTalk API.
//
// This client is based on the example client implemented in the fourth
// exercise of the PWP course.  The functions that are directly
// borrowed from there are marked as such.

"use strict"; // TODO: remove when delivering

const COLLECTIONJSON = "application/vnd.collection+json";
const PLAINJSON = "application/json";

function appendObservationRow(body) {
    $(".resulttable tbody").append(observationRow(body));
}

// Directly borrowed from the PWP exercise 4.
function getResource(href, renderer) {
    $.ajax({
        url: href,
        success: renderer,
        error: renderError,
    });
}

function getSubmittedObservation(data, status, jqxhr) {
    let href = jqxhr.getResponseHeader("Location");
    if (href) {
        getResource(href, appendObservationRow);
    }
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

// Directly borrowed from the PWP exercise 4.
function renderError(jqxhr) {
    let msg = jqxhr.responseJSON["collection"]["error"]["message"];
    $("div.notification").html("<p class='error'>" + msg + "</p>");
}

function renderObservation(body) {
    let nav = $("div.navigation");
    nav.empty();
    let item = body.collection.items[0];
    item.links.forEach(function (it) {
        nav.append("<a href='" + it.href + "'>" + it.rel + "</a>");
    });
    renderObservationForm(item.data, item.href, "PUT");
}

function renderObservationForm(data, href, method) {
    let form = $("<form>");
    form.attr("action", href);
    form.attr("method", method);
    form.submit(submitObservation);
    let new_data = {};
    data.forEach(function (item) {
        new_data[item.name.replace("-", "_")] = item;
    });
    console.log(new_data);
    let order = [
        "location",
        "observed_at",
        "temperature",
        "wind",
        "wind_direction",
        "humidity",
    ];
    order.forEach(function (item) {
        console.log(new_data[item]);
        if (item in new_data) {
            form.append("<label>" + new_data[item].prompt + "</label>");
            form.append(
                "<input type='text' "
                + "name='" + new_data[item].name + "' "
                + "value='" + new_data[item].value + "'>"
            );
        }
    });
    form.append("<input type='submit' name='submit' value='Submit'>");
    $("div.form").html(form);
}

function renderObservations(body) {
    $("div.navigation").empty();
    $(".resulttable thead").html(
        "<tr><th>Location</th><th>Observed at</th></tr>"
    );
    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.collection.items.forEach(function (item) {
        tbody.append(observationRow(item));
    });
    renderObservationForm(
        body.collection.template.data,
        body.collection.href,
        "POST"
    );
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

function submitObservation(event) {
    event.preventDefault();

    let data = {};
    let form = $("div.form form");
    console.log($("div.form form input"));
    $.makeArray($("div.form form input")).forEach(function (item) {
        data[item.name] = item.value;
    });
    sendData(form.attr("action"), form.attr("method"), data, getSubmittedObservation);
}

$(document).ready(function () {
    getResource("http://localhost:5000/api/observations/", renderObservations);
});
