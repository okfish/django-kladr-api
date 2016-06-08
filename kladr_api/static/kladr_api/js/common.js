var $kladr_form_vals = {},
    $value_separator = '. ',
	$DEBUG = false;

function log_message(msg){
	if ($DEBUG && msg) {
		console.log(msg);
	}
}

function format_value (obj, query) {
	var objs;

	if (query.oneString) {
		if (obj.parents) {
			objs = [].concat(obj.parents);
			objs.push(obj);

			return $.kladr.buildAddress(objs);
		}

		return (obj.typeShort ? obj.typeShort + '. ' : '') + obj.name;
	}
	if (obj) {
		log_message('...formatted value:' + obj.name);
	}
	return (obj.typeShort ? obj.typeShort + $value_separator : '') + ( obj.name || obj);
}

function unformat_value (val) {
    // looks ugly but clearly
    return val.split($value_separator).slice(1).join($value_separator) || val
}

function format_label (obj, query) {
	var label = '';

	var name = obj.name.toLowerCase();
	query = query.name.toLowerCase();

	var start = name.indexOf(query);
	start = start > 0 ? start : 0;

	if (obj.typeShort) {
		label += obj.typeShort + '. ';
	}

	if (query.length < obj.name.length) {
		label += obj.name.substr(0, start);
		label += '<strong>' + obj.name.substr(start, query.length) + '</strong>';
		label += obj.name.substr(start + query.length, obj.name.length - query.length - start);
	} else {
		label += '<strong>' + obj.name + '</strong>';
	}

	if (obj.parents) {
		for (var k = obj.parents.length - 1; k > -1; k--) {
			var parent = obj.parents[k];
			if (parent.name) {
				if (label) label += '<small>, </small>';
				label += '<small>' + parent.name + ' ' + parent.typeShort + '.</small>';
			}
		}
	}

	return label;
}

function setLabel($input, text) {
	if (text) {
		text = text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
		$input.parent().parent().find('label').text(text);
	}
}

function showError($input, message) {
	var $parent = $input.parents("form");
	var $tooltip = $parent.find('.form-tooltip');

    $tooltip.find('span').text(message);

	var inputOffset = $input.offset(),
		parentOffset = $parent.offset(),
		inputWidth = $input.outerWidth(),
		inputHeight = $input.outerHeight(),
	    tooltipHeight = $tooltip.outerHeight(),
	    l = (inputOffset.left - parentOffset.left + inputWidth - 10),
	    t = (inputOffset.top - parentOffset.top + (inputHeight - tooltipHeight) / 2 - 1);
	$tooltip.css({
		left: l + 'px',
		top: t + 'px'
	});
	$tooltip.show();
}

function getRegionName ( obj ) {
	var result = '';
	if (obj.parents) {
		for (var k = obj.parents.length - 1; k > -1; k--) {
			var parent = obj.parents[k];
			if (parent.contentType === 'region') {
				result = parent;
				//log_message(k + '...found region: ' + result.name + ':' + result.zip);
			}
		}
	}
	return result;
}

function formUpdate($input) {
	var $parent = $input.parents("form");
	log_message('Updating form...');
	var $result = $.kladr.getAddress($parent, function (objs) {
		var result = false,
			zip = '';
			$.each(objs, function (i, obj) {
				var name = '',
					type = '';
				if ($.type(obj) === 'object') {
					name = obj.name;
					type = ' ' + obj.type;
					log_message(i + '...found kladr obj: ' + name +':'+ type + ':' + obj.zip);
					result = getRegionName(obj);
					zip = obj.zip || zip;
				}
			});
			return { 'region' :result, 'zip' : zip};
	});
	if ($result['region']) {
		var $reg_input = $parent.find('[data-kladr-type="region"]');
		//log_message('...result region: ' + $result['region'].name); 
		$reg_input.kladr('controller').setValue($result['region']);
	}
	if ($result['zip']) {
		var $zip_input = $parent.find('[data-kladr-type="zip"]'); 
		log_message('...found zip: ' + $result['zip']);
		if (!$zip_input.val()) {
			$zip_input.val($result['zip']);
		}
	}
}

function clearKladrInput($parent,$type) {
	var $inp = $parent.find('[data-kladr-type="'+$type+'"]');
	log_message('...found input:'+$inp.val());
	if ($inp.size()>0) {
		if ($inp.attr('data-kladr-id')) {
			log_message('...deleting kladr value:'+$inp.attr('data-kladr-id'));
			$inp.kladr('controller').clear();
		}
		log_message('...deleting input value:'+$inp.attr('name'));
		$inp.val('');
	}
}

function initKladrForm($parent){

	log_message('Init form started:' + $parent.attr('action'));
	var old_vals = {},
		field = null,
		objs = $parent.find('[data-kladr-type]');
	objs.each(function (i) {
		var inp = $(this);
		var inp_type = inp.data('kladr-type');
		inp.kladr({parentInput : $parent,
				   valueFormat : format_value,
	               labelFormat : format_label, 
	               check : on_check,
	               openBefore : on_before_open,
	               select : on_select,
	               change : on_change,
	               receive : on_receive,
	               sendBefore : on_before_send,
	               withParents : true });
		
		log_message('...field:' +i+'-' + inp_type + '; parent: ' + $parent.attr('action'));
		old_vals[inp_type] = unformat_value(inp.val());
		log_message('...unformatted value:' + old_vals[inp_type]);
		var opts = inp.data('kladr-options');
        log_message('...kladr-options:' + opts.parentId + ' ' + opts.parentType);
		inp.removeAttr('data-kladr-options');
		inp.kladr(opts); 
	});
	$kladr_form_vals = old_vals;
	log_message('Set form values:' + $parent.attr('action'));
	$.kladr.setValues(old_vals, $parent);
}

function on_check (obj) {
	
	var $input = $(this);
	var $tooltip = $input.parents("form").find('.form-tooltip');
	
	if (obj && obj.type) {
		setLabel($input, obj.type);
		$tooltip.hide();
	}
	else {
		showError($input, 'Введено неверно');
	}
}

function on_select (obj) {
	
	var $input = $(this);
	var $form = $input.parents("form");
	var $tooltip = $form.find('.form-tooltip');
	setLabel($input, obj.type);
	$tooltip.hide();
}

function on_change (obj) {
	
	var $input = $(this),
		$parent = $input.parents("form"),
    	$inp_type = $input.attr('data-kladr-type'),
	    $inp_code = $input.attr('data-kladr-id');
	log_message('Changing region by ' + $inp_type +':'+ $inp_code);
	if (obj) {
		setLabel($input, obj.type);
	}
	if ($inp_type == 'region') {
		log_message('... Skipped');
		return false;
	}
	if ($inp_type !== 'street' && $inp_type !== 'building')  {
		log_message('... clear street');
		clearKladrInput($parent,'street');
	}
	if ($inp_type !== 'building') {
		//log_message('... changed building to '+ $input.val());
		clearKladrInput($parent,'building');
	}
	if ($inp_type !== 'zip') {
		var $inp = $parent.find('[data-kladr-type="zip"]');
		log_message('... clear zip:' + $inp.attr('name'));
		$inp.val('');
	}
	formUpdate($input);
}

function on_before_open ( ) {
	var $input = $(this),
	    $parent = $input.parents("form"),
	    $inp_type = $input.attr('data-kladr-type');
	log_message('Selecting by:' + $inp_type);
	if ($inp_type == 'city') {
			log_message('... clear region');
			clearKladrInput($parent,'region');
	}
}

function on_before_send ( obj ) {
	log_message('Sending query by:' + obj.type);
}

function on_receive () {
	var obj = $(this),
		obj_type = obj.data('kladr-type'),
		obj_id = obj.attr('data-kladr-id');
		
	if (obj) {
		log_message('Received response by:' + obj_type +':'+ obj_id);
	} else {
	 	log_message('Received BAD response by:'+ obj_type +':'+ obj_id);
	}
}

$(document).ready(function() {

	var $inp = $(document).find(':input[data-kladr-type="city"]');
	log_message('Found Kladr field...'+ $inp.val());
	var $kladr_form = $inp.parents("form");
	
	if ($kladr_form.size()>0) {
		log_message('Found Kladr form...' + $kladr_form.attr('action'));
		initKladrForm($kladr_form);
	}
	// drop 'disabled' attr before submitting
	// see: http://stackoverflow.com/a/1191365
    $('form').on('submit', function() {
        $(this).find(':input').removeAttr('disabled');
    });
    
    // disable submitting on 'enter' click while dropdowns browsing
    // see http://stackoverflow.com/questions/11235622/jquery-disable-form-submit-on-enter
	$(document).on('keyup keypress', 'form input[type="text"]', function(e) {
	  	if(e.which == 13) {
	    	e.preventDefault();
	    	return false;
  		}
	});
});
