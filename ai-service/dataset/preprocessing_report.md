# Dataset Preprocessing Report

This report documents the state and statistics of the processed dataset located in `ai-service/dataset/processed/internships_filtered.csv`.

## 1. Validation Constraints
The dataset was run through the `validate_dataset.py` utility to ensure database schema compatibility.

**Result:** `[Validation] PASSED: All constraints met.`
- ✅ No nulls in required fields (`title`, `company_name`, `description`, `skills`).
- ✅ All string fields conform to the MySQL `VARCHAR(255)` length limits.
- ✅ HTML markup is fully scrubbed from job summaries.

## 2. Job Category Distribution
The automated pipeline categorized the existing filtered roles into the following technical disciplines. A total of **962** software-related internship/entry-level roles are available.

| Category | Count |
| :--- | :--- |
| **Software Engineer** (General) | 491 |
| **Data Science/Analyst** | 308 |
| **AI/ML** | 121 |
| **DevOps/Cloud** | 24 |
| **UI/UX** | 8 |
| **Cybersecurity** | 5 |
| **QA/Testing** | 3 |
| **Frontend** | 1 |
| **Mobile** | 1 |
| **Backend** | 0 |
| **Full Stack** | 0 |

> [!NOTE]
> The current distribution skews heavily toward general software engineering, data science, and AI/ML roles. There is currently a gap in specialized Frontend, Backend, and Full Stack roles in the raw source data. 

## 3. Top 10 Companies by Role Count
Below is the distribution of the top hiring entities present in the filtered dataset:

1. **DeRisk Technologies**: 40
2. **VolunteerMatch**: 37
3. **Kforce Inc**: 26
4. **CrowdDoing**: 24
5. **JLL**: 14
6. **Amazon Web Services (AWS)**: 9
7. **Welocalize**: 9
8. **Steneral Consulting**: 8
9. **iTech Solutions**: 8
10. **AMD**: 7
