import argparse

def parse_test(test):
    X_pretrain = None
    threshold_approach = None
    ablation = None
    match test:
        case "A1":
            X_pretrain = "01-normal.xslx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "A2":
            X_pretrain = "02-normal.xslx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "A3":
            X_pretrain = "03-normal.xslx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "B3":
            X_pretrain = "UnderFrequency.xlsx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
    return X_pretrain, threshold_approach, ablation

def main(args):
    print(f"Running Test: {args.test}")
    X_pretrain, threshold_approach, ablation = parse_test(args.test)
    
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run XSTL transfer learning experiment")
    parser.add_argument('--test', type=str, required=True, help='Insert test number (see table 3 in paper).', choices=[
        "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6"])

    args = parser.parse_args()
    main(args)
