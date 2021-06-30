/**
 * To find expired mdb
 */

let input = document.querySelector("input");

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

if (!input) {
    id = +getParameterByName("MDB_ID") + 1
    url = `/MDB/MessagesIndex?MDB_ID=${id}`
    window.location = url;
}
