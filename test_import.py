import sys
from load_solumina import load_process

def main():

    plan_name = "../SoluminaIngest/PLAN-0000096-1-1-0_Generator.xml"

    if len(sys.argv) > 1:
        plan_name = sys.argv[1]

    process = load_process(plan_name)
    print("Process:\n", process)

if __name__ == "__main__":
    main()
