function loadConstants() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var options = {};

  var rows = 10;
  var cols = 2;

  var optionsSheet = ss.getSheetByName(OPTIONS_NAME);
  var optionsRange = optionsSheet.getRange(OPTIONS_START_ROW + 1, OPTIONS_START_COL + 1, rows, cols);
  var optionsValues = optionsRange.getValues();

  for(var r = 0; r < rows; ++r) {
    var optionId = optionsValues[r][0];
    var optionVal = optionsValues[r][1];

    if(optionId != '') {
      options[optionId] = parseInt(optionVal);
    }
  }

  return options;
}

function loadElementInfo() {

}

function loadElementDistances() {

}

/* sectionNum must be a number from 0 to 5. See sheet for what these mean */
// returns a list of ranges that represent the open times between meals that will be filled
// by the scheduler. List index represents section number
function loadSectionRanges() {
  var sectionList = [];

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var masterSheet = ss.getSheetByName(MASTER_NAME);

  var count = 0;
  var maxRows = masterSheet.getMaxRows();
  var maxCols = masterSheet.getMaxColumns();

  var masterRange = masterSheet.getRange(MASTER_START_ROW + 1, MASTER_START_COL + 1, maxRows, maxCols);
  var rowStart;
  var rowEnd;

  for(var row = 0; row < masterRange.getNumRows() && count < NUM_SECTIONS; ++row) {
    var cell = masterRange.getCell(row + 1, 1);

    if(!cell.isPartOfMerge() && !rowEnd && rowStart == undefined) {
      rowStart = row;
    }
    else if(cell.isPartOfMerge() && rowStart && rowEnd == undefined) {
      rowEnd = row;
    }

    if(rowStart && rowEnd) {
      var sectionRange = masterSheet.getRange(rowStart + MASTER_START_ROW + 1, MASTER_START_COL + 1, rowEnd - rowStart, maxCols); 
      
      sectionList.push(sectionRange);
      
      rowStart = undefined;
      rowEnd = undefined;
      ++count;
    }
  }

  return sectionList;
}