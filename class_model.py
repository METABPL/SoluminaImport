class FCO:
    def __init__(self):
        self.names: str = "" 
        self.x: int = 0   # x coordinate
        self.y: int = 0   # y coordinate
        self.documentations: list["Documentation"] = []


class BPLELementBase(FCO):
    def __init__(self):
        super().__init__()
        self.bplElementUUIDs: str = "" # Universally Unique Identifier of the BPL Element


class BPLElement(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.bplElementNames: str = "" 
        self.bplElementIds: str = "" 
        self.descriptions: str = "" # Describes the BPMN element
        self.prevs: list["BPLElement"] = []


class InputData(BPLElement):
    def __init__(self):
        super().__init__()


class Message(BPLElement):
    def __init__(self):
        super().__init__()


class Activity(BPLElement):
    def __init__(self):
        super().__init__()
        self.textAnnotations: str = "" 
        self.intermediateEvents: list["IntermediateEvent"] = []
        self.nexts: dict[str, "BPLElement"] = {}
        self.prevs: list["BPLElement"] = []


class Task(Activity):
    def __init__(self):
        super().__init__()
        self.documentations: str = "" 
        self.resourceRequirements: list["ResourceRequirement"] = []


class ReceiveTask(Task):
    def __init__(self):
        super().__init__()
        self.asyncAfters: bool = False 
        self.msgRefs: str = "" 
        self.msgCorrelationKeys: str = "" 
        self.msgNames: str = "" 


class Event(BPLElement):
    def __init__(self):
        super().__init__()
        self.nexts: dict[str, "BPLElement"] = {}
        self.prevs: list["BPLElement"] = []


class ErrorEvent(Event):
    def __init__(self):
        super().__init__()


class Value(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.targets: str = "" 
        self.sources: str = "" 


class InValue(Value):
    def __init__(self):
        super().__init__()


class ConnectionBase(BPLElement):
    def __init__(self):
        super().__init__()
        self.outputs: str = "" 
        self.conditionExpressions: str = "" 


class Event2Activity(ConnectionBase):
    def __init__(self):
        super().__init__()


class DataOutputAssoc(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.dsTargetRefs: str = "" 
        self.assocIds: str = "" 


class Header(Activity):
    def __init__(self):
        super().__init__()
        self.warningsLists: str = "" # An ordered list of warnings (each separated by a carriage return (i.e., '\r' character)).


class Fault(BPLElement):
    def __init__(self):
        super().__init__()
        self.severityLevels: str = "" 
        self.originLocs: str = "" # Full model path location of where this fault was identified.
        self.faultTypes: str = "" # Type of the identified fault
        self.faultCategorys: str = "" # Category of the identified fault
        self.faultDescs: str = "" # Detailed description of the identified fault
        self.faultIds: str = "" # Unique ID of the identified fault
        self.gateways: list["Gateway"] = []


class FaultCollection(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.timestamps: str = "" # Timestamp of when these faults were identified
        self.formatVersions: str = "" # Fault XML schema version
        self.faultPtrs: list["FaultPtr"] = []


class FaultPtr(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.fault: "Fault|None" = None


class FaultIndicator(FCO):
    def __init__(self):
        super().__init__()
        self.numFaultsBelows: int = 0 # Number of faults at the current location including in any of the child elements


class Fault2BPLElement(BPLElement):
    def __init__(self):
        super().__init__()


class Gateway(BPLElement):
    def __init__(self):
        super().__init__()
        self.faults: list["Fault"] = []
        self.nexts: dict[str, "BPLElement"] = {}
        self.prevs: list["BPLElement"] = []


class Sequential(Gateway):
    def __init__(self):
        super().__init__()


class Parallel(Sequential):
    def __init__(self):
        super().__init__()


class Documentation(FCO):
    def __init__(self):
        super().__init__()
        self.documentations: str = "" 


class CallActivity(Activity):
    def __init__(self):
        super().__init__()
        self.extensionElements: list["ExtensionElements"] = []
        self.process: "Process|None" = None


class Inclusive(Sequential):
    def __init__(self):
        super().__init__()


class SubProcess(Activity):
    def __init__(self):
        super().__init__()
        self.isOperations: bool = False # TRUE if the SubProcess represents an Operation
        self.isStartableInTasklists: bool = False 
        self.historyTimeToLives: str = "" 
        self.isExecutables: bool = False 
        self.isEventSubProcess: bool = False # Specifies whether the SubProcess is an Event_SubProcess
        self.faultIndicators: list["FaultIndicator"] = []
        self.bplElements: list["BPLElement"] = []
        self.specAnnotations: list["SpecAnnotation"] = []
        self.multiInstanceLoopCharacteristics: list["MultiInstanceLoopCharacteristics"] = []
        self.stepInstructions: list["StepInstructions"] = []
        self.parameters: list["Parameter"] = []
        self.resourceRequirements: list["ResourceRequirement"] = []


class Transaction(SubProcess):
    def __init__(self):
        super().__init__()


class Conditional(Gateway):
    def __init__(self):
        super().__init__()


class EventBased(Conditional):
    def __init__(self):
        super().__init__()


class StartEvent(Event):
    def __init__(self):
        super().__init__()


class IntermediateEvent(Event):
    def __init__(self):
        super().__init__()
        self.iconColors: str = "" 
        self.linkEventDefinitions: list["LinkEventDefinition"] = []
        self.nexts: dict[str, "BPLElement"] = {}


class Process(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.sources: str = "" # Describes where the process plan came from. It could be the filename, database table name, etc.
        self.classifications: str = "" 
        self.bplProcessNames: str = "" 
        self.instructionsLists: str = "" # If the process is an Operation, then an ordered list of instructions can be provided (each separated by a carriage return (i.e., '\r' character)).
        self.isOperations: bool = False # TRUE if the process represents an Operation
        self.bplProcessIds: str = "" 
        self.isStartableInTasklists: bool = False 
        self.isExecutables: bool = False 
        self.historyTimeToLives: str = "" 
        self.faultIndicators: list["FaultIndicator"] = []
        self.bplElements: list["BPLElement"] = []
        self.specAnnotations: list["SpecAnnotation"] = []
        self.formRefs: list["FormRef"] = []
        self.decisionRefs: list["DecisionRef"] = []
        self.headers: list["Header"] = []
        self.footers: list["Footer"] = []
        self.dataCollectionHistorys: list["DataCollectionHistory"] = []
        self.parameters: list["Parameter"] = []
        self.resourceRequirements: list["ResourceRequirement"] = []


class Complex(Sequential):
    def __init__(self):
        super().__init__()


class Artifact(BPLElement):
    def __init__(self):
        super().__init__()
        self.nexts: dict[str, "BPLElement"] = {}


class Annotation(Artifact):
    def __init__(self):
        super().__init__()
        self.nexts: dict[str, "BPLElement"] = {}


class BPMNFolder(FCO):
    def __init__(self):
        super().__init__()
        self.process: list["Process"] = []
        self.bpmnFolders: list["BPMNFolder"] = []
        self.faultIndicators: list["FaultIndicator"] = []
        self.decisions: list["Decision"] = []
        self.forms: list["Form"] = []
        self.faultCollections: list["FaultCollection"] = []


class Lane(BPLELementBase):
    def __init__(self):
        super().__init__()


class Group(Artifact):
    def __init__(self):
        super().__init__()


class DataObject(Artifact):
    def __init__(self):
        super().__init__()


class Intermediate2Gateway(ConnectionBase):
    def __init__(self):
        super().__init__()


class Exclusive(Sequential):
    def __init__(self):
        super().__init__()


class EndEvent(Event):
    def __init__(self):
        super().__init__()


class Gateway2Event(ConnectionBase):
    def __init__(self):
        super().__init__()


class ParallelEventBased(Sequential):
    def __init__(self):
        super().__init__()


class Pool(BPLElement):
    def __init__(self):
        super().__init__()
        self.lanes: list["Lane"] = []


class ExclusiveEventBased(Conditional):
    def __init__(self):
        super().__init__()


class Artifact2Activity(ConnectionBase):
    def __init__(self):
        super().__init__()


class TryConn(FCO):
    def __init__(self):
        super().__init__()


class TestF(FCO):
    def __init__(self):
        super().__init__()


class ScriptTask(Task):
    def __init__(self):
        super().__init__()
        self.scripts: str = "" # Script to execute
        self.scriptFormats: str = "" # Format of the Script


class Parameter(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.scriptFormats: str = "" 
        self.scripts: str = "" 
        self.isArrays: bool = False # True if value is array of values each enclosed in {} and separated by a comma
        self.paramValues: str = "" # Parameter value given as a string
        self.paramTypes: str = "" # Data type of the parameter
        self.paramNames: str = "" # Name of the parameter
        self.keyValues: list["KeyValue"] = []


class InputParameter(Parameter):
    def __init__(self):
        super().__init__()


class OutputParameter(Parameter):
    def __init__(self):
        super().__init__()


class ExtensionElements(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.connectorIds: str = "" 
        self.taskListenerExprs: str = "" # Task listener expression (e.g., Camanuda task listener expression)
        self.values: list["Value"] = []
        self.parameters: list["Parameter"] = []


class UserTask(Task):
    def __init__(self):
        super().__init__()
        self.workLocations: str = "" 
        self.isOperationSteps: bool = False # TRUE if the UserTask represents an Operation's constituent step
        self.roles: str = "" # The role of the person necessary for completing this task
        self.followUpDates: str = "" 
        self.dueDates: str = "" 
        self.assignees: str = "" 
        self.formKeys: str = "" 
        self.prioritys: int = 0 # Lower number means higher priority
        self.candidateGroups: str = "" 
        self.formRefBindings: str = "" 
        self.formRefs: str = "" # Name of the form file (without the filename extension such as .json)
        self.stepInstructions: list["StepInstructions"] = []
        self.extensionElements: list["ExtensionElements"] = []
        self.nexts: dict[str, "BPLElement"] = {}


class SpecAnnotation(BPLElement):
    def __init__(self):
        super().__init__()
        self.bpmnKeywords: str = "" # Keywords from the BPMN model/forms used to make the association (each enclosed in {} and separated by a comma)
        self.docKeywords: str = "" # Keywords from document used to make the association (each enclosed in {} and separated by a comma)
        self.pConstraints: str = "" # Equivalent specification/constraint in the P language
        self.formulaConstraints: str = "" # Equivalent specification/constraint in the FORMULA language
        self.specDescs: str = "" # Textual description of the specification as found in the document
        self.specLocators: str = "" # Section number or ID of the specification within the specified document
        self.docLocators: str = "" # ID or Filename of the document containing the specification
        self.nexts: dict[str, "BPLElement"] = {}


class SpecConn(ConnectionBase):
    def __init__(self):
        super().__init__()


class KeyValue(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.values: str = "" # Value of the key-value entry
        self.keys: str = "" # Key of the key-value entry


class ServiceTask(Task):
    def __init__(self):
        super().__init__()
        self.dataOutputAssocs: list["DataOutputAssoc"] = []
        self.propertys: list["Property"] = []
        self.extensionElements: list["ExtensionElements"] = []


class SendTask(Task):
    def __init__(self):
        super().__init__()
        self.expressions: str = "" 


class Property(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.propertyNames: str = "" 
        self.propertyIds: str = "" 


class BusinessRuleTask(Task):
    def __init__(self):
        super().__init__()
        self.mapDecisionResults: str = "" 
        self.decisionRefs: str = "" 
        self.resultVariables: str = "" 
        self.extensionElements: list["ExtensionElements"] = []
        self.nexts: dict[str, "BPLElement"] = {}


class AnnotationConn(ConnectionBase):
    def __init__(self):
        super().__init__()


class InformationRequirement(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.requiredInputs: list["RequiredInput"] = []


class RequiredInput(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.hrefs: str = "" 


class DecisionTable(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.hitPolicys: str = "" 
        self.decisionRules: list["DecisionRule"] = []
        self.decisionOutputs: list["DecisionOutput"] = []


class DecisionOutput(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.typeRefs: str = "" 
        self.labels: str = "" 


class DecisionRule(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.decisionOutputEntrys: list["DecisionOutputEntry"] = []


class DecisionOutputEntry(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.texts: str = "" 


class DataStoreReference(BPLElement):
    def __init__(self):
        super().__init__()


class MultiInstanceLoopCharacteristics(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.collections: str = "" 


class IntermediateCatchEvent(IntermediateEvent):
    def __init__(self):
        super().__init__()


class IntermediateThrowEvent(IntermediateEvent):
    def __init__(self):
        super().__init__()


class BoundaryEvent(Event):
    def __init__(self):
        super().__init__()
        self.timeDurations: str = "" 


class ResourceRequirement(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.resourceBases: list["ResourceBase"] = []


class ResourceBase(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.quantitys: int = 0 
        self.resNames: str = "" # Name of the consumable resource
        self.resDescs: str = "" # Detailed description of the consumable resource


class ConsumableResource(ResourceBase):
    def __init__(self):
        super().__init__()
        self.unitTypes: str = "" 
        self.keyValues: list["KeyValue"] = []


class NonConsumableResource(ResourceBase):
    def __init__(self):
        super().__init__()
        self.skills: str = "" # List of skills possessed by the resource (each enclosed in {} and separated by a comma)
        self.expertiseLevels: str = "" 


class ToolResource(NonConsumableResource):
    def __init__(self):
        super().__init__()


class HumanResource(NonConsumableResource):
    def __init__(self):
        super().__init__()
        self.certs: str = "" # Certificates that this human resource has and can be used to complete associated buyoff tasks (each enclosed in {} and separated by a comma)
        self.roles: str = "" # Roles that this human resource is capable of performing (each enclosed in {} and separated by a comma)


class Decision(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.decisionIds: str = "" 
        self.decisionTables: list["DecisionTable"] = []
        self.informationRequirements: list["InformationRequirement"] = []


class Form(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.formTypes: str = "" 
        self.formIds: str = "" 
        self.formFields: list["FormField"] = []


class FormField(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.formKeys: str = "" 
        self.texts: str = "" 
        self.conditionals: str = "" 
        self.defaultValues: str = "" 
        self.fieldTypes: str = "" 
        self.fieldLabels: str = "" 
        self.fieldIds: str = "" 
        self.validationConstraints: list["ValidationConstraint"] = []


class ValidationConstraint(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.customValidators: str = "" 
        self.readOnlys: bool = False 
        self.maxValues: int = 0 
        self.minValues: int = 0 
        self.maxLengths: int = 0 
        self.minLengths: int = 0 
        self.requireds: bool = False 


class Activity2Activity(ConnectionBase):
    def __init__(self):
        super().__init__()


class Activity2Gateway(ConnectionBase):
    def __init__(self):
        super().__init__()


class Gateway2Activity(ConnectionBase):
    def __init__(self):
        super().__init__()


class Event2Gateway(ConnectionBase):
    def __init__(self):
        super().__init__()


class Activity2Event(ConnectionBase):
    def __init__(self):
        super().__init__()


class Gateway2Gateway(ConnectionBase):
    def __init__(self):
        super().__init__()


class FormConn(ConnectionBase):
    def __init__(self):
        super().__init__()


class FormRef(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.form: "Form|None" = None
        self.prevs: list["BPLElement"] = []


class DecisionRef(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.decision: "Decision|None" = None
        self.prevs: list["BPLElement"] = []


class DecisionConn(ConnectionBase):
    def __init__(self):
        super().__init__()


class LinkEventDefinition(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.bplElementNames: str = "" 
        self.bplElementIds: str = "" 


class OutValue(Value):
    def __init__(self):
        super().__init__()


class BuyoffTask(UserTask):
    def __init__(self):
        super().__init__()
        self.certs: str = "" # The certificate necessary for completing this buyoff task


class DataCollectionTask(UserTask):
    def __init__(self):
        super().__init__()
        self.target_values: str = "" 
        self.lower_limits: str = "" 
        self.upper_limits: str = "" 


class InspectionTask(UserTask):
    def __init__(self):
        super().__init__()


class Footer(SubProcess):
    def __init__(self):
        super().__init__()
        self.inspectionTasks: list["InspectionTask"] = []


class DataCollectionHistory(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.dataEntrys: list["DataEntry"] = []


class DataEntry(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.entryNumbers: int = 0 # Ordered number of the data entry
        self.keyValues: list["KeyValue"] = []


class DataCollection(SubProcess):
    def __init__(self):
        super().__init__()


class StepInstructions(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.objectIDs: str = "" 
        self.values: str = "" 
        self.types: str = "" 


class Event2Event(ConnectionBase):
    def __init__(self):
        super().__init__()


class LocalVariable(Parameter):
    def __init__(self):
        super().__init__()


