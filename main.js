function main() {
  initUI();
  
  var ranges = loadSectionRanges();

  ranges[5].activate();

//  var date = sheetObject.master.getRange(18,1).getValue();
//  date.setHours(date.getHours()+3);
//  
//  Logger.log(date.toLocaleTimeString('en-US'));
  // testing clasp and git
}

function onOpen() {
  main();
}
