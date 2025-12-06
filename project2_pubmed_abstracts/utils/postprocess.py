import re, pandas as pd

def extract_drug_terms(text):
    possible = re.findall(r'\b[A-Z][a-zA-Z\-]{2,}\b', text)
    stop = {"Diabetes","Mellitus","Type","Insulin","Study","Treatment",
            "Patients","Disease","Metabolic","Therapy","Blood","Sugar"}
    return [p for p in possible if p not in stop]

def filter_and_categorize(df):
    df["extracted_drugs"] = df["output"].apply(extract_drug_terms)
    unique_drugs = sorted({d for lst in df["extracted_drugs"] for d in lst})
    df_drugs = pd.DataFrame(unique_drugs, columns=["raw_term"])

    non_drug_patterns = [
        r'EGFR',r'MAPK',r'JAK',r'ROS',r'RNA',r'DNA',r'Pathway',r'Receptor',
        r'Inflammation',r'Apoptosis',r'Oxidative',r'Reduction',r'Suppression',
        r'Induction',r'Expression',r'Protein',r'Enzyme',r'Factor'
    ]
    mask = df_drugs["raw_term"].apply(lambda x: not any(re.search(p, x, re.I) for p in non_drug_patterns))
    df_drugs = df_drugs[mask]

    drug_suffixes = ("formin","gliflozin","gliptin","glitazone","statin","pril","sartan","olol","coxib","fibrate","tide","mine","fen","azole","afil")
    known_drug_keywords = [
        "metformin","pioglitazone","rosiglitazone","phenformin",
        "sitagliptin","vildagliptin","linagliptin",
        "canagliflozin","dapagliflozin","empagliflozin",
        "liraglutide","semaglutide","exenatide","acarbose",
        "repaglinide","nateglinide","curcumin","resveratrol",
        "berberine","quercetin","tocopherol","umbelliferone",
        "atorvastatin","simvastatin","rosuvastatin","fenofibrate"
    ]
    def looks_like_drug(name):
        n = name.lower()
        return any(n.endswith(suf) for suf in drug_suffixes) or any(k in n for k in known_drug_keywords)

    df_drugs = df_drugs[df_drugs["raw_term"].apply(looks_like_drug)]
    df_drugs["raw_term"] = df_drugs["raw_term"].str.strip().str.replace(r'[^A-Za-z0-9-]', '', regex=True)
    df_drugs = df_drugs.drop_duplicates().reset_index(drop=True)

    def categorize(drug):
        dl = drug.lower()
        if any(k in dl for k in ["formin","glitazone","gliptin","gliflozin"]):
            return "Antidiabetic / Glucose-lowering"
        if any(k in dl for k in ["statin","fibrate","sartan","pril"]):
            return "Cardiometabolic comorbidity"
        if any(k in dl for k in ["curcumin","resveratrol","berberine","quercetin","tocopherol","umbelliferone"]):
            return "Natural compound / Antioxidant"
        if any(k in dl for k in ["coxib","ibuprofen","aspirin","celecoxib"]):
            return "Anti-inflammatory adjunct"
        return "Other / Investigational"

    df_drugs["category"] = df_drugs["raw_term"].apply(categorize)
    return df_drugs