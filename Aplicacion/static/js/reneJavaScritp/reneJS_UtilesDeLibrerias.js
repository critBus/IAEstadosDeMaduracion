//import date.format.js
function getStrFromDate(d,formato){
    //"mm/dd/yy"    06/09/07
    //"hh:MM:ss TT" 05:46:21 PM
	return dateFormat(d, formato);
}