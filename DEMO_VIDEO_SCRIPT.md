# CareSignal Demo Video Script

Target length: 3-5 minutes

## 0:00-0:30 - The problem

"Family caregivers can miss gradual health deterioration because the change happens across several ordinary days. A small oxygen drop, a rising temperature, and new breathing difficulty may not look dramatic in isolation. CareSignal helps make that pattern visible."

## 0:30-1:00 - What CareSignal is

"CareSignal is an educational prototype for the UnivaBio theme, Artificial Intelligence for Human Health. A caregiver records daily observations for a patient. The application applies transparent safety rules, shows the current signal, explains the reasons, and visualizes the trend. It uses synthetic data and is not a diagnostic device."

## 1:00-2:30 - Ahmed live walkthrough

1. Open the dashboard and select Ahmed.
2. Point out the three seeded observations and the current **Urgent** signal.
3. Show the timeline: oxygen falls from 96 to 93 to 89, temperature rises, and pain increases.
4. Explain the three states in the table:
   - Day 1: Stable
   - Day 2: Concerning because oxygen is lower than normal
   - Day 3: Urgent because oxygen is below the safety threshold, fever is present, and moderate breathing difficulty is reported
5. Show the reasons panel and the visible safety disclaimer.

## 2:30-3:30 - Safety architecture

"The most important design decision is that rules decide risk and AI only explains. The pure Python rule engine checks thresholds and trends. If a rule detects an urgent condition, that result cannot be overridden by a language model. If an AI key is unavailable or the AI call fails, CareSignal falls back to a local template explanation and continues working."

"This adapts the idea behind Early Warning Scores, used in hospitals to notice deterioration, for a simpler home-caregiver workflow. We are not claiming to invent a new medical concept; we are making an established safety practice more accessible and explainable."

## 3:30-4:00 - Close

"CareSignal is intentionally focused: it makes gradual change visible, gives caregivers understandable reasons, and keeps professional medical care in the loop. It is an educational prototype using synthetic data. It does not diagnose medical conditions or replace professional medical advice. In an emergency, contact a doctor or emergency services immediately."