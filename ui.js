function initUI() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Scheduling')
     .addItem('Remove LEG Sheets', 'removeLegSheetsMenuItem')
     .addItem('Create LEG Sheets', 'createLegSheetsMenuItem')
     .addToUi();
}

function removeLegSheetsMenuItem() {
  var ui = SpreadsheetApp.getUi();
  
  var result = ui.alert(
    'Please Confirm',
    'This action will permanently remove all LEG schedules and any data contained within their sheets will be lost. Are you sure you want to continue?',
    ui.ButtonSet.YES_NO);
  
  if(result == ui.Button.YES) {
    removeLegSheets();
  }
}

function createLegSheetsMenuItem() {
  createLegSheets();
}
