/* show or hide the discussions box */
$(function() {
	$('#ctr_dis').click(function () {
		$('#discussions').slideToggle('slow');
	});
});

/* update the screen */
$(function() {
	if (!window.WebSocket) { 
		window.WebSocket = window.MozWebSocket; 
	} 
	if (window.WebSocket) {
		var ws_url = window.location.href.replace('http', 'ws') + 'screenshot';
		console.log('ws_url : ' + ws_url);
		socket = new WebSocket(ws_url); 
		socket.onmessage = function(event) {
			$('#main').css('backgroundImage', 'url(' + event.data + ')');
		};
		socket.onopen = function(event) { 
			console.log('Web socket connected');
		}; 
		socket.onclose = function(event) { 
			console.log('Web Socket closed'); 
		};
	} else { 
		alert('Your browser does not support Web Socket.');
	}
});

/* chat room */
$(function() {
	if (!window.WebSocket) { 
		window.WebSocket = window.MozWebSocket; 
	} 
	if (window.WebSocket) {
		var ws_url = window.location.href.replace('http', 'ws') + 'chatRoom';
		console.log('ws_url : ' + ws_url);
		socket = new WebSocket(ws_url); 
		socket.onmessage = function(event) {
			var ta = $('#responseText'); 
			ta.text(ta.text() + "\n" + event.data);
			$('#newMessage').val('');

			/* cache the discusions */
			if (!window.localStorage) {
				console.log('This browser does NOT support localStorage');
			} else {
				localStorage['discussion_content'] = ta.text();
			}
		};
		socket.onopen = function(event) { 
			console.log('Web socket connected');
		}; 
		socket.onclose = function(event) { 
			console.log('Web Socket closed'); 
		};
	} else { 
		alert('Your browser does not support Web Socket.');
	}
});

// init style
$(function() {
	$('#responseText').css('height', $('#discussions').height() * 0.9 + 'px');	
	$('#responseText').css('width', $('#discussions').width() - 2 * parseFloat($('#discussions').css('padding-left')) + 'px');
	$('#row').css('height', $('#discussions').height() * 0.1 + 'px');
	$('#row').css('line-height', $('#discussions').height() * 0.1 + 'px');
});

function send(message) {
	if (!window.WebSocket || message == "") { return; }
	if (socket.readyState == WebSocket.OPEN) {
		socket.send(message);
	} else {
		alert("The socket is not open."); 
	}
}

/* store discussions */
/* cache the discussion as more as 2M. */
$(function () {
	if (!window.localStorage) {
		console.log('This browser does NOT support localStorage');
	} else {
		if (localStorage['discussion_content']) {
			if (localStorage['discussion_content'].length > 2 * 1024 * 1024) {
				localStorage.removeItem('discussion_content');
			}
			$('#responseText').text(localStorage['discussion_content']);
		}
	}
});