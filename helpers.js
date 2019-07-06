// skips row 1, looks at cell, if it is not empty, looks at each subsequent cell below until it finds
// another cell that is not empty. Vertically merges # rows it traversed
// In other words, extends each cell if not empty and vertically merges through empty cells below testing 123
function smoothCells(sheet) {
  var dataRange = sheet.getDataRange();
  var data = dataRange.getValues();
  
  for(var col = 0; col < dataRange.getNumColumns(); ++col) {
    for(var row = 1; row < dataRange.getNumRows() - 1; ++row) {
      //Logger.log(row + ", " + col);
      var cell = data[row][col];
      
      if(cell == "") { // meaning cell is empty
        continue;
      }
      else {
        var count = 0;
        
        try {
          do {
            count++;
            var cellBelow = data[row + count][col];
          } while(cellBelow == "");
        }
        catch(err) {
          Logger.log(err);
        }
        
        sheet.getRange(row + 1, col + 1, count).mergeVertically(); // google sheets uses 1 as the starting index for rows/columns :| pain in the ass
      }
    }
  }
}

function removeLegSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  
  for(var i = 1; i <= NUM_LEGS; ++i) {
    var sheet = ss.getSheetByName(LEG_SHEET_NAME(i));
    
    if(sheet != null) {
      ss.deleteSheet(sheet);
    }
  }
}

function createLegSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var templateLeg = ss.getSheetByName(TEMPLATE_NAME);
  
  for(var i = 1; i <= NUM_LEGS; ++i) {
    var name = LEG_SHEET_NAME(i);
    var legSheet;
    
    try {
      legSheet = ss.insertSheet(name, {template: templateLeg});
    }
    catch(err) {
      Logger.log(err);
      legSheet = ss.getSheetByName(name);
    }
  }
}

function loadConstants() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  var rows = 10;
  var cols = 2;

  var optionsSheet = ss.getSheetByName(OPTIONS_NAME);
  var optionsRange = optionsSheet.getRange(OPTIONS_START_ROW, OPTIONS_START_COL, rows, cols);
  var optionsValues = optionsRange.getValues();

  for(var r = 0; r < rows; ++r) {
    var optionId = optionsValues[r][0];
    var optionVal = optionsValues[r][1];

    if(optionId != '') {
      OPTIONS[optionsValues[r][0]] = parseInt(optionsValues[r][1]);
    }
  }
}