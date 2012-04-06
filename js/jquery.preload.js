/**
 * jQuery.Preload
 * Copyright (c) 2008 Ariel Flesler - aflesler(at)gmail(dot)com
 * Licensed under GPL license (http://www.opensource.org/licenses/gpl-license.php).
 * Date: 1/29/2008
 *
 * @projectDescription Multifunctional preloader
 * @author Ariel Flesler
 * @version 1.0.1
 *
 * @id jQuery.preload
 * @param {String, jQuery, Array< String, <a>, <img> >} original Collection of sources to preload
 * @param {Object} settings Hash of settings.
 *
 * @id jQuery.fn.preload
 * @param {Object} settings Hash of settings.
 * @return {jQuery} Returns the same jQuery object, for chaining.
 *
 * @example Link Mode:
 *	$.preload( '#images a' );
 *
 * @example Rollover Mode:
 *	$.preload( '#images img', {
 *		find:/\.(gif|jpg)/,
 *		replace:'_over.$1'
 *	});
 *
 * @example Src Mode:
 *	$.preload( [ 'red', 'blue', 'yellow' ], {
 *		base:'images/colors/',
 *		ext:'.jpg'
 *	});
 *
 * @example Placeholder Mode:
 *	$.preload( '#images img', {
 *		placeholder:'placeholder.jpg',
 *		notFound:'notfound.jpg'
 *	});
 **/
;(function( $ ){
	
	$.preload = function( original, settings ){
		if( original.split )//selector
			original = $(original);
		if( !original.length )
			return;

		settings = $.extend( {}, $.preload.defaults, settings );
		var sources = $.map( original, function( source ){
			if( !source ) 
				return '';
			if( source.split )//URL Mode
				return settings.base + source + settings.ext;
			var url = source.src || source.href || '';//save the original source
			if( settings.placeholder && source.src )//Placeholder Mode, if it's an image, set it.
				source.src = settings.placeholder;
			if( settings.find )//Rollover mode
				url = url.replace( settings.find, settings.replace );
			return url;
		});
		
		var data = {
			loaded:0,//how many were loaded successfully
			failed:0,//how many urls failed
			next:0,//which one's the next image to load (index)
			done:0,//how many urls were tried
			found:false,//whether the last one was successful
			total:sources.length//how many images are being preloaded overall
		};
		var $img = $(new Array(settings.threshold)).map(function(){
			return new Image();
		}).load(handler).error(handler).each(fetch);
		
		function handler( e ){
			data.found = e.type == 'load';
			data.image = this.src;
			var orig = data.original = original[this.index];
			data[data.found?'loaded':'failed']++;
			data.done++;
			if( settings.placeholder && orig.src )//special case when on placeholder mode
				orig.src = data.found && data.image || settings.notFound || orig.src;
			if( settings.onComplete )
				settings.onComplete( data );
			if( data.done < data.total )//let's continue
				fetch.call( this );
			else{//we are finished
				if($img != null){
					$img.unbind('load').unbind('error');//cleanup
					$img = null;
				}
				if( settings.onFinish )
					settings.onFinish( data );
			}
		};
		function fetch(){
			if( data.next == data.total ) return false;//no more to fetch
			this.index = data.next;//save it, we'll need it.
			data.original = original[data.next];
			this.src = sources[data.next++];
			if( settings.onRequest ){
				data.image = this.src;
				settings.onRequest( data );
			}
		};
	};
	
	$.preload.defaults = {
		threshold:1,//how many images to load simultaneously
		base:'',//URL mode: a base url can be specified, it is prepended to all string urls
		ext:'',//URL mode:same as base, but it's appended after the original url.
		find:null,//Rollover mode: a string or regex for the replacement
		replace:'',//Rollover mode: replacement (can be left empty)
		placeholder:'',//Placeholder Mode: url of an image to set while loading
		notFound:''//Placeholder Mode: Optional url of an image to use when the original wasn't found
		/*
		onRequest:function( data ){ ... },//callback called every time a new url is requested
		onComplete:function( data ){ ... },//callback called every time a response is received(successful or not)
		onFinish:function( data ){ ... }//callback called after all the images were loaded(or failed)
		*/
	};
	
	$.fn.preload = function( settings ){
		$.preload( this, settings );
		return this;
	};
	
})( jQuery );