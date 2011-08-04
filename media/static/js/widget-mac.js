if($ == undefined) {
	var $ = django.jQuery;
}

$('document').ready(function() {
	var mac_fields = $('form input.maiz-input-widget');

	function create_input(mac) {
		var html = '<input type="text" value="'+ mac +'" />';
		return html;
	}

	function expand(index, element) {
		element = $(element)

		element.hide();

		var macs = element.val().split(',');
		var list = [];

		var root = $('<ul></ul>');

		function append_input(content) {
			var input = $(create_input(content));
			root.append($('<li></li>').append(input));
			input.change(condense);

			list[list.length] = input;
		}

		function condense() {
			var vals = [];
			var j = 0;
			for(i in list) {
				var val = list[i].val();
				if(val != '') {
					vals[j++] = val;

					if(list.length - 1 == i) {
						append_input('');
					}
				}
			}
			element.val(vals.join(','));
			console.log(element.val());
		}

		for(i in macs) {
			append_input(macs[i])
		}

		if(macs[0] != '') append_input('');

		element.before(root);
	}

	mac_fields.each(expand);
});
