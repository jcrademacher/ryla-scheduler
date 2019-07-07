/* NOTE: ANY ROW OR COLUMN CONSTANTS ARE REFERENCED TO INDEX 0. THIS IS BECAUSE
/* THIS SCRIPT WILL BE USING VALUE ARRAYS MORE OFTEN THAN THE INDEXING CONVENTION
/* USED BY GOOGLE SHEETS (INDEX 1)

/* MASTER SCHEDULE CONSTANTS */
var SUN_ROW = 2;
var MON_ROW = 37;
var TUES_ROW = 71;
var WED_ROW = 105;

var MASTER_START_COL = 1;
var MASTER_START_ROW = 2;

var NUM_SECTIONS = 6;

var SLOT_SIZE = 30; // in minutes

/* END MASTER SCHEDULE CONSTANTS */

/* SCRIPT OPTIONS */
/* Identifiers within OPTIONS object are pulled from how they are named in the Dropdowns & Script Options sheet */
var OPTIONS_START_ROW = 11;
var OPTIONS_START_COL = 1;

var NUM_LEGS = 'NUM_LEGS';
var MAX_HILL_TRAVELS = 'MAX_HILL_TRAVELS';
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