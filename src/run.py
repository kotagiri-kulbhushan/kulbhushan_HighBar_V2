from src.orchestrator import Orchestrator

def main():
    print("Running Kasparro Agentic System...")

    orch = Orchestrator(data_path="data/synthetic_fb_ads_undergarments.csv")
    orch.run()

if __name__ == "__main__":
    main()

