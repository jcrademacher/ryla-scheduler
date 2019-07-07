function initUI() {
  var ui = SpreadsheetApp.getUi();
  
  createRYLAMenu(ui);
}

function createRYLAMenu(ui) {
  ui.createMenu('RYLA')
     .addItem('Remove LEG sheets', 'removeLegSheetsMenuItem')
     .addItem('Create LEG sheets', 'createLegSheetsMenuItem')
     .addSeparator()
     .addSubMenu(createSchedulingSubMenu(ui))
     .addToUi();
}

function createSchedulingSubMenu(ui) {
  return (
    ui.createMenu('Scheduling')
      .addItem('Run all','runAllMenuItem')
      .addItem('Run master scheduler','na')
      .addItem('Fill LEG schedules from master','na')
  );
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

function runAllMenuItem() {
  var ui = SpreadsheetApp.getUi();

  var result = ui.alert(
    'Please Confirm',
    'This action will attempt to solve the master schedule. Please be patient and do NOT modify the sheet or exit until you see "Finished script" in the top center of the screen. Are you sure you want to continue?',
    ui.ButtonSet.YES_NO);
  
  if(result == ui.Button.YES) {
    scheduleMaster();
  }
}
