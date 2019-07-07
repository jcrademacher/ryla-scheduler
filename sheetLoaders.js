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
  var START_COL = 1;
  var START_ROW = 0;

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var infoSheet = ss.getSheetByName(ELEMENT_INFO_NAME);

  var rowExtend = infoSheet.getMaxRows() - START_ROW;
  var colExtend = infoSheet.getMaxColumns() - START_COL;

  var vals = infoSheet.getRange(START_ROW + 1, START_COL + 1, rowExtend, colExtend).getValues();

  var elements = [];

  for(var r = 1; r < vals.length; ++r) {
    var elementRow = vals[r];
    var elementObj = {};

    elementObj.name = vals[r][0];

    for(var c = 0; c < elementRow.length; ++c) {
      var propName = vals[0][c];
      var parsedVal = parseInt(elementRow[c]);
      var propVal = parsedVal;

      if(propVal !== propVal) {
        propVal = elementRow[c];
      }

      elementObj[propName] = propVal;
    }

    elements.push(elementObj);
  }

  return elements;
}

function loadSectionMapping() {
  var START_ROW = 1;
  var START_COL = 5;

  var retObj = [];

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var optionsSheet = ss.getSheetByName(OPTIONS_NAME);

  var vals = optionsSheet.getRange(START_ROW + 1, START_COL + 1, NUM_SECTIONS, 2).getValues();

  for(var r = 0; r < NUM_SECTIONS; ++r) {
    var name = vals[r][0];
    var val = parseInt(vals[r][1]);
    
    retObj[val] = name;
  }

  return retObj;
}

function loadElementDistances() {

}

// returns a list of ranges that represent the open times between meals that will be filled
// by the scheduler. List index represents section number
function loadSectionRanges() {
  var sectionList = [];

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var masterSheet = ss.getSheetByName(MASTER_NAME);

  var count = 0;
  var rowExtend = masterSheet.getMaxRows() - MASTER_START_ROW;
  var colExtend = masterSheet.getMaxColumns() - MASTER_START_COL;

  var masterRange = masterSheet.getRange(MASTER_START_ROW + 1, MASTER_START_COL + 1, rowExtend, colExtend);
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
      var sectionRange = masterSheet.getRange(rowStart + MASTER_START_ROW + 1, MASTER_START_COL + 1, rowEnd - rowStart, colExtend); 
      
      sectionList.push(sectionRange);
      
      rowStart = undefined;
      rowEnd = undefined;
      ++count;
    }
  }

  return sectionList;
}