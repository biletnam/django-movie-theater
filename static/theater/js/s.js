/**
 * Variables
 */
var seatW = 20;
var seatH = 20;
var seatP = 2;
var maxH = maxW = 0;
var seatCount = 1;
var tentative = [];

/**
 * Redraw floor if exists
 */
$(document).ready(function () {
    if ($('.floor').length && $('.floor .seat').length) {
        redrawFloor();
        Pusher.logToConsole = true;

        var pusher = new Pusher('81c8c04b4e6bbee4d616', {
            cluster: 'eu',
            encrypted: true
        });

        var channel = pusher.subscribe('theater');
        channel.bind('seatupdates_' + MOVIE_ID, function (data) {
            setSeatClass(data.tentative, 'tentative');
            setSeatClass(data.booked, 'booked');
        });
        pingFloor();
    }

});

/**
 * DOM mouse events
 */
$(document).on('change', '.seatcount', function () {
    seatCount = parseInt($(this).val());
});
$(document).on('mouseout', '.floor .seat', unhover);
$(document).on('click', '.floor .seat', onSeatClicked);
$(document).on('mouseover', '.floor .seat', onSeatHover);
$(document).on('click', '.confirm-booking', confirmBooking);
$(document).on('click', '#myModal .btn-primary', makeBooking);
/**
 * UI Loading animation
 */
window.loader = {
    show: function () {
        $('.loading').addClass('show');
    },
    hide: function () {
        $('.loading').removeClass('show');
    }
};


/**
 * Helper methods
 */
function redrawFloor() {
    $('.floor .seat').each(function () {
        var y = parseInt($(this).data('y')) - 1;
        var x = parseInt($(this).data('x')) - 1;
        maxH = Math.max(y, maxH);
        maxW = Math.max(x, maxW);
        $(this).css({
            left: x * (seatW + seatP) + seatP,
            top: y * (seatH + seatP) + seatP,
            width: seatW,
            height: seatH
        });
    });
    maxH += 1;
    maxW += 1;
    $('.floor').css({
        height: maxH * (seatH + seatP) + seatP,
        width: maxW * (seatW + seatP) + seatP
    });
}

function onSeatClicked(e) {
    e.preventDefault();
    if (!$('.seat.hovering').length) {
        return;
    }
    loader.show();

    if (tentative.length) {
        $.ajax({
            url: UNTENTATIVE_URL,
            type: "GET",
            dataType: "json",
            data: {
                movie_id: MOVIE_ID,
                seat_id: tentative.join(',')
            },
            complete: function (r) {
                loader.hide();
            }
        });
        unsetSeatClassById(tentative, 'tentative');
    }
    tentative = [];

    $.ajax({
        url: TENTATIVE_URL,
        type: "GET",
        dataType: "json",
        data: {
            movie_id: MOVIE_ID,
            seat_id: $('.seat.hovering').map(function () {
                var id = $(this).data('id');
                tentative.push(id);
                return id;
            }).toArray().join(',')
        },
        complete: function (r) {
            loader.hide();
        }
    });
}

function onSeatHover() {
    unhover();
    var o = $(this);
    var x = o.data('x');
    var y = o.data('y');
    if (!areAvailable(o, x, y, seatCount)) {
        unhover();
    }
}

function unhover() {
    unsetSeatClass('hovering');
}

function hover(o) {
    o.addClass('hovering');
}

function isNotAvailable(o) {
    return o.hasClass('booked') || o.hasClass('tentative');
}

function isAvailable(o) {
    return !isNotAvailable(o);
}

// validate that this seat and any other (if buying more) is available
// NOT leaving one space in between seats
function areAvailable(o, x, y, count) {
    if (isNotAvailable(o)) {
        return false;
    }
    var validated = [];
    for (var i = 0; i < count; i++) {
        var exists = $('.seat_' + (x + i) + '_' + y);

        if (!exists.length) {
            return false;
        }

        if (isNotAvailable(exists)) {
            return false;
        }
        validated.push(exists);
    }

    // one space before first
    var prev2 = $('.seat_' + (x - 2) + '_' + y);
    var prev = $('.seat_' + (x - 1) + '_' + y);
    if (prev.length && isAvailable(prev)) {
        if (prev2.length && isNotAvailable(prev2)) {
            return false;
        }
    }
    // one space after last
    var next2 = $('.seat_' + (x + count + 1) + '_' + y);
    var next = $('.seat_' + (x + count) + '_' + y);
    if (next.length && isAvailable(next)) {
        if (next2.length && isNotAvailable(next2)) {
            return false;
        }
    }

    for (var s in validated) {
        hover(validated[s]);
    }

    return true;
}
/**
 // copy and paste into dev console
 $('.seat').removeClass('tentative booked');
 $('.seat').each(function () {
    if (Math.random() > .7) {
        $(this).addClass(Math.random() > .8 ? 'tentative' : 'booked');
    }
});
 */

function unsetSeatClass(cls) {
    $('.seat').removeClass(cls);
}
function unsetSeatClassById(array, cls) {
    for (var i = 0; i < array.length; i++) {
        $('.seat_id_' + array[i]).removeClass(cls);
    }
}
function setSeatClass(array, cls) {
    unsetSeatClass(cls);
    for (var i = 0; i < array.length; i++) {
        $('.seat_id_' + array[i]).addClass(cls);
    }
}


function confirmBooking(e) {
    e.preventDefault();
    $('#myModal .modal-body').html('Seats: ' + tentative.join(', '));
    $('#myModal').modal();
}

function makeBooking(){
    loader.show();
    // if ($(this).hasClass('disabled')) {
    //     return;
    // }
    // $(this).addClass('disabled');
    $.ajax({
        url: BOOKING_URL,
        context: $(this),
        type: "GET",
        dataType: "json",
        data: {
            movie_id: MOVIE_ID,
            seat_id: tentative.join(','),
            group: Math.random().toString(36).substring(2) + new Date().getTime().toString(36)
        },
        success: function (r) {
            loader.hide();
            document.location.href = r.redirect
        }
    });
}

function pingFloor() {
    loader.show();
    $.ajax({
        url: PING_URL,
        type: "GET",
        dataType: "json",
        data: {
            movie_id: MOVIE_ID
        },
        success: function (r) {
            loader.hide();

            setSeatClass(r.tentative, 'tentative');
            setSeatClass(r.booked, 'booked');
        }
    });
}