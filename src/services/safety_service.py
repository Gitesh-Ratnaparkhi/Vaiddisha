# src/services/safety_service.py
from src.schemas import DiagnosticOutput, SafetyCheckResult, SafetyWarning

class SafetyService:
    def check_patient_safety(self, diagnosis: DiagnosticOutput, patient_profile: dict | None = None) -> SafetyCheckResult:
        """Evaluates diagnosis against known allergies and health conditions."""
        if not patient_profile:
            return SafetyCheckResult(is_safe=True)

        allergies = (patient_profile.get("allergies") or "").lower()
        conditions = (patient_profile.get("existing_conditions") or "").lower()
        warnings = []

        # Check Allergy Conflicts
        if allergies and allergies != "none":
            for cond in diagnosis.possible_conditions:
                explanation = cond.explanation or ""
                if "penicillin" in allergies and "bacterial" in explanation.lower():
                    warnings.append(SafetyWarning(
                        category="ALLERGY_CONFLICT",
                        severity="CRITICAL",
                        message="Patient has a documented Penicillin allergy. Avoid Beta-lactam antibiotic recommendations."
                    ))

        # Check Pre-existing Condition Contraindications
        if "hypertension" in conditions:
            urgency = diagnosis.urgency_level or ""
            if "high" in urgency.lower():
                warnings.append(SafetyWarning(
                    category="CONDITION_CONTRAINDICATION",
                    severity="HIGH",
                    message="Patient has Hypertension. Ensure blood pressure monitoring during acute distress."
                ))

        return SafetyCheckResult(is_safe=len(warnings) == 0, warnings=warnings)

safety_service = SafetyService()