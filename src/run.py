from src.orchestrator_v2 import OrchestratorV2


def main():
    orch = OrchestratorV2()
    orch.run()
    print(">>> Pipeline Finished Successfully.")
if __name__ == "__main__":
    main()


