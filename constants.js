
var SUN_ROW = 3;
var MON_ROW = 38;
var TUES_ROW = 72;
var WED_ROW = 106;

/* SCRIPT OPTIONS */
/* Identifiers within OPTIONS object are pulled from how they are named in the Dropdowns & Script Options sheet */
var OPTIONS_START_ROW = 12;
var OPTIONS_START_COL = 2;

var OPTIONS = {};
/* END SCRIPT OPTIONS */

/* SHEET NAMES */
var MASTER_NAME = 'Master Schedule';
var TEMPLATE_NAME = 'Template LEG';
var OPTIONS_NAME = 'Dropdowns & Script Options';
var DISTANCES_NAME = 'Distances';
var ELEMENT_INFO_NAME = 'Element Info';

function LEG_SHEET_NAME(num) {
  return "LEG " + num;
  // test
}
/* END SHEET NAMES */