# showcase
Personal project portfolio and independent learning showcase

**showcase/dissertation_program:** My python program to code participant's responses on 5 psychometric scales. See references in corresponding python module under showcase/dissertation_program/scales/<scale_name>.py
1. Creative Achievement Questionnaire
2. Creative Self-efficacy
3. Alternative Uses and Instances
4. International Personality Item Pool
5. Hagen's Matrices Test (Short-form version)
- **(Detailed Description)** The purpose of this dissertation program is to take the raw data (e.g.: diss_survey_22 October 2022_19.48.csv) which contains participants' uncalculated answers for psychometric scales, calculate their scores and export them in a format which is friendly for further analysis in IBM SPSS Statistics (e.g.: showcase/dissertation_program/scales_profiles/output_ipip50.csv). **See example images below**.
- **Demo Guide:** Use the instructions below if you would like to test this program for yourself
  1.  The file 'diss_survey 22 October 2022_19.48.csv' is the raw survey data which will be parsed through, computed, and exported in a more friendly csv format.
  2.  The program has been pre-configured to create a csv file which contains all of the scales, however, it is possible to define which scales should be output.
  3.  Simply navigate to your 'dissertation_program/' directory and run main.py
  4.  In the 'dissertation_program/scales_profiles/' directory your output file will be called 'output_auaifluency_caq_cse_custom_hmts_ipip50.csv'
  - As you can see, the program has taken the raw data from 'diss_survey...' and selected key information to compute participants' scale scores.
  - Input ex:![image](https://user-images.githubusercontent.com/116369016/200949470-3691771a-6f62-4bea-896f-89124e8dd930.png)
  - Output ex:![image](https://user-images.githubusercontent.com/116369016/200949662-f68ae62b-1652-478e-a04a-f0f982ffd50e.png)
- **Test Log:** https://lying-carnation-8b2.notion.site/Program-Testing-4298d903724f41b38991513f02c03c9f 

**showcase/codewars:** My Codewars practise example showcase

**showcase/codewars/data_science:** Codewars practise examples that are related to data science
- Any folder beginning 'ex' contains a solution module and a unittest module which begins with 'test_'
