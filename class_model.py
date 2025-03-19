class FCO:
    def __init__(self):
        self.name: str = "" 
        self.x: int = 0   # x coordinate
        self.y: int = 0   # y coordinate
        self.documentations: list["Documentation"] = []


class BPLELementBase(FCO):
    def __init__(self):
        super().__init__()
        self.BPLElementUUID: str = "" # Universally Unique Identifier of the BPL Element


class BPLElement(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.bplElementName: str = "" 
        self.bplElementId: str = "" 
        self.Description: str = "" # Describes the BPMN element
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
        self.textAnnotation: str = "" 
        self.intermediateEvents: list["IntermediateEvent"] = []
        self.nexts: dict[str, "BPLElement"] = {}
        self.prevs: list["BPLElement"] = []


class Task(Activity):
    def __init__(self):
        super().__init__()
        self.documentation: str = "" 
        self.resourceRequirements: list["ResourceRequirement"] = []


class ReceiveTask(Task):
    def __init__(self):
        super().__init__()
        self.asyncAfter: bool = False 
        self.msgRef: str = "" 
        self.msgCorrelationKey: str = "" 
        self.msgName: str = "" 


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
        self.target: str = "" 
        self.source: str = "" 


class InValue(Value):
    def __init__(self):
        super().__init__()


class ConnectionBase(BPLElement):
    def __init__(self):
        super().__init__()
        self.output: str = "" 
        self.conditionExpression: str = "" 


class Event2Activity(ConnectionBase):
    def __init__(self):
        super().__init__()


class DataOutputAssoc(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.dsTargetRef: str = "" 
        self.assocId: str = "" 


class Header(Activity):
    def __init__(self):
        super().__init__()
        self.warningsList: str = "" # An ordered list of warnings (each separated by a carriage return (i.e., '\r' character)).


class Fault(BPLElement):
    def __init__(self):
        super().__init__()
        self.severityLevel: str = "" 
        self.originLoc: str = "" # Full model path location of where this fault was identified.
        self.faultType: str = "" # Type of the identified fault
        self.faultCategory: str = "" # Category of the identified fault
        self.faultDesc: str = "" # Detailed description of the identified fault
        self.faultId: str = "" # Unique ID of the identified fault
        self.gateways: list["Gateway"] = []


class FaultCollection(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.timestamp: str = "" # Timestamp of when these faults were identified
        self.formatVersion: str = "" # Fault XML schema version
        self.faultPtrs: list["FaultPtr"] = []


class FaultPtr(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.fault: "Fault|None" = None


class FaultIndicator(FCO):
    def __init__(self):
        super().__init__()
        self.numFaultsBelow: int = 0 # Number of faults at the current location including in any of the child elements


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
        self.documentation: str = "" 


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
        self.isOperation: bool = False # TRUE if the SubProcess represents an Operation
        self.isStartableInTasklist: bool = False 
        self.historyTimeToLive: str = "" 
        self.isExecutable: bool = False 
        self.isEventSubProcess: bool = False # Specifies whether the SubProcess is an Event_SubProcess
        self.faultIndicators: list["FaultIndicator"] = []
        self.bPLElements: list["BPLElement"] = []
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
        self.IconColor: str = "" 
        self.linkEventDefinitions: list["LinkEventDefinition"] = []
        self.nexts: dict[str, "BPLElement"] = {}


class Process(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.source: str = "" # Describes where the process plan came from. It could be the filename, database table name, etc.
        self.classification: str = "" 
        self.bplProcessName: str = "" 
        self.instructionsList: str = "" # If the process is an Operation, then an ordered list of instructions can be provided (each separated by a carriage return (i.e., '\r' character)).
        self.isOperation: bool = False # TRUE if the process represents an Operation
        self.bplProcessId: str = "" 
        self.isStartableInTasklist: bool = False 
        self.isExecutable: bool = False 
        self.historyTimeToLive: str = "" 
        self.faultIndicators: list["FaultIndicator"] = []
        self.bPLElements: list["BPLElement"] = []
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
        self.bPMNFolders: list["BPMNFolder"] = []
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
        self.script: str = "" # Script to execute
        self.scriptFormat: str = "" # Format of the Script


class Parameter(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.scriptFormat: str = "" 
        self.script: str = "" 
        self.isArray: bool = False # True if value is array of values each enclosed in {} and separated by a comma
        self.paramValue: str = "" # Parameter value given as a string
        self.paramType: str = "" # Data type of the parameter
        self.paramName: str = "" # Name of the parameter
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
        self.connectorId: str = "" 
        self.taskListenerExpr: str = "" # Task listener expression (e.g., Camanuda task listener expression)
        self.values: list["Value"] = []
        self.parameters: list["Parameter"] = []


class UserTask(Task):
    def __init__(self):
        super().__init__()
        self.workLocation: str = "" 
        self.isOperationStep: bool = False # TRUE if the UserTask represents an Operation's constituent step
        self.role: str = "" # The role of the person necessary for completing this task
        self.followUpDate: str = "" 
        self.dueDate: str = "" 
        self.assignee: str = "" 
        self.formKey: str = "" 
        self.priority: int = 0 # Lower number means higher priority
        self.candidateGroups: str = "" 
        self.formRefBinding: str = "" 
        self.formRef: str = "" # Name of the form file (without the filename extension such as .json)
        self.stepInstructions: list["StepInstructions"] = []
        self.extensionElements: list["ExtensionElements"] = []
        self.nexts: dict[str, "BPLElement"] = {}


class SpecAnnotation(BPLElement):
    def __init__(self):
        super().__init__()
        self.bpmnKeywords: str = "" # Keywords from the BPMN model/forms used to make the association (each enclosed in {} and separated by a comma)
        self.docKeywords: str = "" # Keywords from document used to make the association (each enclosed in {} and separated by a comma)
        self.pConstraint: str = "" # Equivalent specification/constraint in the P language
        self.formulaConstraint: str = "" # Equivalent specification/constraint in the FORMULA language
        self.specDesc: str = "" # Textual description of the specification as found in the document
        self.specLocator: str = "" # Section number or ID of the specification within the specified document
        self.docLocator: str = "" # ID or Filename of the document containing the specification
        self.nexts: dict[str, "BPLElement"] = {}


class SpecConn(ConnectionBase):
    def __init__(self):
        super().__init__()


class KeyValue(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.value: str = "" # Value of the key-value entry
        self.key: str = "" # Key of the key-value entry


class ServiceTask(Task):
    def __init__(self):
        super().__init__()
        self.dataOutputAssocs: list["DataOutputAssoc"] = []
        self.propertys: list["Property"] = []
        self.extensionElements: list["ExtensionElements"] = []


class SendTask(Task):
    def __init__(self):
        super().__init__()
        self.expression: str = "" 


class Property(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.propertyName: str = "" 
        self.propertyId: str = "" 


class BusinessRuleTask(Task):
    def __init__(self):
        super().__init__()
        self.mapDecisionResult: str = "" 
        self.decisionRef: str = "" 
        self.resultVariable: str = "" 
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
        self.href: str = "" 


class DecisionTable(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.hitPolicy: str = "" 
        self.decisionRules: list["DecisionRule"] = []
        self.decisionOutputs: list["DecisionOutput"] = []


class DecisionOutput(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.typeRef: str = "" 
        self.label: str = "" 


class DecisionRule(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.decisionOutputEntrys: list["DecisionOutputEntry"] = []


class DecisionOutputEntry(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.text: str = "" 


class DataStoreReference(BPLElement):
    def __init__(self):
        super().__init__()


class MultiInstanceLoopCharacteristics(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.collection: str = "" 


class IntermediateCatchEvent(IntermediateEvent):
    def __init__(self):
        super().__init__()


class IntermediateThrowEvent(IntermediateEvent):
    def __init__(self):
        super().__init__()


class BoundaryEvent(Event):
    def __init__(self):
        super().__init__()
        self.timeDuration: str = "" 


class ResourceRequirement(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.resourceBases: list["ResourceBase"] = []


class ResourceBase(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.quantity: int = 0 
        self.resName: str = "" # Name of the consumable resource
        self.resDesc: str = "" # Detailed description of the consumable resource


class ConsumableResource(ResourceBase):
    def __init__(self):
        super().__init__()
        self.unitType: str = "" 
        self.keyValues: list["KeyValue"] = []


class NonConsumableResource(ResourceBase):
    def __init__(self):
        super().__init__()
        self.skills: str = "" # List of skills possessed by the resource (each enclosed in {} and separated by a comma)
        self.expertiseLevel: str = "" 


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
        self.decisionId: str = "" 
        self.decisionTables: list["DecisionTable"] = []
        self.informationRequirements: list["InformationRequirement"] = []


class Form(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.formType: str = "" 
        self.formId: str = "" 
        self.formFields: list["FormField"] = []


class FormField(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.formKey: str = "" 
        self.text: str = "" 
        self.conditional: str = "" 
        self.defaultValue: str = "" 
        self.fieldType: str = "" 
        self.fieldLabel: str = "" 
        self.fieldId: str = "" 
        self.validationConstraints: list["ValidationConstraint"] = []


class ValidationConstraint(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.customValidator: str = "" 
        self.readOnly: bool = False 
        self.maxValue: int = 0 
        self.minValue: int = 0 
        self.maxLength: int = 0 
        self.minLength: int = 0 
        self.required: bool = False 


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
        self.bplElementName: str = "" 
        self.bplElementId: str = "" 


class OutValue(Value):
    def __init__(self):
        super().__init__()


class BuyoffTask(UserTask):
    def __init__(self):
        super().__init__()
        self.cert: str = "" # The certificate necessary for completing this buyoff task


class DataCollectionTask(UserTask):
    def __init__(self):
        super().__init__()
        self.target_value: str = "" 
        self.lower_limit: str = "" 
        self.upper_limit: str = "" 


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
        self.entryNumber: int = 0 # Ordered number of the data entry
        self.keyValues: list["KeyValue"] = []


class DataCollection(SubProcess):
    def __init__(self):
        super().__init__()


class StepInstructions(BPLELementBase):
    def __init__(self):
        super().__init__()
        self.objectID: str = "" 
        self.value: str = "" 
        self.type: str = "" 


class Event2Event(ConnectionBase):
    def __init__(self):
        super().__init__()


class LocalVariable(Parameter):
    def __init__(self):
        super().__init__()


