import sys
from pathlib import Path

print(str(Path(__file__).absolute().parent.parent))
sys.path.append(str(Path(__file__).absolute().parent.parent.parent))

from SoluminaImport.load_solumina import load_process

def main():

    plan_name = "../../uc1/tdp8/Plan_XML/PLAN-0000096-1-1-0_Generator.xml"

    if len(sys.argv) > 1:
        plan_name = sys.argv[1]

    process = load_process(plan_name)
    print("Process:\n", process)

if __name__ == "__main__":
    main()
