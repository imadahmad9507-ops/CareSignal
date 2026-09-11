# CareSignal FirstCommit Demo Script

Target length: 3-5 minutes

## Opening: the problem

"Hi, this is CareSignal. Family caregivers can miss gradual health changes because the important pattern is spread across several ordinary days. CareSignal gives them one simple place to record observations, see the direction of change, and prepare a clearer handoff to a professional."

## Dashboard and multiple patients

"The dashboard supports multiple people. Each card shows the current signal and how long ago the last check-in happened. A new caregiver can start from the empty state by adding a first patient."

## Ahmed walkthrough

"I will open Ahmed, our synthetic demo patient. His history shows three check-ins: Stable, then Concerning, then Urgent. Oxygen falls from 96 to 93 to 89, temperature rises from 37.2 to 38.8, and breathing difficulty appears. The chart makes that change visible, while the table preserves the caregiver's notes and exact readings."

"The current page explains why Ahmed is Urgent and shows raw-direction arrows for the latest vital signs. These arrows describe what changed; they do not pretend that every upward or downward movement has the same clinical meaning."

## Add a check-in and validation

"A caregiver can record a new check-in with readings, symptoms, medication adherence, and free-text notes. The form validates impossible values, prevents duplicate dates, and gives feedback while the submission is being saved."

## Report and safety architecture

"The patient summary can be printed or saved as a PDF from the browser. The About page explains the key design decision: rules decide the risk, and AI only explains it. If an AI key is missing or the network call fails, the local explanation template keeps the app working."

## Close

"CareSignal is an educational prototype using synthetic data. It is not a diagnostic tool and does not replace professional medical advice. Its goal is to make gradual change easier to notice, easier to explain, and easier to discuss with the right professional."