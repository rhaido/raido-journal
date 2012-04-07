/**
 * jQuery.Preload - Multifunctional preloader
 * Copyright (c) 2008 Ariel Flesler - aflesler(at)gmail(dot)com
 * Licensed under GPL license (http://www.opensource.org/licenses/gpl-license.php).
 * Date: 1/29/2008
 * @author Ariel Flesler
 * @version 1.0.1
 **/
;(function($){$.preload=function(c,d){if(c.split)c=$(c);if(!c.length)return;d=$.extend({},$.preload.defaults,d);var f=$.map(c,function(a){if(!a)return'';if(a.split)return d.base+a+d.ext;var b=a.src||a.href||'';if(d.placeholder&&a.src)a.src=d.placeholder;if(d.find)b=b.replace(d.find,d.replace);return b});var g={loaded:0,failed:0,next:0,done:0,found:false,total:f.length};var h=$(new Array(d.threshold)).map(function(){return new Image()}).load(handler).error(handler).each(fetch);function handler(e){g.found=e.type=='load';g.image=this.src;var a=g.original=c[this.index];g[g.found?'loaded':'failed']++;g.done++;if(d.placeholder&&a.src)a.src=g.found&&g.image||d.notFound||a.src;if(d.onComplete)d.onComplete(g);if(g.done<g.total)fetch.call(this);else{if(h!=null){h.unbind('load').unbind('error');h=null}if(d.onFinish)d.onFinish(g)}};function fetch(){if(g.next==g.total)return false;this.index=g.next;g.original=c[g.next];this.src=f[g.next++];if(d.onRequest){g.image=this.src;d.onRequest(g)}}};$.preload.defaults={threshold:1,base:'',ext:'',find:null,replace:'',placeholder:'',notFound:''};$.fn.preload=function(a){$.preload(this,a);return this}})(jQuery);