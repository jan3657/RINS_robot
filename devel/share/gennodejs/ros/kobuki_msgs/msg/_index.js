
"use strict";

let Led = require('./Led.js');
let ScanAngle = require('./ScanAngle.js');
let ControllerInfo = require('./ControllerInfo.js');
let DigitalOutput = require('./DigitalOutput.js');
let CliffEvent = require('./CliffEvent.js');
let VersionInfo = require('./VersionInfo.js');
let DockInfraRed = require('./DockInfraRed.js');
let MotorPower = require('./MotorPower.js');
let PowerSystemEvent = require('./PowerSystemEvent.js');
let BumperEvent = require('./BumperEvent.js');
let SensorState = require('./SensorState.js');
let DigitalInputEvent = require('./DigitalInputEvent.js');
let RobotStateEvent = require('./RobotStateEvent.js');
let Sound = require('./Sound.js');
let WheelDropEvent = require('./WheelDropEvent.js');
let ExternalPower = require('./ExternalPower.js');
let ButtonEvent = require('./ButtonEvent.js');
let KeyboardInput = require('./KeyboardInput.js');
let AutoDockingActionGoal = require('./AutoDockingActionGoal.js');
let AutoDockingGoal = require('./AutoDockingGoal.js');
let AutoDockingFeedback = require('./AutoDockingFeedback.js');
let AutoDockingAction = require('./AutoDockingAction.js');
let AutoDockingActionResult = require('./AutoDockingActionResult.js');
let AutoDockingResult = require('./AutoDockingResult.js');
let AutoDockingActionFeedback = require('./AutoDockingActionFeedback.js');

module.exports = {
  Led: Led,
  ScanAngle: ScanAngle,
  ControllerInfo: ControllerInfo,
  DigitalOutput: DigitalOutput,
  CliffEvent: CliffEvent,
  VersionInfo: VersionInfo,
  DockInfraRed: DockInfraRed,
  MotorPower: MotorPower,
  PowerSystemEvent: PowerSystemEvent,
  BumperEvent: BumperEvent,
  SensorState: SensorState,
  DigitalInputEvent: DigitalInputEvent,
  RobotStateEvent: RobotStateEvent,
  Sound: Sound,
  WheelDropEvent: WheelDropEvent,
  ExternalPower: ExternalPower,
  ButtonEvent: ButtonEvent,
  KeyboardInput: KeyboardInput,
  AutoDockingActionGoal: AutoDockingActionGoal,
  AutoDockingGoal: AutoDockingGoal,
  AutoDockingFeedback: AutoDockingFeedback,
  AutoDockingAction: AutoDockingAction,
  AutoDockingActionResult: AutoDockingActionResult,
  AutoDockingResult: AutoDockingResult,
  AutoDockingActionFeedback: AutoDockingActionFeedback,
};
