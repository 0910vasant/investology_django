;(function (global, factory) {
   typeof exports === 'object' && typeof module !== 'undefined'
       && typeof require === 'function' ? factory(require('/static//moment')) :
   typeof define === 'function' && define.amd ? define(['/static//moment'], factory) :
   factory(global.moment)
}(this, (function (moment) { 'use strict';
