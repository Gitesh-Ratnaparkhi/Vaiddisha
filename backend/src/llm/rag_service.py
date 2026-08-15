# src/llm/rag_service.py

class RAGService:
    def __init__(self):
        # A dictionary mapping keywords/conditions to clinical guidelines
        self.guidelines_db = {
            "chest pain": [
                "CLINICAL GUIDELINE: Chest pain must be evaluated immediately for acute coronary syndrome (ACS).",
                "CLINICAL GUIDELINE: Obtain an immediate 12-lead ECG and monitor vital signs.",
                "CLINICAL GUIDELINE: Consider administering aspirin 162-325 mg (chewed) unless contraindicated by allergy or active bleeding."
            ],
            "heart": [
                "CLINICAL GUIDELINE: Assess for cardiovascular risk factors, cardiac enzymes (Troponin), and history of coronary artery disease."
            ],
            "breath": [
                "CLINICAL GUIDELINE: Monitor oxygen saturation (SpO2) and respiratory rate immediately.",
                "CLINICAL GUIDELINE: Administer supplemental oxygen if SpO2 drops below 94% (or 88-92% in COPD patients)."
            ],
            "dyspnea": [
                "CLINICAL GUIDELINE: Assess for potential pulmonary embolism, heart failure exacerbation, or severe asthma/COPD."
            ],
            "cough": [
                "CLINICAL GUIDELINE: Evaluate cough duration and associated symptoms (fever, dyspnea, hemoptysis).",
                "CLINICAL GUIDELINE: Consider chest X-ray if pneumonia, tuberculosis, or malignancy is suspected."
            ],
            "fever": [
                "CLINICAL GUIDELINE: Track temperature trend. Screen for signs of systemic infection or sepsis (qSOFA score).",
                "CLINICAL GUIDELINE: Ensure adequate oral hydration and consider antipyretics (e.g., paracetamol) for symptomatic relief."
            ],
            "headache": [
                "CLINICAL GUIDELINE: Assess for red flags: sudden onset ('thunderclap'), fever, neck stiffness, or focal neurological deficits.",
                "CLINICAL GUIDELINE: For migraine, advise rest in a quiet, dark room, hydration, and appropriate abortive therapy (NSAIDs, triptans)."
            ],
            "diabetes": [
                "CLINICAL GUIDELINE: Perform capillary blood glucose and HbA1c testing.",
                "CLINICAL GUIDELINE: Check for urine/blood ketones if blood glucose is consistently above 250 mg/dL or if patient is vomiting."
            ],
            "sugar": [
                "CLINICAL GUIDELINE: Screen for diabetic ketoacidosis (DKA) or hyperosmolar hyperglycemic state (HHS) in patients with severe hyperglycemia."
            ],
            "hypertension": [
                "CLINICAL GUIDELINE: Confirm blood pressure readings with multiple measurements. Screen for target organ damage.",
                "CLINICAL GUIDELINE: Recommend lifestyle modifications (low sodium, exercise) and evaluate need for antihypertensive pharmacotherapy."
            ],
            "blood pressure": [
                "CLINICAL GUIDELINE: Check for hypertensive crisis (systolic > 180 mmHg or diastolic > 120 mmHg) accompanied by acute organ damage symptoms."
            ],
            "abdominal pain": [
                "CLINICAL GUIDELINE: Perform abdominal examination mapping to quadrants. Check for guarding, rigidity, and rebound tenderness.",
                "CLINICAL GUIDELINE: Maintain Nil Per Os (NPO) status if surgical conditions like appendicitis, cholecystitis, or bowel obstruction are suspected."
            ],
            "stomach": [
                "CLINICAL GUIDELINE: Screen for gastrointestinal bleeding (melena, hematemesis) or peptic ulcer disease."
            ],
            "allergy": [
                "CLINICAL GUIDELINE: Assess for signs of anaphylaxis: respiratory distress, wheezing, hypotension, or angioedema.",
                "CLINICAL GUIDELINE: Administer intramuscular epinephrine immediately if anaphylaxis is diagnosed or highly suspected."
            ],
            "asthma": [
                "CLINICAL GUIDELINE: Assess peak expiratory flow (PEF). Administer inhaled short-acting beta-agonists (SABA) via MDI or nebulizer.",
                "CLINICAL GUIDELINE: Consider early administration of systemic corticosteroids for moderate-to-severe exacerbations."
            ],
            "stroke": [
                "CLINICAL GUIDELINE: Perform FAST (Face, Arm, Speech, Time) assessment immediately.",
                "CLINICAL GUIDELINE: Establish time of symptom onset and activate stroke protocol for potential thrombolysis/thrombectomy within therapeutic window."
            ],
            "paralysis": [
                "CLINICAL GUIDELINE: Rule out acute ischemic stroke, spinal cord compression, or peripheral neuropathy (e.g., Guillain-Barré syndrome)."
            ]
        }

    def retrieve_guidelines(self, query: str) -> list[str]:
        """
        Retrieves matching clinical guidelines based on keywords found in the symptoms query.
        Returns a list of guideline strings.
        """
        if not query:
            return []

        query_lower = query.lower()
        matched_guidelines = []
        
        # Simple keyword matching algorithm for RAG
        for key, guidelines in self.guidelines_db.items():
            if key in query_lower:
                matched_guidelines.extend(guidelines)
                
        # Return unique guidelines, preserving ordering
        seen = set()
        unique_guidelines = []
        for g in matched_guidelines:
            if g not in seen:
                seen.add(g)
                unique_guidelines.append(g)
                
        return unique_guidelines

# Singleton instance
rag_service = RAGService()
